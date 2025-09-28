#!/usr/bin/env python3
"""
Script para ejecutar la aplicación WC Estadísticas GUI
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app.main import main
    main()