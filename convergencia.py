def analizar_convergencia(resultados, probs, tol=1e-10, k_max=100_000):
    return {caso: {n: {"converge": None, "limite": sumas[-1], "k": len(sumas)}
                   for n, sumas in por_p.items()}
            for caso, por_p in resultados.items()}


def imprimir_convergencia(convergencia):
    print("[convergencia] pendiente")


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    imprimir_convergencia(analizar_convergencia(calcular_todo(PROBS), PROBS))
