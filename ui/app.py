"""
Termostato Inteligente - Sistema Experto
Archivo principal de integración y despliegue con Streamlit
Responsable: Daniel
"""

import streamlit as st
from datetime import datetime

# Importación de módulos
from knowledge.datos import obtener_datos
from engine.procesador_hechos import generar_hechos, explicar_hechos
from engine.inferencia import procesar_inferencia_completa, mostrar_resultado

# Configuración de la página
st.set_page_config(
    page_title="Termostato Inteligente",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inicializar_sesion():
    """Inicializa variables de sesión de Streamlit."""
    if 'datos_actuales' not in st.session_state:
        st.session_state.datos_actuales = None
    if 'modo_actual' not in st.session_state:
        st.session_state.modo_actual = None
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    if 'explicacion_actual' not in st.session_state:
        st.session_state.explicacion_actual = []
    if 'resultado_inferencia' not in st.session_state:
        st.session_state.resultado_inferencia = None


def ejecutar_sistema_experto(datos):
    """
    Ejecuta el sistema experto usando CLIPS para la inferencia.
    
    Proceso completo de razonamiento:
    1. Recibe datos del entorno (Módulo de Datos)
    2. Genera hechos estructurados (Procesador de Hechos)
    3. Ejecuta inferencia con motor CLIPS (Motor de Inferencia)
    4. Retorna el modo del termostato con explicación detallada
    
    Args:
        datos: Diccionario con datos del entorno que incluye:
               - temperatura: float (en grados Celsius)
               - ocupada: bool (presencia de personas)
               - hora: int (0-23)
               - dia_semana: str (nombre del día)
               - estacion: str (estación del año)
        
    Returns:
        dict: Resultado completo con:
              - modo: str (CALOR, FRIO, ECO, APAGADO)
              - explicacion: list (pasos del razonamiento)
              - resultado_completo: dict (información detallada del motor CLIPS)
              - hechos_struct: dict (hechos generados para la inferencia)
    """
    # Paso 1 - Generar hechos desde los datos
    hechos_struct = generar_hechos(datos)
    
    # Paso 2 - Ejecutar inferencia con CLIPS
    resultado_clips = procesar_inferencia_completa(hechos_struct, datos)
    
    # Paso 3 - Crear explicación combinada
    explicacion_hechos = explicar_hechos(hechos_struct)
    explicacion_final = (
        explicacion_hechos + 
        ["", "**Motor de Inferencia CLIPS:**"] + 
        resultado_clips["reglas_disparadas"]
    )
    
    return {
        "modo": resultado_clips["modo"],
        "explicacion": explicacion_final,
        "resultado_completo": resultado_clips,
        "hechos_struct": hechos_struct
    }


def main():
    """Función principal que construye la interfaz de Streamlit."""
    
    inicializar_sesion()
    st.title("🌡️ Termostato Inteligente - Sistema Experto")
    st.markdown("""
    ### Bienvenido al Sistema Experto de Control de Temperatura
    
    Este sistema utiliza **inteligencia artificial basada en reglas** para tomar decisiones 
    inteligentes sobre el control de temperatura en tu hogar u oficina.
    
    **¿Cómo funciona?**
    
    El sistema sigue un proceso de razonamiento lógico en 4 etapas:
    
    1. **📊 Captura de datos**: Recolecta información del entorno (temperatura, ocupación, hora)
    2. **📝 Generación de hechos**: Transforma los datos en hechos estructurados que el sistema puede entender
    3. **🧠 Motor de inferencia CLIPS**: Aplica reglas lógicas para razonar y tomar una decisión
    4. **🎯 Recomendación**: Determina el modo óptimo del termostato y explica su razonamiento
    
    **Tecnologías utilizadas:**
    - **CLIPS (C Language Integrated Production System)**: Motor de inferencia profesional utilizado en sistemas expertos
    - **Streamlit**: Framework para crear interfaces web interactivas
    - **Python**: Lenguaje de programación que integra todos los componentes
    """)
    
    st.divider()
    
    with st.sidebar:
        st.header("⚙️ Panel de Control")
        
        # Información del motor de inferencia
        st.subheader("Motor de Inferencia")
        st.success("🧠 **CLIPS** - Encadenamiento hacia adelante")
        st.markdown("""
        **¿Qué es CLIPS?**
        
        CLIPS es un motor de inferencia que utiliza **encadenamiento hacia adelante** 
        (forward chaining) para razonar. Esto significa que:
        
        - Parte de los **hechos conocidos** (temperatura, ocupación, hora)
        - Evalúa las **reglas** definidas en la base de conocimiento
        - **Deduce conclusiones** automáticamente
        - Determina la **mejor acción** a tomar
        
        Es como tener un experto que analiza la situación y toma decisiones por ti.
        """)
        
        st.divider()
        
        # Botón para obtener/actualizar datos
        if st.button("🔄 Actualizar Datos", use_container_width=True, type="primary"):
            with st.spinner("Obteniendo datos del entorno..."):
                st.session_state.datos_actuales = obtener_datos()
                st.success("✅ Datos actualizados")
        
        # Control manual de ocupación
        st.divider()
        st.subheader("👥 Control de Ocupación")
        st.caption("Ajusta manualmente si hay personas en la habitación")
        
        if st.session_state.datos_actuales:
            ocupada = st.checkbox(
                "¿Habitación ocupada?", 
                value=st.session_state.datos_actuales.get('ocupada', True),
                help="Activa si hay personas en la habitación. Esto afecta las decisiones del sistema."
            )
            st.session_state.datos_actuales["ocupada"] = ocupada
            
            if ocupada:
                st.success("✅ Habitación ocupada - El sistema priorizará el confort")
            else:
                st.warning("⚠️ Habitación desocupada - El sistema priorizará el ahorro de energía")
        
        st.divider()
        
        # Información del sistema
        st.subheader("ℹ️ Arquitectura del Sistema")
        st.info("""
        **Módulos integrados:**
        
        - 📊 **Módulo de Datos**: Obtiene información en tiempo real del entorno (temperatura, ocupación, hora)
        
        - 📝 **Procesador de Hechos**: Transforma datos brutos en hechos estructurados que el motor puede procesar
        
        - 🧠 **Motor CLIPS**: Evalúa reglas y ejecuta el razonamiento lógico para determinar el modo óptimo
        
        - 🖥️ **Interfaz Streamlit**: Presenta los resultados de forma visual e interactiva
        
        **Flujo de datos:**
        ```
        Sensores → Datos → Hechos → Motor CLIPS → Decisión → Usuario
        ```
        """)
        
        # Modo manual (opcional)
        st.divider()
        st.subheader("🎛️ Modo Manual (Opcional)")
        st.caption("Simula diferentes escenarios sin necesidad de sensores reales")
        
        modo_manual = st.checkbox("Activar entrada manual de datos")
        
        if modo_manual:
            st.markdown("""
            **💡 Modo de prueba activado**
            
            Usa este modo para:
            - Probar diferentes escenarios
            - Entender cómo el sistema toma decisiones
            - Experimentar sin hardware físico
            """)
            
            temp_manual = st.slider("Temperatura (°C)", 0, 40, 22, 
                                   help="Ajusta la temperatura para ver cómo el sistema responde")
            ocupada_manual = st.checkbox("Habitación ocupada (manual)", value=True,
                                        help="Indica si hay personas presentes")
            hora_manual = st.slider("Hora del día", 0, 23, datetime.now().hour, 
                                   help="Simula diferentes momentos del día")
            
            if st.button("✔️ Aplicar datos manuales", use_container_width=True):
                st.session_state.datos_actuales = {
                    'temperatura': temp_manual,
                    'ocupada': ocupada_manual,
                    'hora': hora_manual,
                    'dia_semana': datetime.now().strftime("%A"),
                    'estacion': 'Invierno'  # Puedes hacerlo dinámico
                }
                st.success("✅ Datos manuales aplicados correctamente")
    
    st.header("📊 Datos Actuales del Entorno")
    
    if st.session_state.datos_actuales is None:
        st.warning("⚠️ No hay datos disponibles. Presiona '🔄 Actualizar Datos' en el panel lateral.")
        st.info("""
        **💡 Para comenzar:**
        
        1. Haz clic en **'🔄 Actualizar Datos'** en el panel lateral para obtener datos reales
        2. O activa el **'Modo Manual'** para simular escenarios de prueba
        3. Una vez tengas los datos, podrás ejecutar el sistema experto
        
        **¿Qué datos necesita el sistema?**
        
        - **Temperatura**: Lectura actual del ambiente en grados Celsius
        - **Ocupación**: Si hay personas presentes en la habitación
        - **Hora**: Momento del día para considerar horarios de descanso
        - **Contexto**: Día de la semana y estación del año
        """)
    else:
        datos = st.session_state.datos_actuales
        
        # Mostrar datos en columnas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Determinar delta si hay temperatura anterior
            delta = None
            if len(st.session_state.historial) > 0:
                temp_anterior = st.session_state.historial[-1]['datos'].get('temperatura')
                if temp_anterior:
                    delta = round(datos['temperatura'] - temp_anterior, 1)
            
            st.metric(
                label="🌡️ Temperatura",
                value=f"{datos['temperatura']}°C",
                delta=f"{delta}°C" if delta else None
            )
        
        with col2:
            st.metric(
                label="👥 Ocupación",
                value="Sí" if datos['ocupada'] else "No"
            )
        
        with col3:
            st.metric(
                label="🕐 Hora",
                value=f"{datos['hora']}:00"
            )
        
        with col4:
            st.metric(
                label="📅 Día",
                value=datos.get('dia_semana', 'N/A')
            )
        
        # Información adicional
        with st.expander("ℹ️ Ver detalles adicionales"):
            st.write(f"**Estación del año:** {datos.get('estacion', 'N/A')}")
            st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.divider()
        
        st.header("🚀 Motor de Inferencia")
        
        st.markdown("""
        **¿Listo para analizar?**
        
        El sistema experto analizará los datos actuales y determinará el modo óptimo del termostato.
        Durante el proceso:
        
        - ✅ Se generarán **hechos** a partir de los datos brutos
        - ✅ Se evaluarán las **reglas** definidas en la base de conocimiento
        - ✅ Se aplicará **razonamiento lógico** usando CLIPS
        - ✅ Se determinará la **mejor acción** a tomar
        - ✅ Se explicará **cómo se llegó** a esa conclusión
        
        Haz clic en el botón para ejecutar el análisis:
        """)
        
        col_btn1, col_btn2 = st.columns([3, 1])
        
        with col_btn1:
            btn_ejecutar = st.button(
                "▶️ Ejecutar Sistema Experto", 
                type="primary", 
                use_container_width=True,
                help="Ejecuta el motor de inferencia CLIPS para analizar los datos"
            )
        
        with col_btn2:
            btn_limpiar = st.button(
                "🗑️ Limpiar",
                use_container_width=True,
                help="Limpia los resultados actuales"
            )
        
        if btn_limpiar:
            st.session_state.modo_actual = None
            st.session_state.explicacion_actual = []
            st.session_state.resultado_inferencia = None
            st.rerun()
        
        if btn_ejecutar:
            with st.spinner("⏳ Ejecutando motor de inferencia CLIPS..."):
                try:
                    # Mostrar progreso
                    progress_text = st.empty()
                    progress_text.text("📊 Analizando datos del entorno...")
                    
                    # Ejecutar sistema experto con CLIPS
                    resultado = ejecutar_sistema_experto(datos)
                    
                    progress_text.text("🧠 Aplicando reglas de inferencia...")
                    
                    # Guardar en sesión
                    st.session_state.modo_actual = resultado["modo"]
                    st.session_state.explicacion_actual = resultado["explicacion"]
                    st.session_state.resultado_inferencia = resultado["resultado_completo"]
                    
                    # Agregar al historial
                    st.session_state.historial.append({
                        'timestamp': datetime.now(),
                        'datos': datos.copy(),
                        'modo': resultado["modo"],
                        'motor': 'CLIPS'
                    })
                    
                    progress_text.empty()
                    st.success("✅ ¡Análisis completado! El sistema ha determinado el modo óptimo del termostato.")
                    
                except Exception as e:
                    st.error(f"❌ Error al ejecutar el sistema experto: {str(e)}")
                    st.exception(e)
                    st.info("""
                    **¿Qué hacer?**
                    - Verifica que los datos estén correctamente cargados
                    - Intenta actualizar los datos nuevamente
                    - Si el problema persiste, revisa la configuración del sistema
                    """)
        
        if st.session_state.modo_actual and st.session_state.resultado_inferencia:
            st.divider()
            
            st.markdown("""
            ### 📋 Resultados del Análisis
            
            El sistema experto ha completado su análisis. A continuación verás:
            
            - **🎯 Modo recomendado**: La decisión del sistema basada en las reglas de inferencia
            - **🧠 Explicación del razonamiento**: Cómo el motor CLIPS llegó a esta conclusión
            - **💡 Recomendaciones adicionales**: Consejos prácticos para optimizar el confort y el ahorro energético
            - **📊 Métricas del sistema**: Indicadores de eficiencia y confort
            """)
            
            # Usar la función de visualización de D'Alessandro (CLIPS)
            mostrar_resultado(
                st.session_state.modo_actual,
                datos,
                st.session_state.resultado_inferencia
            )
        
        if st.session_state.historial:
            st.divider()
            st.header("📜 Historial de Ejecuciones")
            
            st.markdown("""
            **Registro de análisis previos**
            
            Este historial te permite:
            - Ver el comportamiento del sistema a lo largo del tiempo
            - Identificar patrones en las decisiones del termostato
            - Analizar qué modos se utilizan con más frecuencia
            - Evaluar la coherencia de las recomendaciones
            """)
            
            # Estadísticas del historial
            total_ejecuciones = len(st.session_state.historial)
            modos_usados = {}
            for registro in st.session_state.historial:
                modo = registro['modo']
                modos_usados[modo] = modos_usados.get(modo, 0) + 1
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de ejecuciones", total_ejecuciones,
                         help="Número total de veces que se ha ejecutado el sistema")
            with col2:
                if modos_usados:
                    modo_mas_comun = max(modos_usados, key=lambda k: modos_usados[k])
                    st.metric("Modo más usado", modo_mas_comun,
                             help="El modo que más veces ha sido recomendado")
                else:
                    st.metric("Modo más usado", "N/A")
            with col3:
                st.metric("Modos diferentes", len(modos_usados),
                         help="Variedad de modos que el sistema ha recomendado")
            
            # Mostrar historial
            with st.expander(f"📊 Ver historial completo ({total_ejecuciones} registros)", expanded=False):
                st.caption("Mostrando los últimos 10 análisis realizados (más recientes primero)")
                
                # Mostrar últimos 10 registros
                for idx, registro in enumerate(reversed(st.session_state.historial[-10:]), 1):
                    motor = registro.get('motor', 'N/A')
                    st.markdown(f"""
                    **Análisis #{idx}** - {registro['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}
                    
                    - 🌡️ **Temperatura**: {registro['datos']['temperatura']}°C
                    - 👥 **Ocupación**: {'Sí - Habitación ocupada' if registro['datos']['ocupada'] else 'No - Habitación vacía'}
                    - 🕐 **Hora**: {registro['datos'].get('hora', 'N/A')}:00
                    - 🎯 **Modo recomendado**: {registro['modo']}
                    - 🧠 **Motor**: {motor}
                    """)
                    st.divider()
                
                # Botón para limpiar historial
                if st.button("🗑️ Limpiar historial", use_container_width=True):
                    st.session_state.historial = []
                    st.success("✅ Historial limpiado")
                    st.rerun()


if __name__ == "__main__":
    main()