import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import re

# Configuración
FRECUENCIA = 16000
BLOQUE = 1600             # 0.1 segundos
UMBRAL = 0.015           # Sensibilidad del micrófono
SILENCIO_FINAL = 3     # Segundos para terminar
ESPERA_MAXIMA = 10       # Tiempo máximo esperando voz
DURACION_MAXIMA = 30     # Seguridad

print("Cargando modelo...")

modelo = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("Xoli está listo")


def corregir_nombre(texto):
    return re.sub(
        r"\b(sholi|sholito|xolito|xoli)\b",
        "Xoli",
        texto,
        flags=re.IGNORECASE
    )


def detectar_activacion(texto):
    return bool(
        re.search(r"\bXoli\b", texto, re.IGNORECASE)
    )


def grabar_audio():
    print("Escuchando...")

    fragmentos = []
    voz_detectada = False
    silencio = 0
    tiempo = 0

    duracion_bloque = BLOQUE / FRECUENCIA

    with sd.InputStream(
        samplerate=FRECUENCIA,
        channels=1,
        dtype="float32",
        blocksize=BLOQUE
    ) as stream:

        while tiempo < DURACION_MAXIMA:

            audio, overflow = stream.read(BLOQUE)

            if overflow:
                print("Advertencia: se perdieron muestras.")

            fragmentos.append(audio.copy())

            # Calcular intensidad del audio
            volumen = np.sqrt(np.mean(audio ** 2))

            tiempo += duracion_bloque

            if volumen > UMBRAL:
                voz_detectada = True
                silencio = 0

            elif voz_detectada:
                silencio += duracion_bloque

            # Terminar después de una pausa
            if voz_detectada and silencio >= SILENCIO_FINAL:
                print("Fin de la pregunta detectado.")
                break

            # No se detectó ninguna voz
            if not voz_detectada and tiempo >= ESPERA_MAXIMA:
                print("No se detectó voz.")
                break

    if not voz_detectada:
        return None

    return np.concatenate(fragmentos).flatten()

def reconocer_voz():
    audio = grabar_audio()

    if audio is None:
        return None

    print("Procesando audio...")

    segmentos, info = modelo.transcribe(
        audio,
        language="es",
        initial_prompt=(
            "Xoli es un ajolote animatrónico. "
            "Su nombre se escribe Xoli."
        )
    )

    texto = " ".join(
        segmento.text.strip()
        for segmento in segmentos
    )

    texto = corregir_nombre(texto)

    return texto.strip()

if __name__ == "__main__":
    while True:
        try:
            input("\nPresiona ENTER para hablar con Xoli...")

            texto = reconocer_voz()

            if texto:
                print("Escuché:", texto)

                if detectar_activacion(texto):
                    print(" ¡Me llamaron!")
                else:
                    print(" No escuché mi nombre.")

        except KeyboardInterrupt:
            print("\nPrograma detenido.")
            break