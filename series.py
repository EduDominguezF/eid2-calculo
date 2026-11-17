from config import K, CASOS


def termino(caso, i, p):
    q = 1 - p
    if caso == "A":
        return i * q ** (i - 1) * p
    if caso == "B":
        return (1 / i) * q ** (i - 1) * p
    if caso == "C":
        return (i + 1) * q ** (i - 1) * p
    raise ValueError(f"Caso desconocido: {caso}")


def sucesion(caso, p, k=K):
    sumas, acumulado = [], 0.0
    for i in range(1, k + 1):
        acumulado += termino(caso, i, p)
        sumas.append(acumulado)
    return sumas


def calcular_todo(probs, k=K):
    return {caso: {nombre: sucesion(caso, p, k) for nombre, p in probs.items()}
            for caso in CASOS}
