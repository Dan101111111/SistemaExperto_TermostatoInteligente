"""Tests para módulo de datos."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from knowledge.datos import obtener_datos


def test_obtener_datos_estructura():
    """Verifica estructura correcta del diccionario."""
    datos = obtener_datos()
    assert isinstance(datos, dict)
    assert "temperatura" in datos
    assert "hora" in datos
    assert "dia_semana" in datos
    assert "estacion" in datos


def test_obtener_datos_tipos():
    """Verifica tipos de datos correctos."""
    datos = obtener_datos()
    assert isinstance(datos["temperatura"], (int, float))
    assert isinstance(datos["hora"], int)
    assert isinstance(datos["dia_semana"], str)
    assert isinstance(datos["estacion"], str)


def test_obtener_datos_rangos():
    """Verifica rangos válidos de valores."""
    datos = obtener_datos()
    assert 0 <= datos["hora"] <= 23
    assert -50 <= datos["temperatura"] <= 60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

