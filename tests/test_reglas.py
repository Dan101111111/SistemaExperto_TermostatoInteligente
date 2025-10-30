"""Tests para base de conocimiento (reglas CLIPS)."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from knowledge.reglas_clips import (
    TODAS_LAS_REGLAS,
    MODOS_TERMOSTATO,
    CATEGORIAS_TEMPERATURA,
    clasificar_temperatura,
    clasificar_horario,
    obtener_info_modo
)


def test_reglas_definidas():
    """Verifica que reglas estén correctamente definidas."""
    assert len(TODAS_LAS_REGLAS) == 5
    for regla in TODAS_LAS_REGLAS:
        assert isinstance(regla, str)
        assert "defrule" in regla
        assert "=>" in regla


def test_modos_termostato_completos():
    """Verifica que todos los modos estén definidos."""
    modos_esperados = ['CALOR', 'FRIO', 'ECO', 'APAGADO']
    for modo in modos_esperados:
        assert modo in MODOS_TERMOSTATO
        info = MODOS_TERMOSTATO[modo]
        assert 'icono' in info
        assert 'descripcion' in info


def test_clasificacion_temperatura():
    """Verifica clasificación de temperatura."""
    assert clasificar_temperatura(15.0) == "temperatura_baja"
    assert clasificar_temperatura(22.0) == "temperatura_confortable"
    assert clasificar_temperatura(30.0) == "temperatura_alta"
    assert clasificar_temperatura(19.9) == "temperatura_baja"
    assert clasificar_temperatura(20.0) == "temperatura_confortable"
    assert clasificar_temperatura(24.0) == "temperatura_confortable"
    assert clasificar_temperatura(24.1) == "temperatura_alta"


def test_clasificacion_horario():
    """Verifica clasificación de horario."""
    assert clasificar_horario(10) == "horario_dia"
    assert clasificar_horario(15) == "horario_dia"
    assert clasificar_horario(23) == "horario_noche"
    assert clasificar_horario(3) == "horario_noche"
    assert clasificar_horario(6) == "horario_dia"
    assert clasificar_horario(21) == "horario_dia"
    assert clasificar_horario(22) == "horario_noche"
    assert clasificar_horario(5) == "horario_noche"


def test_obtener_info_modo():
    """Verifica obtención de información de modos."""
    info_calor = obtener_info_modo("CALOR")
    assert info_calor is not None
    assert info_calor['icono'] == '🔥'
    
    info_eco = obtener_info_modo("ECO")
    assert info_eco['consumo_energetico'] == 'bajo'


def test_categorias_temperatura_definidas():
    """Verifica que categorías estén completas."""
    assert 'temperatura_baja' in CATEGORIAS_TEMPERATURA
    assert 'temperatura_confortable' in CATEGORIAS_TEMPERATURA
    assert 'temperatura_alta' in CATEGORIAS_TEMPERATURA
    
    for cat, info in CATEGORIAS_TEMPERATURA.items():
        assert 'rango' in info
        assert 'descripcion' in info
        assert 'accion_recomendada' in info


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

