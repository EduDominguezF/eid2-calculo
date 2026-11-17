from config import C_MAX, limpiar_rut, calcular_probabilidades
from series import calcular_todo
from tablas import imprimir_tablas
from convergencia import analizar_convergencia, imprimir_convergencia
from graficos import graficar
from viabilidad import tabla_viabilidad, recomendar


def ejecutar(rut_texto):
    rut = limpiar_rut(rut_texto)
    probs = calcular_probabilidades(rut)

    print(f"\nRUT utilizado: {rut_texto.strip()}")
    print("Dígitos d1..d8: " + ", ".join(rut))
    print("Probabilidades: " + ", ".join(f"{n} = {p:.2f}" for n, p in probs.items()))

    resultados = calcular_todo(probs)
    imprimir_tablas(resultados, probs)

    conv = analizar_convergencia(resultados, probs)
    imprimir_convergencia(conv)
    limites = {c: {n: d["limite"] for n, d in por_p.items()} for c, por_p in conv.items()}

    tabla_viabilidad(limites, probs, C_MAX)
    recomendar(limites, probs, C_MAX)

    return graficar(resultados, probs, limites)


def main():
    import matplotlib.pyplot as plt
    while True:
        texto = input("Ingrese el RUT (ej: 24.365.895-K): ")
        try:
            ejecutar(texto)
            break
        except ValueError as e:
            print(f"RUT inválido: {e} Intente nuevamente.")
    plt.show()

if __name__ == "__main__":
    from visualizacion import Aplicacion
    Aplicacion().mainloop()