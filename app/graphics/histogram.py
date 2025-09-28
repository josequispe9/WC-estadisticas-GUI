"""
Módulo para gráficos de histograma con KDE
"""
import numpy as np
from scipy import stats


def plot_histogram_simple(ax, df_filtrado, bins, mostrar_kde=False):
    """Crear histograma simple"""
    if len(df_filtrado) == 0:
        return

    ax.hist(df_filtrado["TalkingTime"], bins=bins, edgecolor="black", alpha=0.7,
            color='skyblue', label=f'Grupo Principal ({len(df_filtrado)} registros)')

    # Agregar curva KDE si está activada
    if mostrar_kde:
        kde_data = df_filtrado["TalkingTime"]
        kde = stats.gaussian_kde(kde_data)
        x_range = np.linspace(kde_data.min(), kde_data.max(), 200)
        kde_values = kde(x_range)
        # Escalar KDE para que coincida con la escala del histograma
        kde_scaled = kde_values * len(kde_data) * (bins[1] - bins[0])
        ax.plot(x_range, kde_scaled, color='darkblue', linewidth=2,
               label='KDE', alpha=0.8)

    # Mostrar leyenda si hay KDE
    if mostrar_kde:
        ax.legend(fontsize=8)

    ax.set_ylabel("Frecuencia")


def plot_histogram_comparison(ax, ax_twin, df_filtrado, df_comp_filtrado, bins, mostrar_kde=False):
    """Crear histograma con comparación (doble eje Y)"""
    # Histograma grupo principal (eje Y izquierdo)
    if len(df_filtrado) > 0:
        ax.hist(df_filtrado["TalkingTime"], bins=bins, edgecolor="black", alpha=0.7,
                color='skyblue', label=f'Principal ({len(df_filtrado)} reg)')

        # Agregar curva KDE si está activada
        if mostrar_kde:
            kde_data = df_filtrado["TalkingTime"]
            kde = stats.gaussian_kde(kde_data)
            x_range = np.linspace(kde_data.min(), kde_data.max(), 200)
            kde_values = kde(x_range)
            # Escalar KDE para que coincida con la escala del histograma
            kde_scaled = kde_values * len(kde_data) * (bins[1] - bins[0])
            ax.plot(x_range, kde_scaled, color='darkblue', linewidth=2,
                   label='KDE Principal', alpha=0.8)

    # Histograma grupo comparación (eje Y derecho)
    if len(df_comp_filtrado) > 0:
        ax_twin.hist(df_comp_filtrado["TalkingTime"], bins=bins, edgecolor="darkred", alpha=0.7,
                    color='red', label=f'Comparación ({len(df_comp_filtrado)} reg)')

        # Agregar curva KDE para comparación si está activada
        if mostrar_kde:
            kde_data_comp = df_comp_filtrado["TalkingTime"]
            kde_comp = stats.gaussian_kde(kde_data_comp)
            x_range_comp = np.linspace(kde_data_comp.min(), kde_data_comp.max(), 200)
            kde_values_comp = kde_comp(x_range_comp)
            # Escalar KDE para que coincida con la escala del histograma
            kde_scaled_comp = kde_values_comp * len(kde_data_comp) * (bins[1] - bins[0])
            ax_twin.plot(x_range_comp, kde_scaled_comp, color='darkred', linewidth=2,
                        label='KDE Comparación', alpha=0.8)

    # Configurar ejes
    ax.set_ylabel("Frecuencia (Principal)", color='blue')
    ax_twin.set_ylabel("Frecuencia (Comparación)", color='red')
    ax.tick_params(axis='y', labelcolor='blue')
    ax_twin.tick_params(axis='y', labelcolor='red')

    # Leyenda combinada
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_twin.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper right')


def configure_histogram_axes(ax, bins):
    """Configurar ejes del histograma"""
    ax.set_xlabel("Tiempo de conversación (segundos)")

    # Ajustar ticks del eje x para evitar saturación
    if len(bins) > 15:
        step = max(1, len(bins) // 10)
        ax.set_xticks(bins[::step])
    else:
        ax.set_xticks(bins)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)