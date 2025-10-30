"""
MOTOR DE INFERENCIA - CLIPS
============================
Este módulo contiene el motor de inferencia del sistema experto.

Cumple con los requisitos del TEMA 09: Uso exclusivo de CLIPS
Cumple con estructura del PDF: /engine contiene el razonador

Componentes:
- inferencia.py: Motor CLIPS que ejecuta las reglas y gestiona la visualización (D'Alessandro)
- procesador_hechos.py: Transforma datos brutos del entorno en hechos estructurados para CLIPS (Bruno)

El conocimiento (reglas CLIPS, templates y ontología) está en /knowledge/reglas_clips.py

Características:
- Encadenamiento hacia adelante
- Sistema de prioridades basado en salience
- Templates estructurados (estado, resultado)
- Visualización avanzada con Streamlit
- Procesamiento de hechos con clasificación automática
"""

from .inferencia import (
    ejecutar_inferencia,
    procesar_inferencia_completa,
    mostrar_resultado,
    obtener_icono_modo,
    generar_recomendaciones
)

from .procesador_hechos import (
    generar_hechos,
    explicar_hechos
)

__all__ = [
    'ejecutar_inferencia',
    'procesar_inferencia_completa',
    'mostrar_resultado',
    'obtener_icono_modo',
    'generar_recomendaciones',
    'generar_hechos',
    'explicar_hechos'
]

