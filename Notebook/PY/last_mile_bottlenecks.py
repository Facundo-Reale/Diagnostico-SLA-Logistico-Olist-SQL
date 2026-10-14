import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# 1. Cargar datos
df = pd.read_csv('data/04_cuello_de_botella_destino.csv')
df_top = df.sort_values(by='volumen_pedidos', ascending=False).head(10).copy()

# 2. Calcular los volúmenes absolutos
df_top['volumen_fallas'] = np.round(df_top['volumen_pedidos'] * (df_top['tasa_falla_sla'] / 100)).astype(int)

# 3. Calcular la INCIDENCIA NACIONAL
total_pedidos = df_top['volumen_pedidos'].sum()
total_fallas = df_top['volumen_fallas'].sum()

df_top['incidencia_demanda'] = (df_top['volumen_pedidos'] / total_pedidos) * 100
df_top['incidencia_fallas'] = (df_top['volumen_fallas'] / total_fallas) * 100

# 4. Configurar el lienzo
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(11.5, 6), dpi=300)

estados = df_top['estado_destino'].tolist()
inc_demanda = df_top['incidencia_demanda'].values
inc_fallas = df_top['incidencia_fallas'].values

x = np.arange(len(estados))
width = 0.35

# 5. Barras de Incidencia
bar1 = ax.bar(x - width/2, inc_demanda, width, label='% Aporte a la Demanda Nacional (Ventas)', 
              color='#2980B9', edgecolor='white', linewidth=1, zorder=3)
bar2 = ax.bar(x + width/2, inc_fallas, width, label='% Aporte a los Quiebres SLA (Problemas)', 
              color='#C0392B', edgecolor='white', linewidth=1, zorder=3)

# 6. Formato de Ejes
ax.set_ylabel('Incidencia sobre el Total Nacional (%)', fontsize=10, fontweight='bold', color='#2C3E50', labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(estados, fontsize=11, fontweight='bold', color='#2C3E50')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_ylim(0, max(inc_demanda) + 8)

# 7. Etiquetas sobre las barras
def autolabel(rects, is_falla=False):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9,
                    fontweight='bold',
                    color='#922B21' if is_falla else '#154360')

autolabel(bar1)
autolabel(bar2, is_falla=True)

# 8. Limpieza visual y guardado
ax.set_title('Gráfico de Incidencia: Contribución al Negocio vs. Generación de Fallas', 
             fontsize=13, fontweight='bold', color='#1A252F', pad=15, loc='left')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle=':', alpha=0.6, axis='y')
ax.grid(False, axis='x')
ax.legend(loc='upper right', frameon=True, facecolor='white')

os.makedirs('notebooks/images', exist_ok=True)
plt.tight_layout()
plt.savefig('notebooks/images/last_mile_bottlenecks.png', dpi=300, bbox_inches='tight')
plt.show()