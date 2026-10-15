import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

# 1. Cargar el CSV exportado de la Query 07
df = pd.read_csv("data/07_degradacion_satisfaccion_tramos.csv")
col_tramo = [c for c in df.columns if 'tramo' in c.lower()][0]
df[col_tramo] = df[col_tramo].str.replace(r'^\d+\.\s*', '', regex=True)
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
