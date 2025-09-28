"""
Aplicación principal con sistema de pestañas y arquitectura modular
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

# Importar módulos locales
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.loader import load_data, get_available_groups, get_unique_values
from app.data.processor import (filter_data, apply_extremes_filter, calculate_bins,
                           get_descriptive_stats, calculate_comparison_stats)
from app.utils.validators import validate_numeric_input, validate_groups_selection
from app.components.filters_panel import FiltersPanel
from app.components.comparison_panel import ComparisonPanel
from app.components.stats_panel import StatsPanel
from app.graphics.histogram import plot_histogram_simple, plot_histogram_comparison, configure_histogram_axes
from app.graphics.boxplot import plot_boxplot_simple, plot_boxplot_comparison, configure_boxplot_axes
from app.graphics.tipifications import plot_tipifications_distribution
from app.graphics.advanced_plots import (plot_activity_heatmap, plot_time_series, plot_agent_performance,
                                    plot_correlation_matrix, plot_hourly_heatmap)


class AnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WC Estadísticas GUI v3.0 - Análisis de Rendimiento")
        self.root.geometry("1400x900")

        # Configurar protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Cargar datos desde archivo CSV
        self.df_total, file_loaded = load_data()

        # Mostrar información de carga si es necesario
        if not file_loaded:
            messagebox.showwarning("Archivo no encontrado",
                                 "No se encontró el archivo de datos.\n\nSe usarán datos de ejemplo.")

        # Obtener valores únicos para filtros
        self.grupos_disponibles = get_available_groups()
        self.tipificaciones_unicas = get_unique_values(self.df_total, 'Tipificación')
        self.turnos_unicos = get_unique_values(self.df_total, 'Turno')

        # Crear interface con pestañas
        self.create_notebook_interface()

    def create_notebook_interface(self):
        """Crear la interfaz principal con pestañas"""
        # Frame principal que contendrá filtros + pestañas
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame de información del dataset (arriba)
        self.create_info_section(main_container)

        # Panel de filtros principales (compartido para todas las pestañas)
        self.create_shared_filters_section(main_container)

        # Crear el notebook (sistema de pestañas)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Pestaña 1: Análisis Básico
        self.create_basic_analysis_tab()

        # Pestaña 2: Análisis Avanzado
        self.create_advanced_analysis_tab()

        # Pestaña 3: Series Temporales
        self.create_temporal_analysis_tab()

        # Pestaña 4: Comparaciones Múltiples
        self.create_multiple_comparison_tab()

    def create_info_section(self, parent):
        """Crear sección de información del dataset"""
        info_frame = ttk.LabelFrame(parent, text="Información del Dataset", padding="5")
        info_frame.pack(fill=tk.X, pady=(0, 5))

        # Mostrar info básica del dataset cargado
        info_text = f"Registros: {len(self.df_total)} | Columnas: {', '.join(self.df_total.columns[:5])}{'...' if len(self.df_total.columns) > 5 else ''}"
        ttk.Label(info_frame, text=info_text).pack(side=tk.LEFT)

        # Botón para recargar datos
        reload_btn = ttk.Button(info_frame, text="Recargar Datos", command=self.reload_data)
        reload_btn.pack(side=tk.RIGHT)

    def create_shared_filters_section(self, parent):
        """Crear sección de filtros compartida"""
        # Frame contenedor horizontal para filtros principales y comparación
        filters_container = ttk.Frame(parent)
        filters_container.pack(fill=tk.X, pady=(0, 5))

        filters_container.columnconfigure(0, weight=1)  # Filtros principales expansibles
        filters_container.columnconfigure(1, weight=0)  # Filtros comparación fijo

        # Panel de filtros principales (columna 0)
        self.filters_panel = FiltersPanel(filters_container, self.grupos_disponibles,
                                        self.tipificaciones_unicas, self.turnos_unicos)
        self.filters_panel.frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        # Panel de filtros de comparación (columna 1, inicialmente oculto)
        self.comparison_panel = ComparisonPanel(filters_container, self.grupos_disponibles, self.turnos_unicos)
        self.comparison_panel.frame.grid_remove()  # Ocultar inicialmente

        # Frame de controles principales
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, pady=(0, 5))

        # Botón comparar y variables de control
        self.comparar_activo = tk.BooleanVar()
        compare_btn = ttk.Checkbutton(controls_frame, text="Comparar con otro grupo",
                                     variable=self.comparar_activo, command=self.toggle_comparison)
        compare_btn.grid(row=0, column=0, pady=(5, 0), sticky=tk.W)

        # Botones auxiliares (reposicionados)
        select_all_btn = ttk.Button(controls_frame, text="Seleccionar Todos",
                                   command=self.filters_panel.select_all_grupos)
        select_all_btn.grid(row=0, column=1, pady=(5, 0), sticky=tk.W, padx=(20, 5))

        # Botón actualizar (en el centro)
        update_btn = ttk.Button(controls_frame, text="Actualizar Todos los Gráficos", command=self.update_all_charts)
        update_btn.grid(row=0, column=2, pady=(5, 0), padx=(5, 5))

        clear_all_btn = ttk.Button(controls_frame, text="Deseleccionar Todos",
                                  command=self.filters_panel.clear_all_grupos)
        clear_all_btn.grid(row=0, column=3, pady=(5, 0), sticky=tk.E, padx=(5, 0))

    def create_basic_analysis_tab(self):
        """Crear pestaña de análisis básico"""
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="📊 Análisis Básico")

        # Frame principal
        main_frame = ttk.Frame(tab1, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para el gráfico (60% del espacio)
        chart_frame = ttk.Frame(main_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Configurar el gráfico matplotlib
        self.fig_basic = Figure(figsize=(14, 5), dpi=100)
        self.canvas_basic = FigureCanvasTkAgg(self.fig_basic, master=chart_frame)
        self.canvas_basic.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Panel de estadísticas (40% del espacio restante)
        stats_container = ttk.Frame(main_frame)
        stats_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        self.stats_panel = StatsPanel(stats_container)
        self.stats_panel.frame.pack(fill=tk.BOTH, expand=True)

        # Generar gráfico inicial
        self.update_basic_chart()

    def create_advanced_analysis_tab(self):
        """Crear pestaña de análisis avanzado"""
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="🔬 Análisis Avanzado")

        # Frame principal
        main_frame = ttk.Frame(tab2, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Análisis Avanzado", font=('TkDefaultFont', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        # Frame para gráficos (2x2)
        charts_frame = ttk.Frame(main_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar gráficos matplotlib
        self.fig_advanced = Figure(figsize=(16, 8), dpi=100)
        self.canvas_advanced = FigureCanvasTkAgg(self.fig_advanced, master=charts_frame)
        self.canvas_advanced.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Generar gráficos iniciales
        self.update_advanced_charts()

    def create_temporal_analysis_tab(self):
        """Crear pestaña de análisis temporal"""
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="📈 Series Temporales")

        # Frame principal
        main_frame = ttk.Frame(tab3, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Análisis de Series Temporales", font=('TkDefaultFont', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        # Frame para gráficos
        charts_frame = ttk.Frame(main_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar gráficos matplotlib
        self.fig_temporal = Figure(figsize=(16, 10), dpi=100)
        self.canvas_temporal = FigureCanvasTkAgg(self.fig_temporal, master=charts_frame)
        self.canvas_temporal.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Generar gráficos iniciales
        self.update_temporal_charts()

    def create_multiple_comparison_tab(self):
        """Crear pestaña de comparaciones múltiples"""
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text="🔄 Comparaciones")

        # Frame principal
        main_frame = ttk.Frame(tab4, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Comparaciones Múltiples", font=('TkDefaultFont', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        # Información de próximas funcionalidades
        info_text = """🚧 Próximas funcionalidades:

• Comparación simultánea de múltiples grupos
• Análisis estadístico (t-test, ANOVA)
• Gráficos de radar por grupo
• Análisis de rendimiento relativo
• Benchmarking automático

Esta pestaña se desarrollará en futuras versiones."""

        info_label = ttk.Label(main_frame, text=info_text, justify=tk.LEFT, font=('TkDefaultFont', 11))
        info_label.pack(pady=20)

    def toggle_comparison(self):
        """Mostrar/ocultar los filtros de comparación"""
        if self.comparar_activo.get():
            # Posicionar a la derecha de los filtros principales
            self.comparison_panel.frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        else:
            self.comparison_panel.frame.grid_remove()

    def update_all_charts(self):
        """Actualizar todos los gráficos de todas las pestañas"""
        try:
            self.update_basic_chart()
            self.update_advanced_charts()
            self.update_temporal_charts()
        except Exception as e:
            messagebox.showerror("Error al actualizar", f"Error al actualizar gráficos: {str(e)}")

    def reload_data(self):
        """Recargar datos desde archivo"""
        self.df_total, file_loaded = load_data()
        self.tipificaciones_unicas = get_unique_values(self.df_total, 'Tipificación')
        self.turnos_unicos = get_unique_values(self.df_total, 'Turno')

        # Actualizar información del dataset
        messagebox.showinfo("Datos recargados",
                          f"Datos recargados exitosamente\\n"
                          f"Registros: {len(self.df_total)}\\n"
                          f"Columnas: {len(self.df_total.columns)}")

        # Actualizar todos los gráficos con los nuevos datos
        self.update_all_charts()

    def update_basic_chart(self):
        """Actualizar gráficos de análisis básico"""
        # Limpiar figura anterior
        self.fig_basic.clear()

        # Obtener y validar valores de los filtros
        grupos_filtrados = self.filters_panel.get_selected_grupos()
        if not validate_groups_selection(grupos_filtrados):
            return

        tipificacion_filtrada = self.filters_panel.tipificacion_var.get()
        turno_filtrado = self.filters_panel.turno_var.get()

        # Validar valores numéricos
        size_bin = validate_numeric_input(self.filters_panel.size_bin_var.get(), "ancho_intervalo")
        if size_bin is None:
            return

        quitar_x_porciento_extremo_sup = validate_numeric_input(self.filters_panel.quitar_extremo_var.get(), "porcentaje")
        if quitar_x_porciento_extremo_sup is None:
            return

        # Validar % extremo sup para comparación si está activa
        quitar_x_porciento_extremo_sup_comp = 0.0
        if self.comparar_activo.get():
            quitar_x_porciento_extremo_sup_comp = validate_numeric_input(self.comparison_panel.quitar_extremo_comp_var.get(), "porcentaje")
            if quitar_x_porciento_extremo_sup_comp is None:
                return

        # Filtrar datos del grupo principal
        df_filtrado = filter_data(self.df_total, grupos_filtrados, tipificacion_filtrada, turno_filtrado)

        # Verificar si está activa la comparación y filtrar datos del grupo de comparación
        df_comp_filtrado = pd.DataFrame()
        if self.comparar_activo.get():
            grupos_comp_filtrados = self.comparison_panel.get_selected_grupos_comp()
            if grupos_comp_filtrados:
                # Usar la misma tipificación que el grupo principal
                turno_comp_filtrado = self.comparison_panel.turno_comp_var.get()
                df_comp_filtrado = filter_data(self.df_total, grupos_comp_filtrados, tipificacion_filtrada, turno_comp_filtrado)

        if len(df_filtrado) == 0 and len(df_comp_filtrado) == 0:
            # Si no hay datos, mostrar mensaje
            ax = self.fig_basic.add_subplot(111)
            ax.text(0.5, 0.5, 'No hay datos que coincidan con los filtros',
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14)
            ax.set_title("Sin datos")
            self.canvas_basic.draw()
            self.stats_panel.update_stats(df_filtrado, df_comp_filtrado)
            return

        # Aplicar filtros de extremos
        df_filtrado = apply_extremes_filter(df_filtrado, quitar_x_porciento_extremo_sup)
        df_comp_filtrado = apply_extremes_filter(df_comp_filtrado, quitar_x_porciento_extremo_sup_comp)

        # Calcular bins
        bins = calculate_bins(df_filtrado, df_comp_filtrado, size_bin)

        # Crear subplots con proporciones 20-60-20
        gs = self.fig_basic.add_gridspec(1, 3, width_ratios=[1, 3, 1])
        ax1 = self.fig_basic.add_subplot(gs[0, 0])  # Gráfico de barras horizontales
        ax2 = self.fig_basic.add_subplot(gs[0, 1])  # Histograma
        ax3 = self.fig_basic.add_subplot(gs[0, 2])  # Boxplot

        # Gráfico de distribución de tipificaciones
        plot_tipifications_distribution(ax1, self.df_total, grupos_filtrados, turno_filtrado,
                                      self.df_total, self.comparison_panel.get_selected_grupos_comp(),
                                      self.comparison_panel.turno_comp_var.get(), self.comparar_activo.get())

        # Histograma con/sin comparación
        if self.comparar_activo.get() and len(df_comp_filtrado) > 0:
            # Crear segundo eje Y para comparación
            ax2_twin = ax2.twinx()
            plot_histogram_comparison(ax2, ax2_twin, df_filtrado, df_comp_filtrado, bins, self.filters_panel.mostrar_kde.get())
            title_text = f"Histograma - Comparación\\nAzul: {', '.join(grupos_filtrados)} | Rojo: {', '.join(self.comparison_panel.get_selected_grupos_comp())}"
        else:
            plot_histogram_simple(ax2, df_filtrado, bins, self.filters_panel.mostrar_kde.get())
            title_text = f"Histograma\\n{', '.join(grupos_filtrados)} | {turno_filtrado} | {tipificacion_filtrada}"

        ax2.set_title(title_text, fontsize=10)
        configure_histogram_axes(ax2, bins)

        # Boxplot con/sin comparación
        if self.comparar_activo.get() and len(df_comp_filtrado) > 0:
            # Crear segundo eje Y para boxplot de comparación
            ax3_twin = ax3.twinx()
            plot_boxplot_comparison(ax3, ax3_twin, df_filtrado, df_comp_filtrado)
        else:
            plot_boxplot_simple(ax3, df_filtrado)

        configure_boxplot_axes(ax3)

        # Ajustar layout
        self.fig_basic.tight_layout()

        # Actualizar canvas
        self.canvas_basic.draw()

        # Actualizar estadísticas
        self.stats_panel.update_stats(df_filtrado, df_comp_filtrado)

    def update_advanced_charts(self):
        """Actualizar gráficos de análisis avanzado"""
        self.fig_advanced.clear()

        # Obtener datos filtrados básicos para análisis avanzado
        grupos_filtrados = self.filters_panel.get_selected_grupos() if hasattr(self, 'filters_panel') else self.grupos_disponibles[:3]
        tipificacion_filtrada = self.filters_panel.tipificacion_var.get() if hasattr(self, 'filters_panel') else self.tipificaciones_unicas[0]
        turno_filtrado = self.filters_panel.turno_var.get() if hasattr(self, 'filters_panel') else self.turnos_unicos[0]

        df_filtrado = filter_data(self.df_total, grupos_filtrados, tipificacion_filtrada, turno_filtrado)

        # Obtener datos de comparación si está activa
        df_comp_filtrado = pd.DataFrame()
        if hasattr(self, 'comparar_activo') and self.comparar_activo.get():
            grupos_comp_filtrados = self.comparison_panel.get_selected_grupos_comp()
            if grupos_comp_filtrados:
                turno_comp_filtrado = self.comparison_panel.turno_comp_var.get()
                df_comp_filtrado = filter_data(self.df_total, grupos_comp_filtrados, tipificacion_filtrada, turno_comp_filtrado)

        # Crear subplots 1x2 (solo los dos de arriba)
        gs = self.fig_advanced.add_gridspec(1, 2, hspace=0.3, wspace=0.3)

        # Heatmap de actividad
        ax1 = self.fig_advanced.add_subplot(gs[0, 0])
        plot_activity_heatmap(ax1, df_filtrado, df_comp_filtrado, self.comparar_activo.get() if hasattr(self, 'comparar_activo') else False)

        # Rendimiento por agente
        ax2 = self.fig_advanced.add_subplot(gs[0, 1])
        plot_agent_performance(ax2, df_filtrado)

        self.canvas_advanced.draw()

    def update_temporal_charts(self):
        """Actualizar gráficos de análisis temporal"""
        self.fig_temporal.clear()

        # Obtener datos filtrados básicos para análisis temporal
        grupos_filtrados = self.filters_panel.get_selected_grupos() if hasattr(self, 'filters_panel') else self.grupos_disponibles[:3]
        tipificacion_filtrada = self.tipificaciones_unicas[0] if self.tipificaciones_unicas else "Cae Muda o Cortada"
        turno_filtrado = self.turnos_unicos[0] if self.turnos_unicos else "TT"

        df_filtrado = filter_data(self.df_total, grupos_filtrados, tipificacion_filtrada, turno_filtrado)

        # Crear subplot para series de tiempo
        ax = self.fig_temporal.add_subplot(111)
        plot_time_series(ax, df_filtrado)

        self.canvas_temporal.draw()

    def on_closing(self):
        """Manejo apropiado del cierre de la aplicación"""
        try:
            # Cerrar figuras de matplotlib para liberar memoria
            if hasattr(self, 'fig_basic'):
                plt.close(self.fig_basic)
            if hasattr(self, 'fig_advanced'):
                plt.close(self.fig_advanced)
            if hasattr(self, 'fig_temporal'):
                plt.close(self.fig_temporal)
        except:
            pass
        finally:
            # Destruir la ventana principal
            self.root.quit()
            self.root.destroy()


# Función principal para ejecutar la aplicación
def main():
    root = tk.Tk()
    app = AnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()