import matplotlib.pyplot as plt


def graficar(resultados, probs, limites):
    print("[graficos] pendiente")
    return []


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    res = calcular_todo(PROBS)
    limites_prueba = {c: {n: s[-1] for n, s in por_p.items()} for c, por_p in res.items()}
    graficar(res, PROBS, limites_prueba)
    plt.show()
