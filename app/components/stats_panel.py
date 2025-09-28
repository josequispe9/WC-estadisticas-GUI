"""
Panel de estadísticas y outliers
"""
import tkinter as tk
from tkinter import ttk
import pandas as pd


class StatsPanel:
    def __init__(self, parent):
        self.parent = parent

        # Crear el frame principal
        self.frame = ttk.LabelFrame(parent, text="Estadísticas y Outliers", padding="10")
        self.create_widgets()

        # Variables para control de ordenamiento
        self.sort_column = None
        self.sort_reverse = False
        self.current_outliers_df = pd.DataFrame()
        self.agents_sort_column = None
        self.agents_sort_reverse = False
        self.current_agents_data = []

    def create_widgets(self):
        """Crear los widgets del panel de estadísticas"""
        # Frame para estadísticas básicas (lado izquierdo)
        basic_stats_frame = ttk.Frame(self.frame)
        basic_stats_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(basic_stats_frame, text="Estadísticas Descriptivas:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)
        self.stats_text = tk.Text(basic_stats_frame, height=8, width=35)
        self.stats_text.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Frame para outliers (centro)
        outliers_frame = ttk.Frame(self.frame)
        outliers_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(0, 10))

        ttk.Label(outliers_frame, text="Outliers (Valores Extremos):", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)

        # Treeview para mostrar outliers en formato tabla
        columns = ('TalkingTime', 'Nombre Agente', 'Tipificación', 'Turno', 'Sentido', 'Inicio')
        self.outliers_tree = ttk.Treeview(outliers_frame, columns=columns, show='headings', height=8)

        # Configurar columnas con ordenamiento
        self.outliers_tree.heading('TalkingTime', text='Tiempo (seg) ▼', command=lambda: self.sort_outliers_table('TalkingTime'))
        self.outliers_tree.heading('Nombre Agente', text='Agente', command=lambda: self.sort_outliers_table('Nombre Agente'))
        self.outliers_tree.heading('Tipificación', text='Tipificación', command=lambda: self.sort_outliers_table('Tipificación'))
        self.outliers_tree.heading('Turno', text='Turno', command=lambda: self.sort_outliers_table('Turno'))
        self.outliers_tree.heading('Sentido', text='Sentido', command=lambda: self.sort_outliers_table('Sentido'))
        self.outliers_tree.heading('Inicio', text='Fecha/Hora', command=lambda: self.sort_outliers_table('Inicio'))

        # Configurar ancho de columnas
        self.outliers_tree.column('TalkingTime', width=80, anchor=tk.CENTER)
        self.outliers_tree.column('Nombre Agente', width=100, anchor=tk.CENTER)
        self.outliers_tree.column('Tipificación', width=150, anchor=tk.CENTER)
        self.outliers_tree.column('Turno', width=60, anchor=tk.CENTER)
        self.outliers_tree.column('Sentido', width=120, anchor=tk.CENTER)
        self.outliers_tree.column('Inicio', width=140, anchor=tk.CENTER)

        self.outliers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Scrollbar para la tabla de outliers
        outliers_scroll = ttk.Scrollbar(outliers_frame, orient=tk.VERTICAL, command=self.outliers_tree.yview)
        outliers_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.outliers_tree.configure(yscrollcommand=outliers_scroll.set)

        # Frame para análisis de agentes (lado derecho)
        agents_analysis_frame = ttk.Frame(self.frame)
        agents_analysis_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(agents_analysis_frame, text="Análisis de Agentes:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)
        ttk.Label(agents_analysis_frame, text="(Outliers por agente)", font=('TkDefaultFont', 8)).pack(anchor=tk.W)

        # Treeview para mostrar el conteo de agentes
        agents_columns = ('Agente', 'Cantidad', 'Porcentaje')
        self.agents_tree = ttk.Treeview(agents_analysis_frame, columns=agents_columns, show='headings', height=8)

        # Configurar columnas del análisis de agentes con ordenamiento
        self.agents_tree.heading('Agente', text='Agente', command=lambda: self.sort_agents_table('Agente'))
        self.agents_tree.heading('Cantidad', text='Outliers ▼', command=lambda: self.sort_agents_table('Cantidad'))
        self.agents_tree.heading('Porcentaje', text='%', command=lambda: self.sort_agents_table('Porcentaje'))

        # Configurar ancho de columnas del análisis de agentes
        self.agents_tree.column('Agente', width=120, anchor=tk.W)
        self.agents_tree.column('Cantidad', width=60, anchor=tk.CENTER)
        self.agents_tree.column('Porcentaje', width=60, anchor=tk.CENTER)

        self.agents_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Scrollbar para la tabla de análisis de agentes
        agents_scroll = ttk.Scrollbar(agents_analysis_frame, orient=tk.VERTICAL, command=self.agents_tree.yview)
        agents_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.agents_tree.configure(yscrollcommand=agents_scroll.set)

    def update_stats(self, df_filtrado, df_comp_filtrado=None):
        """Actualizar el panel de estadísticas y outliers"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        from app.utils.outliers import detect_outliers, analyze_outliers_by_agent
        from app.data.processor import get_descriptive_stats, calculate_comparison_stats

        # Actualizar estadísticas básicas
        self.stats_text.delete(1.0, tk.END)

        if df_comp_filtrado is None:
            df_comp_filtrado = pd.DataFrame()

        stats_text = ""
        all_outliers = pd.DataFrame()

        # Estadísticas del grupo principal
        if len(df_filtrado) > 0:
            stats = get_descriptive_stats(df_filtrado)
            outliers = detect_outliers(df_filtrado)
            outliers['Grupo'] = 'Principal'  # Marcar outliers del grupo principal

            stats_text += "🔵 GRUPO PRINCIPAL:\n"
            stats_text += f"Registros: {len(df_filtrado)}\n"
            stats_text += f"Media: {stats['mean']:.2f} seg\n"
            stats_text += f"Mediana: {stats['50%']:.2f} seg\n"
            stats_text += f"Desv. estándar: {stats['std']:.2f} seg\n"
            stats_text += f"Outliers: {len(outliers)}\n"

            all_outliers = pd.concat([all_outliers, outliers], ignore_index=True)

        # Estadísticas del grupo de comparación
        if len(df_comp_filtrado) > 0:
            stats_comp = get_descriptive_stats(df_comp_filtrado)
            outliers_comp = detect_outliers(df_comp_filtrado)
            outliers_comp['Grupo'] = 'Comparación'

            if stats_text:
                stats_text += "\n"
            stats_text += "🔴 GRUPO COMPARACIÓN:\n"
            stats_text += f"Registros: {len(df_comp_filtrado)}\n"
            stats_text += f"Media: {stats_comp['mean']:.2f} seg\n"
            stats_text += f"Mediana: {stats_comp['50%']:.2f} seg\n"
            stats_text += f"Desv. estándar: {stats_comp['std']:.2f} seg\n"
            stats_text += f"Outliers: {len(outliers_comp)}\n"

            all_outliers = pd.concat([all_outliers, outliers_comp], ignore_index=True)

            # Agregar comparación directa si ambos grupos tienen datos
            if len(df_filtrado) > 0:
                stats_principal = get_descriptive_stats(df_filtrado)
                comparison = calculate_comparison_stats(stats_principal, stats_comp)
                if comparison:
                    stats_text += "\n📊 COMPARACIÓN:\n"
                    stats_text += f"Dif. Media: {comparison['media_diff']:+.2f} seg\n"
                    stats_text += f"Dif. Mediana: {comparison['mediana_diff']:+.2f} seg\n"
                    stats_text += f"Dif. Desv. Est.: {comparison['std_diff']:+.2f} seg"

        if len(df_filtrado) == 0 and len(df_comp_filtrado) == 0:
            stats_text = "No hay datos para mostrar estadísticas."

        self.stats_text.insert(1.0, stats_text)

        # Actualizar tabla de outliers (combinando ambos grupos)
        self.update_outliers_table(all_outliers)

        # Actualizar análisis de agentes (combinando ambos grupos)
        self.update_agents_analysis(all_outliers)

    def update_outliers_table(self, outliers_df):
        """Actualizar la tabla de outliers"""
        # Guardar el DataFrame actual para ordenamiento
        self.current_outliers_df = outliers_df.copy()

        # Limpiar tabla existente
        for item in self.outliers_tree.get_children():
            self.outliers_tree.delete(item)

        if len(outliers_df) == 0:
            # Insertar mensaje si no hay outliers
            self.outliers_tree.insert('', tk.END, values=('Sin outliers', '', '', '', '', ''))
            return

        # Insertar outliers en la tabla
        for _, row in outliers_df.iterrows():
            # Formatear la fecha para que sea más legible
            fecha_formateada = ''
            if 'Inicio' in row and pd.notna(row['Inicio']):
                try:
                    if isinstance(row['Inicio'], str):
                        fecha_obj = pd.to_datetime(row['Inicio'])
                    else:
                        fecha_obj = row['Inicio']
                    fecha_formateada = fecha_obj.strftime('%d/%m %H:%M')
                except:
                    fecha_formateada = str(row['Inicio'])[:16] if 'Inicio' in row else ''

            # Agregar indicador visual para el grupo si existe la columna
            agente_display = str(row['Nombre Agente'])[:15] if 'Nombre Agente' in row and pd.notna(row['Nombre Agente']) else ''
            if 'Grupo' in row:
                grupo_indicator = '🔵' if row['Grupo'] == 'Principal' else '🔴'
                agente_display = f"{grupo_indicator} {agente_display}"

            values = (
                f"{row['TalkingTime']:.1f}" if pd.notna(row['TalkingTime']) else '',
                agente_display,
                str(row['Tipificación'])[:20] if 'Tipificación' in row and pd.notna(row['Tipificación']) else '',
                str(row['Turno']) if 'Turno' in row and pd.notna(row['Turno']) else '',
                str(row['Sentido'])[:15] if 'Sentido' in row and pd.notna(row['Sentido']) else '',
                fecha_formateada
            )
            self.outliers_tree.insert('', tk.END, values=values)

    def update_agents_analysis(self, outliers_df):
        """Actualizar el análisis de agentes con value_counts"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        from app.utils.outliers import analyze_outliers_by_agent

        # Limpiar tabla existente
        for item in self.agents_tree.get_children():
            self.agents_tree.delete(item)

        agents_data = analyze_outliers_by_agent(outliers_df)

        if not agents_data:
            self.agents_tree.insert('', tk.END, values=('Sin datos', '0', '0%'))
            self.current_agents_data = []
            return

        # Guardar datos para ordenamiento
        self.current_agents_data = agents_data

        # Configurar ordenamiento inicial por cantidad (descendente)
        self.agents_sort_column = 'Cantidad'
        self.agents_sort_reverse = True
        self.update_agents_column_headers()

        # Insertar datos ordenados por cantidad (de mayor a menor)
        for values in agents_data:
            self.agents_tree.insert('', tk.END, values=values)

    def sort_outliers_table(self, column):
        """Ordenar la tabla de outliers por la columna especificada"""
        if len(self.current_outliers_df) == 0:
            return

        # Determinar si cambiar el orden de ascendente a descendente
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False

        # Ordenar el DataFrame
        if column == 'TalkingTime':
            sorted_df = self.current_outliers_df.sort_values('TalkingTime', ascending=self.sort_reverse)
        elif column == 'Inicio':
            # Para fechas, convertir a datetime si es necesario para ordenar correctamente
            temp_df = self.current_outliers_df.copy()
            if 'Inicio' in temp_df.columns:
                try:
                    temp_df['Inicio_sort'] = pd.to_datetime(temp_df['Inicio'])
                    sorted_df = temp_df.sort_values('Inicio_sort', ascending=self.sort_reverse)
                    sorted_df = sorted_df.drop('Inicio_sort', axis=1)
                except:
                    sorted_df = self.current_outliers_df.sort_values(column, ascending=self.sort_reverse)
            else:
                sorted_df = self.current_outliers_df.sort_values(column, ascending=self.sort_reverse)
        else:
            sorted_df = self.current_outliers_df.sort_values(column, ascending=self.sort_reverse)

        # Actualizar los encabezados para mostrar el indicador de ordenamiento
        self.update_column_headers()

        # Actualizar la tabla con los datos ordenados
        self.update_outliers_table(sorted_df)

    def update_column_headers(self):
        """Actualizar los encabezados de las columnas para mostrar indicadores de ordenamiento"""
        headers = {
            'TalkingTime': 'Tiempo (seg)',
            'Nombre Agente': 'Agente',
            'Tipificación': 'Tipificación',
            'Turno': 'Turno',
            'Sentido': 'Sentido',
            'Inicio': 'Fecha/Hora'
        }

        for col, base_text in headers.items():
            if col == self.sort_column:
                indicator = ' ▲' if self.sort_reverse else ' ▼'
                self.outliers_tree.heading(col, text=base_text + indicator)
            else:
                self.outliers_tree.heading(col, text=base_text)

    def sort_agents_table(self, column):
        """Ordenar la tabla de análisis de agentes por la columna especificada"""
        if len(self.current_agents_data) == 0:
            return

        # Determinar si cambiar el orden de ascendente a descendente
        if self.agents_sort_column == column:
            self.agents_sort_reverse = not self.agents_sort_reverse
        else:
            self.agents_sort_column = column
            # Para cantidad, por defecto descendente (más outliers primero)
            self.agents_sort_reverse = False if column != 'Cantidad' else True

        # Ordenar los datos
        if column == 'Agente':
            sorted_data = sorted(self.current_agents_data, key=lambda x: x[0], reverse=self.agents_sort_reverse)
        elif column == 'Cantidad':
            sorted_data = sorted(self.current_agents_data, key=lambda x: int(x[1]), reverse=self.agents_sort_reverse)
        elif column == 'Porcentaje':
            sorted_data = sorted(self.current_agents_data, key=lambda x: float(x[2].replace('%', '')), reverse=self.agents_sort_reverse)

        # Actualizar los encabezados
        self.update_agents_column_headers()

        # Limpiar y repoblar la tabla
        for item in self.agents_tree.get_children():
            self.agents_tree.delete(item)

        for data in sorted_data:
            self.agents_tree.insert('', tk.END, values=data)

    def update_agents_column_headers(self):
        """Actualizar los encabezados de las columnas de agentes para mostrar indicadores de ordenamiento"""
        headers = {
            'Agente': 'Agente',
            'Cantidad': 'Outliers',
            'Porcentaje': '%'
        }

        for col, base_text in headers.items():
            if col == self.agents_sort_column:
                indicator = ' ▲' if self.agents_sort_reverse else ' ▼'
                self.agents_tree.heading(col, text=base_text + indicator)
            else:
                self.agents_tree.heading(col, text=base_text)