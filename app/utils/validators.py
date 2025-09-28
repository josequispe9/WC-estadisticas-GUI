"""
Módulo de validaciones para la aplicación
"""
from tkinter import messagebox


def validate_numeric_input(value, field_name):
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


def validate_groups_selection(grupos_filtrados):
    """Validar que haya al menos un grupo seleccionado"""
    if not grupos_filtrados:
        messagebox.showwarning("Sin grupos seleccionados", "Debes seleccionar al menos un grupo")
        return False
    return True