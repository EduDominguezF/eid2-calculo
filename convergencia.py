from series import termino


def analizar_convergencia(resultados, probs, tol=1e-10, k_max=100_000):
    analisis = {}
    for caso, por_p in resultados.items():
        analisis[caso] = {}
        for nombre, sumas in por_p.items():
            limite = sumas[-1] if sumas else 0.0
            k = len(sumas)
            converge = False
            for siguiente_k in range(k + 1, k_max + 1):
                siguiente = limite + termino(caso, siguiente_k, probs[nombre])
                diferencia = abs(siguiente - limite)
                limite = siguiente
                k = siguiente_k
                if diferencia < tol:
                    converge = True
                    break
            analisis[caso][nombre] = {
                "converge": converge,
                "limite": limite,
                "k": k,
            }
    return analisis


def imprimir_convergencia(convergencia):
    print("\nAnálisis de convergencia")
    print(f"{'Caso':<8}{'p':<10}{'Converge':<12}{'Límite empírico':>20}{'Términos usados':>20}")
    orden_casos = ("A", "B", "C")
    casos = sorted(convergencia, key=lambda caso: (orden_casos.index(caso) if caso in orden_casos else len(orden_casos), caso))
    for caso in casos:
        nombres = sorted(
            convergencia[caso],
            key=lambda nombre: (0, int(nombre[1:])) if nombre.startswith("p") and nombre[1:].isdigit() else (1, nombre),
        )
        for nombre in nombres:
            datos = convergencia[caso][nombre]
            estado = "Sí" if datos["converge"] else "No"
            print(f"{caso:<8}{nombre:<10}{estado:<12}{datos['limite']:>20.10f}{datos['k']:>20}")
if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    imprimir_convergencia(analizar_convergencia(calcular_todo(PROBS), PROBS))
