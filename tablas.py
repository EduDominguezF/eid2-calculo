def imprimir_tablas(resultados, probs):
    print("[tablas] pendiente")


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    imprimir_tablas(calcular_todo(PROBS), PROBS)
