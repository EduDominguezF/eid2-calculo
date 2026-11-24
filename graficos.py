import matplotlib.pyplot as plt

TITULOS = {
    "A": "Caso A – WiFi estándar: i·(1−p)^(i−1)·p",
    "B": "Caso B: (1/i)·(1−p)^(i−1)·p",
    "C": "Caso C: (i+1)·(1−p)^(i−1)·p",
}

COLORES = ["tab:blue", "tab:orange", "tab:green"]
MARCADORES = ["o", "s", "^"]


def graficar(resultados, probs, limites):
    figuras = []
    for caso in ["A", "B", "C"]:
        fig, ax = plt.subplots(figsize=(8, 5))
        for j, (nombre, sumas) in enumerate(resultados[caso].items()):
            color = COLORES[j % len(COLORES)]
            limite = limites[caso][nombre]
            ks = range(1, len(sumas) + 1)
            ax.plot(ks, sumas, color=color, marker=MARCADORES[j % len(MARCADORES)],
                    label=f"{nombre} = {probs[nombre]:.2f}  (límite ≈ {limite:.4f})")
            ax.axhline(limite, color=color, linestyle=":", linewidth=1.5)
        ax.set_title(TITULOS.get(caso, f"Caso {caso}"))
        ax.set_xlabel("k")
        ax.set_ylabel("Sk")
        ax.set_xticks(list(range(1, len(sumas) + 1)))
        ax.grid(True, alpha=0.4)
        ax.legend()
        fig.tight_layout()
        fig.savefig(f"caso_{caso}.png", dpi=120)
        figuras.append(fig)
    return figuras


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    res = calcular_todo(PROBS)
    limites_prueba = {c: {n: s[-1] for n, s in por_p.items()} for c, por_p in res.items()}
    graficar(res, PROBS, limites_prueba)
    plt.show()
