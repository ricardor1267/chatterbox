# 🇪🇸 MeloTTS-Spanish - RunPod Serverless Worker

TTS ligero y rápido optimizado para español (~100-200 MB de modelo).

## ⚡ Ventajas vs Chatterbox

| Característica | MeloTTS-Spanish | Chatterbox Multilingual |
|----------------|-----------------|------------------------|
| **Tamaño del modelo** | ~100-200 MB | ~5.5 GB |
| **Tamaño Docker** | ~1-2 GB | ~8.5 GB |
| **Tiempo de subida** | 5-10 min | 30-60 min |
| **Tiempo de build** | 10-15 min | 20-30 min |
| **Idiomas** | Solo español | 23 idiomas |
| **Voice cloning** | ❌ No | ✅ Sí |
| **Velocidad** | ⚡ Muy rápido | Rápido |
| **CPU inference** | ✅ Sí | ❌ No (GPU) |

## 🚀 Quick Start

### Opción 1: Build Local

```bash
cd /Users/mimac/mining/testApi/git/chatterbox

# Build
docker build --platform linux/amd64 \
  -t ricardor1267/melotts-spanish-worker:latest \
  -f Dockerfile.melo .

# Push
docker push ricardor1267/melotts-spanish-worker:latest
```

### Opción 2: Deploy desde GitHub

1. Conectar GitHub a RunPod
2. Crear template:
   - Repository: `ricardor1267/chatterbox`
   - Branch: `master`
   - **Dockerfile Path**: `Dockerfile.melo`
3. Deploy

## 📖 API Usage

### Input Format

```json
{
  "input": {
    "text": "Texto a sintetizar",
    "speed": 1.0
  }
}
```

### Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `text` | string | *required* | - | Texto en español |
| `speed` | float | `1.0` | 0.5-2.0 | Velocidad de habla |

### Output Format

```json
{
  "audio": "base64_wav_data",
  "sample_rate": 44100,
  "text_length": 42,
  "generation_time": 1.2,
  "language": "es",
  "speed": 1.0
}
```

## 💡 Ejemplos

### Básico (cURL)

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "text": "Hola mundo, este es un ejemplo de MeloTTS en español."
    }
  }'
```

### Con Velocidad Ajustada

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "text": "Este texto se leerá más lentamente.",
      "speed": 0.8
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
            "text": "¡Hola! Este es MeloTTS en español.",
            "speed": 1.0
        }
    }
)

result = response.json()
if "output" in result:
    audio_data = base64.b64decode(result["output"]["audio"])
    with open("output.wav", "wb") as f:
        f.write(audio_data)
    print(f"Audio guardado! Duración: {result['output']['generation_time']}s")
```

## ⚙️ RunPod Configuration

### Template Settings

```
Container Image: ricardor1267/melotts-spanish-worker:latest
Container Disk: 10 GB (mucho menos que Chatterbox)
Docker Command: (dejar vacío)
```

### Endpoint Settings

```
Active Workers: 0 (dev) o 1+ (prod)
Max Workers: 3-5
GPUs: Cualquier GPU o incluso CPU
FlashBoot: ✅ Enabled
```

## 📊 Performance

### Métricas

- **Cold Start**: 10-20s (modelo pequeño)
- **Warm Request**: 0.5-2s
- **Generation Speed**: Muy rápido (~real-time)
- **VRAM Usage**: 500MB-1GB (o CPU)

### Comparación de Costos

| Config | MeloTTS | Chatterbox |
|--------|---------|------------|
| **Container Disk** | 10 GB | 40 GB |
| **GPU Required** | ❌ No | ✅ Sí |
| **Active Worker Cost** | ~$0.10/hr | ~$0.40/hr |

## 🎯 Características

### ✅ Pros

- ⚡ Muy ligero y rápido
- 💰 Costo reducido
- 🖥️ Funciona en CPU
- 🚀 Build y deploy rápidos
- 🇪🇸 Optimizado para español

### ⚠️ Contras

- Solo español (sin otros idiomas)
- Sin voice cloning
- Sin control de emoción
- Calidad ligeramente menor que Chatterbox

## 🔧 Troubleshooting

### Error: Model download failed

```bash
# El modelo se descarga en el primer uso
# Es normal ver este warning en el build
```

### Audio quality issues

```python
# Ajusta la velocidad
speed = 0.9  # Más lento y claro
speed = 1.2  # Más rápido
```

## 📝 Archivos del Proyecto

```
chatterbox/
├── rp_handler_melo.py       # Handler para MeloTTS
├── Dockerfile.melo           # Dockerfile ligero
├── test_input_melo.json      # Input de prueba
└── MELOTTS_README.md         # Este archivo
```

## 🆚 ¿Cuándo Usar Cada Modelo?

### Usa MeloTTS-Spanish si:
- ✅ Solo necesitas español
- ✅ Quieres ahorro de costos
- ✅ Necesitas build/deploy rápido
- ✅ No necesitas voice cloning
- ✅ Funciona con CPU

### Usa Chatterbox si:
- ✅ Necesitas múltiples idiomas
- ✅ Requieres voice cloning
- ✅ Necesitas control de emoción
- ✅ Quieres máxima calidad
- ✅ Tienes GPU disponible

## 🎉 Ventajas para RunPod

1. **Build Rápido**: 10-15 minutos vs 20-30 min
2. **Subida Rápida**: 5-10 minutos vs 30-60 min
3. **Disco Menor**: 10 GB vs 40 GB
4. **Costo Menor**: Funciona en CPU
5. **Cold Start Rápido**: Modelo pequeño

## 📞 Soporte

- **GitHub**: https://github.com/myshell-ai/MeloTTS
- **HuggingFace**: https://huggingface.co/myshell-ai/MeloTTS-Spanish
- **Licencia**: MIT (uso comercial permitido)

---

**¡MeloTTS-Spanish es perfecto si solo necesitas español y quieres optimizar costos! 🚀**
