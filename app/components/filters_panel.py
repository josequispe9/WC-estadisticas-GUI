"""
Panel de filtros principal
"""
import tkinter as tk
from tkinter import ttk


class FiltersPanel:
    def __init__(self, parent, grupos_disponibles, tipificaciones_unicas, turnos_unicos):
        self.parent = parent
        self.grupos_disponibles = grupos_disponibles
        self.tipificaciones_unicas = tipificaciones_unicas
        self.turnos_unicos = turnos_unicos

        # Variables de control
        self.grupos_vars = {}
        self.tipificacion_var = tk.StringVar(value=tipificaciones_unicas[0] if tipificaciones_unicas else "Cae Muda o Cortada")
        self.turno_var = tk.StringVar(value=turnos_unicos[0] if turnos_unicos else "TT")
        self.size_bin_var = tk.StringVar(value="1.0")
        self.quitar_extremo_var = tk.StringVar(value="0.02")
        self.mostrar_kde = tk.BooleanVar()

        # Crear el frame principal
        self.frame = ttk.LabelFrame(parent, text="Filtros Principales", padding="10")
        self.create_widgets()

    def create_widgets(self):
        """Crear los widgets del panel de filtros"""
        # Filtros - GRUPOS con selección múltiple
        ttk.Label(self.frame, text="Grupos:").grid(row=0, column=0, sticky=tk.W)
        grupos_frame = ttk.Frame(self.frame)
        grupos_frame.grid(row=0, column=1, columnspan=3, padx=(5, 0), sticky=(tk.W, tk.E))

        # Crear checkboxes para cada grupo
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

        # Tipificación
        ttk.Label(self.frame, text="Tipificación:").grid(row=2, column=0, sticky=tk.W)
        tipificacion_combo = ttk.Combobox(self.frame, textvariable=self.tipificacion_var,
                                        values=self.tipificaciones_unicas, width=25)
        tipificacion_combo.grid(row=2, column=1, padx=(5, 0), sticky=tk.W)

        # Turno
        ttk.Label(self.frame, text="Turno:").grid(row=2, column=2, sticky=tk.W, padx=(20, 0))
        turno_combo = ttk.Combobox(self.frame, textvariable=self.turno_var,
                                 values=self.turnos_unicos, width=15)
        turno_combo.grid(row=2, column=3, padx=(5, 0), sticky=tk.W)

        # Controles numéricos
        ttk.Label(self.frame, text="Ancho intervalo:").grid(row=3, column=0, sticky=tk.W)
        size_bin_entry = ttk.Entry(self.frame, textvariable=self.size_bin_var, width=15)
        size_bin_entry.grid(row=3, column=1, padx=(5, 0), sticky=tk.W)

        ttk.Label(self.frame, text="% extremo sup:").grid(row=3, column=2, sticky=tk.W, padx=(20, 0))
        extremo_entry = ttk.Entry(self.frame, textvariable=self.quitar_extremo_var, width=15)
        extremo_entry.grid(row=3, column=3, padx=(5, 0), sticky=tk.W)

        # Opción KDE global
        kde_check = ttk.Checkbutton(self.frame, text="Mostrar curva KDE",
                                   variable=self.mostrar_kde)
        kde_check.grid(row=3, column=4, padx=(20, 0), sticky=tk.W)

    def get_selected_grupos(self):
        """Obtener lista de grupos seleccionados"""
        return [grupo for grupo, var in self.grupos_vars.items() if var.get()]

    def select_all_grupos(self):
        """Seleccionar todos los grupos"""
        for var in self.grupos_vars.values():
            var.set(True)

    def clear_all_grupos(self):
        """Deseleccionar todos los grupos"""
        for var in self.grupos_vars.values():
            var.set(False)