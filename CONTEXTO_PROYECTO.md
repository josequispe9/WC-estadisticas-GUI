# Contexto del Proyecto - WC Estadísticas GUI

## Información General
- **Nombre del Proyecto**: WC-estadisticas-GUI
- **Tipo**: Aplicación de escritorio Python con Tkinter para análisis de rendimiento de call center
- **Propósito**: Analizar rendimiento de agentes que venden abonos de telefonía
- **Fecha de última sesión**: 2025-09-28

## Estructura del Proyecto
```
WC-estadisticas-GUI/
├── analisis/                           # Módulos de análisis Jupyter
│   └── analisis-rendimiento-agente.ipynb  # Análisis de rendimiento de agentes
├── app/                               # Aplicación principal
│   └── app.py                        # GUI principal con Tkinter
├── data/                             # Datos del proyecto
│   ├── raw/                         # Datos sin procesar (CSV de reportes)
│   └── process/                     # Datos procesados
│       └── llamadas_procesadas.csv  # Dataset principal procesado
├── .venv/                           # Entorno virtual Python
├── requirements.txt                 # Dependencias Python
├── .gitignore                      # Archivos ignorados por Git
└── CONTEXTO_PROYECTO.md            # Este archivo de contexto
```

## Detalles del Proyecto

### Análisis de Rendimiento (`analisis/analisis-rendimiento-agente.ipynb`)
- **Variables principales**: Tipificación, TalkingTime, Sentido de llamada
- **Grupos de agentes**: 8 equipos diferentes (ap_connection, byl, capa, diana, josefina_marcos, melanie_naty, yasmin_marina, romi)
- **Fuente de datos**: Reportes diarios de interacción de Mitrol
- **Análisis incluye**: Distribución de tiempos, detección de outliers, estadísticas por grupo

### Aplicación GUI (`app/app.py`)
- **Framework**: Tkinter con matplotlib integrado
- **Funcionalidades actuales**:
  - Carga de datos desde `data/process/llamadas_procesadas.csv`
  - Filtros por grupos de agentes, tipificación y turno
  - Visualizaciones: Histograma, boxplot, distribución de tipificaciones
  - Detección y análisis de outliers con método IQR
  - Estadísticas descriptivas detalladas
  - Tablas interactivas con ordenamiento
- **Características técnicas**:
  - Validación de entrada numérica
  - Manejo de errores y datos faltantes
  - Interfaz responsiva con múltiples paneles

## Estado del Proyecto
- ✅ Entorno virtual configurado
- ✅ Dependencias: tkinter, matplotlib, numpy, pandas
- ✅ Análisis base implementado en Jupyter
- ✅ GUI funcional con visualizaciones básicas
- ✅ Sistema de detección de outliers implementado
- ✅ Datos de ejemplo funcionales

## Datos y Variables
- **TalkingTime**: Duración de llamada en segundos
- **Tipificación**: Categorización manual de la interacción
- **Sentido**: Llamada manual o desde discador
- **Turno**: TM (mañana), TT (tarde), TN (noche)
- **Grupos**: Equipos de trabajo organizados por supervisor

## Modificaciones Realizadas

### 2025-09-27 - Funcionalidad de Comparación de Grupos

#### Versión 1.0 - Implementación inicial
- ✅ **Botón "Comparar"**: Agregado checkbox para habilitar modo comparación
- ✅ **Panel de filtros secundario**: Nuevo apartado para seleccionar grupo de comparación (en rojo)
- ✅ **Visualización dual en gráficos**:
  - Histograma: Muestra ambos grupos superpuestos (azul vs rojo)
  - Boxplot: Visualización lado a lado de ambos grupos
  - Gráfico de barras: Mantiene funcionalidad original
- ✅ **Estadísticas comparativas**:
  - Panel dividido en dos secciones (🔵 Principal / 🔴 Comparación)
  - Cálculo automático de diferencias (media, mediana, desviación estándar)
  - Indicadores visuales en tablas de outliers

#### Versión 2.0 - Mejoras de UI/UX y Visualización
- ✅ **Reposicionamiento de filtros**: Panel de comparación aparece a la derecha de filtros principales
- ✅ **Reorganización de botones**: "Actualizar Gráfico" centrado entre "Seleccionar Todos" y "Deseleccionar Todos"
- ✅ **Doble eje Y para visualizaciones**:
  - **Histograma**: Eje Y izquierdo (azul) para grupo principal, eje Y derecho (rojo) para comparación
  - **Boxplot**: Posicionamiento dual con escalas independientes en cada eje Y
- ✅ **Barras duales en tipificaciones**: Barras horizontales azules y rojas lado a lado para cada tipificación
- ✅ **Leyendas y etiquetas mejoradas**: Colores diferenciados y escalas independientes

#### Versión 3.0 - Optimizaciones y Nuevas Funcionalidades
- ✅ **Simplificación de filtros de comparación**:
  - Eliminada opción de tipificación para grupo de comparación (siempre usa la misma que grupo principal)
  - Agregado control individual de "% extremo sup" para cada grupo
- ✅ **Curvas de densidad KDE**:
  - Opción global para mostrar/ocultar curvas KDE en histogramas
  - KDE escalado automáticamente para coincidir con escala del histograma
  - Funciona tanto en modo simple como en modo comparación con doble eje Y
- ✅ **Mejoras técnicas**:
  - Validación independiente de parámetros para cada grupo
  - Lógica optimizada para filtrado con misma tipificación
  - Importación de scipy.stats para cálculos KDE

#### Versión 4.0 - Refactorización Completa y Sistema de Pestañas
- ✅ **Arquitectura modular**:
  - Separación en módulos: `data/`, `graphics/`, `components/`, `utils/`
  - Código organizado por responsabilidades
  - Facilita mantenimiento y extensibilidad
- ✅ **Sistema de pestañas (ttk.Notebook)**:
  - **📊 Análisis Básico**: Funcionalidad completa (histograma, boxplot, tipificaciones, outliers, comparación de grupos)
  - **🔬 Análisis Avanzado**: ⚠️ En desarrollo - Heatmap de actividad, rendimiento por agente (top 5)
  - **📈 Series Temporales**: ⚠️ En desarrollo - Evolución temporal de métricas
  - **🔄 Comparaciones**: ⚠️ En desarrollo - Funcionalidades de comparación múltiple
- ✅ **Nuevos gráficos implementados**:
  - Heatmap de actividad por hora/día (reemplazó gráfico de violín)
  - Análisis de rendimiento por agente (top 5, color consistente)
  - Matriz de correlación entre variables
  - Series temporales con media y mediana diaria
- ✅ **Componentes UI modulares**:
  - `FiltersPanel`: Panel de filtros principales
  - `ComparisonPanel`: Panel de filtros de comparación
  - `StatsPanel`: Panel de estadísticas y outliers
- ✅ **Mejoras técnicas**:
  - Backup automático de versión anterior (`app_backup_v2.py`)
  - Script de ejecución simplificado (`run_app.py`)
  - Gestión de datos centralizada
  - Validaciones modulares

#### Versión 5.0 - Correcciones Finales y Optimizaciones
- ✅ **Correcciones de UI**:
  - Posicionamiento correcto de filtros de comparación a la derecha de filtros principales
  - Protocolo de cierre adecuado de la aplicación (cleanup de figuras matplotlib)
- ✅ **Eliminación de dependencias innecesarias**:
  - Removido seaborn de requirements.txt e imports
  - Mantenimiento del estilo visual consistente sin librerías externas
- ✅ **Optimización de gráficos avanzados**:
  - Heatmap de actividad reemplazó gráfico de violín (mejor rendimiento)
  - Top 5 agentes en lugar de top 20 (visualización más clara)
  - Color consistente en gráfico de rendimiento por agente

## Estado Actual de Pestañas
- ✅ **📊 Análisis Básico**: Completamente funcional
- ⚠️ **🔬 Análisis Avanzado**: En desarrollo (funciones básicas implementadas)
- ⚠️ **📈 Series Temporales**: En desarrollo (estructura preparada)
- ⚠️ **🔄 Comparaciones**: En desarrollo (preparado para futuras funcionalidades)

## Próximas Tareas
*(Se actualizará según necesidades del usuario)*

## Notas Importantes
- El proyecto no está inicializado como repositorio Git
- Las tipificaciones son cargadas manualmente por agentes (posible margen de error)
- Los datos son sensibles al rendimiento del call center
- La app maneja fallback con datos de ejemplo si no encuentra el CSV

---
*Archivo creado para mantener contexto entre sesiones de Claude Code*