# Guía de Despliegue de Chatterbox en RunPod

Esta guía te llevará paso a paso desde el código hasta tener tu endpoint de Chatterbox funcionando en RunPod.

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Pruebas Locales](#pruebas-locales)
4. [Construcción y Push de la Imagen Docker](#construcción-y-push-de-la-imagen-docker)
5. [Configuración en RunPod](#configuración-en-runpod)
6. [Publicación en RunPod Hub](#publicación-en-runpod-hub)
7. [Uso del API](#uso-del-api)
8. [Troubleshooting](#troubleshooting)

---

## Requisitos Previos

### Software Necesario

- **Python 3.11** o superior
- **Docker Desktop** instalado y en ejecución
- **Cuenta en Docker Hub** (https://hub.docker.com)
- **Cuenta en RunPod** (https://runpod.io)
- **Git** para clonar el repositorio

### Hardware Recomendado

Para pruebas locales:
- GPU NVIDIA con al menos 16GB VRAM (opcional, puede probar con CPU)
- 32GB RAM
- 50GB de espacio en disco

---

## Estructura del Proyecto

Después de seguir esta guía, tu proyecto tendrá la siguiente estructura:

```
chatterbox/
├── .runpod/
│   ├── handler.py          # Manejador de RunPod
│   ├── Dockerfile          # Imagen Docker para RunPod
│   ├── hub.json           # Configuración de RunPod Hub
│   ├── tests.json         # Tests automáticos
│   ├── README.md          # Documentación para Hub
│   ├── test_input.json    # Input de prueba
│   ├── test_local.py      # Script de pruebas locales
│   ├── build.sh           # Script de construcción
│   └── DEPLOYMENT_GUIDE.md # Esta guía
├── src/
│   └── chatterbox/        # Código fuente de Chatterbox
├── pyproject.toml         # Dependencias del proyecto
└── README.md              # README original
```

---

## Pruebas Locales

### Paso 1: Instalar Dependencias

```bash
cd /Users/mimac/mining/testApi/git/chatterbox

# Crear entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar Chatterbox
pip install -e .

# Instalar RunPod SDK
pip install runpod
```

### Paso 2: Probar el Handler Localmente

```bash
cd .runpod

# Ejecutar tests locales
python test_local.py
```

Esto probará:
- ✅ TTS básico en inglés
- ✅ TTS multilingüe (inglés, español, francés)
- ✅ Manejo de errores
- ✅ Variaciones de parámetros

### Paso 3: Prueba con test_input.json

```bash
# Desde el directorio .runpod
python handler.py

# O usando el formato de RunPod
python -c "
import json
from handler import handler

with open('test_input.json') as f:
    job = json.load(f)

result = handler({'input': job['input']})
print(json.dumps(result, indent=2))
"
```

---

## Construcción y Push de la Imagen Docker

### Paso 1: Preparar Docker Hub

1. Inicia sesión en Docker Hub:
```bash
docker login
# Ingresa tu usuario y contraseña de Docker Hub
```

### Paso 2: Construir la Imagen

**Opción A: Usar el script de construcción**

```bash
cd /Users/mimac/mining/testApi/git/chatterbox

# Reemplaza 'tu-usuario' con tu nombre de usuario de Docker Hub
./.runpod/build.sh tu-usuario
```

**Opción B: Construir manualmente**

```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd /Users/mimac/mining/testApi/git/chatterbox

# Construir la imagen (IMPORTANTE: debe ser linux/amd64)
docker build --platform linux/amd64 \
  -t tu-usuario/chatterbox-runpod:latest \
  -f .runpod/Dockerfile .
```

**Nota importante**: El parámetro `--platform linux/amd64` es **obligatorio** porque RunPod usa servidores Linux AMD64. Sin esto, obtendrás errores de "exec format error".

### Paso 3: Probar la Imagen Localmente (Opcional)

```bash
# Ejecutar el contenedor localmente
docker run --rm \
  --gpus all \
  -v $(pwd)/.runpod:/workspace/.runpod \
  tu-usuario/chatterbox-runpod:latest

# Nota: Verás un warning sobre test_input.json - esto es normal
```

### Paso 4: Push a Docker Hub

```bash
docker push tu-usuario/chatterbox-runpod:latest
```

Este proceso puede tomar 10-30 minutos dependiendo de tu conexión, ya que la imagen es grande (~10-15GB).

---

## Configuración en RunPod

### Paso 1: Crear un Template

1. Ve a [RunPod Templates](https://www.runpod.io/console/serverless/user/templates)
2. Click en **"New Template"**
3. Configura:
   - **Template Name**: `Chatterbox TTS`
   - **Container Image**: `tu-usuario/chatterbox-runpod:latest`
   - **Container Disk**: `40 GB`
   - **Docker Command**: Deja en blanco (usa CMD del Dockerfile)
   
4. En **Advanced**:
   - **Environment Variables**: Ninguna necesaria por ahora
   - **Expose HTTP Ports**: Deja vacío
   - **Expose TCP Ports**: Deja vacío

5. Click **"Save Template"**

### Paso 2: Crear un Endpoint

1. Ve a [RunPod Endpoints](https://www.runpod.io/console/serverless/user/endpoints)
2. Click en **"New Endpoint"**
3. Configura:
   - **Endpoint Name**: `chatterbox-tts`
   - **Select Template**: Selecciona tu template "Chatterbox TTS"
   - **Active Workers**: `0` (para desarrollo - 1 para producción)
   - **Max Workers**: `3`
   - **Idle Timeout**: `5` segundos
   - **FlashBoot**: Activado (recomendado)
   - **GPUs/Worker**: `1`

4. Selecciona GPUs permitidas (recomendado):
   - ✅ NVIDIA RTX A4000 (16GB)
   - ✅ NVIDIA RTX A5000 (24GB)
   - ✅ NVIDIA L4 (24GB)
   - ✅ NVIDIA RTX 4090 (24GB)

5. Click **"Deploy"**

### Paso 3: Esperar el Despliegue

El primer despliegue puede tomar 5-10 minutos:
- RunPod descargará tu imagen Docker
- Iniciará el build
- Ejecutará los health checks

Monitorea el progreso en la pestaña **"Builds"**.

---

## Publicación en RunPod Hub

Si quieres publicar tu modelo en el RunPod Hub para que otros lo usen:

### Paso 1: Preparar el Repositorio GitHub

1. **Hacer Fork del Repositorio Original**:
   ```bash
   # Si aún no has hecho fork, ve a:
   # https://github.com/resemble-ai/chatterbox
   # Y haz click en "Fork"
   ```

2. **Agregar los Archivos RunPod**:
   ```bash
   cd /Users/mimac/mining/testApi/git/chatterbox
   git add .runpod/
   git commit -m "Add RunPod serverless support"
   git push origin master
   ```

### Paso 2: Conectar GitHub con RunPod

1. Ve a [RunPod Settings](https://www.runpod.io/console/user/settings)
2. En la sección **"Connections"**, busca **GitHub**
3. Click en **"Connect"**
4. Autoriza RunPod en GitHub
5. Selecciona "Only select repositories" y elige tu fork de Chatterbox

### Paso 3: Publicar en el Hub

1. Ve a [RunPod Hub Publishing](https://www.runpod.io/console/hub/publish)
2. Selecciona tu repositorio de GitHub
3. RunPod detectará automáticamente los archivos `.runpod/hub.json` y `.runpod/tests.json`
4. Revisa la configuración y click **"Publish"**

### Paso 4: Validación

RunPod ejecutará automáticamente:
- Build de la imagen Docker
- Tests definidos en `tests.json`
- Validación de la configuración

Si todo pasa, tu modelo estará disponible en el Hub público de RunPod.

---

## Uso del API

### Obtener tu API Key

1. Ve a [RunPod Settings - API Keys](https://www.runpod.io/console/user/settings)
2. Click en **"Create API Key"**
3. Guarda la key de forma segura

### Ejemplos de Uso

#### 1. TTS Básico en Inglés (Bash/cURL)

```bash
#!/bin/bash

RUNPOD_API_KEY="tu-api-key-aqui"
ENDPOINT_ID="tu-endpoint-id"

curl -X POST "https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -d '{
    "input": {
      "text": "Hello! This is Chatterbox text to speech.",
      "model_type": "english",
      "exaggeration": 0.5,
      "cfg_weight": 0.5
    }
  }' | jq '.'
```

#### 2. TTS Multilingüe (Python)

```python
import requests
import base64
import json

RUNPOD_API_KEY = "tu-api-key-aqui"
ENDPOINT_ID = "tu-endpoint-id"

def synthesize_speech(text, language="en", save_path="output.wav"):
    """Sintetiza voz y guarda el audio"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    payload = {
        "input": {
            "text": text,
            "model_type": "multilingual",
            "language_id": language,
            "exaggeration": 0.5,
            "cfg_weight": 0.5
        }
    }
    
    print(f"Sintetizando: '{text[:50]}...'")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        if "output" in result:
            # Decodificar y guardar audio
            audio_data = base64.b64decode(result["output"]["audio"])
            
            with open(save_path, "wb") as f:
                f.write(audio_data)
            
            print(f"✅ Audio guardado en: {save_path}")
            print(f"   Duración: {result['output']['duration']}s")
            print(f"   Idioma: {result['output']['language']}")
            return save_path
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return None
    else:
        print(f"❌ HTTP Error {response.status_code}: {response.text}")
        return None

# Ejemplo de uso
synthesize_speech(
    text="Hola, este es un ejemplo de síntesis de voz en español.",
    language="es",
    save_path="output_spanish.wav"
)
```

#### 3. Clonación de Voz con Audio de Referencia (Python)

```python
import requests
import base64

def synthesize_with_voice(text, reference_audio_path, language="en"):
    """Sintetiza voz clonando la voz del audio de referencia"""
    
    # Leer y codificar audio de referencia
    with open(reference_audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    payload = {
        "input": {
            "text": text,
            "model_type": "multilingual",
            "language_id": language,
            "audio_prompt": audio_b64,  # Audio de referencia
            "exaggeration": 0.5,
            "cfg_weight": 0.5
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if "output" in result:
        audio_data = base64.b64decode(result["output"]["audio"])
        output_path = "cloned_voice_output.wav"
        
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        print(f"✅ Voz clonada guardada en: {output_path}")
        return output_path
    else:
        print(f"❌ Error: {result}")
        return None

# Ejemplo
synthesize_with_voice(
    text="This will sound like the reference voice!",
    reference_audio_path="mi_voz.wav",
    language="en"
)
```

#### 4. Procesamiento Asíncrono (Para Lotes)

```python
import requests
import time

def async_synthesis(texts, language="en"):
    """Procesa múltiples textos de forma asíncrona"""
    url_run = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    url_status = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    job_ids = []
    
    # Enviar todos los trabajos
    for text in texts:
        payload = {
            "input": {
                "text": text,
                "model_type": "multilingual",
                "language_id": language
            }
        }
        
        response = requests.post(url_run, headers=headers, json=payload)
        result = response.json()
        
        if "id" in result:
            job_ids.append((result["id"], text[:30]))
            print(f"✅ Job enviado: {result['id']}")
    
    # Esperar resultados
    completed = []
    while len(completed) < len(job_ids):
        for job_id, text_preview in job_ids:
            if job_id in [c[0] for c in completed]:
                continue
            
            response = requests.get(
                f"{url_status}/{job_id}",
                headers=headers
            )
            result = response.json()
            
            status = result.get("status")
            
            if status == "COMPLETED":
                completed.append((job_id, result))
                print(f"✅ Completado: {text_preview}...")
            elif status == "FAILED":
                completed.append((job_id, {"error": result.get("error")}))
                print(f"❌ Fallido: {text_preview}...")
        
        if len(completed) < len(job_ids):
            time.sleep(2)  # Esperar antes de volver a verificar
    
    return completed

# Ejemplo
texts = [
    "Hello, this is the first text.",
    "This is the second text to synthesize.",
    "And here's the third one."
]

results = async_synthesis(texts, language="en")
```

---

## Troubleshooting

### Problema: "exec format error"

**Causa**: La imagen Docker no se construyó para linux/amd64.

**Solución**:
```bash
docker build --platform linux/amd64 -t tu-usuario/chatterbox-runpod:latest -f .runpod/Dockerfile .
```

### Problema: Cold Start muy lento (>60 segundos)

**Causa**: El modelo se descarga en cada inicio.

**Soluciones**:
1. Usar FlashBoot en RunPod (habilitar en configuración del endpoint)
2. Pre-descargar modelos en el Dockerfile (ya implementado)
3. Mantener 1 Active Worker para producción

### Problema: Out of Memory (OOM)

**Causa**: GPU sin suficiente VRAM.

**Soluciones**:
- Usar GPUs con mínimo 16GB VRAM
- En `hub.json`, limita a GPUs específicas:
  ```json
  "gpuIds": ["NVIDIA RTX A5000", "NVIDIA L4", "NVIDIA RTX 4090"]
  ```

### Problema: "Unsupported language: xx"

**Causa**: Código de idioma inválido.

**Solución**: Usa uno de los 23 idiomas soportados:
```
ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh
```

### Problema: Audio con calidad pobre

**Soluciones**:
1. Verifica que el audio de referencia sea de alta calidad
2. Ajusta parámetros:
   - `exaggeration`: 0.3-0.7
   - `cfg_weight`: 0.3-0.7
3. Para transferencia de idioma, usa `cfg_weight=0`

### Problema: Endpoint no responde

**Pasos de diagnóstico**:
1. Verifica que el endpoint esté activo en el dashboard
2. Revisa los logs en la pestaña "Logs" del endpoint
3. Verifica que tu API key sea correcta
4. Intenta con el test request en la consola de RunPod

### Problema: Build falla en RunPod

**Causa común**: Dependencias faltantes o error en Dockerfile.

**Solución**:
1. Revisa los logs del build
2. Prueba construir localmente primero
3. Verifica que todas las dependencias estén en `pyproject.toml`

---

## Recursos Adicionales

- **Documentación RunPod**: https://docs.runpod.io
- **Chatterbox GitHub**: https://github.com/resemble-ai/chatterbox
- **RunPod Discord**: https://discord.gg/runpod
- **Resemble AI Discord**: https://discord.gg/rJq9cRJBJ6

---

## Próximos Pasos

Después de completar esta guía:

1. ✅ Optimiza tu endpoint según tus necesidades de costo/latencia
2. ✅ Implementa monitoreo y logging
3. ✅ Configura alertas para errores
4. ✅ Considera usar Network Volumes para modelos grandes
5. ✅ Implementa rate limiting si es público
6. ✅ Documenta casos de uso específicos para tu aplicación

---

**¿Necesitas ayuda?** Abre un issue en el repositorio o únete a nuestro Discord.
