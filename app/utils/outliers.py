"""
Módulo para detección y análisis de outliers
"""
import pandas as pd


def detect_outliers(df_filtrado):
    """Detectar outliers usando el método IQR (Interquartile Range)"""
    if len(df_filtrado) == 0:
        return pd.DataFrame()

    Q1 = df_filtrado['TalkingTime'].quantile(0.25)
    Q3 = df_filtrado['TalkingTime'].quantile(0.75)
    IQR = Q3 - Q1

    # Definir límites para outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filtrar outliers
    outliers = df_filtrado[(df_filtrado['TalkingTime'] < lower_bound) |
                           (df_filtrado['TalkingTime'] > upper_bound)]

    return outliers.sort_values('TalkingTime', ascending=False)


def analyze_outliers_by_agent(outliers_df):
    """Analizar outliers por agente"""
    if len(outliers_df) == 0:
        return []

    if 'Nombre Agente' in outliers_df.columns:
        agent_counts = outliers_df['Nombre Agente'].value_counts()
        total_outliers = len(outliers_df)

        agents_data = []
        for agent, count in agent_counts.items():
            percentage = (count / total_outliers) * 100
            agents_data.append((
                str(agent)[:15],
                str(count),
                f"{percentage:.1f}%"
            ))
        return agents_data
    return []