"""
Módulo para gráficos avanzados
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def plot_activity_heatmap(ax, df_filtrado, df_comp_filtrado=None, comparar_activo=False):
    """Crear heatmap de actividad por hora y día"""
    # Usar el DataFrame principal, o combinado si hay comparación
    df_to_use = df_filtrado
    if comparar_activo and len(df_comp_filtrado) > 0:
        df_to_use = pd.concat([df_filtrado, df_comp_filtrado], ignore_index=True)

    if len(df_to_use) == 0 or 'Inicio' not in df_to_use.columns:
        ax.text(0.5, 0.5, 'Sin datos temporales\ndisponibles', ha='center', va='center',
                transform=ax.transAxes, fontsize=12)
        return

    df_temp = df_to_use.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_temp['Inicio']):
        df_temp['Inicio'] = pd.to_datetime(df_temp['Inicio'])

    df_temp['Hora'] = df_temp['Inicio'].dt.hour
    df_temp['Dia_Semana'] = df_temp['Inicio'].dt.day_name()

    # Crear pivot table
    pivot_data = df_temp.groupby(['Dia_Semana', 'Hora']).size().unstack(fill_value=0)

    # Asegurar orden de días
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex(day_order, fill_value=0)

    # Crear heatmap con estilo similar al resto de gráficos
    im = ax.imshow(pivot_data, cmap='Blues', aspect='auto')
    ax.set_xticks(range(24))
    ax.set_xticklabels(range(24))
    ax.set_yticks(range(len(day_order)))
    ax.set_yticklabels(['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'])

    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Día de la semana")
    ax.set_title("Heatmap de Actividad\n(Llamadas por hora/día)")
    ax.grid(True, alpha=0.3)


def plot_time_series(ax, df):
    """Crear gráfico de series de tiempo"""
    if len(df) == 0 or 'Inicio' not in df.columns:
        ax.text(0.5, 0.5, 'Sin datos de tiempo\ndisponibles', ha='center', va='center',
                transform=ax.transAxes, fontsize=12)
        return

    # Convertir a datetime si es necesario
    df_temp = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_temp['Inicio']):
        df_temp['Inicio'] = pd.to_datetime(df_temp['Inicio'])

    # Agrupar por día y calcular estadísticas
    df_temp['Fecha'] = df_temp['Inicio'].dt.date
    daily_stats = df_temp.groupby('Fecha')['TalkingTime'].agg(['mean', 'median', 'count']).reset_index()

    ax.plot(daily_stats['Fecha'], daily_stats['mean'], marker='o', label='Media diaria', linewidth=2)
    ax.plot(daily_stats['Fecha'], daily_stats['median'], marker='s', label='Mediana diaria', linewidth=2)

    ax.set_title("Evolución Temporal de TalkingTime")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Tiempo de conversación (segundos)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)


def plot_agent_performance(ax, df):
    """Crear gráfico de rendimiento por agente"""
    if len(df) == 0 or 'Nombre Agente' not in df.columns:
        ax.text(0.5, 0.5, 'Sin datos de agentes\ndisponibles', ha='center', va='center',
                transform=ax.transAxes, fontsize=12)
        return

    # Calcular estadísticas por agente
    agent_stats = df.groupby('Nombre Agente')['TalkingTime'].agg(['mean', 'count']).reset_index()
    agent_stats = agent_stats[agent_stats['count'] >= 5]  # Filtrar agentes con pocas llamadas
    agent_stats = agent_stats.sort_values('mean', ascending=True).head(5)  # Top 5

    # Crear gráfico de barras horizontal con color consistente
    y_pos = np.arange(len(agent_stats))
    bars = ax.barh(y_pos, agent_stats['mean'], alpha=0.7, color='skyblue')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(agent_stats['Nombre Agente'], fontsize=10)
    ax.set_xlabel("Tiempo promedio de conversación (segundos)")
    ax.set_title("Rendimiento por Agente\n(Top 5 - Mayor a menor tiempo)")
    ax.grid(True, alpha=0.3, axis='x')


def plot_correlation_matrix(ax, df):
    """Crear matriz de correlación"""
    if len(df) == 0:
        ax.text(0.5, 0.5, 'Sin datos para\ncorrelación', ha='center', va='center',
                transform=ax.transAxes, fontsize=12)
        return

    # Seleccionar columnas numéricas relevantes
    numeric_cols = ['TalkingTime']

    # Agregar variables categóricas codificadas
    df_corr = df.copy()
    df_corr['Turno_TM'] = (df_corr['Turno'] == 'TM').astype(int)
    df_corr['Turno_TT'] = (df_corr['Turno'] == 'TT').astype(int)
    df_corr['Sentido_Manual'] = (df_corr['Sentido'] == 'Manual').astype(int) if 'Sentido' in df.columns else 0

    # Si hay columna de fecha, agregar información temporal
    if 'Inicio' in df.columns:
        df_corr['Hora'] = pd.to_datetime(df_corr['Inicio']).dt.hour
        numeric_cols.append('Hora')

    corr_cols = numeric_cols + ['Turno_TM', 'Turno_TT', 'Sentido_Manual']
    corr_matrix = df_corr[corr_cols].corr()

    # Crear heatmap
    im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
    ax.set_yticklabels(corr_matrix.columns)

    # Agregar valores en las celdas
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=8)

    ax.set_title("Matriz de Correlación")
    plt.colorbar(im, ax=ax, shrink=0.8)


def plot_hourly_heatmap(ax, df):
    """Crear heatmap de actividad por hora"""
    if len(df) == 0 or 'Inicio' not in df.columns:
        ax.text(0.5, 0.5, 'Sin datos temporales\ndisponibles', ha='center', va='center',
                transform=ax.transAxes, fontsize=12)
        return

    df_temp = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_temp['Inicio']):
        df_temp['Inicio'] = pd.to_datetime(df_temp['Inicio'])

    df_temp['Hora'] = df_temp['Inicio'].dt.hour
    df_temp['Dia_Semana'] = df_temp['Inicio'].dt.day_name()

    # Crear pivot table
    pivot_data = df_temp.groupby(['Dia_Semana', 'Hora']).size().unstack(fill_value=0)

    # Asegurar orden de días
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex(day_order, fill_value=0)

    # Crear heatmap
    im = ax.imshow(pivot_data, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(24))
    ax.set_xticklabels(range(24))
    ax.set_yticks(range(len(day_order)))
    ax.set_yticklabels(['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'])

    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Día de la semana")
    ax.set_title("Heatmap de Actividad\n(Número de llamadas)")

    plt.colorbar(im, ax=ax, shrink=0.8)