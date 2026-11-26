K = 10                 # Número de sumas parciales que se tabulan (S1..S10)
C_MAX = 10             # Umbral de costo máximo (transmisiones esperadas)
CASOS = ["A", "B", "C"]
TOL = 1e-12            # Criterio de parada: término i-ésimo menor que TOL
K_MAX = 100_000        # Máximo de términos antes de declarar divergencia
EPS_ESTABLE = 1e-6     # |S_k - L| < EPS_ESTABLE  =>  la sucesión se considera estabilizada
RUT_PRUEBA = "24365895"

DESCRIPCIONES = {
    "A": "Caso A (WiFi estándar): S_k = Σ i·(1−p)^(i−1)·p",
    "B": "Caso B (fibra, reintentos decrecientes): S_k = Σ (1/i)·(1−p)^(i−1)·p",
    "C": "Caso C (red móvil con copia extra): S_k = Σ (i+1)·(1−p)^(i−1)·p",
}

INTERPRETACIONES = {
    "A": "número esperado de transmisiones",
    "B": "costo total esperado con reintentos decrecientes",
    "C": "costo esperado total incluyendo transmisión base y copia",
}


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


def ordenar_casos(casos):
    return sorted(casos, key=lambda c: (CASOS.index(c) if c in CASOS else len(CASOS), c))


def ordenar_probs(nombres):
    return sorted(nombres, key=lambda n: (0, int(n[1:])) if n[1:].isdigit() else (1, n))


PROBS = calcular_probabilidades(RUT_PRUEBA)
