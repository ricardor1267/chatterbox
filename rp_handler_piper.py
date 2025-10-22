"""
RunPod Serverless Worker for Piper TTS Spanish
ULTRA-LIGHTWEIGHT: ~10-30 MB model, ~500 MB Docker total
"""
import runpod
import wave
import json
import base64
import subprocess
import tempfile
import os
import time
from pathlib import Path

# Model will be downloaded on first use
VOICE_MODEL = "es_ES-mls_10246-low"  # Spanish, low quality = smallest size (~10 MB)
MODEL_PATH = "/workspace/models"

def download_voice():
    """Download Piper voice model if not exists"""
    model_file = f"{MODEL_PATH}/{VOICE_MODEL}.onnx"
    
    if os.path.exists(model_file):
        print(f"✓ Model already downloaded: {VOICE_MODEL}")
        return model_file
    
    print(f"⏳ Downloading voice model: {VOICE_MODEL}...")
    os.makedirs(MODEL_PATH, exist_ok=True)
    
    # Download from Hugging Face
    base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/mls_10246/low"
    
    # Download .onnx file
    onnx_url = f"{base_url}/{VOICE_MODEL}.onnx"
    subprocess.run([
        "wget", "-q", "-O", model_file, onnx_url
    ], check=True)
    
    # Download .onnx.json config
    json_url = f"{base_url}/{VOICE_MODEL}.onnx.json"
    subprocess.run([
        "wget", "-q", "-O", f"{model_file}.json", json_url
    ], check=True)
    
    print(f"✓ Model downloaded: {VOICE_MODEL}")
    return model_file


def audio_to_base64(audio_path):
    """Convert audio file to base64"""
    with open(audio_path, 'rb') as f:
        audio_bytes = f.read()
    return base64.b64encode(audio_bytes).decode('utf-8')


def handler(job):
    """
    RunPod Serverless Handler for Piper TTS Spanish
    
    Input format:
    {
        "input": {
            "text": "Texto a sintetizar en español (required)"
        }
    }
    
    Returns:
    {
        "audio": "base64_wav_data",
        "sample_rate": 22050,
        "text_length": 42,
        "generation_time": 0.5,
        "language": "es"
    }
    """
    try:
        print("=" * 60)
        print("🇪🇸 Piper TTS Spanish - Processing Request")
        print("=" * 60)
        
        job_input = job.get("input", {})
        
        # Validate input
        if not job_input:
            return {"error": "Missing 'input' in job"}
        
        text = job_input.get("text")
        if not text:
            return {"error": "Missing required field: 'text'"}
        
        print(f"📝 Text: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        # Download model if needed
        model_file = download_voice()
        
        # Create temporary output file
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        output_path = temp_output.name
        temp_output.close()
        
        # Generate TTS using Piper
        print(f"🔊 Generating audio with Piper...")
        start_time = time.time()
        
        # Run piper command
        process = subprocess.Popen(
            ['piper', '--model', model_file, '--output_file', output_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=text)
        
        if process.returncode != 0:
            return {"error": f"Piper failed: {stderr}"}
        
        generation_time = time.time() - start_time
        
        # Convert to base64
        print(f"📦 Encoding audio...")
        audio_base64 = audio_to_base64(output_path)
        
        # Get audio info
        with wave.open(output_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            duration = n_frames / sample_rate
        
        # Cleanup
        os.unlink(output_path)
        
        print(f"✓ Success! Generated {duration:.2f}s audio in {generation_time:.2f}s")
        print("=" * 60)
        
        return {
            "audio": audio_base64,
            "sample_rate": sample_rate,
            "duration": round(duration, 2),
            "text_length": len(text),
            "generation_time": round(generation_time, 2),
            "language": "es",
            "model": VOICE_MODEL
        }
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"✗ Error in handler:")
        print(error_trace)
        return {"error": str(e)}


# Start the serverless worker
if __name__ == "__main__":
    print("🚀 Starting Piper TTS Spanish RunPod Worker...")
    print(f"🎤 Voice: {VOICE_MODEL}")
    runpod.serverless.start({"handler": handler})
