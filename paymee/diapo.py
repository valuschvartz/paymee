import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ImageDraw, ImageFont 
import numpy as np

# --- Paleta de colores ---
COLOR_CORAL = '#FF6B81'       # Rosa coral
COLOR_CELESTE = '#A5E4FF'     # Celeste pastel
COLOR_LAVANDA = '#D9C6FF'     # Lavanda suave
COLOR_BACKGROUND = '#F7F8FA'  # Gris humo
COLOR_TEXT_DARK = '#333333'   # Texto oscuro para contraste
COLOR_DARK_TITLE = '#2a2a2a'  # Títulos más oscuros
COLOR_ARROW = '#666666'       # Color para las flechas

# --- Creación de iconos con un mejor control ---
def create_styled_icon(text, icon_color, text_color='white', size=120, font_size_ratio=0.6):
    img = Image.new('RGBA', (size, size), (0,0,0,0)) # Fondo transparente
    d = ImageDraw.Draw(img)
    d.ellipse((0, 0, size, size), fill=icon_color)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", int(size * font_size_ratio)) 
    except IOError:
        font = ImageFont.load_default() 
    
    bbox = d.textbbox((0,0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) / 2
    y = (size - text_height) / 2 - (size * 0.05) 
    d.text((x, y), text, fill=text_color, font=font)
    return img

# Iconos estilizados
icon_paymee = create_styled_icon("P", COLOR_CORAL)
icon_psp = create_styled_icon("🏛", COLOR_CELESTE, font_size_ratio=0.5) 
icon_bcra = create_styled_icon("🛡", COLOR_LAVANDA, font_size_ratio=0.5) 

# --- Configuración de la figura y los ejes ---
fig, ax = plt.subplots(figsize=(16, 9)) # Formato 16:9
fig.set_facecolor(COLOR_BACKGROUND)
ax.set_facecolor(COLOR_BACKGROUND)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off') # Sin ejes

# --- Título principal ---
ax.text(8.5, 7.8, "Implementación y Alianza Técnica", 
        fontsize=40, fontweight='bold', color=COLOR_DARK_TITLE, ha='left', va='center')

# --- Contenido del lado izquierdo (bloque de texto) ---
card_width_left = 7.0 # Ligeramente más ancho
card_height_left = 6.8 # Ligeramente más corto y centrado
x_start_left = 0.8
y_start_left = 1.0 # Posición vertical más centrada

rect_left = FancyBboxPatch((x_start_left, y_start_left), card_width_left, card_height_left,
                           boxstyle="round,pad=0,rounding_size=0.3",
                           facecolor=COLOR_LAVANDA, edgecolor='none', zorder=2)
ax.add_patch(rect_left)

# Puntos de texto dentro del bloque izquierdo
text_offset_x = x_start_left + 0.6
current_y = y_start_left + card_height_left - 0.7 # Inicio del primer punto

# Punto 1
ax.text(text_offset_x, current_y, "Integración regulada:",
        fontsize=16, fontweight='bold', color=COLOR_TEXT_DARK, ha='left', va='top', zorder=3)
current_y -= 0.4
ax.text(text_offset_x + 0.2, current_y, "Paymee operará junto a un PSP autorizado por el BCRA.",
        fontsize=13, color=COLOR_TEXT_DARK, ha='left', va='top', wrap=True, zorder=3, linespacing=1.3, transform=ax.transData)

current_y -= 1.3
ax.text(text_offset_x, current_y, "Alianzas técnicas:",
        fontsize=16, fontweight='bold', color=COLOR_TEXT_DARK, ha='left', va='top', zorder=3)
current_y -= 0.4
ax.text(text_offset_x + 0.2, current_y, "Evaluamos acuerdos con Fiserv y Geopagos, certificados en PCI CPOC y EMV L3.",
        fontsize=13, color=COLOR_TEXT_DARK, ha='left', va='top', wrap=True, zorder=3, linespacing=1.3, transform=ax.transData)

current_y -= 1.3
ax.text(text_offset_x, current_y, "Seguridad total:",
        fontsize=16, fontweight='bold', color=COLOR_TEXT_DARK, ha='left', va='top', zorder=3)
current_y -= 0.4
ax.text(text_offset_x + 0.2, current_y, "Cumplimiento normativo, interoperabilidad QR + NFC y seguridad garantizada desde el MVP.",
        fontsize=13, color=COLOR_TEXT_DARK, ha='left', va='top', wrap=True, zorder=3, linespacing=1.3, transform=ax.transData)


# --- Flujo de iconos al lado derecho (Alineación y Espaciado Corregidos) ---
icon_center_y = 3.5 # Altura central de los iconos (más bajo y centrado)
icon_spacing = 3.2 # Espacio ajustado entre centros de iconos
icon_start_x = 9.0 # Posición inicial

# Paymee Icon
imagebox_paymee = OffsetImage(icon_paymee, zoom=0.7) 
ab_paymee = AnnotationBbox(imagebox_paymee, (icon_start_x, icon_center_y),
                          xybox=(0,0), xycoords='data', boxcoords='offset points', frameon=False)
ax.add_artist(ab_paymee)
ax.text(icon_start_x, icon_center_y - 1.0, "Paymee", fontsize=14, fontweight='bold', color=COLOR_TEXT_DARK, ha='center', va='center')


# Flecha 1
arrow_start_1 = (icon_start_x + 0.8, icon_center_y)
arrow_end_1 = (icon_start_x + icon_spacing - 0.8, icon_center_y)
ax.annotate("", xy=arrow_end_1, xytext=arrow_start_1,
            arrowprops=dict(arrowstyle="->", color=COLOR_ARROW, lw=2), zorder=3)

# PSP Icon
x_pos_psp = icon_start_x + icon_spacing
imagebox_psp = OffsetImage(icon_psp, zoom=0.7)
ab_psp = AnnotationBbox(imagebox_psp, (x_pos_psp, icon_center_y),
                       xybox=(0,0), xycoords='data', boxcoords='offset points', frameon=False)
ax.add_artist(ab_psp)
ax.text(x_pos_psp, icon_center_y - 1.0, "PSP", fontsize=14, fontweight='bold', color=COLOR_TEXT_DARK, ha='center', va='center')


# Flecha 2
arrow_start_2 = (x_pos_psp + 0.8, icon_center_y)
arrow_end_2 = (x_pos_psp + icon_spacing - 0.8, icon_center_y)
ax.annotate("", xy=arrow_end_2, xytext=arrow_start_2,
            arrowprops=dict(arrowstyle="->", color=COLOR_ARROW, lw=2), zorder=3)

# BCRA Icon
x_pos_bcra = icon_start_x + (2 * icon_spacing)
imagebox_bcra = OffsetImage(icon_bcra, zoom=0.7)
ab_bcra = AnnotationBbox(imagebox_bcra, (x_pos_bcra, icon_center_y),
                        xybox=(0,0), xycoords='data', boxcoords='offset points', frameon=False)
ax.add_artist(ab_bcra)
ax.text(x_pos_bcra, icon_center_y - 1.0, "BCRA", fontsize=14, fontweight='bold', color=COLOR_TEXT_DARK, ha='center', va='center')

# --- Elementos decorativos (manchas sutiles en fondo) ---
circle1 = Ellipse((15.5, 8.5), 2.5, 2.5, facecolor=COLOR_LAVANDA, alpha=0.3, zorder=1)
circle2 = Ellipse((0.5, 0.5), 2.0, 2.0, facecolor=COLOR_CORAL, alpha=0.2, zorder=1)
circle3 = Ellipse((1.5, 8.0), 1.0, 1.0, facecolor=COLOR_CELESTE, alpha=0.2, zorder=1)
ax.add_patch(circle1)
ax.add_patch(circle2)
ax.add_patch(circle3)

plt.tight_layout()
plt.show()