K = 10
C_MAX = 10
CASOS = ["A", "B", "C"]
RUT_PRUEBA = "24365895"


def limpiar_rut(texto):
    limpio = texto.replace(".", "").replace("-", "").replace(" ", "").upper()
    primeros = limpio[:8]
    if len(primeros) < 8 or not primeros.isdigit():
        raise ValueError("El RUT debe tener al menos 8 dígitos (sin contar la K).")
    return primeros


def calcular_probabilidades(rut):
    d1, d2, d3, d4, d5, d6, d7, d8 = (int(c) for c in rut)
    return {
        "p1": (d1 + d3 + d5 + 1) * 2 / 100,
        "p2": (d2 + d4 + d6 + 1) * 3 / 100,
        "p3": (d7 + d8 + 1) * 4 / 100,
    }


PROBS = calcular_probabilidades(RUT_PRUEBA)
