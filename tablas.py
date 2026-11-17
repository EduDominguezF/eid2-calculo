"""Requisito 2: imprimir 3 tablas (una por caso), columnas p1, p2, p3 y filas k = 1..10.
(Responsable: Budini)
"""


def imprimir_tablas(resultados, probs):
    """resultados: ver contrato en series.py. probs: {"p1": float, "p2": float, "p3": float}"""
    # TODO Budini
    print("[tablas] pendiente")


if __name__ == "__main__":
    # Prueba independiente con datos de la base
    from config import PROBS
    from series import calcular_todo
    imprimir_tablas(calcular_todo(PROBS), PROBS)
