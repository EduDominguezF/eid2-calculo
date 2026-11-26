import matplotlib.pyplot as plt

from config import K, C_MAX, DESCRIPCIONES, ordenar_casos, ordenar_probs

COLORES = ["#65a9ff", "#ffbd69", "#54d6a0"]
MARCADORES = ["o", "s", "^"]
ESTILOS = ["-", "--", "-."]
K_GRAFICO_MAX = 300


def k_para_grafico(convergencia_caso):
    """Rango de k suficiente para que todas las curvas se vean estabilizadas (error < 0.5%)."""
    k_graf = K
    for d in convergencia_caso.values():
        sumas, limite = d["sumas"], d["limite"]
        k = next((i for i, s in enumerate(sumas, start=1)
                  if abs(s - limite) <= 0.005 * abs(limite)), len(sumas))
        k_graf = max(k_graf, k)
    return min(int(k_graf * 1.2) + 1, K_GRAFICO_MAX)


def graficar(convergencia, c_max=C_MAX, guardar=True):
    figuras = []
    for caso in ordenar_casos(convergencia):
        fig, ax = plt.subplots(figsize=(9, 5.5))
        fig.patch.set_facecolor("#151f30")
        ax.set_facecolor("#151f30")
        por_p = convergencia[caso]
        k_graf = k_para_grafico(por_p)

        for j, nombre in enumerate(ordenar_probs(por_p)):
            d = por_p[nombre]
            color = COLORES[j % len(COLORES)]
            sumas = d["sumas"][:k_graf]
            ks = range(1, len(sumas) + 1)
            ax.plot(ks, sumas, color=color, linewidth=1.8, linestyle=ESTILOS[j % len(ESTILOS)],
                    label=f"{nombre} = {d['p']:.2f}   →  L ≈ {d['limite']:.4f}")
            ax.plot(list(ks)[:K], sumas[:K], linestyle="none",
                    marker=MARCADORES[j % len(MARCADORES)], color=color, markersize=5)
            ax.axhline(d["limite"], color=color, linestyle=":", linewidth=1.2, alpha=0.8)
            ax.annotate(f"L = {d['limite']:.4f}", xy=(k_graf, d["limite"]),
                        xytext=(-4, 4), textcoords="offset points",
                        ha="right", va="bottom", color=color, fontsize=9, fontweight="bold")

        max_lim = max(d["limite"] for d in por_p.values())
        if max_lim >= 0.5 * c_max:
            ax.axhline(c_max, color="#ff667a", linewidth=1.5, label=f"C_máx = {c_max:g}")
        ax.axvline(K, color="#8796ab", linestyle=":", linewidth=1)
        ax.text(K, ax.get_ylim()[0], f" k = {K} (tabla)", color="#aab8cc", fontsize=8,
                va="bottom", ha="left")

        ax.set_title(DESCRIPCIONES.get(caso, f"Caso {caso}"))
        ax.set_xlabel("k (número de términos sumados)")
        ax.set_ylabel("S_k (suma parcial)")
        ax.tick_params(colors="#c3d0e1")
        ax.xaxis.label.set_color("#d7e2f0")
        ax.yaxis.label.set_color("#d7e2f0")
        ax.title.set_color("#f1f5fb")
        for borde in ax.spines.values():
            borde.set_color("#46566d")
        ax.set_xlim(0, k_graf + 1)
        ax.grid(True, color="#506079", alpha=0.3)
        ax.legend(loc="lower right", facecolor="#202c3e", edgecolor="#46566d", labelcolor="#e5edf8")
        fig.tight_layout()
        if guardar:
            fig.savefig(f"caso_{caso}.png", dpi=120)
        figuras.append(fig)
    return figuras


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    from convergencia import analizar_convergencia
    graficar(analizar_convergencia(calcular_todo(PROBS), PROBS))
    plt.show()
