"""
Motor de inferencia CLIPS y visualización de resultados.
Responsable: D'Alessandro
"""

from typing import Dict, Any, List
import clips
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from knowledge.reglas_clips import (
    TEMPLATE_ESTADO,
    TEMPLATE_RESULTADO,
    TODAS_LAS_REGLAS,
    obtener_info_modo
)

# Importar Streamlit si está disponible
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    # Mock para pruebas sin Streamlit
    class MockSt:
        def markdown(self, *args, **kwargs): pass
        def info(self, *args, **kwargs): pass
        def warning(self, *args, **kwargs): pass
        def expander(self, *args, **kwargs):
            class MockExpander:
                def __enter__(self): return self
                def __exit__(self, *args): pass
            return MockExpander()
        def columns(self, *args): return [MockSt()] * (args[0] if args else 3)
        def metric(self, *args, **kwargs): pass
    st = MockSt()


def inicializar_clips():
    """Inicializa CLIPS y carga templates y reglas."""
    env = clips.Environment()
    env.build(TEMPLATE_ESTADO)
    env.build(TEMPLATE_RESULTADO)
    
    for regla in TODAS_LAS_REGLAS:
        env.build(regla)
    
    return env


def ejecutar_inferencia(hechos_struct: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta motor CLIPS con los hechos proporcionados.
    Retorna el modo decidido, razón y prioridad.
    """
    env = inicializar_clips()
    
    meta = hechos_struct.get("meta", {})
    temperatura = float(meta.get("temperatura", 22.0))
    ocupada = meta.get("ocupada", True)
    hora = int(meta.get("hora", 12))
    
    # Extraer categorías de los tags
    tags = hechos_struct.get("tags", [])
    categoria_temp = "temperatura_confortable"
    horario = "horario_dia"
    
    for tag in tags:
        if "temperatura_" in tag:
            categoria_temp = tag
        if "horario_" in tag:
            horario = tag
    
    estado_template = env.find_template("estado")
    # Crear hecho de estado
    slots_data = {
        'temperatura': temperatura,
        'ocupada': clips.Symbol("TRUE" if ocupada else "FALSE"),
        'hora': hora,
        'categoria-temp': clips.Symbol(categoria_temp),
        'horario': clips.Symbol(horario)
    }
    estado_template.assert_fact(**slots_data)
    
    # Ejecutar inferencia
    env.run()
    
    # Obtener resultados
    resultados = []
    resultado_template = env.find_template("resultado")
    
    for fact in resultado_template.facts():
        resultados.append({
            "modo": str(fact["modo"]),
            "razon": str(fact["razon"]),
            "prioridad": int(fact["prioridad"])
        })
    
    # Seleccionar resultado con mayor prioridad
    if resultados:
        resultado_final = max(resultados, key=lambda x: x["prioridad"])
    else:
        resultado_final = {
            "modo": "ECO",
            "razon": "Modo por defecto",
            "prioridad": 0
        }
    return {
        "modo": resultado_final["modo"],
        "razon": resultado_final["razon"],
        "prioridad": resultado_final["prioridad"],
        "hechos_evaluados": [
            f"Temperatura: {temperatura}°C ({categoria_temp})",
            f"Ocupación: {'Sí' if ocupada else 'No'}",
            f"Hora: {hora}:00 ({horario})"
        ],
        "reglas_disparadas": [f"Regla activada: {resultado_final['razon']}"]
    }


def obtener_icono_modo(modo: str) -> str:
    """Retorna emoji del modo."""
    iconos = {
        'CALOR': '🔥',
        'FRIO': '❄️',
        'ECO': '🌱',
        'APAGADO': '⚫',
        'VENTILACION': '💨'
    }
    return iconos.get(modo.upper(), '⚙️')


def obtener_color_modo(modo: str) -> str:
    """Retorna color del modo."""
    colores = {
        'CALOR': '#ff6b6b',
        'FRIO': '#4dabf7',
        'ECO': '#51cf66',
        'APAGADO': '#868e96',
        'VENTILACION': '#74c0fc'
    }
    return colores.get(modo.upper(), '#868e96')


def generar_recomendaciones(modo: str, datos: Dict[str, Any]) -> List[str]:
    """Genera recomendaciones según el modo y datos actuales."""
    recomendaciones = []
    temperatura = datos.get('temperatura', 22)
    ocupada = datos.get('ocupada', True)
    hora = datos.get('hora', 12)
    
    if modo == 'CALOR':
        recomendaciones.append("💡 Cierra puertas y ventanas para conservar el calor")
        recomendaciones.append("🪟 Asegúrate de que no haya corrientes de aire")
        if temperatura < 15:
            recomendaciones.append("⚠️ Temperatura muy baja, considera usar ropa abrigada")
    
    elif modo == 'FRIO':
        recomendaciones.append("💡 Ventila la habitación durante las horas más frescas")
        recomendaciones.append("🪟 Cierra cortinas durante el día para bloquear el sol")
        if temperatura > 30:
            recomendaciones.append("⚠️ Temperatura muy alta, mantente hidratado")
    
    elif modo == 'ECO':
        recomendaciones.append("✅ Modo eficiente activado - ahorro de energía")
        recomendaciones.append("🌍 Contribuyes a reducir el consumo energético")
        if not ocupada:
            recomendaciones.append("💤 Sistema en espera por falta de ocupación")
    
    elif modo == 'APAGADO':
        recomendaciones.append("🌙 Sistema apagado - horario de descanso")
        recomendaciones.append("💰 Máximo ahorro energético")
    
    return recomendaciones


def mostrar_resultado(modo: str, datos: Dict[str, Any], resultado_inferencia: Dict[str, Any] = None):
    """Muestra resultados en Streamlit."""
    
    icono = obtener_icono_modo(modo)
    color = obtener_color_modo(modo)
    st.markdown("---")
    st.markdown("### 🎯 Resultado del Sistema Experto")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: {color}; 
                    border-radius: 15px; color: white;'>
            <h1 style='margin: 0; font-size: 60px;'>{icono}</h1>
            <h2 style='margin: 10px 0;'>Modo {modo}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    with st.expander("🧠 Ver explicación del razonamiento", expanded=True):
        if resultado_inferencia:
            st.markdown("**Motor de inferencia CLIPS:**")
            st.info(resultado_inferencia.get("razon", "Modo determinado por motor CLIPS"))
            
            st.markdown("**Hechos evaluados:**")
            for hecho in resultado_inferencia.get("hechos_evaluados", []):
                st.markdown(f"- {hecho}")
            
            st.markdown("**Reglas disparadas:**")
            for regla in resultado_inferencia.get("reglas_disparadas", []):
                st.markdown(f"- {regla}")
        else:
            st.markdown("Inferencia realizada basándose en temperatura, ocupación y horario")
    
    recomendaciones = generar_recomendaciones(modo, datos)
    if recomendaciones:
        st.markdown("### 💡 Recomendaciones")
        for rec in recomendaciones:
            st.markdown(f"- {rec}")
    
    st.markdown("---")
    st.warning("""
    ⚠️ **Aviso importante:** Este sistema experto es una herramienta de asistencia. 
    Las decisiones finales sobre el control de temperatura deben considerar el confort 
    personal y las condiciones específicas del entorno. No reemplaza el criterio humano.
    """)
    st.markdown("### 📊 Métricas del sistema")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        eficiencia = "Alta" if modo in ["ECO", "APAGADO"] else "Media"
        st.metric("Eficiencia energética", eficiencia)
    
    with col2:
        confort = "Óptimo" if modo in ["CALOR", "FRIO", "ECO"] else "Bajo"
        st.metric("Nivel de confort", confort)
    
    with col3:
        if resultado_inferencia:
            st.metric("Prioridad de acción", resultado_inferencia.get("prioridad", "N/A"))
        else:
            st.metric("Estado", "Activo")


def procesar_inferencia_completa(hechos_struct: Dict[str, Any], datos: Dict[str, Any]) -> Dict[str, Any]:
    """Ejecuta inferencia CLIPS y prepara resultado completo."""
    resultado = ejecutar_inferencia(hechos_struct)
    return {
        "modo": resultado["modo"],
        "razon": resultado["razon"],
        "prioridad": resultado["prioridad"],
        "hechos_evaluados": resultado["hechos_evaluados"],
        "reglas_disparadas": resultado["reglas_disparadas"],
        "datos_originales": datos,
        "hechos_struct": hechos_struct
    }


if __name__ == "__main__":
    print("PRUEBA LOCAL DEL MÓDULO DE INFERENCIA (CLIPS)")
    
    # Simular hechos de prueba
    hechos_prueba = {
        "hechos": [
            {"clave": "temperatura", "valor": 17.0},
            {"clave": "ocupada", "valor": True},
            {"clave": "hora", "valor": 10}
        ],
        "tags": ["temperatura_baja", "habitacion_ocupada", "horario_dia"],
        "meta": {
            "temperatura": 17.0,
            "hora": 10,
            "ocupada": True,
            "dia_semana": "Lunes",
            "estacion": "Invierno"
        }
    }
    
    # Ejecutar inferencia
    resultado = ejecutar_inferencia(hechos_prueba)
    
    print("\n📊 RESULTADO DE LA INFERENCIA:")
    print(f"  Modo: {resultado['modo']}")
    print(f"  Razón: {resultado['razon']}")
    print(f"  Prioridad: {resultado['prioridad']}")
    
    print("\n🔍 HECHOS EVALUADOS:")
    for hecho in resultado["hechos_evaluados"]:
        print(f"  - {hecho}")
    
    print("\n⚙️ REGLAS DISPARADAS:")
    for regla in resultado["reglas_disparadas"]:
        print(f"  - {regla}")
    
    print("\n" + "=" * 60)
    print("✅ Prueba completada exitosamente")
    print("=" * 60)