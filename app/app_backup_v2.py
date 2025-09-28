import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import os
from scipy import stats

class AnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de TalkingTime")
        self.root.geometry("1000x700")
        
        # Cargar datos desde archivo CSV
        self.load_data()
        
        # Crear interface
        self.create_widgets()
        
        # Generar gráfico inicial
        self.update_chart()
    
    def load_data(self):
        """Cargar datos desde el archivo CSV"""
        csv_path = "/home/josequispe/Desktop/github-projects/WC-estadisticas-GUI/data/process/llamadas_procesadas.csv"
        
        try:
            if os.path.exists(csv_path):
                self.df_total = pd.read_csv(csv_path, sep=';', encoding='utf-8')
                print(f"✅ Archivo cargado exitosamente: {len(self.df_total)} registros")
                print(f"Columnas disponibles: {list(self.df_total.columns)}")
                
                # Mostrar información básica del dataset
                if hasattr(self, 'root'):  # Solo si la ventana ya existe
                    messagebox.showinfo("Datos cargados", 
                                      f"Archivo cargado exitosamente\n"
                                      f"Registros: {len(self.df_total)}\n"
                                      f"Columnas: {len(self.df_total.columns)}")
            else:
                print("❌ Archivo no encontrado, creando datos de ejemplo...")
                self.create_sample_data()
                if hasattr(self, 'root'):  # Solo si la ventana ya existe
                    messagebox.showwarning("Archivo no encontrado", 
                                         f"No se encontró el archivo:\n{csv_path}\n\n"
                                         "Se usarán datos de ejemplo.")
        except Exception as e:
            print(f"❌ Error al cargar archivo: {e}")
            print("Creando datos de ejemplo...")
            self.create_sample_data()
            if hasattr(self, 'root'):  # Solo si la ventana ya existe
                messagebox.showerror("Error al cargar archivo", 
                                   f"Error: {str(e)}\n\nSe usarán datos de ejemplo.")
    
    def create_sample_data(self):
        """Crear datos de ejemplo que simulan tu dataset (fallback)"""
        n_samples = 1000
        
        grupos = ["yasmin_marina", "melanie_naty", "josefina_marcos", "otro_grupo"]
        tipificaciones = ["Cae Muda o Cortada", "Llamada Completa", "No Contesta"]
        turnos = ["TT", "TM", "TN"]
        
        data = {
            'grupo': np.random.choice(grupos, n_samples),
            'Tipificación': np.random.choice(tipificaciones, n_samples),
            'Turno': np.random.choice(turnos, n_samples),
            'TalkingTime': np.random.exponential(scale=30, size=n_samples)
        }
        
        self.df_total = pd.DataFrame(data)
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de información del dataset
        info_frame = ttk.LabelFrame(main_frame, text="Información del Dataset", padding="5")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Mostrar info básica del dataset cargado
        info_text = f"Registros: {len(self.df_total)} | Columnas: {', '.join(self.df_total.columns[:5])}{'...' if len(self.df_total.columns) > 5 else ''}"
        ttk.Label(info_frame, text=info_text).pack(side=tk.LEFT)
        
        # Botón para recargar datos
        reload_btn = ttk.Button(info_frame, text="Recargar Datos", command=self.load_data)
        reload_btn.pack(side=tk.RIGHT)
        
        # Frame de controles
        controls_frame = ttk.LabelFrame(main_frame, text="Filtros", padding="10")
        controls_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Definir grupos disponibles
        self.grupos_disponibles = ['ap_connection', 'byl', 'capa', 'diana', 
                                  'josefina_marcos', 'melanie_naty', 'yasmin_marina', 'romi']
        
        # Obtener valores únicos del dataset cargado para los filtros
        tipificaciones_unicas = sorted(self.df_total['Tipificación'].unique()) if 'Tipificación' in self.df_total.columns else ["Cae Muda o Cortada"]
        turnos_unicos = sorted(self.df_total['Turno'].unique()) if 'Turno' in self.df_total.columns else ["TT"]
        
        # Filtros - GRUPOS con selección múltiple
        ttk.Label(controls_frame, text="Grupos:").grid(row=0, column=0, sticky=tk.W)
        grupos_frame = ttk.Frame(controls_frame)
        grupos_frame.grid(row=0, column=1, columnspan=3, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # Crear checkboxes para cada grupo
        self.grupos_vars = {}
        grupos_por_fila = 4
        for i, grupo in enumerate(self.grupos_disponibles):
            var = tk.BooleanVar()
            # Marcar los primeros 3 grupos por defecto
            if i < 3:
                var.set(True)
            self.grupos_vars[grupo] = var
            
            checkbox = ttk.Checkbutton(grupos_frame, text=grupo, variable=var)
            row = i // grupos_por_fila
            col = i % grupos_por_fila
            checkbox.grid(row=row, column=col, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(controls_frame, text="Tipificación:").grid(row=2, column=0, sticky=tk.W)
        self.tipificacion_var = tk.StringVar(value=tipificaciones_unicas[0] if tipificaciones_unicas else "Cae Muda o Cortada")
        tipificacion_combo = ttk.Combobox(controls_frame, textvariable=self.tipificacion_var, 
                                        values=tipificaciones_unicas, width=25)
        tipificacion_combo.grid(row=2, column=1, padx=(5, 0), sticky=tk.W)
        
        ttk.Label(controls_frame, text="Turno:").grid(row=2, column=2, sticky=tk.W, padx=(20, 0))
        self.turno_var = tk.StringVar(value=turnos_unicos[0] if turnos_unicos else "TT")
        turno_combo = ttk.Combobox(controls_frame, textvariable=self.turno_var, 
                                 values=turnos_unicos, width=15)
        turno_combo.grid(row=2, column=3, padx=(5, 0), sticky=tk.W)
        
        # Controles numéricos con Entry (sin límites)
        ttk.Label(controls_frame, text="Ancho intervalo:").grid(row=3, column=0, sticky=tk.W)
        self.size_bin_var = tk.StringVar(value="1.0")
        size_bin_entry = ttk.Entry(controls_frame, textvariable=self.size_bin_var, width=15)
        size_bin_entry.grid(row=3, column=1, padx=(5, 0), sticky=tk.W)
        
        ttk.Label(controls_frame, text="% extremo sup:").grid(row=3, column=2, sticky=tk.W, padx=(20, 0))
        self.quitar_extremo_var = tk.StringVar(value="0.02")
        extremo_entry = ttk.Entry(controls_frame, textvariable=self.quitar_extremo_var, width=15)
        extremo_entry.grid(row=3, column=3, padx=(5, 0), sticky=tk.W)

        # Opción KDE global
        self.mostrar_kde = tk.BooleanVar()
        kde_check = ttk.Checkbutton(controls_frame, text="Mostrar curva KDE",
                                   variable=self.mostrar_kde)
        kde_check.grid(row=3, column=4, padx=(20, 0), sticky=tk.W)

        # Botón comparar y variables de control
        self.comparar_activo = tk.BooleanVar()
        compare_btn = ttk.Checkbutton(controls_frame, text="Comparar con otro grupo",
                                     variable=self.comparar_activo, command=self.toggle_comparison)
        compare_btn.grid(row=4, column=0, pady=(15, 0), sticky=tk.W)

        # Botones auxiliares (reposicionados)
        select_all_btn = ttk.Button(controls_frame, text="Seleccionar Todos",
                                   command=self.select_all_grupos)
        select_all_btn.grid(row=4, column=1, pady=(15, 0), sticky=tk.W, padx=(20, 5))

        # Botón actualizar (en el centro)
        update_btn = ttk.Button(controls_frame, text="Actualizar Gráfico", command=self.update_chart)
        update_btn.grid(row=4, column=2, pady=(15, 0), padx=(5, 5))

        clear_all_btn = ttk.Button(controls_frame, text="Deseleccionar Todos",
                                  command=self.clear_all_grupos)
        clear_all_btn.grid(row=4, column=3, pady=(15, 0), sticky=tk.E, padx=(5, 0))

        # Frame para filtros de comparación (a la derecha de los filtros principales)
        self.comparison_frame = ttk.LabelFrame(controls_frame, text="Filtros para Comparación (Grupo Rojo)", padding="10")
        self.comparison_frame.grid(row=0, column=5, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(20, 0))
        self.create_comparison_filters()
        self.comparison_frame.grid_remove()  # Ocultar inicialmente
        
        # Frame para el gráfico
        chart_frame = ttk.Frame(main_frame)
        chart_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el gráfico matplotlib
        self.fig = Figure(figsize=(14, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Frame para estadísticas y outliers
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas y Outliers", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        # Frame para estadísticas básicas (lado izquierdo)
        basic_stats_frame = ttk.Frame(stats_frame)
        basic_stats_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(basic_stats_frame, text="Estadísticas Descriptivas:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)
        self.stats_text = tk.Text(basic_stats_frame, height=8, width=35)
        self.stats_text.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Frame para outliers (centro)
        outliers_frame = ttk.Frame(stats_frame)
        outliers_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(0, 10))

        # Frame para análisis de agentes (lado derecho)
        agents_analysis_frame = ttk.Frame(stats_frame)
        agents_analysis_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(outliers_frame, text="Outliers (Valores Extremos):", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)

        # Treeview para mostrar outliers en formato tabla
        columns = ('TalkingTime', 'Nombre Agente', 'Tipificación', 'Turno', 'Sentido', 'Inicio')
        self.outliers_tree = ttk.Treeview(outliers_frame, columns=columns, show='headings', height=8)

        # Variables para controlar el ordenamiento
        self.sort_column = None
        self.sort_reverse = False
        self.current_outliers_df = pd.DataFrame()

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

        # Contenido del frame de análisis de agentes
        ttk.Label(agents_analysis_frame, text="Análisis de Agentes:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)
        ttk.Label(agents_analysis_frame, text="(Outliers por agente)", font=('TkDefaultFont', 8)).pack(anchor=tk.W)

        # Treeview para mostrar el conteo de agentes
        agents_columns = ('Agente', 'Cantidad', 'Porcentaje')
        self.agents_tree = ttk.Treeview(agents_analysis_frame, columns=agents_columns, show='headings', height=8)

        # Variables para controlar el ordenamiento de agentes
        self.agents_sort_column = None
        self.agents_sort_reverse = False
        self.current_agents_data = []

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
        
        # Configurar peso de las filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # Ajustado porque agregamos más filas
    
    def select_all_grupos(self):
        """Seleccionar todos los grupos"""
        for var in self.grupos_vars.values():
            var.set(True)
    
    def clear_all_grupos(self):
        """Deseleccionar todos los grupos"""
        for var in self.grupos_vars.values():
            var.set(False)

    def create_comparison_filters(self):
        """Crear los filtros para el grupo de comparación"""
        # Obtener valores únicos del dataset para los filtros de comparación
        tipificaciones_unicas = sorted(self.df_total['Tipificación'].unique()) if 'Tipificación' in self.df_total.columns else ["Cae Muda o Cortada"]
        turnos_unicos = sorted(self.df_total['Turno'].unique()) if 'Turno' in self.df_total.columns else ["TT"]

        # Filtros - GRUPOS de comparación con selección múltiple
        ttk.Label(self.comparison_frame, text="Grupos:").grid(row=0, column=0, sticky=tk.W)
        grupos_comp_frame = ttk.Frame(self.comparison_frame)
        grupos_comp_frame.grid(row=0, column=1, columnspan=3, padx=(5, 0), sticky=(tk.W, tk.E))

        # Crear checkboxes para cada grupo de comparación
        self.grupos_comp_vars = {}
        grupos_por_fila = 4
        for i, grupo in enumerate(self.grupos_disponibles):
            var = tk.BooleanVar()
            # Marcar diferentes grupos por defecto para comparación
            if i >= 3 and i < 6:  # Seleccionar grupos 4, 5, 6 por defecto
                var.set(True)
            self.grupos_comp_vars[grupo] = var

            checkbox = ttk.Checkbutton(grupos_comp_frame, text=grupo, variable=var)
            row = i // grupos_por_fila
            col = i % grupos_por_fila
            checkbox.grid(row=row, column=col, sticky=tk.W, padx=(0, 10))

        # Turno para comparación
        ttk.Label(self.comparison_frame, text="Turno:").grid(row=2, column=0, sticky=tk.W)
        self.turno_comp_var = tk.StringVar(value=turnos_unicos[0] if turnos_unicos else "TT")
        turno_comp_combo = ttk.Combobox(self.comparison_frame, textvariable=self.turno_comp_var,
                                       values=turnos_unicos, width=15)
        turno_comp_combo.grid(row=2, column=1, padx=(5, 0), sticky=tk.W)

        # % extremo superior para comparación
        ttk.Label(self.comparison_frame, text="% extremo sup:").grid(row=2, column=2, sticky=tk.W, padx=(20, 0))
        self.quitar_extremo_comp_var = tk.StringVar(value="0.02")
        extremo_comp_entry = ttk.Entry(self.comparison_frame, textvariable=self.quitar_extremo_comp_var, width=15)
        extremo_comp_entry.grid(row=2, column=3, padx=(5, 0), sticky=tk.W)

        # Botones auxiliares para comparación
        select_all_comp_btn = ttk.Button(self.comparison_frame, text="Seleccionar Todos",
                                        command=self.select_all_grupos_comp)
        select_all_comp_btn.grid(row=3, column=0, pady=(10, 0), sticky=tk.W)

        clear_all_comp_btn = ttk.Button(self.comparison_frame, text="Deseleccionar Todos",
                                       command=self.clear_all_grupos_comp)
        clear_all_comp_btn.grid(row=3, column=3, pady=(10, 0), sticky=tk.E)

    def toggle_comparison(self):
        """Mostrar/ocultar los filtros de comparación"""
        if self.comparar_activo.get():
            self.comparison_frame.grid(row=0, column=5, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(20, 0))
        else:
            self.comparison_frame.grid_remove()

    def select_all_grupos_comp(self):
        """Seleccionar todos los grupos de comparación"""
        for var in self.grupos_comp_vars.values():
            var.set(True)

    def clear_all_grupos_comp(self):
        """Deseleccionar todos los grupos de comparación"""
        for var in self.grupos_comp_vars.values():
            var.set(False)

    def get_selected_grupos_comp(self):
        """Obtener lista de grupos seleccionados para comparación"""
        return [grupo for grupo, var in self.grupos_comp_vars.items() if var.get()]
    
    def get_selected_grupos(self):
        """Obtener lista de grupos seleccionados"""
        return [grupo for grupo, var in self.grupos_vars.items() if var.get()]
    
    def validate_numeric_input(self, value, field_name):
        """Validar entrada numérica y convertir a float"""
        try:
            num_value = float(value)
            if field_name == "ancho_intervalo" and num_value <= 0:
                raise ValueError("El ancho de intervalo debe ser mayor que 0")
            if field_name == "porcentaje" and (num_value < 0 or num_value >= 1):
                raise ValueError("El porcentaje debe estar entre 0 y 1 (no inclusive)")
            return num_value
        except ValueError as e:
            if "could not convert" in str(e):
                messagebox.showerror("Error de entrada", f"'{value}' no es un número válido para {field_name}")
            else:
                messagebox.showerror("Error de validación", str(e))
            return None
    
    def update_chart(self):
        # Limpiar figura anterior
        self.fig.clear()
        
        # Obtener y validar valores de los filtros
        grupos_filtrados = self.get_selected_grupos()
        if not grupos_filtrados:
            messagebox.showwarning("Sin grupos seleccionados", "Debes seleccionar al menos un grupo")
            return
        
        tipificacion_filtrada = self.tipificacion_var.get()
        turno_filtrado = self.turno_var.get()
        
        # Validar valores numéricos
        size_bin = self.validate_numeric_input(self.size_bin_var.get(), "ancho_intervalo")
        if size_bin is None:
            return
            
        quitar_x_porciento_extremo_sup = self.validate_numeric_input(self.quitar_extremo_var.get(), "porcentaje")
        if quitar_x_porciento_extremo_sup is None:
            return

        # Validar % extremo sup para comparación si está activa
        quitar_x_porciento_extremo_sup_comp = 0.0
        if self.comparar_activo.get():
            quitar_x_porciento_extremo_sup_comp = self.validate_numeric_input(self.quitar_extremo_comp_var.get(), "porcentaje")
            if quitar_x_porciento_extremo_sup_comp is None:
                return
        
        # Filtrar datos del grupo principal
        df = self.df_total.copy()
        df_filtrado = df[(df["grupo"].isin(grupos_filtrados)) &
                        (df["Tipificación"] == tipificacion_filtrada) &
                        (df["Turno"] == turno_filtrado)]

        # Verificar si está activa la comparación y filtrar datos del grupo de comparación
        df_comp_filtrado = pd.DataFrame()
        if self.comparar_activo.get():
            grupos_comp_filtrados = self.get_selected_grupos_comp()
            if grupos_comp_filtrados:
                # Usar la misma tipificación que el grupo principal
                turno_comp_filtrado = self.turno_comp_var.get()

                df_comp_filtrado = df[(df["grupo"].isin(grupos_comp_filtrados)) &
                                     (df["Tipificación"] == tipificacion_filtrada) &
                                     (df["Turno"] == turno_comp_filtrado)]

        if len(df_filtrado) == 0 and len(df_comp_filtrado) == 0:
            # Si no hay datos, mostrar mensaje
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No hay datos que coincidan con los filtros',
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14)
            ax.set_title("Sin datos")
            self.canvas.draw()
            self.update_stats(df_filtrado, df_comp_filtrado)
            return
        
        # Quitar extremos superiores si se especifica
        if quitar_x_porciento_extremo_sup > 0:
            if len(df_filtrado) > 0:
                limite_sup = df_filtrado["TalkingTime"].quantile(1 - quitar_x_porciento_extremo_sup)
                df_filtrado = df_filtrado[df_filtrado["TalkingTime"] <= limite_sup]

        if quitar_x_porciento_extremo_sup_comp > 0:
            if len(df_comp_filtrado) > 0:
                limite_sup_comp = df_comp_filtrado["TalkingTime"].quantile(1 - quitar_x_porciento_extremo_sup_comp)
                df_comp_filtrado = df_comp_filtrado[df_comp_filtrado["TalkingTime"] <= limite_sup_comp]

        # Crear bins considerando ambos datasets
        max_value = 0
        if len(df_filtrado) > 0:
            max_value = max(max_value, df_filtrado["TalkingTime"].max())
        if len(df_comp_filtrado) > 0:
            max_value = max(max_value, df_comp_filtrado["TalkingTime"].max())

        if max_value > 0:
            bins = np.arange(0, max_value + size_bin, size_bin)
        else:
            bins = np.array([0, size_bin])

        # Crear subplots con proporciones 20-60-20
        gs = self.fig.add_gridspec(1, 3, width_ratios=[1, 3, 1])
        ax1 = self.fig.add_subplot(gs[0, 0])  # Gráfico de barras horizontales
        ax2 = self.fig.add_subplot(gs[0, 1])  # Histograma
        ax3 = self.fig.add_subplot(gs[0, 2])  # Boxplot

        # Gráfico de barras horizontales para tipificaciones (izquierda)
        df_total_filtered = df[(df["grupo"].isin(grupos_filtrados)) & (df["Turno"] == turno_filtrado)]

        # Obtener datos de comparación para tipificaciones
        df_comp_total_filtered = pd.DataFrame()
        if self.comparar_activo.get() and len(df_comp_filtrado) > 0:
            grupos_comp_filtrados = self.get_selected_grupos_comp()
            turno_comp_filtrado = self.turno_comp_var.get()
            df_comp_total_filtered = df[(df["grupo"].isin(grupos_comp_filtrados)) & (df["Turno"] == turno_comp_filtrado)]

        if len(df_total_filtered) > 0 and 'Tipificación' in df_total_filtered.columns:
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
            if self.comparar_activo.get() and len(df_comp_filtrado) > 0:
                bars1 = ax1.barh(y_pos - bar_height/2, pct_principal, bar_height,
                               alpha=0.8, color='skyblue', edgecolor='black', label='Principal')
                bars2 = ax1.barh(y_pos + bar_height/2, pct_comparacion, bar_height,
                               alpha=0.8, color='red', edgecolor='darkred', label='Comparación')
                ax1.legend(fontsize=8)
            else:
                bars1 = ax1.barh(y_pos, pct_principal, alpha=0.7, color='skyblue', edgecolor='black')

            # Configurar el gráfico
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels(short_labels, fontsize=8)
            ax1.set_xlabel("Porcentaje (%)", fontsize=9)
            ax1.set_title("Distribución de\nTipificaciones", fontsize=10)
            ax1.grid(True, alpha=0.3, axis='x')
            ax1.invert_yaxis()
        else:
            ax1.text(0.5, 0.5, 'Sin datos\npara mostrar', ha='center', va='center',
                    transform=ax1.transAxes, fontsize=10)
            ax1.set_title("Distribución de\nTipificaciones", fontsize=10)

        # Histograma en el centro con doble eje Y
        if self.comparar_activo.get() and len(df_comp_filtrado) > 0:
            # Crear segundo eje Y para comparación
            ax2_twin = ax2.twinx()

            # Histograma grupo principal (eje Y izquierdo)
            if len(df_filtrado) > 0:
                n1, _, _ = ax2.hist(df_filtrado["TalkingTime"], bins=bins, edgecolor="black", alpha=0.7,
                        color='skyblue', label=f'Principal ({len(df_filtrado)} reg)')

                # Agregar curva KDE si está activada
                if self.mostrar_kde.get():
                    kde_data = df_filtrado["TalkingTime"]
                    kde = stats.gaussian_kde(kde_data)
                    x_range = np.linspace(kde_data.min(), kde_data.max(), 200)
                    kde_values = kde(x_range)
                    # Escalar KDE para que coincida con la escala del histograma
                    kde_scaled = kde_values * len(kde_data) * (bins[1] - bins[0])
                    ax2.plot(x_range, kde_scaled, color='darkblue', linewidth=2,
                           label='KDE Principal', alpha=0.8)

            # Histograma grupo comparación (eje Y derecho)
            n2, _, _ = ax2_twin.hist(df_comp_filtrado["TalkingTime"], bins=bins, edgecolor="darkred", alpha=0.7,
                    color='red', label=f'Comparación ({len(df_comp_filtrado)} reg)')

            # Agregar curva KDE para comparación si está activada
            if self.mostrar_kde.get() and len(df_comp_filtrado) > 0:
                kde_data_comp = df_comp_filtrado["TalkingTime"]
                kde_comp = stats.gaussian_kde(kde_data_comp)
                x_range_comp = np.linspace(kde_data_comp.min(), kde_data_comp.max(), 200)
                kde_values_comp = kde_comp(x_range_comp)
                # Escalar KDE para que coincida con la escala del histograma
                kde_scaled_comp = kde_values_comp * len(kde_data_comp) * (bins[1] - bins[0])
                ax2_twin.plot(x_range_comp, kde_scaled_comp, color='darkred', linewidth=2,
                            label='KDE Comparación', alpha=0.8)

            # Configurar ejes
            ax2.set_ylabel("Frecuencia (Principal)", color='blue')
            ax2_twin.set_ylabel("Frecuencia (Comparación)", color='red')
            ax2.tick_params(axis='y', labelcolor='blue')
            ax2_twin.tick_params(axis='y', labelcolor='red')

            # Leyenda combinada
            lines1, labels1 = ax2.get_legend_handles_labels()
            lines2, labels2 = ax2_twin.get_legend_handles_labels()
            ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper right')

            title_text = f"Histograma - Comparación\\nAzul: {', '.join(grupos_filtrados)} | Rojo: {', '.join(self.get_selected_grupos_comp())}"
        else:
            # Histograma simple
            if len(df_filtrado) > 0:
                ax2.hist(df_filtrado["TalkingTime"], bins=bins, edgecolor="black", alpha=0.7,
                        color='skyblue', label=f'Grupo Principal ({len(df_filtrado)} registros)')

                # Agregar curva KDE si está activada
                if self.mostrar_kde.get():
                    kde_data = df_filtrado["TalkingTime"]
                    kde = stats.gaussian_kde(kde_data)
                    x_range = np.linspace(kde_data.min(), kde_data.max(), 200)
                    kde_values = kde(x_range)
                    # Escalar KDE para que coincida con la escala del histograma
                    kde_scaled = kde_values * len(kde_data) * (bins[1] - bins[0])
                    ax2.plot(x_range, kde_scaled, color='darkblue', linewidth=2,
                           label='KDE', alpha=0.8)

                # Mostrar leyenda si hay KDE
                if self.mostrar_kde.get():
                    ax2.legend(fontsize=8)

            ax2.set_ylabel("Frecuencia")
            title_text = f"Histograma\\n{', '.join(grupos_filtrados)} | {turno_filtrado} | {tipificacion_filtrada}"

        ax2.set_title(title_text, fontsize=10)
        ax2.set_xlabel("Tiempo de conversación (segundos)")

        # Ajustar ticks del eje x para evitar saturación
        if len(bins) > 15:
            step = max(1, len(bins) // 10)
            ax2.set_xticks(bins[::step])
        else:
            ax2.set_xticks(bins)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)

        # Boxplot vertical a la derecha con doble eje Y
        if self.comparar_activo.get() and len(df_comp_filtrado) > 0:
            # Crear segundo eje Y para boxplot de comparación
            ax3_twin = ax3.twinx()

            # Boxplot grupo principal (eje Y izquierdo)
            if len(df_filtrado) > 0:
                bp1 = ax3.boxplot([df_filtrado["TalkingTime"]], positions=[0.8], widths=0.6,
                                 vert=True, patch_artist=True, labels=['Principal'])
                bp1['boxes'][0].set_facecolor('lightblue')
                bp1['boxes'][0].set_alpha(0.7)

            # Boxplot grupo comparación (eje Y derecho)
            bp2 = ax3_twin.boxplot([df_comp_filtrado["TalkingTime"]], positions=[1.2], widths=0.6,
                                  vert=True, patch_artist=True, labels=['Comparación'])
            bp2['boxes'][0].set_facecolor('lightcoral')
            bp2['boxes'][0].set_alpha(0.7)

            # Configurar ejes
            ax3.set_ylabel("TalkingTime (Principal)", color='blue')
            ax3_twin.set_ylabel("TalkingTime (Comparación)", color='red')
            ax3.tick_params(axis='y', labelcolor='blue')
            ax3_twin.tick_params(axis='y', labelcolor='red')

            # Configurar etiquetas del eje X
            ax3.set_xlim(0.5, 1.5)
            ax3.set_xticks([0.8, 1.2])
            ax3.set_xticklabels(['Principal', 'Comparación'], fontsize=8)
            ax3_twin.set_xlim(0.5, 1.5)
            ax3_twin.set_xticks([])
        else:
            # Boxplot simple
            if len(df_filtrado) > 0:
                bp = ax3.boxplot([df_filtrado["TalkingTime"]], vert=True, patch_artist=True,
                               labels=['Principal'])
                bp['boxes'][0].set_facecolor('lightblue')
                bp['boxes'][0].set_alpha(0.7)

            ax3.set_ylabel("Tiempo de conversación (segundos)")

        ax3.set_title("Boxplot de\nTalkingTime")
        ax3.grid(True, alpha=0.3)
        
        # Ajustar layout
        self.fig.tight_layout()
        
        # Actualizar canvas
        self.canvas.draw()
        
        # Actualizar estadísticas
        self.update_stats(df_filtrado, df_comp_filtrado)
    
    def detect_outliers(self, df_filtrado):
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
        # Limpiar tabla existente
        for item in self.agents_tree.get_children():
            self.agents_tree.delete(item)

        if len(outliers_df) == 0:
            # Insertar mensaje si no hay outliers
            self.agents_tree.insert('', tk.END, values=('Sin datos', '0', '0%'))
            self.current_agents_data = []
            return

        # Calcular value_counts de agentes
        if 'Nombre Agente' in outliers_df.columns:
            agent_counts = outliers_df['Nombre Agente'].value_counts()
            total_outliers = len(outliers_df)

            # Preparar datos para guardar y ordenar
            agents_data = []
            for agent, count in agent_counts.items():
                percentage = (count / total_outliers) * 100
                values = (
                    str(agent)[:15],  # Truncar nombre si es muy largo
                    str(count),
                    f"{percentage:.1f}%"
                )
                agents_data.append(values)

            # Guardar datos para ordenamiento
            self.current_agents_data = agents_data

            # Configurar ordenamiento inicial por cantidad (descendente)
            self.agents_sort_column = 'Cantidad'
            self.agents_sort_reverse = True
            self.update_agents_column_headers()

            # Insertar datos ordenados por cantidad (de mayor a menor)
            for values in agents_data:
                self.agents_tree.insert('', tk.END, values=values)
        else:
            self.agents_tree.insert('', tk.END, values=('Sin datos', '0', '0%'))
            self.current_agents_data = []

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

    def update_stats(self, df_filtrado, df_comp_filtrado=None):
        """Actualizar el panel de estadísticas y outliers"""
        # Actualizar estadísticas básicas
        self.stats_text.delete(1.0, tk.END)

        if df_comp_filtrado is None:
            df_comp_filtrado = pd.DataFrame()

        stats_text = ""
        all_outliers = pd.DataFrame()

        # Estadísticas del grupo principal
        if len(df_filtrado) > 0:
            stats = df_filtrado["TalkingTime"].describe()
            outliers = self.detect_outliers(df_filtrado)
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
            stats_comp = df_comp_filtrado["TalkingTime"].describe()
            outliers_comp = self.detect_outliers(df_comp_filtrado)
            outliers_comp['Grupo'] = 'Comparación'  # Marcar outliers del grupo de comparación

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
                stats_text += "\n📊 COMPARACIÓN:\n"
                media_diff = stats_comp['mean'] - stats['mean']
                mediana_diff = stats_comp['50%'] - stats['50%']
                std_diff = stats_comp['std'] - stats['std']

                stats_text += f"Dif. Media: {media_diff:+.2f} seg\n"
                stats_text += f"Dif. Mediana: {mediana_diff:+.2f} seg\n"
                stats_text += f"Dif. Desv. Est.: {std_diff:+.2f} seg"

        if len(df_filtrado) == 0 and len(df_comp_filtrado) == 0:
            stats_text = "No hay datos para mostrar estadísticas."

        self.stats_text.insert(1.0, stats_text)

        # Actualizar tabla de outliers (combinando ambos grupos)
        self.update_outliers_table(all_outliers)

        # Actualizar análisis de agentes (combinando ambos grupos)
        self.update_agents_analysis(all_outliers)

# Crear y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalysisApp(root)
    root.mainloop()