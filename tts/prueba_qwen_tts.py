
from pathlib import Path
import time

import torch
import soundfile as sf
import sounddevice as sd
from qwen_tts import Qwen3TTSModel

CARPETA = Path(__file__).resolve().parent

MODELO = "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign"

DESCRIPCION = (
                   "A voice reminiscent of Unikitty from The LEGO Movie, "
    "but with a lower, more natural pitch. "
    "A lively, friendly animated character with a light, "
    "rounded voice and casual Mexican Spanish pronunciation. "
    "The delivery is conversational, not theatrical."
)

TEXTO = (
    "Hola, Soy Xoli."
    "Qué emoción conocerte! "
    "¿Qué te gustaría preguntar?"
)

# Seleccionar dispositivo disponible
dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"
tipo_dato = torch.float16 if dispositivo.startswith("cuda") else torch.float32

print(f"Dispositivo: {dispositivo}")
print("Cargando modelo Qwen3-TTS...")

inicio = time.perf_counter()

modelo = Qwen3TTSModel.from_pretrained(
    MODELO,
    device_map=dispositivo,
    dtype=tipo_dato,
    attn_implementation="sdpa"
)

print(f"Modelo cargado en {time.perf_counter() - inicio:.2f} s")

print("Generando la voz de Xoli...")
inicio = time.perf_counter()

with torch.inference_mode():
    audios, frecuencia = modelo.generate_voice_design(
        text=TEXTO,
        language="Spanish",
        instruct=DESCRIPCION,
    )

duracion = time.perf_counter() - inicio
print(f"Tiempo de generación: {duracion:.2f} s")

archivo = CARPETA / "xoli_qwen.wav"

sf.write(str(archivo), audios[0], frecuencia)
print(f"Audio guardado en: {archivo}")

sd.play(audios[0], frecuencia)
sd.wait()

print("¡Prueba terminada!")
