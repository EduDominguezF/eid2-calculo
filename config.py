RUT = "24365895"

K = 10         
C_MAX = 10     
CASOS = ["A", "B", "C"]


def calcular_probabilidades(rut=RUT):
    d = [int(c) for c in rut[:8]]
    d1, d2, d3, d4, d5, d6, d7, d8 = d
    return {
        "p1": (d1 + d3 + d5 + 1) * 2 / 100,
        "p2": (d2 + d4 + d6 + 1) * 3 / 100,
        "p3": (d7 + d8 + 1) * 4 / 100,
    }


PROBS = calcular_probabilidades()
