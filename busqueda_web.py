
from ddgs import DDGS

def buscar_internet(pregunta):
    try:
        buscador = DDGS()

        resultados = buscador.text(
            pregunta,
            region="mx-es",
            max_results=3
        )

        fuentes = []

        for resultado in resultados:
            fuentes.append({
                "titulo": resultado.get("title", ""),
                "url": resultado.get("href", ""),
                "resumen": resultado.get("body", "")
            })

        return fuentes

    except Exception as error:
        print("Error en búsqueda web:", error)
        return []


if __name__ == "__main__":
    pregunta = input("¿Qué quieres buscar? ")

    resultados = buscar_internet(pregunta)

    for resultado in resultados:
        print("\nTítulo:", resultado["titulo"])
        print("Resumen:", resultado["resumen"])
        print("Fuente:", resultado["url"])
