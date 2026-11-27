from config import TOL, K_MAX, EPS_ESTABLE, ordenar_casos, ordenar_probs
from series import termino, razon_cociente, limite_teorico, FORMULAS_LIMITE


def analizar_una(caso, p, tol=TOL, k_max=K_MAX, eps=EPS_ESTABLE):
    sumas, acumulado, converge = [], 0.0, False
    for i in range(1, k_max + 1):
        a_i = termino(caso, i, p)
        acumulado += a_i
        sumas.append(acumulado)
        if i > 1 and a_i < tol:
            converge = razon_cociente(caso, p) < 1
            break

    limite = acumulado
    k_estable = len(sumas)
    while k_estable > 1 and abs(sumas[k_estable - 2] - limite) < eps:
        k_estable -= 1
    teorico = limite_teorico(caso, p)
    return {
        "p": p,
        "razon": razon_cociente(caso, p),
        "converge": converge,
        "limite": limite,
        "teorico": teorico,
        "error": abs(limite - teorico),
        "k_total": len(sumas),
        "k_estable": k_estable,
        "sumas": sumas,
    }


def analizar_convergencia(resultados, probs):
    return {caso: {nombre: analizar_una(caso, probs[nombre]) for nombre in por_p}
            for caso, por_p in resultados.items()}


def imprimir_convergencia(convergencia, resultados=None):
    print("\n2) ANÁLISIS DE CONVERGENCIA")
    print("Criterio del cociente: a_(i+1)/a_i -> (1 - p) < 1 para 0 < p < 1  =>  la serie converge.")
    print(f"Límite empírico: se suman términos hasta que a_i < {TOL:g}; "
          f"k estable = primer k con |S_k - L| < {EPS_ESTABLE:g} para todo k posterior.")
    print("Límites teóricos: A = " + FORMULAS_LIMITE["A"] + ",  B = " + FORMULAS_LIMITE["B"]
          + ",  C = " + FORMULAS_LIMITE["C"])
    encabezado = (f"{'Caso':<6}{'p':<12}{'Razón':>8}{'Converge':>10}{'S10':>14}"
                  f"{'Límite empírico':>18}{'Límite teórico':>17}{'Error':>11}{'k estable':>11}")
    print("-" * len(encabezado))
    print(encabezado)
    print("-" * len(encabezado))
    for caso in ordenar_casos(convergencia):
        for nombre in ordenar_probs(convergencia[caso]):
            d = convergencia[caso][nombre]
            s10 = resultados[caso][nombre][-1] if resultados else d["sumas"][min(9, len(d["sumas"]) - 1)]
            estado = "Sí" if d["converge"] else "No"
            print(f"{caso:<6}{nombre + '=' + format(d['p'], '.2f'):<12}{d['razon']:>8.4f}{estado:>10}"
                  f"{s10:>14.6f}{d['limite']:>18.10f}{d['teorico']:>17.10f}"
                  f"{d['error']:>11.1e}{d['k_estable']:>11}")
    print("-" * len(encabezado))
    datos = [d for por_p in convergencia.values() for d in por_p.values()]
    n_convergentes = sum(d["converge"] for d in datos)
    error_maximo = max(d["error"] for d in datos)
    print(f"Conclusión: {n_convergentes} de {len(datos)} sucesiones convergen; "
          f"el límite empírico coincide con el teórico (error máximo {error_maximo:.1e}).")
    print("Mientras menor es p, la razón (1 - p) se acerca a 1 y se necesitan más términos para estabilizar.")


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    resultados = calcular_todo(PROBS)
    imprimir_convergencia(analizar_convergencia(resultados, PROBS), resultados)
