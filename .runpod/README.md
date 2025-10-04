# 🎙️ Chatterbox TTS - RunPod Serverless

<div align="center">

![Chatterbox](https://www.resemble.ai/wp-content/uploads/2025/09/Chatterbox-Multilingual-1.png)

**Implementación serverless de Chatterbox TTS en RunPod**

[![RunPod](https://img.shields.io/badge/RunPod-Deploy-blue)](https://runpod.io)
[![License](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org)

[Documentación](#documentación) • [Inicio Rápido](#inicio-rápido) • [Ejemplos](#ejemplos) • [Soporte](#soporte)

</div>

---

## 📋 Contenido del Directorio

```
.runpod/
├── handler.py                  # Manejador principal de RunPod
├── Dockerfile                  # Imagen Docker optimizada
├── hub.json                    # Configuración para RunPod Hub
├── tests.json                  # Tests automáticos
├── README.md                   # Este archivo
├── DEPLOYMENT_GUIDE.md         # Guía completa de despliegue
├── integration_examples.py     # Ejemplos de integración
├── test_input.json            # Input de prueba
├── test_local.py              # Script de tests locales
└── build.sh                   # Script de construcción
```

## 🚀 Inicio Rápido

### Opción 1: Desplegar desde RunPod Hub (Recomendado)

1. Ve a [RunPod Hub](https://www.runpod.io/console/hub)
2. Busca "Chatterbox TTS"
3. Click en "Deploy"
4. ¡Listo! Tu endpoint estará disponible en minutos

### Opción 2: Desplegar desde tu propio Docker

```bash
# 1. Construir imagen
./build.sh tu-usuario-dockerhub

# 2. Push a Docker Hub
docker push tu-usuario/chatterbox-runpod:latest

# 3. Crear template en RunPod
# Ve a: https://www.runpod.io/console/serverless/user/templates
# Usa la imagen: tu-usuario/chatterbox-runpod:latest
```

## 📚 Documentación

### Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** | Guía completa paso a paso para desplegar |
| **[integration_examples.py](integration_examples.py)** | Ejemplos en FastAPI, Flask, Django, Streamlit, Telegram, Discord |
| **[handler.py](handler.py)** | Código del manejador de RunPod |
| **[hub.json](hub.json)** | Configuración de metadatos para Hub |
| **[tests.json](tests.json)** | Definición de tests automáticos |

### Uso del API

#### Ejemplo Básico (cURL)

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -d '{
    "input": {
      "text": "Hello world!",
      "model_type": "multilingual",
      "language_id": "en"
    }
  }'
```

#### Ejemplo Python

```python
import requests
import base64

RUNPOD_API_KEY = "your-key"
ENDPOINT_ID = "your-endpoint"

response = requests.post(
    f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    },
    json={
        "input": {
            "text": "Hola, ¿cómo estás?",
            "model_type": "multilingual",
            "language_id": "es",
            "exaggeration": 0.5,
            "cfg_weight": 0.5
        }
    }
)

result = response.json()
if "output" in result:
    audio_data = base64.b64decode(result["output"]["audio"])
    with open("output.wav", "wb") as f:
        f.write(audio_data)
    print(f"✅ Audio guardado! Duración: {result['output']['duration']}s")
```

## 🧪 Tests Locales

### Ejecutar Tests

```bash
cd .runpod

# Tests completos
python test_local.py

# Test manual con test_input.json
python handler.py
```

### Tests Incluidos

- ✅ TTS básico en inglés
- ✅ TTS multilingüe (23 idiomas)
- ✅ Clonación de voz
- ✅ Manejo de errores
- ✅ Validación de parámetros

## 🌍 Idiomas Soportados

<details>
<summary><strong>Ver todos los idiomas (23 total)</strong></summary>

| Código | Idioma | Código | Idioma |
|--------|--------|--------|--------|
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
| `it` | Italian |  |  |
| `ja` | Japanese |  |  |
| `ko` | Korean |  |  |

</details>

## ⚙️ Parámetros del API

### Input Parameters

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `text` | string | ✅ | - | Texto a sintetizar (máx 500 chars) |
| `model_type` | string | ❌ | `"multilingual"` | `"english"` o `"multilingual"` |
| `language_id` | string | ⚠️* | `"en"` | Código de idioma (2 letras) |
| `audio_prompt` | string | ❌ | - | Audio de referencia en base64 |
| `exaggeration` | float | ❌ | `0.5` | Intensidad emocional (0.25-2.0) |
| `temperature` | float | ❌ | `0.8` | Temperatura de muestreo (0.05-5.0) |
| `cfg_weight` | float | ❌ | `0.5` | Peso CFG (0.0-1.0) |
| `seed` | integer | ❌ | `0` | Semilla aleatoria (0=aleatorio) |
| `min_p` | float | ❌ | `0.05` | Umbral mínimo de probabilidad |
| `top_p` | float | ❌ | `1.0` | Nucleus sampling threshold |
| `repetition_penalty` | float | ❌ | `1.2` | Penalización por repetición |

\* Requerido cuando `model_type` es `"multilingual"`

### Output Format

```json
{
  "audio": "base64_encoded_wav_data",
  "sample_rate": 24000,
  "duration": 3.45,
  "model_used": "multilingual",
  "language": "en",
  "text_length": 42
}
```

## 💡 Ejemplos

### 1. TTS Multilingüe

```python
# Español
payload = {
    "input": {
        "text": "Hola mundo, este es Chatterbox",
        "model_type": "multilingual",
        "language_id": "es"
    }
}

# Francés
payload = {
    "input": {
        "text": "Bonjour le monde",
        "model_type": "multilingual",
        "language_id": "fr"
    }
}
```

### 2. Clonación de Voz

```python
import base64

# Leer audio de referencia
with open("mi_voz.wav", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    "input": {
        "text": "Este texto sonará como la voz de referencia",
        "model_type": "multilingual",
        "language_id": "es",
        "audio_prompt": audio_b64
    }
}
```

### 3. Voz Expresiva

```python
# Para voz dramática y expresiva
payload = {
    "input": {
        "text": "¡Esto es increíble!",
        "model_type": "multilingual",
        "language_id": "es",
        "exaggeration": 1.5,  # Más expresión
        "cfg_weight": 0.3      # Habla más lenta
    }
}
```

### 4. Transferencia de Idioma

```python
# Audio en inglés, pero hablar español
# (set cfg_weight=0 para reducir acento)
with open("english_voice.wav", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    "input": {
        "text": "Hola, ahora hablo español",
        "model_type": "multilingual",
        "language_id": "es",
        "audio_prompt": audio_b64,
        "cfg_weight": 0.0  # Reduce transferencia de acento
    }
}
```

## 🔧 Configuración Avanzada

### GPU Recomendadas

Para mejor rendimiento/costo:

| GPU | VRAM | Rendimiento | Costo |
|-----|------|-------------|-------|
| RTX A4000 | 16GB | Bueno | $ |
| RTX A5000 | 24GB | Excelente | $$ |
| L4 | 24GB | Excelente | $$ |
| RTX 4090 | 24GB | Óptimo | $$$ |

### Optimización de Costos

```json
// En hub.json - Limitar a GPUs específicas
{
  "config": {
    "gpuIds": [
      "NVIDIA RTX A4000",
      "NVIDIA L4"
    ]
  }
}
```

### Workers Configuration

- **Development**: 0 active workers (paga solo cuando usas)
- **Production**: 1+ active workers (baja latencia, costo constante)
- **Max Workers**: 3-5 (para manejo de picos)

## 📊 Performance

### Métricas Típicas

- **Cold Start**: 30-60 segundos (primera solicitud)
- **Warm Request**: 2-8 segundos (workers activos)
- **Throughput**: ~10 segundos de audio/segundo de generación
- **VRAM Usage**: ~12-15GB

### Optimizaciones Implementadas

✅ Pre-descarga de modelos en Dockerfile  
✅ Caché de modelos entre invocaciones  
✅ Manejo eficiente de memoria  
✅ Conversión optimizada de audio  

## 🐛 Troubleshooting

### Problema: Cold starts muy lentos

**Solución**: 
- Habilita FlashBoot en RunPod
- Mantén 1 active worker en producción
- Los modelos están pre-descargados en la imagen

### Problema: Out of Memory

**Solución**:
- Usa GPUs con mínimo 16GB VRAM
- Limita `gpuIds` en `hub.json`
- Reduce `max_workers` si es necesario

### Problema: "Unsupported language"

**Solución**:
Usa códigos de idioma válidos (ver lista arriba)

### Problema: Audio de baja calidad

**Solución**:
- Ajusta `exaggeration` (0.3-0.7)
- Ajusta `cfg_weight` (0.3-0.7)
- Usa audio de referencia de alta calidad
- Para transferencia de idioma: `cfg_weight=0`

## 🔐 Watermarking

Todo el audio generado incluye **Perth Watermarking** imperceptible:

- ✅ Sobrevive compresión MP3
- ✅ Resistente a edición de audio
- ✅ ~100% precisión de detección
- ✅ Imperceptible para humanos

## 📖 Recursos

### Documentación

- 📘 [Guía de Despliegue Completa](DEPLOYMENT_GUIDE.md)
- 💻 [Ejemplos de Integración](integration_examples.py)
- 🔧 [RunPod Docs](https://docs.runpod.io)

### Repositorios

- 🐙 [Chatterbox GitHub](https://github.com/resemble-ai/chatterbox)
- 🚀 [RunPod Python SDK](https://github.com/runpod/runpod-python)

### Comunidad

- 💬 [Resemble AI Discord](https://discord.gg/rJq9cRJBJ6)
- 💬 [RunPod Discord](https://discord.gg/runpod)

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](../LICENSE) para detalles.

## 🙏 Agradecimientos

- **Resemble AI** - Por el increíble modelo Chatterbox TTS
- **RunPod** - Por la plataforma serverless GPU
- **Comunidad Open Source** - Por el soporte y feedback

---

<div align="center">

**Hecho con ♥️ por la comunidad**

[⬆ Volver arriba](#-chatterbox-tts---runpod-serverless)

</div>
