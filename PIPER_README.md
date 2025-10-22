# 🇪🇸 Piper TTS Spanish - RunPod Serverless Worker

## ⚡ EL MÁS LIGERO Y RÁPIDO

### 📊 Comparación de Tamaños

| Modelo | Tamaño Modelo | Tamaño Docker | Build | Upload |
|--------|---------------|---------------|-------|--------|
| **Piper TTS** ⚡⚡⚡ | **10-30 MB** | **~500 MB** | 5 min | 2-3 min |
| MeloTTS | 100-200 MB | 1-2 GB | 10-15 min | 5-10 min |
| Chatterbox | 5.5 GB | 8.5 GB | 20-30 min | 30-60 min |

### ✨ Ventajas de Piper

- ⚡ **ULTRA LIGERO**: 10-30 MB por voz
- 🚀 **ULTRA RÁPIDO**: Optimizado para Raspberry Pi
- 💻 **CPU**: No necesita GPU
- 🌍 **Español**: Múltiples voces españolas
- 📦 **Docker pequeño**: ~500 MB
- ⏱️ **Build rápido**: 5 minutos
- 📤 **Subida rápida**: 2-3 minutos
- 🆓 **MIT License**

## 🚀 Quick Start

### Deploy desde GitHub (RECOMENDADO)

1. **Conectar GitHub**: https://runpod.io/console/serverless/user/settings
2. **Crear Template**:
   - Repository: `ricardor1267/chatterbox`
   - Branch: `master`
   - **Dockerfile Path**: `Dockerfile.piper` ⬅️ IMPORTANTE
   - Container Disk: `5 GB`
3. **Deploy**

## 📖 API Usage

### Input Format

```json
{
  "input": {
    "text": "Texto en español"
  }
}
```

### Output Format

```json
{
  "audio": "base64_wav_data",
  "sample_rate": 22050,
  "duration": 2.5,
  "text_length": 42,
  "generation_time": 0.5,
  "language": "es",
  "model": "es_ES-mls_10246-low"
}
```

## 💡 Ejemplos

### cURL

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "text": "Hola, este es Piper TTS en español."
    }
  }'
```

### Python

```python
import requests
import base64

response = requests.post(
    f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "input": {
            "text": "¡Hola! Piper TTS es increíblemente rápido."
        }
    }
)

result = response.json()
if "output" in result:
    audio_data = base64.b64decode(result["output"]["audio"])
    with open("output.wav", "wb") as f:
        f.write(audio_data)
```

## ⚙️ RunPod Configuration

```
Container Image: ricardor1267/piper-spanish-worker:latest
Container Disk: 5 GB
GPUs: Cualquiera o CPU
```

## 📊 Performance

- **Cold Start**: 5-10s
- **Warm Request**: 0.3-1s
- **Generation**: Real-time o más rápido
- **VRAM**: 0 MB (usa CPU)

## 🆚 Comparación Completa

| Característica | Piper | MeloTTS | Chatterbox |
|----------------|-------|---------|------------|
| **Tamaño modelo** | 10-30 MB | 100-200 MB | 5.5 GB |
| **Docker size** | 500 MB | 1-2 GB | 8.5 GB |
| **Build time** | 5 min | 10-15 min | 20-30 min |
| **Upload time** | 2-3 min | 5-10 min | 30-60 min |
| **GPU** | ❌ No | ❌ No | ✅ Sí |
| **Velocidad** | ⚡⚡⚡ | ⚡⚡ | ⚡ |
| **Calidad** | Buena | Muy buena | Excelente |
| **Voice cloning** | ❌ | ❌ | ✅ |
| **Costo** | Muy bajo | Bajo | Medio |

## 🎯 ¿Cuándo Usar Piper?

### ✅ Usa Piper si:
- Necesitas el worker **MÁS LIGERO** posible
- Quieres **deploy ultra rápido**
- Trabajas con **presupuesto limitado**
- Solo necesitas **español básico**
- Quieres algo que **siempre funcione**

### ⚠️ NO uses Piper si:
- Necesitas **máxima calidad de voz**
- Requieres **voice cloning**
- Necesitas **control de emoción**
- Quieres **múltiples idiomas**

## 🎤 Voces Disponibles

Piper tiene varias voces en español:

| Voz | Tamaño | Calidad |
|-----|--------|---------|
| `es_ES-mls_10246-low` | ~10 MB | Buena (default) |
| `es_ES-mls_10246-medium` | ~20 MB | Muy buena |
| `es_ES-sharvard-medium` | ~25 MB | Muy buena |
| `es_MX-iss-medium` | ~20 MB | Muy buena (México) |

Para cambiar voz, edita `VOICE_MODEL` en `rp_handler_piper.py`

## 💰 Costos Estimados

### RunPod Serverless

| Config | Costo/hora | Uso Mensual (1000 req/día) |
|--------|-----------|----------------------------|
| 0 active workers | $0 | ~$15-30 |
| 1 active worker (CPU) | ~$0.05 | ~$36 + usage |

**Piper es el más económico** porque:
- Usa CPU (no GPU cara)
- Workers más baratos
- Menos disco necesario

## 🔧 Troubleshooting

### Model download fails
```
# Normal - descargará en primer uso
# Solo ~10 MB, toma segundos
```

### Audio quality low
```
# Usa voz de mayor calidad:
VOICE_MODEL = "es_ES-mls_10246-medium"  # 20 MB
```

## 📝 Archivos

```
chatterbox/
├── rp_handler_piper.py      # Handler para Piper
├── Dockerfile.piper          # Docker ultra-ligero
├── test_input_piper.json     # Input de prueba
└── PIPER_README.md           # Este archivo
```

## 🏆 Resumen

**Piper TTS es perfecto si**:
- ✅ Quieres el worker **MÁS PEQUEÑO**
- ✅ Necesitas **deploy RÁPIDO**  
- ✅ Tienes **presupuesto limitado**
- ✅ Solo necesitas **español**
- ✅ Priorizas **velocidad sobre calidad máxima**

**Total para deploy**:
- Build: 5 min
- Upload: 2-3 min
- **Total: 7-8 minutos** ⚡

## 📞 Links

- **GitHub**: https://github.com/rhasspy/piper
- **Voices**: https://huggingface.co/rhasspy/piper-voices
- **Samples**: https://rhasspy.github.io/piper-samples/
- **License**: MIT

---

**¡Piper es la solución más ligera y rápida para TTS en español! 🚀**

**Deploy time**: 7-8 minutos total
**Docker size**: 500 MB
**Model size**: 10 MB

**¡IMPOSIBLE MÁS LIGERO!** ⚡⚡⚡
