# 🎯 GUÍA RÁPIDA - Worker de Chatterbox para RunPod

## ✅ Lo Que Se Ha Creado

He creado un worker completo y optimizado para RunPod siguiendo el tutorial oficial:

### Archivos Creados

```
chatterbox/
├── rp_handler.py          ✅ Handler principal con caché de modelos
├── Dockerfile             ✅ Imagen Docker optimizada
├── test_input.json        ✅ Input de prueba
├── build_worker.sh        ✅ Script de construcción
├── test_worker.py         ✅ Script de tests locales
├── WORKER_README.md       ✅ Documentación completa
└── QUICK_START.md         ✅ Esta guía
```

### Características del Worker

✅ **Caché de modelos** - Los modelos se cargan una vez y se reutilizan  
✅ **Manejo de errores** - Validación completa y mensajes claros  
✅ **23 idiomas** - Soporte multilingüe completo  
✅ **Clonación de voz** - Zero-shot voice cloning  
✅ **Logs detallados** - Fácil debugging  
✅ **Pre-carga de modelos** - Dockerfile descarga modelos en build time  

---

## 🚀 OPCIÓN 1: Prueba Local (Recomendado)

Antes de desplegar, prueba localmente:

### Paso 1: Instalar Dependencias

```bash
cd /Users/mimac/mining/testApi/git/chatterbox

# Instalar RunPod SDK
pip install runpod
```

### Paso 2: Probar el Handler

```bash
# Ejecutar tests
python test_worker.py

# O probar con test_input.json
python rp_handler.py
```

**Resultado esperado**:
```
🚀 Starting Chatterbox TTS RunPod Worker...
🔧 Device: CUDA
====================================================================
🎙️  Chatterbox TTS - Processing Request
====================================================================
📝 Text: Hello! Welcome to Chatterbox...
🤖 Model: multilingual
✓ Using cached multilingual model
⚙️  Parameters: exaggeration=0.5, cfg_weight=0.5, temp=0.8
🌍 Language: en (English)
🔊 Generating audio...
📦 Encoding audio...
✓ Success! Generated 3.45s audio in 2.1s
====================================================================
```

---

## 🐳 OPCIÓN 2: Construir Docker

### Paso 1: Construir Imagen

```bash
cd /Users/mimac/mining/testApi/git/chatterbox

# Construir (reemplaza con tu usuario de Docker Hub)
./build_worker.sh ricardor1267

# O manualmente:
docker build --platform linux/amd64 \
  -t ricardor1267/chatterbox-runpod-worker:latest \
  -f Dockerfile .
```

**Tiempo estimado**: 20-40 minutos (descarga modelos)

### Paso 2: Subir a Docker Hub

```bash
# Login
docker login

# Push
docker push ricardor1267/chatterbox-runpod-worker:latest
```

**Tiempo estimado**: 10-30 minutos (dependiendo de tu conexión)

---

## ☁️ OPCIÓN 3: Desplegar en RunPod

### Paso 1: Crear Template

1. Ve a: https://runpod.io/console/serverless/user/templates
2. Click **"New Template"**
3. Configura:

```
Template Name: Chatterbox TTS Worker
Container Image: ricardor1267/chatterbox-runpod-worker:latest
Container Disk: 40 GB
Docker Command: (dejar vacío)
```

4. Click **"Save Template"**

### Paso 2: Crear Endpoint

1. Ve a: https://runpod.io/console/serverless/user/endpoints
2. Click **"New Endpoint"**
3. Configura:

```
Endpoint Name: chatterbox-tts
Template: Chatterbox TTS Worker
Active Workers: 0 (para desarrollo)
Max Workers: 3
GPUs: RTX A4000, L4, RTX 4090 (16-24GB VRAM)
FlashBoot: ✅ Enabled
```

4. Click **"Deploy"**

### Paso 3: Esperar Despliegue

- Tiempo: 5-10 minutos
- Monitorea en la pestaña "Builds"

### Paso 4: Probar

```bash
# Obtén tu ENDPOINT_ID y API_KEY del dashboard

curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "input": {
      "text": "Hello! Testing Chatterbox on RunPod!",
      "model_type": "english"
    }
  }'
```

---

## 📝 Ejemplos de Uso

### Ejemplo 1: TTS Básico

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "input": {
      "text": "Hello world!",
      "model_type": "english"
    }
  }'
```

### Ejemplo 2: Multilingüe

```bash
# Español
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "input": {
      "text": "Hola mundo!",
      "model_type": "multilingual",
      "language_id": "es"
    }
  }'
```

### Ejemplo 3: Con Python

```python
import requests
import base64

API_KEY = "tu-api-key"
ENDPOINT_ID = "tu-endpoint-id"

response = requests.post(
    f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json={
        "input": {
            "text": "Esto es una prueba!",
            "model_type": "multilingual",
            "language_id": "es"
        }
    }
)

result = response.json()
if "output" in result:
    audio_data = base64.b64decode(result["output"]["audio"])
    with open("output.wav", "wb") as f:
        f.write(audio_data)
    print(f"✓ Audio guardado! Duración: {result['output']['duration']}s")
```

---

## 🎯 Próximos Pasos

### Para Desarrollo

```bash
# 1. Prueba local
python test_worker.py

# 2. Modifica rp_handler.py si necesario

# 3. Vuelve a probar
python rp_handler.py
```

### Para Producción

```bash
# 1. Construye Docker
./build_worker.sh ricardor1267

# 2. Sube a Docker Hub
docker push ricardor1267/chatterbox-runpod-worker:latest

# 3. Despliega en RunPod
# (Sigue pasos arriba)

# 4. Configura workers activos
# Active Workers: 1+ para baja latencia
```

---

## 📊 Comparación: Handler Antiguo vs Nuevo

| Característica | handler.py (antiguo) | rp_handler.py (nuevo) |
|----------------|---------------------|----------------------|
| Caché de modelos | ❌ | ✅ |
| Logs detallados | ❌ | ✅ |
| Validación robusta | Básica | ✅ Completa |
| Manejo de errores | Básico | ✅ Avanzado |
| Emojis en logs | ❌ | ✅ |
| Métricas de tiempo | ❌ | ✅ |
| Documentación | Básica | ✅ Completa |

---

## 🔧 Diferencias Clave del Nuevo Worker

### 1. Caché de Modelos
```python
# Antiguo: Cargaba modelo en cada request
MODEL_CACHE = {
    "english": None,
    "multilingual": None
}
# Nuevo: Cachea y reutiliza modelos
```

### 2. Logs Mejorados
```python
# Antiguo: print(f"Generating...")
# Nuevo:
print("=" * 60)
print("🎙️  Chatterbox TTS - Processing Request")
print(f"📝 Text: {text[:100]}...")
print(f"🤖 Model: {model_type}")
```

### 3. Validación Completa
```python
# Valida todos los parámetros
# Mensajes de error claros
# Manejo de edge cases
```

### 4. Métricas
```python
# Retorna generation_time
# Logs de performance
# Tracking de duración
```

---

## 💡 Tips y Mejores Prácticas

### Tip 1: Prueba Local Primero
Siempre prueba localmente antes de construir Docker:
```bash
python test_worker.py
```

### Tip 2: Usa FlashBoot
Habilita FlashBoot en RunPod para cold starts más rápidos

### Tip 3: Active Workers
- **Desarrollo**: 0 active workers (ahorra costos)
- **Producción**: 1+ active workers (baja latencia)

### Tip 4: Monitorea Costos
- Revisa el dashboard de RunPod regularmente
- Set max workers para limitar costos
- Usa /run (async) para batch jobs

### Tip 5: GPU Selection
- **Mínimo**: RTX A4000 (16GB)
- **Recomendado**: RTX A5000 o L4 (24GB)
- **Óptimo**: RTX 4090 (24GB)

---

## ⚠️ Troubleshooting Rápido

### Problema: Test local falla

```bash
# Solución: Instala dependencias
pip install runpod chatterbox-tts
```

### Problema: Docker build lento

```
# Normal: Descarga ~10GB de modelos
# Tiempo: 20-40 minutos
# Paciencia! Solo se hace una vez
```

### Problema: Out of memory en RunPod

```
# Solución: Usa GPU con más VRAM
# Selecciona: RTX A5000, L4, o RTX 4090
```

### Problema: Cold start muy lento

```
# Soluciones:
1. ✅ Habilita FlashBoot
2. ✅ Modelos pre-descargados (ya hecho)
3. ✅ Usa 1+ active workers en producción
```

---

## 📚 Documentación Completa

- **WORKER_README.md** - Documentación técnica completa
- **test_worker.py** - Tests y ejemplos
- **rp_handler.py** - Código del handler (comentado)

---

## 🎉 ¡Listo para Empezar!

### Checklist Rápido

```
[ ] 1. Probar localmente: python test_worker.py
[ ] 2. Construir Docker: ./build_worker.sh ricardor1267
[ ] 3. Subir a Docker Hub: docker push ...
[ ] 4. Crear Template en RunPod
[ ] 5. Crear Endpoint en RunPod
[ ] 6. Probar con curl
[ ] 7. ✅ ¡Funcionando!
```

---

## 🆘 ¿Necesitas Ayuda?

1. **Revisa WORKER_README.md** - Documentación completa
2. **Corre test_worker.py** - Debugging local
3. **Revisa logs en RunPod** - Console → Endpoint → Logs
4. **Pregúntame** - Estoy aquí para ayudar

---

**¡Éxito con tu worker de Chatterbox en RunPod! 🚀**
