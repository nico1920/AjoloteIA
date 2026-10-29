
from pathlib import Path
from kokoro_onnx import Kokoro
import librosa
import soundfile as sf
import sounddevice as sd

CARPETA = Path(__file__).resolve().parent

kokoro = Kokoro(
    str(CARPETA / "modelos_voz" / "kokoro-v1.0.onnx"),
    str(CARPETA / "modelos_voz" / "voices-v1.0.bin")
)

texto = (
    "¡Holaaaa! ¡Soy Xoli! "
    "¡Qué emoción conocerte! "
    "¿Quieres descubrir algo increíble conmigo?"
)

# Generamos una sola vez el audio original
audio, frecuencia = kokoro.create(
    texto,
    voice="ef_dora",
    speed=1.08,
    lang="es"
)

# Probamos diferentes tonos
for semitonos in [0, 2, 4, 6]:
    print(f"\nProbando tono: +{semitonos} semitonos")

    if semitonos == 0:
        resultado = audio
    else:
        resultado = librosa.effects.pitch_shift(
            audio,
            sr=frecuencia,
            n_steps=semitonos
        )

    nombre = CARPETA / f"xoli_tono_{semitonos}.wav"
    sf.write(nombre, resultado, frecuencia)

    sd.play(resultado, frecuencia)
    sd.wait()

print("\n¡Pruebas terminadas!")

