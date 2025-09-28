"""
Módulo para gráficos de boxplot
"""


def plot_boxplot_simple(ax, df_filtrado):
    """Crear boxplot simple"""
    if len(df_filtrado) == 0:
        return

    bp = ax.boxplot([df_filtrado["TalkingTime"]], vert=True, patch_artist=True,
                   labels=['Principal'])
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][0].set_alpha(0.7)

    ax.set_ylabel("Tiempo de conversación (segundos)")


def plot_boxplot_comparison(ax, ax_twin, df_filtrado, df_comp_filtrado):
    """Crear boxplot con comparación (doble eje Y)"""
    # Boxplot grupo principal (eje Y izquierdo)
    if len(df_filtrado) > 0:
        bp1 = ax.boxplot([df_filtrado["TalkingTime"]], positions=[0.8], widths=0.6,
                         vert=True, patch_artist=True, labels=['Principal'])
        bp1['boxes'][0].set_facecolor('lightblue')
        bp1['boxes'][0].set_alpha(0.7)

    # Boxplot grupo comparación (eje Y derecho)
    if len(df_comp_filtrado) > 0:
        bp2 = ax_twin.boxplot([df_comp_filtrado["TalkingTime"]], positions=[1.2], widths=0.6,
                              vert=True, patch_artist=True, labels=['Comparación'])
        bp2['boxes'][0].set_facecolor('lightcoral')
        bp2['boxes'][0].set_alpha(0.7)

    # Configurar ejes
    ax.set_ylabel("TalkingTime (Principal)", color='blue')
    ax_twin.set_ylabel("TalkingTime (Comparación)", color='red')
    ax.tick_params(axis='y', labelcolor='blue')
    ax_twin.tick_params(axis='y', labelcolor='red')

    # Configurar etiquetas del eje X
    ax.set_xlim(0.5, 1.5)
    ax.set_xticks([0.8, 1.2])
    ax.set_xticklabels(['Principal', 'Comparación'], fontsize=8)
    ax_twin.set_xlim(0.5, 1.5)
    ax_twin.set_xticks([])


def configure_boxplot_axes(ax):
    """Configurar ejes del boxplot"""
    ax.set_title("Boxplot de\nTalkingTime")
    ax.grid(True, alpha=0.3)