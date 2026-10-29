from faster_whisper import WhisperModel

modelo = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

segmentos, info = modelo.transcribe(
    "audios/Prueba1.mp4",
    language="es"
)

for segmento in segmentos:
    print(segmento.text)