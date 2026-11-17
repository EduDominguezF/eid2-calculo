"""Requisito 3: para cada (caso, probabilidad) decir si converge y su límite empírico.
(Responsable: Poblete)

Ojo: con solo 10 términos y p chico la suma aún no se estabiliza; conviene seguir sumando
términos (series.termino) hasta que |S_{k+1} - S_k| < tolerancia.

Formato de salida (CONTRATO):
    convergencia = {"A": {"p1": {"converge": bool, "limite": float, "k": int}, ...}, ...}
"""


def analizar_convergencia(resultados, probs, tol=1e-6, k_max=100_000):
    # TODO Poblete. Placeholder: usa S10 como "límite" para que main.py corra.
    return {caso: {n: {"converge": None, "limite": sumas[-1], "k": len(sumas)}
                   for n, sumas in por_p.items()}
            for caso, por_p in resultados.items()}


def imprimir_convergencia(convergencia):
    # TODO Poblete
    print("[convergencia] pendiente")


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    imprimir_convergencia(analizar_convergencia(calcular_todo(PROBS), PROBS))
