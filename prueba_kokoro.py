
from pathlib import Path
from kokoro_onnx import Kokoro
import sounddevice as sd
import soundfile as sf
import time

# Rutas de los modelos
CARPETA = Path(__file__).resolve().parent

MODELO = CARPETA / "modelos_voz" / "kokoro-v1.0.onnx"
VOCES = CARPETA / "modelos_voz" / "voices-v1.0.bin"

# Inicializar Kokoro
print("Cargando Kokoro...")

kokoro = Kokoro(str(MODELO), str(VOCES))

print("Modelo cargado correctamente.")

# Frase de prueba
texto = (
    "Cámara mis niños soy Xoli, pregúntenme lo que quieran. "
    "¿Qué vamos a descubrir hoy?"
)

# Voz y velocidad
VOZ = "em_santa"
VELOCIDAD = 1.0

print("Generando voz...")

inicio = time.perf_counter()

audio, frecuencia = kokoro.create(
    texto,
    voice=VOZ,
    speed=VELOCIDAD,
    lang="es"
)

fin = time.perf_counter()

print(f"Tiempo de síntesis: {fin - inicio:.2f} s")

# Guardar resultado
sf.write("prueba_xoli.wav", audio, frecuencia)

# Reproducir
print("Xoli está hablando...")

sd.play(audio, frecuencia)
sd.wait()

print("Prueba terminada.")
