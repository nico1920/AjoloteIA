
import subprocess
import sys
import wave
import time
from pathlib import Path

import numpy as np
import sounddevice as sd

# ==========================================
# CONFIGURACIÓN DE VOZ
# ==========================================

CARPETA = Path(__file__).resolve().parent

MODELO_VOZ = (
    CARPETA
    / "modelos_voz"
    / "es_MX-ald-medium.onnx"
)

ARCHIVO_AUDIO = CARPETA / "respuesta_xoli.wav"


# ==========================================
# SÍNTESIS DE VOZ
# ==========================================

def sintetizar_voz(texto):

    if not texto or not texto.strip():
        return

    if not MODELO_VOZ.exists():
        print("No se encontró el modelo de voz.")
        return

    print("Xoli está preparando su voz...")

    inicio = time.perf_counter()

    # Ejecutamos Piper desde nuestro entorno virtual
    comando = [
        sys.executable,
        "-m",
        "piper",
        "-m",
        str(MODELO_VOZ),
        "-f",
        str(ARCHIVO_AUDIO),
        "--",
        texto
    ]

    try:
        subprocess.run(
            comando,
            check=True
        )

    except subprocess.CalledProcessError as error:
        print("Error al generar audio:", error)
        return

    fin = time.perf_counter()

    print(
        f"Síntesis completada en "
        f"{fin - inicio:.2f} segundos"
    )

    reproducir_audio()


# ==========================================
# REPRODUCCIÓN
# ==========================================

def reproducir_audio():

    with wave.open(str(ARCHIVO_AUDIO), "rb") as wav:

        frecuencia = wav.getframerate()
        canales = wav.getnchannels()
        muestras = wav.readframes(wav.getnframes())

        audio = np.frombuffer(
            muestras,
            dtype=np.int16
        ).reshape(-1, canales)

    print("Xoli está hablando...")

    sd.play(audio, samplerate=frecuencia)
    sd.wait()


# ==========================================
# PRUEBA INDIVIDUAL
# ==========================================

if __name__ == "__main__":

    sintetizar_voz(
        "¡Hola! Soy Sholi, tu ajolote de confianza. "
        "¿Qué vamos a descubrir hoy?"
    )
