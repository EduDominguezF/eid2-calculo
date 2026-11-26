from config import INTERPRETACIONES, ordenar_casos, ordenar_probs


def tabla_viabilidad(convergencia, c_max):
    viabilidad = {}
    print(f"\n3) TABLA DE VIABILIDAD (umbral C_máx = {c_max:g} transmisiones esperadas)")
    encabezado = f"{'Caso':<6}{'p':<12}{'Límite empírico':>18}{'¿≤ C_máx?':>12}{'Estado':>12}"
    print("-" * len(encabezado))
    print(encabezado)
    print("-" * len(encabezado))
    for caso in ordenar_casos(convergencia):
        viabilidad[caso] = {}
        for nombre in ordenar_probs(convergencia[caso]):
            d = convergencia[caso][nombre]
            cumple = d["converge"] and d["limite"] <= c_max
            viabilidad[caso][nombre] = cumple
            print(f"{caso:<6}{nombre + '=' + format(d['p'], '.2f'):<12}{d['limite']:>18.6f}"
                  f"{'Sí' if cumple else 'No':>12}{'CUMPLE' if cumple else 'NO CUMPLE':>12}")
    print("-" * len(encabezado))
    total = sum(v for por_p in viabilidad.values() for v in por_p.values())
    print(f"Combinaciones que cumplen: {total} de {sum(len(v) for v in viabilidad.values())}.")
    return viabilidad


def recomendar(convergencia, viabilidad, c_max):
    """Entre las viables minimiza el límite (costo esperado); desempata por k estable."""
    candidatas = []
    for caso in ordenar_casos(convergencia):
        for nombre in ordenar_probs(convergencia[caso]):
            if viabilidad[caso][nombre]:
                d = convergencia[caso][nombre]
                candidatas.append((d["limite"], d["k_estable"], caso, nombre))

    print("\n4) RECOMENDACIÓN")
    if not candidatas:
        print(f"No hay combinaciones viables: ninguna cumple el umbral de {c_max:g}.")
        return None

    _, _, caso, nombre = min(candidatas)
    d = convergencia[caso][nombre]
    margen = c_max - d["limite"]
    print(f"Se recomienda: Caso {caso} con {nombre} = {d['p']:.2f}.")
    print("Justificación (análisis de convergencia):")
    print(f"  - La serie converge (criterio del cociente: razón 1 - p = {d['razon']:.4f} < 1).")
    print(f"  - Su límite empírico es {d['limite']:.6f} ({INTERPRETACIONES[caso]}), "
          f"igual al teórico {d['teorico']:.6f}.")
    print(f"  - Cumple C_máx = {c_max:g} con un margen de {margen:.6f}.")
    print(f"  - Entre las opciones viables, tiene el menor costo esperado; "
          f"se estabiliza en k = {d['k_estable']} términos (|S_k - L| < 1e-6).")

    no_viables = [(c, n) for c in viabilidad for n in viabilidad[c] if not viabilidad[c][n]]
    if no_viables:
        lista = ", ".join(f"{c}-{n}" for c, n in no_viables)
        print(f"  - Se descartan {lista}: su límite supera C_máx porque p es pequeño "
              f"(1/p crece) y la convergencia es lenta.")
    return caso, nombre


if __name__ == "__main__":
    from config import PROBS, C_MAX
    from series import calcular_todo
    from convergencia import analizar_convergencia
    conv = analizar_convergencia(calcular_todo(PROBS), PROBS)
    recomendar(conv, tabla_viabilidad(conv, C_MAX), C_MAX)
