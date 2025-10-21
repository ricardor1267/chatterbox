"""
RunPod Serverless Worker for Chatterbox TTS
Optimized handler with model caching and error handling
"""
import runpod
import torch
import torchaudio as ta
import base64
import io
import tempfile
import os
import time

# Global model cache
MODEL_CACHE = {
    "english": None,
    "multilingual": None
}

def initialize_model(model_type="multilingual"):
    """
    Initialize and cache TTS models
    
    Args:
        model_type (str): "english" or "multilingual"
    
    Returns:
        model: Loaded TTS model
    """
    global MODEL_CACHE
    
    # Return cached model if available
    if MODEL_CACHE[model_type] is not None:
        print(f"✓ Using cached {model_type} model")
        return MODEL_CACHE[model_type]
    
    # Initialize new model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"⏳ Loading {model_type} model on {device}...")
    
    start_time = time.time()
    
    try:
        if model_type == "english":
            from chatterbox.tts import ChatterboxTTS
            MODEL_CACHE["english"] = ChatterboxTTS.from_pretrained(device=device)
        elif model_type == "multilingual":
            from chatterbox.mtl_tts import ChatterboxMultilingualTTS
            MODEL_CACHE["multilingual"] = ChatterboxMultilingualTTS.from_pretrained(device=device)
        else:
            raise ValueError(f"Invalid model_type: {model_type}")
        
        load_time = time.time() - start_time
        print(f"✓ {model_type.capitalize()} model loaded in {load_time:.2f}s")
        return MODEL_CACHE[model_type]
    
    except Exception as e:
        print(f"✗ Failed to load {model_type} model: {str(e)}")
        raise


def audio_to_base64(audio_tensor, sample_rate):
    """Convert audio tensor to base64 WAV"""
    buffer = io.BytesIO()
    ta.save(buffer, audio_tensor, sample_rate, format="wav")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')


def base64_to_audio_file(base64_string):
    """Convert base64 audio to temporary file"""
    audio_bytes = base64.b64decode(base64_string)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_file.write(audio_bytes)
    temp_file.close()
    return temp_file.name


def handler(job):
    """
    RunPod Serverless Handler for Chatterbox TTS
    
    Input format:
    {
        "input": {
            "text": "Text to synthesize (required)",
            "model_type": "multilingual" or "english" (default: "multilingual"),
            "language_id": "en" (required for multilingual),
            "audio_prompt": "base64_audio" (optional - for voice cloning),
            "exaggeration": 0.5 (optional, range: 0.25-2.0),
            "temperature": 0.8 (optional, range: 0.05-5.0),
            "cfg_weight": 0.5 (optional, range: 0.0-1.0),
            "seed": 0 (optional, 0 for random),
            "min_p": 0.05 (optional),
            "top_p": 1.0 (optional),
            "repetition_penalty": 1.2 (optional)
        }
    }
    
    Returns:
    {
        "audio": "base64_wav_data",
        "sample_rate": 24000,
        "duration": 3.45,
        "model_used": "multilingual",
        "language": "en",
        "text_length": 42,
        "generation_time": 2.1
    }
    """
    try:
        print("=" * 60)
        print("🎙️  Chatterbox TTS - Processing Request")
        print("=" * 60)
        
        job_input = job.get("input", {})
        
        # Validate input
        if not job_input:
            return {"error": "Missing 'input' in job"}
        
        text = job_input.get("text")
        if not text:
            return {"error": "Missing required field: 'text'"}
        
        print(f"📝 Text: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        # Truncate text if too long
        original_length = len(text)
        if len(text) > 500:
            text = text[:500]
            print(f"⚠️  Text truncated from {original_length} to 500 characters")
        
        # Get parameters with defaults
        model_type = job_input.get("model_type", "multilingual")
        if model_type not in ["english", "multilingual"]:
            return {"error": f"Invalid model_type: '{model_type}'. Must be 'english' or 'multilingual'"}
        
        print(f"🤖 Model: {model_type}")
        
        # Initialize model (uses cache if available)
        model = initialize_model(model_type)
        
        # Generation parameters
        exaggeration = float(job_input.get("exaggeration", 0.5))
        temperature = float(job_input.get("temperature", 0.8))
        cfg_weight = float(job_input.get("cfg_weight", 0.5))
        seed = int(job_input.get("seed", 0))
        min_p = float(job_input.get("min_p", 0.05))
        top_p = float(job_input.get("top_p", 1.0))
        repetition_penalty = float(job_input.get("repetition_penalty", 1.2))
        
        print(f"⚙️  Parameters: exaggeration={exaggeration}, cfg_weight={cfg_weight}, temp={temperature}")
        
        # Set seed if provided
        if seed != 0:
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
            print(f"🎲 Seed: {seed}")
        
        # Handle audio prompt for voice cloning
        audio_prompt_path = None
        if "audio_prompt" in job_input and job_input["audio_prompt"]:
            try:
                audio_prompt_path = base64_to_audio_file(job_input["audio_prompt"])
                print(f"🎤 Voice cloning: Using reference audio")
            except Exception as e:
                return {"error": f"Invalid audio_prompt: {str(e)}"}
        
        # Generate audio
        print(f"🔊 Generating audio...")
        start_time = time.time()
        
        if model_type == "english":
            wav = model.generate(
                text,
                audio_prompt_path=audio_prompt_path,
                exaggeration=exaggeration,
                temperature=temperature,
                cfg_weight=cfg_weight,
                min_p=min_p,
                top_p=top_p,
                repetition_penalty=repetition_penalty
            )
            sample_rate = model.sr
            language_used = "en"
        
        else:  # multilingual
            language_id = job_input.get("language_id", "en")
            
            # Validate language
            from chatterbox.mtl_tts import SUPPORTED_LANGUAGES
            if language_id not in SUPPORTED_LANGUAGES:
                return {
                    "error": f"Unsupported language: '{language_id}'",
                    "supported_languages": list(SUPPORTED_LANGUAGES.keys())
                }
            
            print(f"🌍 Language: {language_id} ({SUPPORTED_LANGUAGES.get(language_id, 'Unknown')})")
            
            generate_kwargs = {
                "exaggeration": exaggeration,
                "temperature": temperature,
                "cfg_weight": cfg_weight,
            }
            
            if audio_prompt_path:
                generate_kwargs["audio_prompt_path"] = audio_prompt_path
            
            wav = model.generate(
                text,
                language_id=language_id,
                **generate_kwargs
            )
            sample_rate = model.sr
            language_used = language_id
        
        generation_time = time.time() - start_time
        
        # Cleanup temp file
        if audio_prompt_path and os.path.exists(audio_prompt_path):
            os.unlink(audio_prompt_path)
        
        # Convert to base64
        print(f"📦 Encoding audio...")
        audio_base64 = audio_to_base64(wav, sample_rate)
        
        # Calculate duration
        duration = wav.shape[-1] / sample_rate
        
        print(f"✓ Success! Generated {duration:.2f}s audio in {generation_time:.2f}s")
        print("=" * 60)
        
        return {
            "audio": audio_base64,
            "sample_rate": sample_rate,
            "duration": round(duration, 2),
            "model_used": model_type,
            "language": language_used,
            "text_length": len(text),
            "generation_time": round(generation_time, 2)
        }
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"✗ Error in handler:")
        print(error_trace)
        return {"error": str(e)}


# Start the serverless worker
if __name__ == "__main__":
    print("🚀 Starting Chatterbox TTS RunPod Worker...")
    print(f"🔧 Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    runpod.serverless.start({"handler": handler})
