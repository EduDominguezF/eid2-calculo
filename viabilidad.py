def tabla_viabilidad(limites, probs, c_max):
    print("[viabilidad] pendiente")
    return {}


def recomendar(limites, probs, c_max):
    print("[recomendacion] pendiente")


if __name__ == "__main__":
    limites_falsos = {"A": {"p1": 12.5, "p2": 4.0, "p3": 2.1},
                      "B": {"p1": 0.9, "p2": 0.7, "p3": 0.5},
                      "C": {"p1": 13.5, "p2": 5.0, "p3": 3.1}}
    probs_falsas = {"p1": 0.08, "p2": 0.25, "p3": 0.48}
    tabla_viabilidad(limites_falsos, probs_falsas, 10)
    recomendar(limites_falsos, probs_falsas, 10)
