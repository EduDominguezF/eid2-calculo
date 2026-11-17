"""Punto de entrada: python main.py  (Responsable: base — nadie más lo edita)"""
from config import RUT, PROBS, C_MAX
from series import calcular_todo
from tablas import imprimir_tablas
from convergencia import analizar_convergencia, imprimir_convergencia
from graficos import graficar
from viabilidad import tabla_viabilidad, recomendar


def main():
    print(f"RUT utilizado: {RUT}")
    print("Probabilidades: " + ", ".join(f"{n} = {p:.2f}" for n, p in PROBS.items()))

    resultados = calcular_todo(PROBS)
    imprimir_tablas(resultados, PROBS)

    conv = analizar_convergencia(resultados, PROBS)
    imprimir_convergencia(conv)
    limites = {c: {n: d["limite"] for n, d in por_p.items()} for c, por_p in conv.items()}

    tabla_viabilidad(limites, PROBS, C_MAX)
    recomendar(limites, PROBS, C_MAX)

    graficar(resultados, PROBS, limites)  # al final, porque plt.show() bloquea


if __name__ == "__main__":
    main()
