"""
Procesador de hechos: transforma datos brutos en hechos estructurados para CLIPS.
Responsable: Bruno
"""

from typing import Dict, Any, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from knowledge.reglas_clips import (
    clasificar_temperatura,
    clasificar_horario,
    inferir_ocupacion_por_hora
)


def generar_hechos(datos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforma datos del entorno en hechos que CLIPS puede procesar.
    
    Args:
        datos: {temperatura, hora, ocupada, dia_semana, estacion}
    Returns:
        dict: {hechos, tags, meta}
    """
    temperatura = float(datos.get("temperatura", 25.0))
    hora = int(datos.get("hora", 12))
    dia_semana = datos.get("dia_semana", None)
    estacion = datos.get("estacion", None)
    ocupada = datos.get("ocupada", None)

    # Inferir ocupación si no se proporciona
    if ocupada is None:
        ocupada = inferir_ocupacion_por_hora(hora)

    tags: List[str] = []
    hechos: List[Dict[str, Any]] = []

    # Clasificar temperatura
    temp_tag = clasificar_temperatura(temperatura)
    tags.append(temp_tag)
    hechos.append({"clave": "temperatura", "valor": temperatura})
    hechos.append({"clave": "categoria_temperatura", "valor": temp_tag})

    # Clasificar ocupación
    if ocupada:
        tags.append("habitacion_ocupada")
    else:
        tags.append("habitacion_desocupada")
    hechos.append({"clave": "ocupada", "valor": bool(ocupada)})

    # Clasificar horario
    horario_tag = clasificar_horario(hora)
    tags.append(horario_tag)
    hechos.append({"clave": "hora", "valor": hora})
    hechos.append({"clave": "horario", "valor": horario_tag})

    # Datos adicionales
    if dia_semana:
        hechos.append({"clave": "dia_semana", "valor": dia_semana})
        tags.append(f"dia_{dia_semana.lower()}")
    
    if estacion:
        hechos.append({"clave": "estacion", "valor": estacion})
        tags.append(f"estacion_{estacion.lower()}")

    # Determinar acción recomendada
    if temp_tag == "temperatura_alta" and ocupada:
        necesidad = "enfriar"
    elif temp_tag == "temperatura_baja" and ocupada:
        necesidad = "calentar"
    elif temp_tag == "temperatura_confortable" and ocupada:
        necesidad = "mantener"
    else:
        necesidad = "ahorro"

    hechos.append({"clave": "accion_recomendada", "valor": necesidad})
    tags.append(f"accion_{necesidad}")
    return {
        "hechos": hechos,
        "tags": tags,
        "meta": {
            "temperatura": temperatura,
            "hora": hora,
            "ocupada": ocupada,
            "dia_semana": dia_semana,
            "estacion": estacion
        }
    }


def explicar_hechos(hechos_struct: Dict[str, Any]) -> List[str]:
    """Genera explicación legible de los hechos para el usuario."""
    meta = hechos_struct.get("meta", {})
    
    explicacion = [
        f"🌡️ Temperatura: {meta.get('temperatura')}°C → {clasificar_temperatura(meta.get('temperatura', 0))}",
        f"🕐 Hora: {meta.get('hora')}:00 → {clasificar_horario(meta.get('hora', 0))}",
        f"👥 Ocupación: {'Sí' if meta.get('ocupada') else 'No'}"
    ]

    for h in hechos_struct["hechos"]:
        if h["clave"] == "accion_recomendada":
            explicacion.append(f"💡 Acción sugerida: {h['valor']}")
            break

    return explicacion


if __name__ == "__main__":
    print("PROCESADOR DE HECHOS - DEMO")

    # Caso de prueba
    datos_prueba = {
        "temperatura": 28.3,
        "ocupada": True,
        "hora": 15,
        "dia_semana": "Lunes",
        "estacion": "Verano"
    }

    # Generar hechos
    estructura = generar_hechos(datos_prueba)

    print("\n📊 HECHOS GENERADOS:")
    for h in estructura["hechos"]:
        print(f"  - {h['clave']}: {h['valor']}")

    print("\n🏷️ TAGS:")
    print(f"  {', '.join(estructura['tags'])}")

    print("\n💬 EXPLICACIÓN:")
    for linea in explicar_hechos(estructura):
        print(f"  {linea}")

    print("\n✅ Procesador de hechos funcionando correctamente")
    print("=" * 60)

