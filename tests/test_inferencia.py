"""Tests para motor de inferencia CLIPS."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.procesador_hechos import generar_hechos
from engine.inferencia import ejecutar_inferencia


def test_inferencia_modo_calor():
    """Test inferencia: modo CALOR con temp baja y ocupación."""
    datos = {"temperatura": 16.0, "ocupada": True, "hora": 10}
    hechos = generar_hechos(datos)
    resultado = ejecutar_inferencia(hechos)
    assert resultado["modo"] == "CALOR"
    assert resultado["prioridad"] == 10
    assert "temperatura baja" in resultado["razon"].lower()
    assert len(resultado["hechos_evaluados"]) > 0


def test_inferencia_modo_frio():
    """Test inferencia: modo FRIO con temp alta y ocupación."""
    datos = {"temperatura": 30.0, "ocupada": True, "hora": 14}
    hechos = generar_hechos(datos)
    resultado = ejecutar_inferencia(hechos)
    assert resultado["modo"] == "FRIO"
    assert resultado["prioridad"] == 10
    assert "temperatura alta" in resultado["razon"].lower()


def test_inferencia_modo_eco_desocupada():
    """Test inferencia: modo ECO con desocupación."""
    datos = {"temperatura": 22.0, "ocupada": False, "hora": 14}
    hechos = generar_hechos(datos)
    resultado = ejecutar_inferencia(hechos)
    assert resultado["modo"] == "ECO"
    assert resultado["prioridad"] == 9
    assert "desocupada" in resultado["razon"].lower()


def test_inferencia_modo_eco_confortable():
    """Test inferencia: modo ECO con temperatura confortable."""
    datos = {"temperatura": 22.0, "ocupada": True, "hora": 10}
    hechos = generar_hechos(datos)
    resultado = ejecutar_inferencia(hechos)
    assert resultado["modo"] == "ECO"
    assert resultado["prioridad"] == 8
    assert "confortable" in resultado["razon"].lower()


def test_inferencia_modo_apagado():
    """Test inferencia: modo APAGADO en horario nocturno."""
    datos = {"temperatura": 22.0, "ocupada": False, "hora": 23}
    hechos = generar_hechos(datos)
    resultado = ejecutar_inferencia(hechos)
    assert resultado["modo"] == "APAGADO"
    assert resultado["prioridad"] == 11
    assert "nocturno" in resultado["razon"].lower()


def test_caso_borde_temperatura_limite():
    """Caso borde: temperaturas en límites de categorías."""
    datos_limite = {"temperatura": 19.9, "ocupada": True, "hora": 10}
    hechos = generar_hechos(datos_limite)
    resultado = ejecutar_inferencia(hechos)
    assert resultado["modo"] == "CALOR"
    
    datos_confort = {"temperatura": 20.0, "ocupada": True, "hora": 10}
    hechos_confort = generar_hechos(datos_confort)
    resultado_confort = ejecutar_inferencia(hechos_confort)
    assert resultado_confort["modo"] == "ECO"


def test_caso_borde_cambio_horario():
    """Caso borde: transición día/noche a las 22:00."""
    datos_dia = {"temperatura": 22.0, "ocupada": False, "hora": 21}
    hechos_dia = generar_hechos(datos_dia)
    resultado_dia = ejecutar_inferencia(hechos_dia)
    assert resultado_dia["modo"] == "ECO"
    assert resultado_dia["prioridad"] == 9
    
    datos_noche = {"temperatura": 22.0, "ocupada": False, "hora": 22}
    hechos_noche = generar_hechos(datos_noche)
    resultado_noche = ejecutar_inferencia(hechos_noche)
    assert resultado_noche["modo"] == "APAGADO"
    assert resultado_noche["prioridad"] == 11


def test_explicacion_razonamiento():
    """Test de explicación y trazabilidad."""
    datos = {"temperatura": 17.0, "ocupada": True, "hora": 10}
    hechos = generar_hechos(datos)
    resultado = ejecutar_inferencia(hechos)
    
    assert "razon" in resultado
    assert len(resultado["razon"]) > 10
    assert "hechos_evaluados" in resultado
    assert len(resultado["hechos_evaluados"]) >= 3
    assert "reglas_disparadas" in resultado
    assert len(resultado["reglas_disparadas"]) > 0


def test_sistema_prioridades():
    """Test de sistema de prioridades entre reglas."""
    datos = {"temperatura": 22.0, "ocupada": False, "hora": 23}
    hechos = generar_hechos(datos)
    resultado = ejecutar_inferencia(hechos)
    assert resultado["modo"] == "APAGADO"
    assert resultado["prioridad"] == 11


def test_consistencia_multiples_ejecuciones():
    """Test de determinismo: misma entrada, misma salida."""
    datos = {"temperatura": 25.0, "ocupada": True, "hora": 15}
    resultados = []
    for _ in range(3):
        hechos = generar_hechos(datos)
        resultado = ejecutar_inferencia(hechos)
        resultados.append(resultado["modo"])
    assert len(set(resultados)) == 1
    assert resultados[0] == "FRIO"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

