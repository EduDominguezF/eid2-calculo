from config import DESCRIPCIONES, ordenar_casos, ordenar_probs


def imprimir_tablas(resultados, probs):
    ancho_fila = 6
    ancho_col = 14
    nombres = ordenar_probs(probs)
    separador = "=" * (ancho_fila + (ancho_col + 3) * len(nombres))

    print("\n1) SUMAS PARCIALES S1..S10")
    for caso in ordenar_casos(resultados):
        por_p = resultados[caso]
        print()
        print(separador)
        print(DESCRIPCIONES.get(caso, f"Caso {caso}"))
        print(separador)

        encabezado = f"{'k':<{ancho_fila}}" + "".join(
            f" | {f'{n} = {probs[n]:.2f}':>{ancho_col}}" for n in nombres)
        print(encabezado)
        print("-" * len(encabezado))

        for i in range(len(por_p[nombres[0]])):
            fila = f"{f'S{i + 1}':<{ancho_fila}}" + "".join(
                f" | {por_p[n][i]:>{ancho_col}.6f}" for n in nombres)
            print(fila)
        print(separador)


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    imprimir_tablas(calcular_todo(PROBS), PROBS)
