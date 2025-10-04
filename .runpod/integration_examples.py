"""
Ejemplos de integración de Chatterbox RunPod en diferentes frameworks
"""

# ============================================================================
# EJEMPLO 1: FastAPI Backend
# ============================================================================

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import requests
import base64
from typing import Optional

app = FastAPI()

RUNPOD_API_KEY = "your-api-key"
ENDPOINT_ID = "your-endpoint-id"


class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    exaggeration: float = 0.5
    cfg_weight: float = 0.5


@app.post("/synthesize")
async def synthesize_text(request: TTSRequest):
    """Endpoint para sintetizar texto a voz"""
    
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    payload = {
        "input": {
            "text": request.text,
            "model_type": "multilingual",
            "language_id": request.language,
            "exaggeration": request.exaggeration,
            "cfg_weight": request.cfg_weight
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if "output" in result:
            return {
                "success": True,
                "audio_base64": result["output"]["audio"],
                "duration": result["output"]["duration"],
                "sample_rate": result["output"]["sample_rate"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
            
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clone-voice")
async def clone_voice(
    text: str,
    language: str = "en",
    audio_file: UploadFile = File(...)
):
    """Endpoint para clonar voz desde audio de referencia"""
    
    # Leer audio de referencia
    audio_bytes = await audio_file.read()
    audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
    
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
            "audio_prompt": audio_b64,
            "exaggeration": 0.5,
            "cfg_weight": 0.5
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if "output" in result:
            return {
                "success": True,
                "audio_base64": result["output"]["audio"],
                "duration": result["output"]["duration"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error"))
            
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# EJEMPLO 2: Flask Application
# ============================================================================

from flask import Flask, request, jsonify, send_file
import requests
import base64
import io

flask_app = Flask(__name__)

RUNPOD_API_KEY = "your-api-key"
ENDPOINT_ID = "your-endpoint-id"


@flask_app.route('/tts', methods=['POST'])
def text_to_speech():
    """Flask endpoint para TTS"""
    data = request.json
    
    text = data.get('text')
    language = data.get('language', 'en')
    
    if not text:
        return jsonify({'error': 'Missing text parameter'}), 400
    
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
            "exaggeration": data.get('exaggeration', 0.5),
            "cfg_weight": data.get('cfg_weight', 0.5)
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        result = response.json()
        
        if "output" in result:
            # Opción 1: Devolver base64
            return jsonify({
                'success': True,
                'audio': result["output"]["audio"],
                'duration': result["output"]["duration"]
            })
        else:
            return jsonify({'error': result.get('error', 'Unknown error')}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@flask_app.route('/tts/audio', methods=['POST'])
def text_to_speech_audio():
    """Flask endpoint que devuelve audio directamente"""
    data = request.json
    text = data.get('text')
    language = data.get('language', 'en')
    
    if not text:
        return jsonify({'error': 'Missing text parameter'}), 400
    
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    payload = {
        "input": {
            "text": text,
            "model_type": "multilingual",
            "language_id": language
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        result = response.json()
        
        if "output" in result:
            # Decodificar y devolver audio
            audio_data = base64.b64decode(result["output"]["audio"])
            audio_io = io.BytesIO(audio_data)
            audio_io.seek(0)
            
            return send_file(
                audio_io,
                mimetype='audio/wav',
                as_attachment=True,
                download_name='speech.wav'
            )
        else:
            return jsonify({'error': result.get('error')}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# EJEMPLO 3: Django View
# ============================================================================

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
import base64
import json

RUNPOD_API_KEY = "your-api-key"
ENDPOINT_ID = "your-endpoint-id"


@csrf_exempt
@require_http_methods(["POST"])
def django_tts_view(request):
    """Django view para TTS"""
    try:
        data = json.loads(request.body)
        text = data.get('text')
        language = data.get('language', 'en')
        
        if not text:
            return JsonResponse({'error': 'Missing text parameter'}, status=400)
        
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
                "exaggeration": data.get('exaggeration', 0.5),
                "cfg_weight": data.get('cfg_weight', 0.5)
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        result = response.json()
        
        if "output" in result:
            return JsonResponse({
                'success': True,
                'audio': result["output"]["audio"],
                'duration': result["output"]["duration"],
                'sample_rate': result["output"]["sample_rate"]
            })
        else:
            return JsonResponse(
                {'error': result.get('error', 'Unknown error')},
                status=500
            )
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# EJEMPLO 4: Streamlit App
# ============================================================================

import streamlit as st
import requests
import base64
from io import BytesIO

RUNPOD_API_KEY = "your-api-key"
ENDPOINT_ID = "your-endpoint-id"


def streamlit_tts_app():
    """Aplicación Streamlit para TTS"""
    
    st.title("🎙️ Chatterbox TTS - Multilingual")
    st.write("Genera voz en 23 idiomas usando Chatterbox")
    
    # Inputs
    text = st.text_area(
        "Texto a sintetizar:",
        "Hola, este es un ejemplo de síntesis de voz.",
        height=150
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox(
            "Idioma:",
            ["en", "es", "fr", "de", "it", "pt", "ja", "zh", "ar", "hi"],
            index=1
        )
    
    with col2:
        model_type = st.selectbox(
            "Modelo:",
            ["multilingual", "english"]
        )
    
    # Parámetros avanzados
    with st.expander("⚙️ Parámetros avanzados"):
        exaggeration = st.slider("Exaggeration", 0.25, 2.0, 0.5, 0.05)
        cfg_weight = st.slider("CFG Weight", 0.0, 1.0, 0.5, 0.05)
        temperature = st.slider("Temperature", 0.05, 5.0, 0.8, 0.05)
    
    # Audio de referencia
    audio_file = st.file_uploader(
        "Audio de referencia (opcional):",
        type=['wav', 'mp3', 'flac']
    )
    
    if st.button("🎵 Generar Audio", type="primary"):
        with st.spinner("Generando audio..."):
            
            url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {RUNPOD_API_KEY}"
            }
            
            payload = {
                "input": {
                    "text": text,
                    "model_type": model_type,
                    "language_id": language if model_type == "multilingual" else "en",
                    "exaggeration": exaggeration,
                    "cfg_weight": cfg_weight,
                    "temperature": temperature
                }
            }
            
            # Agregar audio de referencia si existe
            if audio_file is not None:
                audio_bytes = audio_file.read()
                audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
                payload["input"]["audio_prompt"] = audio_b64
            
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=120)
                result = response.json()
                
                if "output" in result:
                    # Decodificar audio
                    audio_data = base64.b64decode(result["output"]["audio"])
                    
                    # Mostrar información
                    st.success("✅ Audio generado exitosamente!")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Duración", f"{result['output']['duration']}s")
                    col2.metric("Sample Rate", f"{result['output']['sample_rate']}Hz")
                    col3.metric("Idioma", result['output']['language'])
                    
                    # Reproducir audio
                    st.audio(audio_data, format='audio/wav')
                    
                    # Botón de descarga
                    st.download_button(
                        label="📥 Descargar Audio",
                        data=audio_data,
                        file_name="chatterbox_output.wav",
                        mime="audio/wav"
                    )
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ============================================================================
# EJEMPLO 5: Cliente Python Asíncrono
# ============================================================================

import asyncio
import aiohttp
import base64


class ChatterboxClient:
    """Cliente asíncrono para Chatterbox RunPod"""
    
    def __init__(self, api_key: str, endpoint_id: str):
        self.api_key = api_key
        self.endpoint_id = endpoint_id
        self.base_url = f"https://api.runpod.ai/v2/{endpoint_id}"
        
    async def synthesize(
        self,
        text: str,
        language: str = "en",
        model_type: str = "multilingual",
        audio_prompt: bytes = None,
        **kwargs
    ):
        """Sintetiza texto a voz de forma asíncrona"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "input": {
                "text": text,
                "model_type": model_type,
                "language_id": language,
                **kwargs
            }
        }
        
        if audio_prompt:
            payload["input"]["audio_prompt"] = base64.b64encode(audio_prompt).decode('utf-8')
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/runsync",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                result = await response.json()
                
                if "output" in result:
                    audio_data = base64.b64decode(result["output"]["audio"])
                    return {
                        "audio": audio_data,
                        "duration": result["output"]["duration"],
                        "sample_rate": result["output"]["sample_rate"],
                        "language": result["output"]["language"]
                    }
                else:
                    raise Exception(result.get("error", "Unknown error"))
    
    async def synthesize_batch(self, texts: list, language: str = "en"):
        """Sintetiza múltiples textos en paralelo"""
        tasks = [
            self.synthesize(text, language)
            for text in texts
        ]
        return await asyncio.gather(*tasks)


async def example_async():
    """Ejemplo de uso del cliente asíncrono"""
    client = ChatterboxClient(
        api_key="your-api-key",
        endpoint_id="your-endpoint-id"
    )
    
    # Síntesis simple
    result = await client.synthesize(
        text="Hello, this is an async example!",
        language="en"
    )
    
    print(f"Audio duration: {result['duration']}s")
    
    # Síntesis en lote
    texts = [
        "This is the first text.",
        "And this is the second text.",
        "Finally, the third text."
    ]
    
    results = await client.synthesize_batch(texts, language="en")
    
    for i, result in enumerate(results):
        print(f"Text {i+1}: {result['duration']}s")


# ============================================================================
# EJEMPLO 6: Telegram Bot
# ============================================================================

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import base64
from io import BytesIO

TELEGRAM_BOT_TOKEN = "your-telegram-token"
RUNPOD_API_KEY = "your-api-key"
ENDPOINT_ID = "your-endpoint-id"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await update.message.reply_text(
        "¡Hola! 👋\n\n"
        "Envíame un texto y lo convertiré en voz.\n\n"
        "Comandos:\n"
        "/lang <código> - Cambiar idioma (ej: /lang es)\n"
        "/help - Mostrar ayuda"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    await update.message.reply_text(
        "🎙️ Chatterbox TTS Bot\n\n"
        "Idiomas soportados:\n"
        "en - English\n"
        "es - Español\n"
        "fr - Français\n"
        "de - Deutsch\n"
        "it - Italiano\n"
        "pt - Português\n"
        "ja - 日本語\n"
        "zh - 中文\n"
        "Y 15 más...\n\n"
        "Uso:\n"
        "1. Selecciona idioma: /lang es\n"
        "2. Envía tu texto\n"
        "3. Recibe el audio"
    )


async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /lang para cambiar idioma"""
    if not context.args:
        await update.message.reply_text("Uso: /lang <código>\nEjemplo: /lang es")
        return
    
    lang = context.args[0].lower()
    context.user_data['language'] = lang
    await update.message.reply_text(f"✅ Idioma cambiado a: {lang}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes de texto y los convierte en voz"""
    text = update.message.text
    language = context.user_data.get('language', 'en')
    
    # Enviar mensaje de "escribiendo..."
    await update.message.reply_text("🎵 Generando audio...")
    
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
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        result = response.json()
        
        if "output" in result:
            # Decodificar audio
            audio_data = base64.b64decode(result["output"]["audio"])
            audio_io = BytesIO(audio_data)
            audio_io.seek(0)
            
            # Enviar audio
            await update.message.reply_voice(
                voice=audio_io,
                caption=f"🎵 Duración: {result['output']['duration']}s"
            )
        else:
            await update.message.reply_text(
                f"❌ Error: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def run_telegram_bot():
    """Inicia el bot de Telegram"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("lang", lang_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot iniciado...")
    app.run_polling()


# ============================================================================
# EJEMPLO 7: Discord Bot
# ============================================================================

import discord
from discord.ext import commands
import requests
import base64
from io import BytesIO

DISCORD_BOT_TOKEN = "your-discord-token"
RUNPOD_API_KEY = "your-api-key"
ENDPOINT_ID = "your-endpoint-id"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')


@bot.command(name='tts')
async def discord_tts(ctx, language: str = "en", *, text: str):
    """
    Genera audio TTS
    Uso: !tts es Hola mundo
    """
    await ctx.send("🎵 Generando audio...")
    
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
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        result = response.json()
        
        if "output" in result:
            audio_data = base64.b64decode(result["output"]["audio"])
            audio_file = discord.File(
                BytesIO(audio_data),
                filename="speech.wav"
            )
            
            await ctx.send(
                f"🎵 Duración: {result['output']['duration']}s",
                file=audio_file
            )
        else:
            await ctx.send(f"❌ Error: {result.get('error')}")
            
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='languages')
async def list_languages(ctx):
    """Lista idiomas soportados"""
    langs = """
    🌍 **Idiomas Soportados:**
    
    • en - English
    • es - Español
    • fr - Français
    • de - Deutsch
    • it - Italiano
    • pt - Português
    • ja - 日本語
    • zh - 中文
    • ar - العربية
    • hi - हिन्दी
    
    Y 13 más...
    """
    await ctx.send(langs)


# Para ejecutar el bot:
# bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    print("Ejemplos de integración cargados.")
    print("Ejecuta las funciones específicas según tu framework.")
