"""
Panel de filtros para comparación
"""
import tkinter as tk
from tkinter import ttk


class ComparisonPanel:
    def __init__(self, parent, grupos_disponibles, turnos_unicos):
        self.parent = parent
        self.grupos_disponibles = grupos_disponibles
        self.turnos_unicos = turnos_unicos

        # Variables de control
        self.grupos_comp_vars = {}
        self.turno_comp_var = tk.StringVar(value=turnos_unicos[0] if turnos_unicos else "TT")
        self.quitar_extremo_comp_var = tk.StringVar(value="0.02")
        self.comparar_activo = tk.BooleanVar()

        # Crear el frame principal
        self.frame = ttk.LabelFrame(parent, text="Filtros para Comparación (Grupo Rojo)", padding="10")
        self.create_widgets()

    def create_widgets(self):
        """Crear los widgets del panel de comparación"""
        # Filtros - GRUPOS de comparación con selección múltiple
        ttk.Label(self.frame, text="Grupos:").grid(row=0, column=0, sticky=tk.W)
        grupos_comp_frame = ttk.Frame(self.frame)
        grupos_comp_frame.grid(row=0, column=1, columnspan=3, padx=(5, 0), sticky=(tk.W, tk.E))

        # Crear checkboxes para cada grupo de comparación
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
        ttk.Label(self.frame, text="Turno:").grid(row=2, column=0, sticky=tk.W)
        turno_comp_combo = ttk.Combobox(self.frame, textvariable=self.turno_comp_var,
                                       values=self.turnos_unicos, width=15)
        turno_comp_combo.grid(row=2, column=1, padx=(5, 0), sticky=tk.W)

        # % extremo superior para comparación
        ttk.Label(self.frame, text="% extremo sup:").grid(row=2, column=2, sticky=tk.W, padx=(20, 0))
        extremo_comp_entry = ttk.Entry(self.frame, textvariable=self.quitar_extremo_comp_var, width=15)
        extremo_comp_entry.grid(row=2, column=3, padx=(5, 0), sticky=tk.W)

        # Botones auxiliares para comparación
        select_all_comp_btn = ttk.Button(self.frame, text="Seleccionar Todos",
                                        command=self.select_all_grupos_comp)
        select_all_comp_btn.grid(row=3, column=0, pady=(10, 0), sticky=tk.W)

        clear_all_comp_btn = ttk.Button(self.frame, text="Deseleccionar Todos",
                                       command=self.clear_all_grupos_comp)
        clear_all_comp_btn.grid(row=3, column=3, pady=(10, 0), sticky=tk.E)

    def get_selected_grupos_comp(self):
        """Obtener lista de grupos seleccionados para comparación"""
        return [grupo for grupo, var in self.grupos_comp_vars.items() if var.get()]

    def select_all_grupos_comp(self):
        """Seleccionar todos los grupos de comparación"""
        for var in self.grupos_comp_vars.values():
            var.set(True)

    def clear_all_grupos_comp(self):
        """Deseleccionar todos los grupos de comparación"""
        for var in self.grupos_comp_vars.values():
            var.set(False)