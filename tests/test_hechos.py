"""Tests para procesador de hechos."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.procesador_hechos import generar_hechos, explicar_hechos


def test_generar_hechos_basico():
    """Prueba básica de generación de hechos."""
    datos = {
        "temperatura": 22.0,
        "ocupada": True,
        "hora": 14,
        "dia_semana": "Lunes",
        "estacion": "Verano"
    }
    resultado = generar_hechos(datos)
    assert "hechos" in resultado
    assert "tags" in resultado
    assert "meta" in resultado
    assert len(resultado["hechos"]) > 0
    assert len(resultado["tags"]) > 0


def test_generar_hechos_temperatura_baja():
    """Verifica clasificación temperatura baja."""
    datos = {"temperatura": 15.0, "ocupada": True, "hora": 10}
    resultado = generar_hechos(datos)
    assert "temperatura_baja" in resultado["tags"]


def test_generar_hechos_temperatura_alta():
    """Verifica clasificación temperatura alta."""
    datos = {"temperatura": 30.0, "ocupada": True, "hora": 10}
    resultado = generar_hechos(datos)
    assert "temperatura_alta" in resultado["tags"]


def test_generar_hechos_temperatura_confortable():
    """Verifica clasificación temperatura confortable."""
    datos = {"temperatura": 22.0, "ocupada": True, "hora": 10}
    resultado = generar_hechos(datos)
    assert "temperatura_confortable" in resultado["tags"]


def test_generar_hechos_ocupacion():
    """Verifica detección de ocupación."""
    datos_ocupada = {"temperatura": 22.0, "ocupada": True, "hora": 10}
    datos_desocupada = {"temperatura": 22.0, "ocupada": False, "hora": 10}
    resultado_ocupada = generar_hechos(datos_ocupada)
    resultado_desocupada = generar_hechos(datos_desocupada)
    assert "habitacion_ocupada" in resultado_ocupada["tags"]
    assert "habitacion_desocupada" in resultado_desocupada["tags"]


def test_explicar_hechos():
    """Verifica generación de explicación."""
    datos = {"temperatura": 22.0, "ocupada": True, "hora": 14}
    hechos = generar_hechos(datos)
    explicacion = explicar_hechos(hechos)
    assert isinstance(explicacion, list)
    assert len(explicacion) > 0


def test_caso_borde_temperatura_extrema():
    """Caso borde: temperatura extremadamente baja."""
    datos = {"temperatura": -10.0, "ocupada": True, "hora": 10}
    resultado = generar_hechos(datos)
    assert "temperatura_baja" in resultado["tags"]
    assert resultado["meta"]["temperatura"] == -10.0


def test_caso_borde_hora_limite():
    """Caso borde: hora límite día/noche."""
    datos_noche = {"temperatura": 22.0, "ocupada": True, "hora": 22}
    resultado_noche = generar_hechos(datos_noche)
    assert "horario_noche" in resultado_noche["tags"]
    
    datos_dia = {"temperatura": 22.0, "ocupada": True, "hora": 21}
    resultado_dia = generar_hechos(datos_dia)
    assert "horario_dia" in resultado_dia["tags"]


def test_inferencia_ocupacion_sin_sensor():
    """Verifica inferencia de ocupación sin sensor."""
    datos_dia = {"temperatura": 22.0, "hora": 15}
    resultado_dia = generar_hechos(datos_dia)
    assert resultado_dia["meta"]["ocupada"] == True
    
    datos_noche = {"temperatura": 22.0, "hora": 3}
    resultado_noche = generar_hechos(datos_noche)
    assert resultado_noche["meta"]["ocupada"] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

