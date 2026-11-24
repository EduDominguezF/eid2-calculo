def tabla_viabilidad(limites, probs, c_max):
    viabilidad = {}
    print(f"\nTabla de viabilidad (umbral: {c_max:g})")
    print(f"{'Caso':<8}{'p':<18}{'Límite':>16}{'Estado':>14}")
    orden_casos = ("A", "B", "C")
    casos = sorted(limites, key=lambda caso: (orden_casos.index(caso) if caso in orden_casos else len(orden_casos), caso))
    for caso in casos:
        viabilidad[caso] = {}
        nombres = sorted(
            limites[caso],
            key=lambda nombre: (0, int(nombre[1:])) if nombre.startswith("p") and nombre[1:].isdigit() else (1, nombre),
        )
        for nombre in nombres:
            limite = limites[caso][nombre]
            cumple = limite <= c_max
            viabilidad[caso][nombre] = cumple
            p = probs[nombre]
            estado = "CUMPLE" if cumple else "NO CUMPLE"
            print(f"{caso:<8}{nombre}={p:<13.4f}{limite:>16.6f}{estado:>14}")
    return viabilidad


def recomendar(limites, probs, c_max):
    descripciones = {
        "A": "número esperado de transmisiones",
        "B": "costo con reintentos más baratos",
        "C": "costo con copia extra",
    }
    orden_casos = ("A", "B", "C")
    candidatas = []
    casos = sorted(limites, key=lambda caso: (orden_casos.index(caso) if caso in orden_casos else len(orden_casos), caso))
    for caso in casos:
        nombres = sorted(
            limites[caso],
            key=lambda nombre: (0, int(nombre[1:])) if nombre.startswith("p") and nombre[1:].isdigit() else (1, nombre),
        )
        for nombre in nombres:
            limite = limites[caso][nombre]
            if limite <= c_max:
                orden_p = int(nombre[1:]) if nombre.startswith("p") and nombre[1:].isdigit() else 0
                candidatas.append((limite, orden_casos.index(caso) if caso in orden_casos else len(orden_casos), orden_p, caso, nombre))
    if not candidatas:
        print(f"\nNo hay combinaciones viables: ninguna cumple el umbral de {c_max:g}.")
        return
    limite, _, _, caso, nombre = min(candidatas)
    margen = c_max - limite
    print(f"\nRecomendación: Caso {caso}, {nombre} (p={probs[nombre]:.4f}).")
    print(
        f"La serie del Caso {caso} ({descripciones.get(caso, 'costo esperado')}) converge "
        f"a {limite:.6f}; cumple el umbral de {c_max:g} con un margen de {margen:.6f}."
    )


if __name__ == "__main__":
    limites_prueba = {"A": {"p1": 12.5, "p2": 4.0, "p3": 2.1},
                      "B": {"p1": 0.9, "p2": 0.7, "p3": 0.5},
                      "C": {"p1": 13.5, "p2": 5.0, "p3": 3.1}}
    probs_prueba = {"p1": 0.08, "p2": 0.25, "p3": 0.48}
    tabla_viabilidad(limites_prueba, probs_prueba, 10)
    recomendar(limites_prueba, probs_prueba, 10)
