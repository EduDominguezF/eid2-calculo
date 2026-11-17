"""Requisito 4: 3 gráficos (uno por caso), cada uno con 3 curvas S_k vs k
y una línea horizontal en el valor al que se estabiliza cada curva.
(Responsable: Budini)
"""
import matplotlib.pyplot as plt


def graficar(resultados, probs, limites):
    """limites: {"A": {"p1": float, "p2": float, "p3": float}, "B": {...}, "C": {...}}"""
    # TODO Budini (usar plt.savefig para guardar los PNG y plt.show() al final)
    print("[graficos] pendiente")


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    res = calcular_todo(PROBS)
    limites_falsos = {c: {n: s[-1] for n, s in por_p.items()} for c, por_p in res.items()}
    graficar(res, PROBS, limites_falsos)
