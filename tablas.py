DESCRIPCIONES = {
    "A": "Caso A – WiFi estándar: i·(1−p)^(i−1)·p",
    "B": "Caso B: (1/i)·(1−p)^(i−1)·p",
    "C": "Caso C: (i+1)·(1−p)^(i−1)·p",
}


def imprimir_tablas(resultados, probs):
    ancho_fila = 6
    ancho_col = 14
    nombres = list(probs.keys())
    separador = "=" * (ancho_fila + (ancho_col + 3) * len(nombres))

    for caso, por_p in resultados.items():
        print()
        print(separador)
        print(DESCRIPCIONES.get(caso, f"Caso {caso}"))
        print(separador)

        encabezado = f"{'Sk':<{ancho_fila}}" + "".join(
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
