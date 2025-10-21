# 🎙️ Chatterbox TTS - RunPod Serverless Worker

Production-ready RunPod serverless worker for Chatterbox TTS with multilingual support and voice cloning.

## 🚀 Quick Start

### Option 1: Deploy Pre-built Image (Fastest)

```bash
# Use in RunPod Template
Container Image: ricardor1267/chatterbox-runpod-worker:latest
```

### Option 2: Build Your Own

```bash
# 1. Build Docker image
./build_worker.sh your-dockerhub-username

# 2. Push to Docker Hub
docker push your-dockerhub-username/chatterbox-runpod-worker:latest

# 3. Create RunPod Template with your image
```

## 📋 Files Structure

```
chatterbox/
├── rp_handler.py          # Main RunPod handler with model caching
├── Dockerfile             # Optimized Docker image with pre-loaded models
├── test_input.json        # Sample input for testing
├── build_worker.sh        # Docker build script
├── test_worker.py         # Local testing script
└── WORKER_README.md       # This file
```

## 🧪 Local Testing

### Test the handler locally:

```bash
# Install dependencies
pip install runpod chatterbox-tts

# Run all tests
python test_worker.py

# Or test directly with test_input.json
python rp_handler.py
```

## 📖 API Documentation

### Input Format

```json
{
  "input": {
    "text": "Text to synthesize (required)",
    "model_type": "multilingual",
    "language_id": "en",
    "audio_prompt": "base64_audio",
    "exaggeration": 0.5,
    "temperature": 0.8,
    "cfg_weight": 0.5,
    "seed": 0
  }
}
```

### Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `text` | string | *required* | 1-500 chars | Text to synthesize |
| `model_type` | string | `"multilingual"` | - | `"english"` or `"multilingual"` |
| `language_id` | string | `"en"` | - | Language code (23 languages) |
| `audio_prompt` | string | `null` | - | Base64 audio for voice cloning |
| `exaggeration` | float | `0.5` | 0.25-2.0 | Emotion intensity (0.5=neutral) |
| `temperature` | float | `0.8` | 0.05-5.0 | Sampling randomness |
| `cfg_weight` | float | `0.5` | 0.0-1.0 | CFG guidance (0=off for lang transfer) |
| `seed` | integer | `0` | - | Random seed (0=random) |
| `min_p` | float | `0.05` | 0.0-1.0 | Min-p sampling threshold |
| `top_p` | float | `1.0` | 0.0-1.0 | Nucleus sampling (1.0=off) |
| `repetition_penalty` | float | `1.2` | 1.0-2.0 | Repetition penalty |

### Output Format

```json
{
  "audio": "base64_encoded_wav_data",
  "sample_rate": 24000,
  "duration": 3.45,
  "model_used": "multilingual",
  "language": "en",
  "text_length": 42,
  "generation_time": 2.1
}
```

### Error Format

```json
{
  "error": "Error message description"
}
```

## 🌍 Supported Languages (23)

| Code | Language | Code | Language |
|------|----------|------|----------|
| `ar` | Arabic | `ms` | Malay |
| `da` | Danish | `nl` | Dutch |
| `de` | German | `no` | Norwegian |
| `el` | Greek | `pl` | Polish |
| `en` | English | `pt` | Portuguese |
| `es` | Spanish | `ru` | Russian |
| `fi` | Finnish | `sv` | Swedish |
| `fr` | French | `sw` | Swahili |
| `he` | Hebrew | `tr` | Turkish |
| `hi` | Hindi | `zh` | Chinese |
| `it` | Italian | | |
| `ja` | Japanese | | |
| `ko` | Korean | | |

## 💡 Usage Examples

### Example 1: Basic English TTS

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -d '{
    "input": {
      "text": "Hello! Welcome to Chatterbox TTS on RunPod.",
      "model_type": "english"
    }
  }'
```

### Example 2: Multilingual TTS

```bash
# Spanish
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -d '{
    "input": {
      "text": "Hola, bienvenido a Chatterbox!",
      "model_type": "multilingual",
      "language_id": "es"
    }
  }'

# French
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -d '{
    "input": {
      "text": "Bonjour et bienvenue!",
      "model_type": "multilingual",
      "language_id": "fr"
    }
  }'
```

### Example 3: Expressive Speech

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -d '{
    "input": {
      "text": "This is so exciting and dramatic!",
      "model_type": "english",
      "exaggeration": 1.5,
      "cfg_weight": 0.3
    }
  }'
```

### Example 4: Voice Cloning (Python)

```python
import requests
import base64

RUNPOD_API_KEY = "your-api-key"
ENDPOINT_ID = "your-endpoint-id"

# Read reference audio
with open("reference_voice.wav", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode('utf-8')

# Send request
response = requests.post(
    f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    },
    json={
        "input": {
            "text": "This will sound like the reference voice!",
            "model_type": "multilingual",
            "language_id": "en",
            "audio_prompt": audio_b64,
            "exaggeration": 0.5,
            "cfg_weight": 0.5
        }
    },
    timeout=120
)

result = response.json()

if "output" in result:
    # Save generated audio
    audio_data = base64.b64decode(result["output"]["audio"])
    with open("cloned_output.wav", "wb") as f:
        f.write(audio_data)
    print(f"✓ Audio saved! Duration: {result['output']['duration']}s")
else:
    print(f"✗ Error: {result.get('error', 'Unknown error')}")
```

### Example 5: Async Processing (Python)

```python
import requests
import time

# Submit async job
response = requests.post(
    f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run",  # Note: /run not /runsync
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    },
    json={
        "input": {
            "text": "Processing this asynchronously...",
            "model_type": "english"
        }
    }
)

job_id = response.json()["id"]
print(f"Job submitted: {job_id}")

# Poll for results
while True:
    status_response = requests.get(
        f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{job_id}",
        headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"}
    )
    
    status_data = status_response.json()
    status = status_data.get("status")
    
    if status == "COMPLETED":
        print("✓ Job completed!")
        output = status_data["output"]
        # Process output...
        break
    elif status == "FAILED":
        print(f"✗ Job failed: {status_data.get('error')}")
        break
    else:
        print(f"Status: {status}")
        time.sleep(2)
```

## 🏗️ Deployment Guide

### Step 1: Build Docker Image

```bash
# Navigate to project directory
cd /Users/mimac/mining/testApi/git/chatterbox

# Build image (replace with your Docker Hub username)
./build_worker.sh ricardor1267

# Or manually:
docker build --platform linux/amd64 \
  -t ricardor1267/chatterbox-runpod-worker:latest \
  -f Dockerfile .
```

**Note**: The `--platform linux/amd64` flag is required for RunPod compatibility.

### Step 2: Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push image
docker push ricardor1267/chatterbox-runpod-worker:latest
```

### Step 3: Create RunPod Template

1. Go to https://runpod.io/console/serverless/user/templates
2. Click **"New Template"**
3. Configure:
   - **Template Name**: `Chatterbox TTS Worker`
   - **Container Image**: `ricardor1267/chatterbox-runpod-worker:latest`
   - **Container Disk**: `40 GB`
   - **Docker Command**: *(leave empty)*
4. Click **"Save Template"**

### Step 4: Create Endpoint

1. Go to https://runpod.io/console/serverless/user/endpoints
2. Click **"New Endpoint"**
3. Configure:
   - **Endpoint Name**: `chatterbox-tts`
   - **Select Template**: Your "Chatterbox TTS Worker" template
   - **Active Workers**: 
     - `0` for development (pay per use)
     - `1+` for production (always ready)
   - **Max Workers**: `3-5`
   - **Idle Timeout**: `5 seconds`
   - **FlashBoot**: ✅ Enabled (recommended)
   - **GPUs/Worker**: `1`
4. Select GPU types (16GB+ VRAM recommended):
   - ✅ NVIDIA RTX A4000
   - ✅ NVIDIA RTX A5000
   - ✅ NVIDIA L4
   - ✅ NVIDIA RTX 4090
5. Click **"Deploy"**

### Step 5: Test Your Endpoint

```bash
# Get your endpoint ID and API key from RunPod console

# Test basic request
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"input": {"text": "Testing Chatterbox on RunPod!"}}'
```

## ⚡ Performance Metrics

### Latency
- **Cold Start**: 30-60 seconds (first request, model loading)
- **Warm Request**: 2-8 seconds (with active workers)
- **Generation Speed**: ~10 seconds of audio per second

### Resource Usage
- **VRAM**: 12-15GB
- **RAM**: 8-16GB
- **Disk**: 20-30GB (with models)

### Throughput
- **Single Worker**: ~5-10 requests/minute
- **With Scaling**: Unlimited (auto-scales)

## 💰 Cost Optimization

### Development Setup (Minimal Cost)
```
Active Workers: 0
Max Workers: 3
Cost: ~$0.0005 per request
Use Case: Testing, low volume
```

### Production Setup (Low Latency)
```
Active Workers: 1
Max Workers: 5
Cost: ~$0.40/hour + usage
Use Case: Production apps, high availability
```

### Batch Processing Setup
```
Active Workers: 0
Max Workers: 10
Use /run (async) instead of /runsync
Cost: Pay per use, no idle cost
Use Case: Batch jobs, audiobooks
```

## 🔧 Troubleshooting

### Issue: Cold start takes too long

**Solutions**:
- ✅ Enable FlashBoot in endpoint settings
- ✅ Keep 1+ active workers in production
- ✅ Models are pre-downloaded in Dockerfile (already done)

### Issue: Out of memory error

**Solutions**:
- Use GPU with 16GB+ VRAM (RTX A4000 minimum)
- Limit to specific GPU types in endpoint settings
- Reduce max workers if needed

### Issue: "Unsupported language" error

**Solution**:
Check that `language_id` is one of the 23 supported languages (see list above)

### Issue: Audio quality is poor

**Solutions**:
- Ensure reference audio is high quality (for voice cloning)
- Adjust parameters:
  - `exaggeration`: 0.3-0.7 for better quality
  - `cfg_weight`: 0.3-0.7 (or 0 for language transfer)
- Match reference audio language with target language

### Issue: Timeout errors

**Solutions**:
- Increase timeout in your HTTP client (120+ seconds recommended)
- Use `/run` (async) instead of `/runsync` for long texts
- Keep text under 500 characters

## 📊 Monitoring

### Check Endpoint Health

```bash
curl https://api.runpod.ai/v2/{ENDPOINT_ID}/health \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}"
```

### View Logs

1. Go to RunPod Console
2. Navigate to your endpoint
3. Click "Logs" tab
4. Monitor real-time execution

### Metrics to Monitor

- Request count
- Error rate
- Average latency
- Active workers
- Queue depth
- Cost per request

## 🔐 Security Best Practices

1. **Never commit API keys** to git
2. **Use environment variables** for sensitive data
3. **Rotate API keys** periodically
4. **Monitor usage** for unexpected spikes
5. **Set max workers limit** to control costs

## 📚 Additional Resources

- **RunPod Docs**: https://docs.runpod.io/serverless
- **Chatterbox GitHub**: https://github.com/resemble-ai/chatterbox
- **Discord Support**: https://discord.gg/rJq9cRJBJ6
- **Your Repository**: https://github.com/ricardor1267/chatterbox

## 🆘 Support

If you encounter issues:

1. **Check Logs**: RunPod Console → Your Endpoint → Logs
2. **Test Locally**: Run `python test_worker.py`
3. **Review Documentation**: Check this README
4. **Ask for Help**: 
   - RunPod Discord: https://discord.gg/runpod
   - Resemble AI Discord: https://discord.gg/rJq9cRJBJ6

## 📝 License

MIT License - See main repository LICENSE file

---

**Made with ♥️ for RunPod Serverless**

**Quick Links**:
- 🚀 [Deploy Guide](#deployment-guide)
- 📖 [API Docs](#api-documentation)
- 💡 [Examples](#usage-examples)
- 🔧 [Troubleshooting](#troubleshooting)
