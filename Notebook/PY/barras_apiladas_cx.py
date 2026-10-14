import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

# 1. Cargar el CSV exportado de la Query 07
df = pd.read_csv("data/07_degradacion_satisfaccion_tramos.csv")

fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)

colores = ["#C0392B", "#E67E22", "#F1C40F", "#82E0AA", "#27AE60"]
categorias = [
    "pct_1_estrella",
    "pct_2_estrellas",
    "pct_3_estrellas",
    "pct_4_estrellas",
    "pct_5_estrellas",
]
etiquetas = ["1 Estrella", "2 Estrellas", "3 Estrellas", "4 Estrellas", "5 Estrellas"]

bottom = np.zeros(len(df))
for i, col in enumerate(categorias):
  valores = df[col].values
  bars = ax.barh(
      df["tramo_entrega"],
      valores,
      left=bottom,
      color=colores[i],
      label=etiquetas[i],
      height=0.6,
      edgecolor="white",
  )

  # Imprimir valor porcentual dentro de las barras si hay espacio suficiente
  for j, val in enumerate(valores):
    if val >= 7.5:
      ax.text(
          bottom[j] + val / 2,
          j,
          f"{val:.1f}%",
          ha="center",
          va="center",
          color="white" if i in [0, 4] else "#2C3E50",
          fontsize=9,
          fontweight="bold",
      )
  bottom += valores

# Invertir para que '0 Días (A Tiempo)' quede arriba
ax.invert_yaxis()

# Anotación del punto de quiebre (tramo de 3 a 5 días)
# Ubicamos dinámicamente la fila del tramo 3 a 5 días
idx_quiebre = df[df["tramo_entrega"].str.contains("3 a 5")].index[0]
val_1_estrella = df.loc[idx_quiebre, "pct_1_estrella"]

ax.annotate(
    "PUNTO DE QUIEBRE (Días 3 a 5)\nLas calificaciones de 1 estrella\nsaltan"
    f" drásticamente al {val_1_estrella:.1f}%",
    xy=(val_1_estrella / 2, idx_quiebre),
    xytext=(60, idx_quiebre - 0.3),
    arrowprops=dict(
        facecolor="#C0392B", shrink=0.08, width=1.2, headwidth=6, alpha=0.85
    ),
    fontsize=9.5,
    fontweight="bold",
    color="#922B21",
    bbox=dict(
        boxstyle="round,pad=0.35",
        facecolor="#FDEDEC",
        edgecolor="#E6B0AA",
        alpha=0.95,
    ),
)

ax.set_xlabel(
    "Distribución Porcentual de Reseñas (%)",
    fontsize=11,
    fontweight="bold",
    color="#2C3E50",
    labelpad=10,
)
ax.set_title(
    "Degradación de la Satisfacción (Customer Experience) según Días de Demora"
    " en Entrega",
    fontsize=13,
    fontweight="bold",
    color="#1A252F",
    pad=15,
    loc="left",
)
ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_xlim(0, 100)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=5,
    frameon=True,
    facecolor="white",
    fontsize=9.5,
)

os.makedirs("notebooks/images", exist_ok=True)
plt.tight_layout()
plt.savefig(
    "notebooks/images/barras_apiladas_cx.png", dpi=300, bbox_inches="tight"
)
plt.show()