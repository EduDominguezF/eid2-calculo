import matplotlib.pyplot as plt

from config import K, C_MAX, DESCRIPCIONES, ordenar_casos, ordenar_probs

COLORES = ["#65a9ff", "#ffbd69", "#54d6a0"]
MARCADORES = ["o", "s", "^"]
ESTILOS = ["-", "--", "-."]
K_GRAFICO_MAX = 1500


def k_para_grafico(convergencia_caso):
    k_grafico = K
    for d in convergencia_caso.values():
        sumas, limite = d["sumas"], d["limite"]
        k = next((i for i, suma in enumerate(sumas, start=1)
                  if abs(suma - limite) <= 0.005 * abs(limite)), len(sumas))
        k_grafico = max(k_grafico, k)
    return min(int(k_grafico * 1.2) + 1, K_GRAFICO_MAX)


def graficar(convergencia, c_max=C_MAX, guardar=True):
    figuras = []
    for caso in ordenar_casos(convergencia):
        figura, ejes = plt.subplots(figsize=(9, 5.5))
        figura.patch.set_facecolor("#151f30")
        ejes.set_facecolor("#151f30")
        por_p = convergencia[caso]
        k_grafico = k_para_grafico(por_p)

        for j, nombre in enumerate(ordenar_probs(por_p)):
            d = por_p[nombre]
            color = COLORES[j % len(COLORES)]
            sumas = d["sumas"][:k_grafico]
            valores_k = range(1, len(sumas) + 1)
            ejes.plot(valores_k, sumas, color=color, linewidth=1.8, linestyle=ESTILOS[j % len(ESTILOS)],
                    label=f"{nombre} = {d['p']:.2f}   →  L ≈ {d['limite']:.4f}")
            ejes.plot(list(valores_k)[:K], sumas[:K], linestyle="none",
                    marker=MARCADORES[j % len(MARCADORES)], color=color, markersize=5)
            ejes.axhline(d["limite"], color=color, linestyle=":", linewidth=1.2, alpha=0.8)
            ejes.annotate(f"L = {d['limite']:.4f}", xy=(k_grafico, d["limite"]),
                        xytext=(-4, 4), textcoords="offset points",
                        ha="right", va="bottom", color=color, fontsize=9, fontweight="bold")

        limite_maximo = max(d["limite"] for d in por_p.values())
        if limite_maximo >= 0.5 * c_max:
            ejes.axhline(c_max, color="#ff667a", linewidth=1.5, label=f"C_máx = {c_max:g}")
        ejes.axvline(K, color="#8796ab", linestyle=":", linewidth=1)
        ejes.text(K, ejes.get_ylim()[0], f" k = {K} (tabla)", color="#aab8cc", fontsize=8,
                va="bottom", ha="left")

        ejes.set_title(DESCRIPCIONES.get(caso, f"Caso {caso}"))
        ejes.set_xlabel("k (número de términos sumados)")
        ejes.set_ylabel("S_k (suma parcial)")
        ejes.tick_params(colors="#c3d0e1")
        ejes.xaxis.label.set_color("#d7e2f0")
        ejes.yaxis.label.set_color("#d7e2f0")
        ejes.title.set_color("#f1f5fb")
        for borde in ejes.spines.values():
            borde.set_color("#46566d")
        ejes.set_xlim(0, k_grafico + 1)
        ejes.grid(True, color="#506079", alpha=0.3)
        ejes.legend(loc="lower right", facecolor="#202c3e", edgecolor="#46566d", labelcolor="#e5edf8")
        figura.tight_layout()
        if guardar:
            figura.savefig(f"caso_{caso}.png", dpi=120)
        figuras.append(figura)
    return figuras


if __name__ == "__main__":
    from config import PROBS
    from series import calcular_todo
    from convergencia import analizar_convergencia
    graficar(analizar_convergencia(calcular_todo(PROBS), PROBS))
    plt.show()
