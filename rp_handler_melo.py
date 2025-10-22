"""
RunPod Serverless Worker for MeloTTS-Spanish
Lightweight TTS (~100-200 MB) optimized for Spanish
"""
import runpod
import torch
import base64
import io
import time
import tempfile
import os

# Global model cache
tts_model = None

def initialize_model():
    """Initialize and cache MeloTTS Spanish model"""
    global tts_model
    
    if tts_model is not None:
        print("✓ Using cached MeloTTS model")
        return tts_model
    
    print("⏳ Loading MeloTTS Spanish model...")
    start_time = time.time()
    
    try:
        from melo.api import TTS
        
        # Determine device
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"🔧 Device: {device}")
        
        # Load Spanish model
        tts_model = TTS(language='ES', device=device)
        
        load_time = time.time() - start_time
        print(f"✓ MeloTTS Spanish model loaded in {load_time:.2f}s")
        
        return tts_model
    
    except Exception as e:
        print(f"✗ Failed to load model: {str(e)}")
        raise


def audio_to_base64(audio_path):
    """Convert audio file to base64"""
    with open(audio_path, 'rb') as f:
        audio_bytes = f.read()
    return base64.b64encode(audio_bytes).decode('utf-8')


def handler(job):
    """
    RunPod Serverless Handler for MeloTTS-Spanish
    
    Input format:
    {
        "input": {
            "text": "Texto a sintetizar (required)",
            "speed": 1.0 (optional, 0.5-2.0, default: 1.0)
        }
    }
    
    Returns:
    {
        "audio": "base64_wav_data",
        "sample_rate": 44100,
        "text_length": 42,
        "generation_time": 1.2,
        "language": "es"
    }
    """
    try:
        print("=" * 60)
        print("🇪🇸 MeloTTS-Spanish - Processing Request")
        print("=" * 60)
        
        job_input = job.get("input", {})
        
        # Validate input
        if not job_input:
            return {"error": "Missing 'input' in job"}
        
        text = job_input.get("text")
        if not text:
            return {"error": "Missing required field: 'text'"}
        
        print(f"📝 Text: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        # Get speed parameter
        speed = float(job_input.get("speed", 1.0))
        if speed < 0.5 or speed > 2.0:
            speed = 1.0
            print(f"⚠️  Speed adjusted to 1.0 (was out of range)")
        
        print(f"⚙️  Speed: {speed}x")
        
        # Initialize model
        model = initialize_model()
        
        # Get speaker ID
        speaker_ids = model.hps.data.spk2id
        speaker_id = speaker_ids['ES']  # Spanish speaker
        
        # Generate audio
        print(f"🔊 Generating audio...")
        start_time = time.time()
        
        # Create temporary output file
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        output_path = temp_output.name
        temp_output.close()
        
        # Generate TTS
        model.tts_to_file(text, speaker_id, output_path, speed=speed)
        
        generation_time = time.time() - start_time
        
        # Convert to base64
        print(f"📦 Encoding audio...")
        audio_base64 = audio_to_base64(output_path)
        
        # Get file size for duration estimation
        file_size = os.path.getsize(output_path)
        duration_estimate = file_size / 88200  # Rough estimate for 44.1kHz stereo
        
        # Cleanup
        os.unlink(output_path)
        
        print(f"✓ Success! Generated ~{duration_estimate:.2f}s audio in {generation_time:.2f}s")
        print("=" * 60)
        
        return {
            "audio": audio_base64,
            "sample_rate": 44100,
            "text_length": len(text),
            "generation_time": round(generation_time, 2),
            "language": "es",
            "speed": speed
        }
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"✗ Error in handler:")
        print(error_trace)
        return {"error": str(e)}


# Start the serverless worker
if __name__ == "__main__":
    print("🚀 Starting MeloTTS-Spanish RunPod Worker...")
    print(f"🔧 Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    runpod.serverless.start({"handler": handler})
