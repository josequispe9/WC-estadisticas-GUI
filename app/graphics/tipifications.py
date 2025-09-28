"""
Módulo para gráficos de distribución de tipificaciones
"""
import numpy as np
import pandas as pd


def plot_tipifications_distribution(ax, df, grupos_filtrados, turno_filtrado,
                                   df_comp=None, grupos_comp_filtrados=None,
                                   turno_comp_filtrado=None, comparar_activo=False):
    """Crear gráfico de distribución de tipificaciones"""

    # Filtrar datos del grupo principal
    df_total_filtered = df[(df["grupo"].isin(grupos_filtrados)) & (df["Turno"] == turno_filtrado)]

    # Obtener datos de comparación para tipificaciones
    df_comp_total_filtered = pd.DataFrame()
    if comparar_activo and df_comp is not None and grupos_comp_filtrados:
        df_comp_total_filtered = df[(df["grupo"].isin(grupos_comp_filtrados)) &
                                   (df["Turno"] == turno_comp_filtrado)]

    if len(df_total_filtered) == 0:
        ax.text(0.5, 0.5, 'Sin datos\npara mostrar', ha='center', va='center',
                transform=ax.transAxes, fontsize=10)
        ax.set_title("Distribución de\nTipificaciones", fontsize=10)
        return

    # Obtener conteos y porcentajes
    tipificacion_counts = df_total_filtered['Tipificación'].value_counts()
    total_records = len(df_total_filtered)
    percentages = (tipificacion_counts / total_records) * 100

    # Obtener tipificaciones de comparación
    tipificacion_counts_comp = pd.Series(dtype=int)
    percentages_comp = pd.Series(dtype=float)
    if len(df_comp_total_filtered) > 0:
        tipificacion_counts_comp = df_comp_total_filtered['Tipificación'].value_counts()
        total_records_comp = len(df_comp_total_filtered)
        percentages_comp = (tipificacion_counts_comp / total_records_comp) * 100

    # Combinar todas las tipificaciones únicas
    all_tipificaciones = set(tipificacion_counts.index)
    if len(tipificacion_counts_comp) > 0:
        all_tipificaciones.update(tipificacion_counts_comp.index)
    all_tipificaciones = sorted(list(all_tipificaciones))

    # Crear etiquetas más cortas
    short_labels = [tip[:15] + '...' if len(tip) > 15 else tip for tip in all_tipificaciones]

    y_pos = np.arange(len(all_tipificaciones))
    bar_height = 0.35

    # Preparar datos para ambos grupos
    pct_principal = [percentages.get(tip, 0) for tip in all_tipificaciones]
    pct_comparacion = [percentages_comp.get(tip, 0) for tip in all_tipificaciones]

    # Crear barras duales
    if comparar_activo and len(df_comp_total_filtered) > 0:
        bars1 = ax.barh(y_pos - bar_height/2, pct_principal, bar_height,
                       alpha=0.8, color='skyblue', edgecolor='black', label='Principal')
        bars2 = ax.barh(y_pos + bar_height/2, pct_comparacion, bar_height,
                       alpha=0.8, color='red', edgecolor='darkred', label='Comparación')
        ax.legend(fontsize=8)
    else:
        bars1 = ax.barh(y_pos, pct_principal, alpha=0.7, color='skyblue', edgecolor='black')

    # Configurar el gráfico
    ax.set_yticks(y_pos)
    ax.set_yticklabels(short_labels, fontsize=8)
    ax.set_xlabel("Porcentaje (%)", fontsize=9)
    ax.set_title("Distribución de\nTipificaciones", fontsize=10)
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()