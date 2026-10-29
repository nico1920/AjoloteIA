
from ia.microfono import reconocer_voz, detectar_activacion
from ia.cerebro import generar_respuesta

# ==========================================
# CONFIGURACIÓN
# ==========================================

MAX_TURNOS = 5

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():

    turnos_restantes = 0

    print("\nXoli está listo para conversar.")
    print("Presiona Ctrl+C para salir.")

    while True:

        input("\nPresiona ENTER para hablar con Xoli...")

        # 1. Escuchar y transcribir
        texto = reconocer_voz()

        if not texto:
            print("No se detectó ninguna pregunta.")
            continue

        print("\nEscuché:", texto)

        # 2. Detectar si mencionaron su nombre
        activado = detectar_activacion(texto)

        # 3. Comprobar estado de conversación
        if turnos_restantes == 0:

            if not activado:
                print("Xoli está esperando su nombre.")
                continue

            print("¡Xoli activado!")
            turnos_restantes = MAX_TURNOS

        elif activado:
            # Si vuelven a llamarlo, reiniciamos turnos
            turnos_restantes = MAX_TURNOS

        # 4. Enviar la pregunta al cerebro
        respuesta = generar_respuesta(texto)

        # 5. Actualizar estado
        if respuesta is not None:

            turnos_restantes -= 1

            print(
                f"\nTurnos restantes: {turnos_restantes}"
            )

        if turnos_restantes == 0:
            print("\nXoli volvió al estado de espera.")


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\nXoli se ha despedido.")
