"""
BASE DE CONOCIMIENTO
====================
Este módulo contiene el CONOCIMIENTO del dominio del sistema experto.

Cumple con estructura del PDF: /knowledge contiene reglas y parámetros

Componentes:
- reglas_clips.py: Reglas CLIPS, templates, ontología del dominio y funciones de clasificación (Mario)
- datos.py: Obtención de datos del entorno en tiempo real desde API Open-Meteo (Trujillo, Perú) (Igor)

Sistema: CLIPS (cumple requisitos del TEMA 09)
Motor: Encadenamiento hacia adelante con sistema de prioridades
"""

from .datos import obtener_datos
from .reglas_clips import (
    TODAS_LAS_REGLAS,
    MODOS_TERMOSTATO,
    CATEGORIAS_TEMPERATURA,
    CATEGORIAS_HORARIO,
    clasificar_temperatura,
    clasificar_horario,
    obtener_info_modo
)

__all__ = [
    'obtener_datos',
    'TODAS_LAS_REGLAS',
    'MODOS_TERMOSTATO',
    'CATEGORIAS_TEMPERATURA',
    'CATEGORIAS_HORARIO',
    'clasificar_temperatura',
    'clasificar_horario',
    'obtener_info_modo'
]

