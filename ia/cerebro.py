
from ollama import chat
import time

# ==========================================
# CONFIGURACIÓN DE XOLI
# ==========================================

MODELO = "qwen3:4b-instruct"

PROMPT_SISTEMA = """
Eres Xoli, un ajolote animatrónico que funciona
como guía interactivo de una escuela de ingeniería.

Tu personalidad es amigable, curiosa y divertida.
Hablas español mexicano de forma natural.

Reglas:
1. Responde en máximo tres oraciones.
2. Conserva el contexto de la conversación.
3. Si el usuario dice "sí", realiza lo que ofreciste.
4. No preguntes repetidamente si quiere un ejemplo.
5. Cuando soliciten un ejemplo, proporciónalo directamente.
6. Evita repetir información que ya explicaste.
7. No inventes información específica de la escuela.
8. Si desconoces una respuesta, reconócelo.
9. No respondas con emojis, ni caracteres. Responde como si estuvieras conversando con alguien en persona.

Prioriza respuestas útiles, concretas y naturales.
"""

# Lista que almacenará la conversación
historial = [
    {
        "role": "system",
        "content": PROMPT_SISTEMA
    }
]

print("Xoli está listo para conversar 🦎")
print("Escribe 'salir' para terminar.\n")


# ==========================================
# BUCLE DE CONVERSACIÓN
# ==========================================

def generar_respuesta(pregunta):
    global historial

    historial.append({
        "role": "user",
        "content": pregunta
    })

    print("Xoli está pensando...")

    inicio = time.perf_counter()
    primer_fragmento = None
    texto = ""

    try:
        respuesta = chat(
            model=MODELO,
            messages=historial,
            think=False,
            stream=True,
            keep_alive="30m",
            options={
                "temperature": 0.5,
                "num_predict": 150
            }
        )

        print("\nXoli: ", end="", flush=True)

        for fragmento in respuesta:
            contenido = fragmento.message.content or ""

            if contenido and primer_fragmento is None:
                primer_fragmento = time.perf_counter()

            print(contenido, end="", flush=True)
            texto += contenido

        fin = time.perf_counter()

        if primer_fragmento is not None:
            print(
                f"\nPrimer texto: "
                f"{primer_fragmento - inicio:.2f} s"
            )

        print(f"Tiempo total: {fin - inicio:.2f} s")

    except Exception as error:
        historial.pop()
        print("\nError:", error)
        return None

    historial.append({
        "role": "assistant",
        "content": texto
    })

    historial = [historial[0]] + historial[1:][-10:]

    return texto


# Permite probar cerebro.py por separado
if __name__ == "__main__":

    print("Xoli está listo para conversar")

    while True:
        try:
            pregunta = input("\nTú: ").strip()

            if pregunta.lower() == "salir":
                break

            if pregunta:
                generar_respuesta(pregunta)

        except KeyboardInterrupt:
            break

