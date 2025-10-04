# 🎉 Chatterbox TTS v1.0.0 - RunPod Serverless Release

## 🚀 RunPod Serverless Support

This release adds **complete RunPod Serverless support** to Chatterbox TTS, enabling production-grade, auto-scaling deployment with pay-per-use pricing.

## ✨ What's New

### 🎙️ Core Features
- ✅ **23 Languages**: Full multilingual support (ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh)
- ✅ **Zero-shot Voice Cloning**: Clone any voice with just seconds of reference audio
- ✅ **Emotion Control**: Unique exaggeration parameter for expressive speech
- ✅ **Production-Ready**: Optimized for serverless deployment with fast cold starts

### 🐳 RunPod Implementation
- ✅ **Complete Handler** (`handler.py`): Processes all TTS requests with full validation
- ✅ **Optimized Dockerfile**: Pre-loads models for 30-60s cold starts
- ✅ **Hub Configuration** (`hub.json`): Ready for RunPod Hub publishing
- ✅ **Automated Tests** (`tests.json`): 5 quality assurance tests
- ✅ **Build Scripts**: One-command Docker image building

### 📚 Documentation
- ✅ **[Deployment Guide](.runpod/DEPLOYMENT_GUIDE.md)**: 50+ page step-by-step guide
- ✅ **[API Documentation](.runpod/README.md)**: Complete API reference
- ✅ **[Integration Examples](.runpod/integration_examples.py)**: 7 framework examples
  - FastAPI Backend
  - Flask Application
  - Django Views
  - Streamlit App
  - Async Client
  - Telegram Bot
  - Discord Bot
- ✅ **[Testing Guide](.runpod/test_local.py)**: Local testing before deployment

## 📦 Installation & Deployment

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/ricardor1267/chatterbox.git
cd chatterbox

# 2. Build Docker image
cd .runpod
./build.sh your-dockerhub-username

# 3. Push to Docker Hub
docker push your-dockerhub-username/chatterbox-runpod:latest

# 4. Deploy on RunPod
# Follow: .runpod/DEPLOYMENT_GUIDE.md
```

### Local Installation (Standard Usage)

```bash
pip install chatterbox-tts
```

## 🎯 Use Cases

- 🎮 **Gaming**: Dynamic voiceovers in multiple languages
- 🎬 **Content Creation**: Videos, podcasts, audiobooks
- 🤖 **AI Agents**: Voice interfaces for chatbots and assistants
- 📱 **Apps**: Mobile and web applications with TTS
- 🌐 **Localization**: Multi-language content generation

## 💰 Pricing (RunPod)

- **Development** (0 active workers): ~$0.0005 per request
- **Production** (1+ active workers): ~$0.40/hour + usage
- **GPU Requirements**: 16-24GB VRAM (RTX A4000 or better)

## 📊 Performance

- **Cold Start**: 30-60 seconds (first request)
- **Warm Request**: 2-8 seconds (with active workers)
- **Quality**: Outperforms ElevenLabs in evaluations
- **Languages**: 23 supported out of the box

## 🔐 Built-in Watermarking

All generated audio includes **Perth (Perceptual Threshold) Watermarking**:
- Imperceptible to human listeners
- Survives MP3 compression and audio editing
- ~100% detection accuracy
- Responsible AI compliance

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [DEPLOYMENT_GUIDE.md](.runpod/DEPLOYMENT_GUIDE.md) | Complete step-by-step deployment guide |
| [README.md](.runpod/README.md) | API documentation and quick start |
| [INSTRUCCIONES_RICARDO.md](.runpod/INSTRUCCIONES_RICARDO.md) | Specific instructions for setup |
| [integration_examples.py](.runpod/integration_examples.py) | Code examples for 7 frameworks |
| [EXECUTIVE_SUMMARY.md](.runpod/EXECUTIVE_SUMMARY.md) | Project overview and roadmap |

## 🛠️ Technical Details

### GPU Support
- NVIDIA CUDA 12.1 + cuDNN 8
- Minimum: 16GB VRAM (RTX A4000)
- Recommended: 24GB VRAM (RTX A5000, L4, RTX 4090)

### Model Architecture
- 0.5B parameter Llama backbone
- S3 Tokenizer for audio encoding
- Flow matching for generation
- HiFT-GAN vocoder

### API Parameters
- `text`: Text to synthesize (max 500 chars)
- `model_type`: "english" or "multilingual"
- `language_id`: 2-letter language code
- `audio_prompt`: Base64 reference audio (optional)
- `exaggeration`: Emotion intensity (0.25-2.0)
- `cfg_weight`: Classifier-free guidance (0.0-1.0)
- `temperature`: Sampling temperature (0.05-5.0)
- And more...

## 🧪 Testing

### Automated Tests
```bash
# Run all tests
cd .runpod
python test_local.py
```

### Manual Testing
```bash
# Test with sample input
python handler.py
```

## 🔗 Links

- **Repository**: https://github.com/ricardor1267/chatterbox
- **RunPod Directory**: https://github.com/ricardor1267/chatterbox/tree/master/.runpod
- **Original Chatterbox**: https://github.com/resemble-ai/chatterbox
- **RunPod Platform**: https://runpod.io
- **Resemble AI**: https://resemble.ai
- **Discord**: https://discord.gg/rJq9cRJBJ6

## 🙏 Acknowledgements

- **Resemble AI** - For the amazing Chatterbox TTS model
- **RunPod** - For the serverless GPU platform
- **Community** - For testing and feedback

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

## 🆘 Support

- 📘 Read the [Deployment Guide](.runpod/DEPLOYMENT_GUIDE.md)
- 💬 Join [Discord](https://discord.gg/rJq9cRJBJ6)
- 🐛 Report issues on [GitHub](https://github.com/ricardor1267/chatterbox/issues)

## 🎯 Next Steps

1. ✅ Tag created: `v1.0.0-runpod`
2. ⏳ **Create GitHub Release** (manual step required)
3. ⏳ Connect GitHub to RunPod
4. ⏳ Publish to RunPod Hub

---

**Made with ♥️ by the community**

**Deploy now**: Follow [.runpod/DEPLOYMENT_GUIDE.md](.runpod/DEPLOYMENT_GUIDE.md)
