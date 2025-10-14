import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Datos proporcionados
data = {
    'Actor': ['Mercado Pago', 'Getnet', 'Ualá Bis', 'Paymee'],
    'Crédito': [6.29, 6.19, 4.4, 3.9],
    'Débito': [3.25, 3.19, 2.9, 2.3],
    'QR interoperable': [0.8, 0.8, 0.6, 0.6]
}
df = pd.DataFrame(data)
df_long = df.melt(id_vars='Actor', var_name='Categoría', value_name='Tasa (%)')

# Paleta de colores ajustada
COLOR_CORAL = '#FF6B81'       # Rosa coral (Original, no lo usaremos para QR de Paymee ahora)
COLOR_CELESTE = '#A5E4FF'     # Celeste pastel (Crédito Competidores)
COLOR_LAVANDA = '#D9C6FF'     # Lavanda suave (Débito Competidores)
COLOR_GREY_QR = '#B0B0B0'     # Gris neutro (QR Competidores)
COLOR_BACKGROUND = '#F7F8FA'  # Gris humo

# Tonos más fuertes para Paymee
DARK_CELESTE_PAYMEE = '#50B0D1' # Crédito Paymee
DARK_LAVANDA_PAYMEE = '#A080D0' # Débito Paymee
DARK_GREY_QR_PAYMEE = '#858585' # QR Paymee

def get_color_enhanced(row):
    if row['Actor'] == 'Paymee':
        if row['Categoría'] == 'Crédito':
            return DARK_CELESTE_PAYMEE
        elif row['Categoría'] == 'Débito':
            return DARK_LAVANDA_PAYMEE
        elif row['Categoría'] == 'QR interoperable':
            return DARK_GREY_QR_PAYMEE
    else: # Competidores
        if row['Categoría'] == 'Crédito':
            return COLOR_CELESTE
        elif row['Categoría'] == 'Débito':
            return COLOR_LAVANDA
        elif row['Categoría'] == 'QR interoperable':
            return COLOR_GREY_QR
    return '#CCCCCC'

df_long['Color'] = df_long.apply(get_color_enhanced, axis=1)

# Orden de los actores en el eje Y
actor_order = ['Mercado Pago', 'Getnet', 'Ualá Bis', 'Paymee']
df_long['Actor'] = pd.Categorical(df_long['Actor'], categories=actor_order, ordered=True)

# Configuración del gráfico
sns.set_style("whitegrid") # Mantenemos esto, pero luego quitaremos las líneas con ax.grid(False)
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor(COLOR_BACKGROUND)
ax.set_facecolor(COLOR_BACKGROUND)

# Variables para dibujar las barras
bar_width = 0.25
y_positions = np.arange(len(df_long['Actor'].unique()))
category_offsets = {'Crédito': -bar_width, 'Débito': 0, 'QR interoperable': bar_width}

# Dibujar las barras y etiquetas
for i, actor in enumerate(actor_order):
    actor_data = df_long[df_long['Actor'] == actor]
    for category, offset in category_offsets.items():
        row = actor_data[actor_data['Categoría'] == category].iloc[0]
        tasa = row['Tasa (%)']
        color = row['Color']
        y_center = y_positions[i] + offset

        # Barra
        ax.barh(y_center, tasa, height=bar_width * 0.9, color=color, edgecolor='none', zorder=3)

        # Etiqueta de datos
        label_text = f'{tasa:.2f}%'
        if actor == 'Paymee' and category == 'QR interoperable':
             label_text += ' (3 meses gratis)'

        ax.text(tasa + 0.05, y_center, label_text, ha='left', va='center', fontsize=10, color='#333333')

# Personalización final
ax.set_yticks(y_positions)
ax.set_yticklabels(actor_order, fontsize=12)
ax.set_xlim(0, df['Crédito'].max() * 1.25) # Ajusta el límite X si es necesario
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xlabel(''); ax.set_ylabel('')
ax.tick_params(axis='x', length=0); ax.tick_params(axis='y', length=0)
ax.set_xticks([])

# --- Novedad: Remover las líneas de la cuadrícula ---
ax.grid(False) # Deshabilita la cuadrícula

# Leyenda
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, fc=COLOR_CELESTE, edgecolor='none'),
    plt.Rectangle((0, 0), 1, 1, fc=DARK_CELESTE_PAYMEE, edgecolor='none'),
    plt.Rectangle((0, 0), 1, 1, fc=COLOR_LAVANDA, edgecolor='none'),
    plt.Rectangle((0, 0), 1, 1, fc=DARK_LAVANDA_PAYMEE, edgecolor='none'),
    plt.Rectangle((0, 0), 1, 1, fc=COLOR_GREY_QR, edgecolor='none'),
    plt.Rectangle((0, 0), 1, 1, fc=DARK_GREY_QR_PAYMEE, edgecolor='none')
]
legend_labels = [
    'Crédito (Competidores)', 'Crédito (Paymee)',
    'Débito (Competidores)', 'Débito (Paymee)',
    'QR (Competidores)', 'QR (Paymee)'
]

ax.legend(legend_handles, legend_labels, loc='upper right', ncol=2, frameon=False, fontsize=10)

# Título y Nota
fig_title = 'Benchmark de comisiones – Argentina 2025'
fig_note = 'Nota: Paymee ofrece hasta 40 % menos comisión en crédito inmediato frente a la competencia.'

ax.set_title(fig_title, fontsize=14, fontweight='bold', color='#333333', pad=20)
# --- Novedad: Aumentar el tamaño de fuente de la nota ---
fig.text(0.5, 0.01, fig_note, ha='center', va='bottom', fontsize=12, color='#666666', transform=fig.transFigure) # fontSize a 12

plt.tight_layout(rect=[0, 0.05, 1, 1]) # Ajusta el layout para hacer espacio para la nota al pie
plt.savefig('paymee_competitor_comparison_final_no_grid_large_note.png') # Nuevo nombre de archivo
plt.show()