import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

# 1. Cargar datos de la Query 02
df = pd.read_csv("data/02_evolucion_temporal_sla.csv")

# 2. Configurar el lienzo
plt.style.use(
    "seaborn-v0_8-whitegrid"
    if "seaborn-v0_8-whitegrid" in plt.style.available
    else "default"
)
fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)

x = df["total_pedidos"]
y = df["tasa_sla_breach"]

# 3. Línea horizontal del promedio histórico (7.9%)
bench_val = 7.94
ax.axhline(
    bench_val,
    color="#7F8C8D",
    linestyle="--",
    linewidth=1.3,
    alpha=0.85,
    label=f"Promedio Histórico ({bench_val:.1f}%)",
    zorder=2,
)

# 4. Diferenciar meses regulares vs. picos de estrés operativo
picos_meses = ["2017-11", "2018-02", "2018-03"]
mask_picos = df["purchase_month"].astype(str).isin(picos_meses)

# Puntos regulares (meses estándar)
ax.scatter(
    x[~mask_picos],
    y[~mask_picos],
    color="#34495E",
    s=60,
    alpha=0.7,
    edgecolors="white",
    linewidth=0.8,
    label="Meses Regulares",
    zorder=4,
)

# Puntos críticos (shock operativo)
ax.scatter(
    x[mask_picos],
    y[mask_picos],
    color="#C0392B",
    s=95,
    alpha=0.95,
    edgecolors="#922B21",
    linewidth=1.5,
    label="Picos de Falla (Shock Operativo)",
    zorder=5,
)

# 5. Etiquetas para los picos críticos
anotaciones = {
    "2017-11": "Black Friday 2017\n(13.8%)",
    "2018-02": "Febrero 2018\n(15.7%)",
    "2018-03": "Huelga Correios 2018\n(20.5%)",
}

for _, row in df[mask_picos].iterrows():
  m = str(row["purchase_month"])
  offset_x = 120
  offset_y = 0.5 if m != "2018-03" else -0.5
  ax.annotate(
      anotaciones[m],
      (row["total_pedidos"], row["tasa_sla_breach"]),
      xytext=(row["total_pedidos"] + offset_x, row["tasa_sla_breach"] + offset_y),
      fontsize=8.5,
      fontweight="bold",
      color="#922B21",
  )

# 6. Formato de ejes y diseño limpio
ax.set_xlabel(
    "Cantidad de Envíos (Volumen Mensual)",
    fontsize=10,
    fontweight="bold",
    color="#2C3E50",
    labelpad=10,
)
ax.set_ylabel(
    "% Envíos Tardes (SLA Breach)",
    fontsize=10,
    fontweight="bold",
    color="#2C3E50",
    labelpad=10,
)
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_ylim(0, 24)

ax.set_title(
    "Dispersión Mensual: Volumen de Envíos vs. Tasa de Incumplimiento SLA",
    fontsize=11.5,
    fontweight="bold",
    color="#1A252F",
    pad=12,
    loc="left",
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(True, linestyle=":", alpha=0.5)
ax.legend(loc="upper left", frameon=True, facecolor="white", fontsize=8.8)

# 7. Guardado
os.makedirs("notebooks/images", exist_ok=True)
plt.tight_layout()
plt.savefig(
    "notebooks/images/scatter_volumen_vs_sla.png", dpi=300, bbox_inches="tight"
)
plt.show()