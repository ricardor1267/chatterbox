"""
RunPod Serverless Handler for Chatterbox TTS
Supports both English-only and Multilingual models
"""
import runpod
import torch
import torchaudio as ta
import base64
import io
import tempfile
import os
from pathlib import Path

# Global model instances
tts_model = None
mtl_model = None


def initialize_models(model_type="multilingual"):
    """
    Initialize the TTS models based on the requested type.
    
    Args:
        model_type: "english" or "multilingual"
    """
    global tts_model, mtl_model
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Initializing models on device: {device}")
    
    if model_type == "english" and tts_model is None:
        print("Loading English TTS model...")
        from chatterbox.tts import ChatterboxTTS
        tts_model = ChatterboxTTS.from_pretrained(device=device)
        print("English TTS model loaded successfully")
        
    elif model_type == "multilingual" and mtl_model is None:
        print("Loading Multilingual TTS model...")
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        mtl_model = ChatterboxMultilingualTTS.from_pretrained(device=device)
        print("Multilingual TTS model loaded successfully")


def audio_to_base64(audio_tensor, sample_rate):
    """Convert audio tensor to base64 encoded WAV"""
    buffer = io.BytesIO()
    ta.save(buffer, audio_tensor, sample_rate, format="wav")
    buffer.seek(0)
    audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return audio_base64


def base64_to_audio_file(base64_string):
    """Convert base64 audio to temporary file"""
    audio_bytes = base64.b64decode(base64_string)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_file.write(audio_bytes)
    temp_file.close()
    return temp_file.name


def handler(job):
    """
    RunPod handler function for Chatterbox TTS
    
    Expected input format:
    {
        "input": {
            "text": "Text to synthesize",
            "model_type": "multilingual" or "english" (default: "multilingual"),
            "language_id": "en" (required for multilingual),
            "audio_prompt": "base64_encoded_audio" (optional),
            "exaggeration": 0.5 (optional),
            "temperature": 0.8 (optional),
            "cfg_weight": 0.5 (optional),
            "seed": 0 (optional),
            "min_p": 0.05 (optional),
            "top_p": 1.0 (optional),
            "repetition_penalty": 1.2 (optional)
        }
    }
    """
    try:
        job_input = job.get("input", {})
        
        # Validate required fields
        if "text" not in job_input:
            return {"error": "Missing required field: 'text'"}
        
        text = job_input["text"]
        if len(text) > 500:
            text = text[:500]
        
        # Get model type
        model_type = job_input.get("model_type", "multilingual")
        if model_type not in ["english", "multilingual"]:
            return {"error": "model_type must be 'english' or 'multilingual'"}
        
        # Initialize the appropriate model
        initialize_models(model_type)
        
        # Get generation parameters
        exaggeration = float(job_input.get("exaggeration", 0.5))
        temperature = float(job_input.get("temperature", 0.8))
        cfg_weight = float(job_input.get("cfg_weight", 0.5))
        seed = int(job_input.get("seed", 0))
        min_p = float(job_input.get("min_p", 0.05))
        top_p = float(job_input.get("top_p", 1.0))
        repetition_penalty = float(job_input.get("repetition_penalty", 1.2))
        
        # Set seed if provided
        if seed != 0:
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
        
        # Handle audio prompt if provided
        audio_prompt_path = None
        if "audio_prompt" in job_input:
            audio_prompt_path = base64_to_audio_file(job_input["audio_prompt"])
        
        # Generate audio based on model type
        if model_type == "english":
            wav = tts_model.generate(
                text,
                audio_prompt_path=audio_prompt_path,
                exaggeration=exaggeration,
                temperature=temperature,
                cfg_weight=cfg_weight,
                min_p=min_p,
                top_p=top_p,
                repetition_penalty=repetition_penalty
            )
            sample_rate = tts_model.sr
            language_used = "en"
            
        else:  # multilingual
            language_id = job_input.get("language_id", "en")
            
            # Validate language ID
            from chatterbox.mtl_tts import SUPPORTED_LANGUAGES
            if language_id not in SUPPORTED_LANGUAGES:
                return {
                    "error": f"Unsupported language: {language_id}",
                    "supported_languages": list(SUPPORTED_LANGUAGES.keys())
                }
            
            generate_kwargs = {
                "exaggeration": exaggeration,
                "temperature": temperature,
                "cfg_weight": cfg_weight,
            }
            
            if audio_prompt_path:
                generate_kwargs["audio_prompt_path"] = audio_prompt_path
            
            wav = mtl_model.generate(
                text,
                language_id=language_id,
                **generate_kwargs
            )
            sample_rate = mtl_model.sr
            language_used = language_id
        
        # Clean up temporary audio file if created
        if audio_prompt_path and os.path.exists(audio_prompt_path):
            os.unlink(audio_prompt_path)
        
        # Convert audio to base64
        audio_base64 = audio_to_base64(wav, sample_rate)
        
        # Calculate duration
        duration = wav.shape[-1] / sample_rate
        
        return {
            "audio": audio_base64,
            "sample_rate": sample_rate,
            "duration": round(duration, 2),
            "model_used": model_type,
            "language": language_used,
            "text_length": len(text)
        }
        
    except Exception as e:
        return {"error": str(e)}


# Start the serverless worker
runpod.serverless.start({"handler": handler})
