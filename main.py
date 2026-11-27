
#Nombres: Javier Poblete, Alessandro Budini, Eduardo Dominguez
#Calculo Basico

import sys

from config import C_MAX, limpiar_rut, calcular_probabilidades
from series import calcular_todo
from tablas import imprimir_tablas
from convergencia import analizar_convergencia, imprimir_convergencia
from graficos import graficar
from viabilidad import tabla_viabilidad, recomendar

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")


def ejecutar(rut_texto):
    rut = limpiar_rut(rut_texto)
    probs = calcular_probabilidades(rut)
    d = [int(c) for c in rut]

    print("=" * 70)
    print("EID N°2 - Protocolo ARQ: Límites, Sucesiones y Series")
    print("=" * 70)
    print(f"RUT utilizado: {rut_texto.strip()}")
    print("Dígitos: " + ", ".join(f"d{i} = {c}" for i, c in enumerate(rut, start=1)))
    print(f"p1 = (d1+d3+d5+1)·2/100 = ({d[0]}+{d[2]}+{d[4]}+1)·2/100 = {probs['p1']:.2f}")
    print(f"p2 = (d2+d4+d6+1)·3/100 = ({d[1]}+{d[3]}+{d[5]}+1)·3/100 = {probs['p2']:.2f}")
    print(f"p3 = (d7+d8+1)·4/100    = ({d[6]}+{d[7]}+1)·4/100    = {probs['p3']:.2f}")

    resultados = calcular_todo(probs)
    imprimir_tablas(resultados, probs)

    conv = analizar_convergencia(resultados, probs)
    imprimir_convergencia(conv, resultados)

    viabilidad = tabla_viabilidad(conv, C_MAX)
    recomendacion = recomendar(conv, viabilidad, C_MAX)

    figuras = graficar(conv, C_MAX)
    print("\nGráficos generados: caso_A.png, caso_B.png, caso_C.png")
    return {"figuras": figuras, "probs": probs, "resultados": resultados,
            "convergencia": conv, "viabilidad": viabilidad,
            "recomendacion": recomendacion, "c_max": C_MAX, "rut": rut}


def modo_consola(rut=None):
    import matplotlib.pyplot as plt
    while True:
        texto = rut if rut is not None else input("Ingrese el RUT (ej: 24.365.895-K): ")
        try:
            ejecutar(texto)
            break
        except ValueError as e:
            print(f"RUT inválido: {e} Intente nuevamente.")
            rut = None
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        modo_consola(" ".join(sys.argv[1:]))
    else:
        try:
            from PyQt6.QtWidgets import QApplication
            from visualizacion import Aplicacion
        except ImportError:
            print("PyQt6 no está disponible: se ejecuta en modo consola.")
            modo_consola()
            sys.exit(0)

        aplicacion = QApplication(sys.argv)
        ventana = Aplicacion(ejecutar)
        ventana.show()
        sys.exit(aplicacion.exec())





