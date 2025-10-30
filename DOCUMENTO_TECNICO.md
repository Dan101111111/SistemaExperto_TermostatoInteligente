# 📄 DOCUMENTO TÉCNICO - Termostato Inteligente con Sistema Experto

**Proyecto:** Sistema Experto para Control Automático de Temperatura  
**Curso:** Sistemas Inteligentes  
**Fecha:** Octubre 2025  
**Equipo:** Igor, Bruno, Mario, D'Alessandro, Daniel

---

## 📑 Índice

1. [Problema y Contexto Real](#1-problema-y-contexto-real)
2. [Dominio del Conocimiento](#2-dominio-del-conocimiento)
3. [Representación del Conocimiento](#3-representación-del-conocimiento)
4. [Motor de Inferencia](#4-motor-de-inferencia)
5. [Limitaciones y Riesgos Éticos](#5-limitaciones-y-riesgos-éticos)
6. [Validación de Decisiones](#6-validación-de-decisiones)
7. [Asistencia de Inteligencia Artificial](#7-asistencia-de-inteligencia-artificial)
8. [Estadísticas del Proyecto](#8-estadísticas-del-proyecto)
9. [Transparencia y Responsabilidad](#9-transparencia-y-responsabilidad)
10. [Conclusiones](#10-conclusiones)

---

## 1. Problema y Contexto Real

### 1.1 Contexto

En la actualidad, el consumo energético residencial representa una parte significativa del gasto energético global. Los sistemas HVAC (calefacción, ventilación y aire acondicionado) son responsables de aproximadamente el 40% del consumo energético en hogares. El desafío es lograr un equilibrio entre el confort térmico de los ocupantes y la eficiencia energética.

### 1.2 Problemática Identificada

**Problema principal:** Los termostatos convencionales no consideran múltiples variables contextuales simultáneamente, lo que resulta en:

- ❌ **Desperdicio energético:** Sistema activo cuando la habitación está vacía
- ❌ **Incomodidad:** Temperatura no adecuada cuando hay personas presentes
- ❌ **Falta de optimización:** No considera horarios de uso ni patrones de ocupación
- ❌ **Decisiones reactivas:** Responde solo a temperatura, ignora contexto

### 1.3 Solución Propuesta

Desarrollar un **Sistema Experto basado en reglas** que tome decisiones inteligentes considerando:

- 🌡️ **Temperatura ambiente** (datos en tiempo real vía API)
- 👥 **Ocupación de la habitación** (detectada manualmente o por sensor)
- 🕐 **Hora del día** (para distinguir horarios activos vs descanso)
- 📅 **Contexto temporal** (día de la semana, estación del año)

**Objetivo:** Optimizar el balance entre confort térmico y eficiencia energética mediante razonamiento automatizado.

### 1.4 Justificación del Enfoque con Sistemas Expertos

Un sistema experto es apropiado para este dominio porque:

1. **Conocimiento experto codificable:** Las reglas para control de temperatura son claras y pueden expresarse como "SI-ENTONCES"
2. **Dominio bien definido:** El espacio de decisiones es finito (4 modos del termostato)
3. **Explicabilidad requerida:** Los usuarios necesitan entender por qué el sistema tomó una decisión
4. **Trazabilidad:** Capacidad de auditar cada decisión y su razonamiento

---

## 2. Dominio del Conocimiento

### 2.1 ¿De qué es experto este sistema?

Este sistema es experto en **control automático de climatización residencial**, específicamente en:

- **Decisión de modos de operación** del termostato según condiciones ambientales
- **Optimización de confort vs eficiencia energética**
- **Adaptación a patrones de ocupación** humana
- **Gestión de horarios** (día activo vs noche de descanso)

### 2.2 Conocimiento del Dominio

El sistema encapsula el conocimiento de un experto en HVAC que considera:

**Rangos de Temperatura:**

- **Baja** (< 20°C): Requiere calefacción si hay ocupación
- **Confortable** (20-24°C): Mantener, modo eco
- **Alta** (> 24°C): Requiere aire acondicionado si hay ocupación

**Clasificación de Horarios:**

- **Día** (6:00 - 21:59): Alta probabilidad de ocupación
- **Noche** (22:00 - 5:59): Baja probabilidad de ocupación

**Modos del Termostato:**

- 🔥 **CALOR**: Calefacción activa - Alto consumo, óptimo confort en clima frío
- ❄️ **FRIO**: Aire acondicionado activo - Alto consumo, óptimo confort en clima cálido
- 🌱 **ECO**: Modo eficiente, temperatura mantenida - Bajo consumo, buen confort
- ⚫ **APAGADO**: Sistema desactivado - Sin consumo, sin confort

### 2.3 Criterios de Decisión del Experto

El sistema aplica la siguiente lógica de un experto en HVAC:

- **Máxima prioridad a ahorro nocturno:** Si es de noche y no hay ocupación → APAGADO
- **Prioridad a confort humano:** Si hay personas y hace frío/calor → CALOR/FRIO
- **Ahorro cuando no hay ocupación:** Si está vacía → ECO
- **Mantenimiento cuando es confortable:** Si la temperatura es adecuada → ECO

---

## 3. Representación del Conocimiento

### 3.1 Paradigma Utilizado: Sistema Basado en Reglas

El conocimiento se representa mediante **reglas de producción** en formato:

```
SI <condiciones>
ENTONCES <acción>
```

### 3.2 Motor de Reglas: CLIPS

**Tecnología:** CLIPS (C Language Integrated Production System) versión 6.x via CLIPSPy

**¿Por qué CLIPS?**

- Motor de inferencia probado y maduro (desde 1985)
- Encadenamiento hacia adelante (forward chaining)
- Sistema de prioridades para resolución de conflictos
- Templates para estructurar hechos
- Trazabilidad completa del razonamiento

### 3.3 Templates CLIPS (Estructura de Hechos)

#### Template `estado` (Entrada)

```clips
(deftemplate estado
    (slot temperatura (type FLOAT))
    (slot ocupada (type SYMBOL) (allowed-symbols TRUE FALSE))
    (slot hora (type INTEGER))
    (slot categoria-temp (type SYMBOL))
    (slot horario (type SYMBOL)))
```

**Slots:**

- `temperatura`: Valor numérico en °C
- `ocupada`: Booleano (TRUE/FALSE)
- `hora`: Entero 0-23
- `categoria-temp`: Símbolo (temperatura_baja, temperatura_confortable, temperatura_alta)
- `horario`: Símbolo (horario_dia, horario_noche)

#### Template `resultado` (Salida)

```clips
(deftemplate resultado
    (slot modo (type SYMBOL))
    (slot razon (type STRING))
    (slot prioridad (type INTEGER)))
```

**Slots:**

- `modo`: Símbolo (CALOR, FRIO, ECO, APAGADO)
- `razon`: Explicación textual de la decisión
- `prioridad`: Nivel de importancia (mayor = más prioritario)

### 3.4 Reglas de Producción (Base de Conocimiento)

#### Regla 1: modo-calor (Prioridad 10)

```clips
(defrule modo-calor
    "Activa calefacción cuando hace frío y hay personas"
    (estado (ocupada TRUE) (categoria-temp temperatura_baja))
    =>
    (assert (resultado
        (modo CALOR)
        (razon "Habitación ocupada con temperatura baja")
        (prioridad 10))))
```

**Conocimiento encapsulado:** Si hay personas y hace frío, priorizamos su confort activando calefacción.

#### Regla 2: modo-frio (Prioridad 10)

```clips
(defrule modo-frio
    "Activa aire acondicionado cuando hace calor y hay personas"
    (estado (ocupada TRUE) (categoria-temp temperatura_alta))
    =>
    (assert (resultado
        (modo FRIO)
        (razon "Habitación ocupada con temperatura alta")
        (prioridad 10))))
```

**Conocimiento encapsulado:** Si hay personas y hace calor, priorizamos su confort activando aire acondicionado.

#### Regla 3: modo-eco-desocupada (Prioridad 9)

```clips
(defrule modo-eco-desocupada
    "Modo ahorro cuando no hay personas"
    (estado (ocupada FALSE))
    =>
    (assert (resultado
        (modo ECO)
        (razon "Habitación desocupada - ahorro de energía")
        (prioridad 9))))
```

**Conocimiento encapsulado:** Si no hay personas, priorizamos ahorro energético sobre confort.

#### Regla 4: modo-eco-confortable (Prioridad 8)

```clips
(defrule modo-eco-confortable
    "Mantiene temperatura cuando está en rango confortable"
    (estado (ocupada TRUE) (categoria-temp temperatura_confortable))
    =>
    (assert (resultado
        (modo ECO)
        (razon "Temperatura confortable - ahorro de energía")
        (prioridad 8))))
```

**Conocimiento encapsulado:** Si la temperatura ya es adecuada, no es necesario gastar energía extra.

#### Regla 5: modo-apagado (Prioridad 11 - Máxima)

```clips
(defrule modo-apagado
    "Apaga completamente en horario nocturno sin ocupación"
    (estado (ocupada FALSE) (horario horario_noche))
    =>
    (assert (resultado
        (modo APAGADO)
        (razon "Horario nocturno sin ocupación")
        (prioridad 11))))
```

**Conocimiento encapsulado:** De noche sin ocupación, el máximo ahorro es apagar todo el sistema.

### 3.5 Ontología del Dominio

El sistema define conceptos y relaciones del dominio HVAC:

```python
CATEGORIAS_TEMPERATURA = {
    'temperatura_baja': {
        'rango': '< 20°C',
        'descripcion': 'Temperatura fría que requiere calefacción',
        'accion_recomendada': 'calentar'
    },
    'temperatura_confortable': {
        'rango': '20-24°C',
        'descripcion': 'Temperatura ideal para confort humano',
        'accion_recomendada': 'mantener'
    },
    'temperatura_alta': {
        'rango': '> 24°C',
        'descripcion': 'Temperatura cálida que requiere enfriamiento',
        'accion_recomendada': 'enfriar'
    }
}
```

---

## 4. Motor de Inferencia

### 4.1 Tipo de Encadenamiento

**Método utilizado:** Encadenamiento hacia adelante (Forward Chaining)

**¿Por qué forward chaining?**

1. **Razonamiento dirigido por datos:** Partimos de los datos del entorno (temperatura, ocupación, hora) y deducimos la acción
2. **Procesamiento eficiente:** Todas las reglas se evalúan y se selecciona la de mayor prioridad
3. **Explicabilidad natural:** Es fácil rastrear qué hechos dispararon qué reglas
4. **Adecuado para control:** En sistemas de control, partimos de sensores y decidimos acciones

### 4.2 Proceso de Inferencia Paso a Paso

#### Paso 1: Obtención de Datos (Módulo `knowledge/datos.py`)

```python
datos = {
    'temperatura': 17.5,  # API Open-Meteo (Trujillo, Perú)
    'ocupada': True,      # Input del usuario
    'hora': 10,           # Sistema operativo
    'dia_semana': 'Lunes',
    'estacion': 'Invierno'
}
```

#### Paso 2: Generación de Hechos (Módulo `engine/procesador_hechos.py`)

```python
hechos_struct = generar_hechos(datos)
# Resultado:
{
    "hechos": [
        {"clave": "temperatura", "valor": 17.5},
        {"clave": "categoria_temperatura", "valor": "temperatura_baja"},
        {"clave": "ocupada", "valor": True},
        {"clave": "hora", "valor": 10},
        {"clave": "horario", "valor": "horario_dia"}
    ],
    "tags": ["temperatura_baja", "habitacion_ocupada", "horario_dia"],
    "meta": {...}
}
```

#### Paso 3: Inicialización del Motor CLIPS (Módulo `engine/inferencia.py`)

```python
env = clips.Environment()
env.build(TEMPLATE_ESTADO)
env.build(TEMPLATE_RESULTADO)
for regla in TODAS_LAS_REGLAS:
    env.build(regla)
```

#### Paso 4: Assertion de Hechos en CLIPS

```python
estado_template = env.find_template("estado")
estado_template.assert_fact(
    temperatura=17.5,
    ocupada=clips.Symbol("TRUE"),
    hora=10,
    categoria_temp=clips.Symbol("temperatura_baja"),
    horario=clips.Symbol("horario_dia")
)
```

#### Paso 5: Ejecución del Motor de Inferencia

```python
env.run()  # CLIPS evalúa todas las reglas
```

**En este punto CLIPS:**

1. Evalúa cada regla contra los hechos presentes
2. Identifica qué reglas tienen condiciones satisfechas
3. Dispara las reglas que aplican
4. Assertan nuevos hechos (resultados)

#### Paso 6: Extracción de Resultados

```python
resultados = []
resultado_template = env.find_template("resultado")
for fact in resultado_template.facts():
    resultados.append({
        "modo": str(fact["modo"]),
        "razon": str(fact["razon"]),
        "prioridad": int(fact["prioridad"])
    })
```

#### Paso 7: Resolución de Conflictos por Prioridad

```python
# Si múltiples reglas se dispararon, seleccionar por prioridad
resultado_final = max(resultados, key=lambda x: x["prioridad"])
```

### 4.3 Ejemplo Completo de Inferencia

**Entrada:**

- Temperatura: 17.5°C
- Ocupada: Sí
- Hora: 10:00

**Procesamiento CLIPS:**

```
CLIPS evalúa reglas:
  ✅ modo-calor → Condiciones satisfechas (ocupada=TRUE, temp=temperatura_baja)
  ❌ modo-frio → Condiciones no satisfechas
  ❌ modo-eco-desocupada → Condiciones no satisfechas
  ❌ modo-eco-confortable → Condiciones no satisfechas
  ❌ modo-apagado → Condiciones no satisfechas

CLIPS dispara:
  modo-calor → (assert (resultado (modo CALOR) (razon "...") (prioridad 10)))

Resolución de conflictos:
  Solo 1 resultado → seleccionar directamente
```

**Salida:**

```python
{
    "modo": "CALOR",
    "razon": "Habitación ocupada con temperatura baja",
    "prioridad": 10,
    "hechos_evaluados": [
        "Temperatura: 17.5°C (temperatura_baja)",
        "Ocupación: Sí",
        "Hora: 10:00 (horario_dia)"
    ],
    "reglas_disparadas": [
        "Regla activada: Habitación ocupada con temperatura baja"
    ]
}
```

### 4.4 Sistema de Prioridades

El motor CLIPS resuelve conflictos cuando múltiples reglas se disparan simultáneamente:

- **Prioridad 11** (Máxima): `modo-apagado` - Ahorro nocturno es la máxima prioridad cuando no hay ocupación
- **Prioridad 10** (Alta): `modo-calor` / `modo-frio` - Confort humano tiene alta prioridad
- **Prioridad 9** (Media-Alta): `modo-eco-desocupada` - Ahorro por falta de ocupación
- **Prioridad 8** (Media): `modo-eco-confortable` - Mantenimiento cuando ya es confortable

**Ejemplo de resolución:** Si a las 23:00 la habitación está desocupada, `modo-eco-desocupada` (prioridad 9) y `modo-apagado` (prioridad 11) se disparan. El resultado es `modo-apagado` por mayor prioridad.

---

## 5. Limitaciones y Riesgos Éticos

### 5.1 Limitaciones Técnicas del Sistema

#### 5.1.1 Limitaciones de Sensado

- **Ocupación manual:** El sistema no detecta automáticamente ocupación, requiere input del usuario (impacto bajo - el usuario debe actualizar manualmente)
- **Temperatura de API:** Usa temperatura exterior (API meteorológica), no temperatura interior real (impacto medio - puede no reflejar temperatura exacta de la habitación)
- **Sin sensores de confort:** No mide humedad, velocidad del aire, radiación (impacto medio - confort real puede variar)

**Mitigación actual:** Modo manual permite al usuario ingresar datos simulados.

**Extensión futura:** Integración con sensores DHT22 (temperatura/humedad) y PIR (ocupación).

#### 5.1.2 Limitaciones del Modelo de Conocimiento

**Supuestos simplificados:**

1. **Umbral de temperatura único:** Usa 20°C y 24°C para todos los usuarios

   - **Realidad:** El confort térmico es subjetivo y varía por persona
   - **Riesgo:** Algunos usuarios pueden sentir frío a 20°C, otros calor

2. **Horario nocturno fijo:** Asume 22:00-6:00 como horario de descanso

   - **Realidad:** Horarios de sueño varían (trabajadores nocturnos, etc.)
   - **Riesgo:** Sistema podría apagarse cuando alguien necesita el termostato

3. **Inferencia de ocupación simplificada:** Asume ocupación entre 8:00-22:00
   - **Realidad:** Patrones de ocupación son impredecibles
   - **Riesgo:** Modo ECO cuando debería estar activo, o viceversa

#### 5.1.3 Casos Donde el Sistema NO es Confiable

❌ **No usar en estos escenarios:**

1. **Personas con condiciones médicas sensibles** (ancianos, bebés, personas con hipotermia)
   - El sistema no considera necesidades médicas especiales
2. **Ambientes críticos** (laboratorios, hospitales, data centers)

   - Requieren precisión que excede la capacidad del sistema

3. **Situaciones de emergencia** (olas de calor extremas, clima severo)

   - Las reglas no contemplan escenarios extremos

4. **Usuarios ausentes por periodos largos** (vacaciones)
   - Sin actualización de ocupación, podría desperdiciar energía

### 5.2 Riesgos Éticos

#### 5.2.1 Decisiones Automatizadas sin Supervisión

**Riesgo:** El sistema toma decisiones que afectan el bienestar físico de personas (temperatura corporal, confort).

**Mitigación implementada:**

- ⚠️ **Aviso visible en la interfaz:**  
  "Este sistema experto es una herramienta de asistencia. Las decisiones finales sobre el control de temperatura deben considerar el confort personal y las condiciones específicas del entorno. No reemplaza el criterio humano."

- ✅ **Control manual siempre disponible:** El usuario puede sobrescribir cualquier decisión del sistema.

#### 5.2.2 Privacidad de Datos

**Riesgo:** El sistema registra patrones de ocupación (cuándo hay personas en casa).

**Mitigación implementada:**

- ✅ Historial almacenado solo en sesión local (no persiste entre reinicios)
- ✅ No se envían datos a servidores externos
- ✅ API meteorológica no recibe información del usuario (solo coordenadas de Trujillo, Perú)

**Recomendación para despliegue real:**

- Implementar anonimización de datos de ocupación
- Encriptar historial si se almacena
- Política de retención de datos (borrar logs antiguos)

#### 5.2.3 Sesgo y Discriminación

**Análisis:**

- ✅ **No hay sesgo discriminatorio:** El sistema no usa atributos sensibles (raza, género, edad, religión)
- ✅ Las reglas aplican por igual a todos los usuarios

**Limitación identificada:**

- ⚠️ Umbrales de confort (20-24°C) están basados en estándares ISO para adultos sanos
- Poblaciones especiales (niños, ancianos) pueden tener diferentes necesidades

#### 5.2.4 Responsabilidad y Transparencia

**Pregunta clave:** ¿Quién es responsable si el sistema falla y causa daño?

**Respuesta del proyecto:**

- ✅ **El usuario final es responsable de la decisión final**
- ✅ El sistema solo **asiste**, no **decide automáticamente**
- ✅ Explicabilidad completa: el usuario ve por qué se recomendó cada modo
- ✅ Control manual: el usuario puede ignorar la recomendación

### 5.3 Limitaciones de Escalabilidad

- **Multi-habitación:** Sistema diseñado para 1 habitación. Solución futura: arquitectura distribuida
- **Predicción:** No predice patrones futuros. Solución futura: integración con Machine Learning para forecasting
- **Aprendizaje:** Reglas estáticas, no aprende. Solución futura: sistema híbrido (reglas + aprendizaje adaptativo)
- **Integración IoT:** No se comunica con termostatos reales. Solución futura: API REST para integración con dispositivos

---

## 6. Validación de Decisiones

### 6.1 ¿Quién Valida las Decisiones del Sistema?

**Respuesta:** El **usuario humano** es el validador final y responsable de cada decisión.

### 6.2 Mecanismos de Validación Implementados

#### 6.2.1 Validación en Tiempo Real (Interfaz Streamlit)

La aplicación Streamlit muestra **antes de aplicar** la decisión:

1. **Modo recomendado:** Visualización clara del modo sugerido
2. **Razonamiento completo:**
   - Hechos evaluados (qué "vio" el sistema)
   - Reglas disparadas (qué lógica aplicó)
   - Razón textual (por qué llegó a esa conclusión)
3. **Recomendaciones adicionales:** Consejos prácticos según el modo
4. **Descargo de responsabilidad:** Aviso de que es una herramienta de asistencia

**Ejemplo de visualización:**

```
┌─────────────────────────────────────┐
│   🔥 Modo CALOR                     │
├─────────────────────────────────────┤
│ Razón:                              │
│ "Habitación ocupada con             │
│  temperatura baja"                  │
│                                     │
│ Hechos Evaluados:                   │
│ • Temperatura: 17.5°C (baja)        │
│ • Ocupación: Sí                     │
│ • Hora: 10:00 (día)                 │
│                                     │
│ Recomendaciones:                    │
│ 💡 Cierra puertas y ventanas        │
│ 🪟 Evita corrientes de aire         │
│                                     │
│ ⚠️ AVISO: Este sistema es           │
│ asistencia, la decisión final es   │
│ del usuario.                        │
└─────────────────────────────────────┘
```

El usuario ve esta información y **decide** si:

- ✅ Acepta la recomendación
- ❌ La ignora y usa control manual
- 🔄 Ajusta parámetros y re-ejecuta

#### 6.2.2 Validación Técnica (Pruebas Automatizadas)

**Tests con pytest:**

- ✅ `test_inferencia_modo_calor()` - Valida que CALOR se active correctamente
- ✅ `test_caso_borde_temperatura_limite()` - Valida comportamiento en límites
- ✅ `test_explicacion_razonamiento()` - Valida que hay trazabilidad

**Ejecutar validación:**

```bash
pytest tests/ -v
```

#### 6.2.3 Validación por Experto (Recomendado para Producción)

**Para un despliegue real, se recomienda:**

1. **Validación por experto en HVAC:**

   - Revisar umbrales de temperatura (20°C, 24°C)
   - Validar prioridades de reglas
   - Aprobar lógica de horarios

2. **Validación por usuarios finales:**

   - Beta testing con usuarios reales
   - Ajuste de parámetros según feedback
   - Validación de que las decisiones son aceptables

3. **Auditoría periódica:**
   - Revisar historial de decisiones
   - Detectar patrones incorrectos
   - Ajustar reglas si es necesario

### 6.3 Humano Responsable

**En un entorno de producción:**

- **Usuario final:** Ocupante de la vivienda - Decisión final de activar/desactivar modo
- **Administrador del sistema:** Técnico HVAC o propietario - Configuración de parámetros y umbrales
- **Desarrollador:** Equipo de desarrollo - Mantenimiento de reglas y corrección de bugs
- **Auditor:** Experto en HVAC (externo) - Validación periódica de que las reglas son apropiadas

**Declaración de responsabilidad:**

> "Este sistema experto NO toma decisiones por sí solo. Cada recomendación debe ser evaluada y aprobada por el usuario final. El sistema no se conecta directamente a actuadores de termostatos reales sin intervención humana. En caso de despliegue real, se recomienda una válvula manual de sobrescritura siempre accesible."

---

## 7. Asistencia de Inteligencia Artificial

De acuerdo con las políticas de uso responsable de IA del curso, declaramos explícitamente qué partes del proyecto fueron asistidas por herramientas de inteligencia artificial.

### 7.0 Herramientas de IA Utilizadas

El equipo utilizó las siguientes herramientas de IA para asistir en el desarrollo del proyecto:

**Herramientas principales:**

1. **Cursor AI** (2024)

   - Editor de código con IA integrada
   - Generación de código base y sugerencias
   - Autocompletado inteligente
   - Refactorización asistida

2. **GitHub Copilot** (2024)

   - Asistente de programación de GitHub
   - Sugerencias de código en tiempo real
   - Generación de funciones y bloques de código
   - Ayuda con sintaxis y patrones de código

3. **Claude Sonnet 3.5** (Anthropic, 2024)

   - Asistente de IA conversacional
   - Revisión y mejora de documentación
   - Explicación de conceptos técnicos
   - Validación de lógica de reglas CLIPS
   - Generación de casos de prueba

4. **ChatGPT-4** (OpenAI, 2024)
   - Asistente de IA conversacional
   - Consultas sobre mejores prácticas
   - Debugging y solución de problemas
   - Generación de documentación técnica
   - Revisión de código y sugerencias de mejora

**Uso responsable declarado:**

✅ Todas las herramientas fueron usadas como **asistentes**, no como generadores automáticos  
✅ Todo el código generado fue **revisado, comprendido y modificado** por el equipo  
✅ Las decisiones de diseño y arquitectura fueron **humanas**  
✅ El equipo puede **explicar y justificar** cada línea de código  
✅ No se copió código sin comprender su funcionamiento

### 7.1 Detalle de Asistencia por Módulo

#### 7.1.1 Igor - Adquisición de Datos

**Trabajo realizado por Igor:**

- Definición de estructura de datos de salida
- Integración real con API Open-Meteo para temperatura
- Cálculo de estación del año
- Manejo de timeouts y errores de API
- Coordenadas de Trujillo, Perú para demostración

**Asistencia de IA:**

- **Cursor AI:** Generó estructura básica de la función `obtener_datos()`
- **GitHub Copilot:** Sugirió uso de biblioteca `requests` para HTTP
- **ChatGPT-4:** Proporcionó esqueleto de manejo de excepciones y mejores prácticas para peticiones HTTP

**Modificaciones humanas:**

- Integración completa con API real
- Lógica de cálculo de estación según mes
- Estructura de datos compatible con el resto del sistema
- Ajuste de coordenadas específicas de Trujillo, Perú

#### 7.1.2 Bruno - Procesamiento de Hechos

**Trabajo realizado por Bruno:**

- Diseño de algoritmo de clasificación de temperatura
- Definición de umbrales (20°C, 24°C)
- Clasificación de horarios (día 6-22h, noche 22-6h)
- Inferencia de ocupación cuando no hay sensor
- Generación de estructura de hechos con tags y metadata
- Función de explicación para el usuario

**Asistencia de IA:**

- **Cursor AI:** Generó esqueleto de función `generar_hechos()`
- **GitHub Copilot:** Sugirió uso de listas y diccionarios para estructura de salida
- **Claude Sonnet 3.5:** Proporcionó plantilla básica de función `explicar_hechos()` y validó la lógica de clasificación
- **ChatGPT-4:** Ayudó con la estructura de metadata y sugerencias de mejores prácticas

**Modificaciones humanas:**

- Lógica completa de clasificación y categorización
- Inferencia de ocupación por horario
- Generación de tags semánticos
- Metadata estructurada para CLIPS
- Algoritmos de clasificación personalizados

#### 7.1.3 Mario - Base de Conocimiento

**Trabajo realizado por Mario:**

- Diseño de las 5 reglas CLIPS
- Definición de prioridades de reglas (8, 9, 10, 11)
- Creación de templates CLIPS (estado, resultado)
- Ontología del dominio (categorías, modos, descripciones)
- Parámetros del dominio (umbrales, rangos)
- Funciones de clasificación (`clasificar_temperatura`, `clasificar_horario`)

**Asistencia de IA:**

- **Cursor AI:** Sugirió sintaxis básica de reglas CLIPS con `defrule`
- **GitHub Copilot:** Proporcionó plantilla de template con `deftemplate`
- **Claude Sonnet 3.5:** Validó la lógica de las reglas CLIPS y sugirió mejoras en el sistema de prioridades
- **ChatGPT-4:** Generó esqueleto de funciones de utilidad y proporcionó ejemplos de reglas CLIPS

**Modificaciones humanas:**

- Diseño completo de la lógica de cada regla
- Sistema de prioridades para resolución de conflictos
- Slots y tipos de datos en templates
- Funciones de clasificación con lógica específica del dominio
- Ontología completa del dominio HVAC

#### 7.1.4 D'Alessandro - Motor de Inferencia CLIPS

**Trabajo realizado por D'Alessandro:**

- Inicialización del entorno CLIPS
- Carga dinámica de templates y reglas
- Assertion de hechos en formato CLIPS
- Ejecución del motor de inferencia (env.run())
- Extracción y parsing de resultados de CLIPS
- Sistema de selección por prioridad
- Generación de explicaciones (hechos evaluados, reglas disparadas)
- Funciones de visualización en Streamlit
- Generación de recomendaciones contextuales
- Diseño de colores e iconos por modo

**Asistencia de IA:**

- **Cursor AI:** Generó esqueleto básico de `inicializar_clips()` y sugirió estructura de `ejecutar_inferencia()`
- **GitHub Copilot:** Proporcionó plantilla de iteración sobre hechos CLIPS
- **Claude Sonnet 3.5:** Ayudó con la lógica de conversión de tipos entre Python y CLIPS
- **ChatGPT-4:** Generó esqueleto de funciones de visualización Streamlit y sugirió función básica de recomendaciones

**Modificaciones humanas:**

- Integración completa con CLIPSPy y conversión de tipos
- Sistema completo de prioridades para resolución de conflictos
- Extracción inteligente de resultados múltiples
- Visualización HTML/CSS personalizada
- Recomendaciones contextuales por modo
- Manejo de casos especiales y errores
- Diseño completo del sistema de explicabilidad

#### 7.1.5 Daniel - Integración y UI

**Trabajo realizado por Daniel:**

- Arquitectura completa de integración (flujo datos → hechos → CLIPS → UI)
- Interfaz Streamlit completa (panel de control, visualización, historial)
- Gestión de estado con `st.session_state`
- Mensajes educativos para el usuario
- Diseño de explicabilidad y trazabilidad en UI
- Descargos de responsabilidad visibles
- Documentación completa del proyecto (7 documentos)
- Configuración de requirements.txt
- Pruebas de integración end-to-end

**Asistencia de IA:**

- **Cursor AI:** Generó layout básico de Streamlit (columnas, botones, métricas)
- **GitHub Copilot:** Sugirió uso de componentes Streamlit (sidebar, expander, metrics) y proporcionó plantilla básica de gestión de estado
- **Claude Sonnet 3.5:** Ayudó con la estructura de documentación técnica y revisión de contenido
- **ChatGPT-4:** Ayudó con sintaxis de visualizaciones HTML/CSS y generación de texto explicativo para usuarios

**Modificaciones humanas:**

- Diseño completo del flujo UX
- Mensajes educativos y explicativos
- Visualización de explicaciones del razonamiento
- Sistema de historial de decisiones
- Documentación exhaustiva (manual de usuario, documento técnico, README)
- Integración de todos los módulos
- Arquitectura completa del sistema

### 7.2 Responsabilidad y Comprensión del Código

**Declaración del equipo:**

> "Todos los integrantes pueden explicar cualquier parte del código. Las herramientas de IA (Cursor AI, GitHub Copilot, Claude Sonnet 3.5 y ChatGPT-4) asistieron en la generación de estructuras base y sugerencias, pero cada línea fue revisada, comprendida y modificada según las necesidades del proyecto. Ningún código fue copiado directamente sin entender su funcionamiento."

**Herramientas utilizadas:**

- **Cursor AI** (2024) - Editor con IA integrada para generación de código base
- **GitHub Copilot** (2024) - Asistente de programación con sugerencias en tiempo real
- **Claude Sonnet 3.5** (Anthropic, 2024) - Asistente conversacional para revisión y validación
- **ChatGPT-4** (OpenAI, 2024) - Asistente conversacional para documentación y debugging

**Política cumplida:**

- ✅ Transparencia total en uso de IA
- ✅ Responsabilidad del equipo por el código
- ✅ Comprensión completa del sistema
- ✅ Privacidad de datos respetada
- ✅ Originalidad y ética en el desarrollo
- ✅ Declaración explícita de todas las herramientas usadas
- ✅ Validación humana de todas las decisiones técnicas

---

## 8. Estadísticas del Proyecto

- **Líneas de código Python:** ~1,500
- **Archivos Python principales:** 6
- **Reglas CLIPS:** 5
- **Tests automatizados:** 28
- **Archivos de documentación:** 7
- **Tiempo total de desarrollo:** ~40 horas

---

## 9. Transparencia y Responsabilidad

### 9.1 Transparencia en la Interfaz

La aplicación Streamlit **siempre muestra**:

1. **✅ Recomendación del sistema** (modo sugerido)
2. **✅ Justificación completa**:
   - Hechos evaluados (temperatura, ocupación, hora)
   - Reglas disparadas (qué lógica se aplicó)
   - Razón textual explicativa
3. **✅ Descargo de responsabilidad:**
   > "⚠️ **Aviso importante:** Este sistema experto es una herramienta de asistencia. Las decisiones finales sobre el control de temperatura deben considerar el confort personal y las condiciones específicas del entorno. No reemplaza el criterio humano."

### 9.2 No Discriminación

**Análisis de sesgo:**

- ✅ El sistema NO usa atributos sensibles (raza, género, edad, religión, nacionalidad)
- ✅ Las reglas aplican por igual a todos los usuarios
- ✅ Decisiones basadas solo en: temperatura, ocupación, hora

**Limitación reconocida:**

- ⚠️ Umbrales de confort (20-24°C) son promedios estadísticos
- Grupos específicos (niños, ancianos, personas con condiciones médicas) pueden requerir ajustes
- **Solución:** Control manual siempre disponible

### 9.3 Limitaciones Declaradas

**El sistema declara explícitamente:**

❌ **NO está diseñado para:**

- Uso médico (pacientes con hipotermia, ancianos vulnerables)
- Ambientes críticos (hospitales, laboratorios)
- Situaciones de emergencia (clima extremo)
- Funcionamiento completamente autónomo sin supervisión

✅ **SÍ está diseñado para:**

- Asistencia en hogares con ocupantes sanos
- Escenarios típicos de uso residencial
- Operación con supervisión humana

### 9.4 No Sustitución de Criterio Profesional

**Declaración clara:**

> "Este sistema experto puede **asistir** en decisiones de climatización, pero **NO suplanta** el criterio de un técnico HVAC profesional, ni el juicio del usuario final sobre su propio confort."

**En la interfaz:**

- Control manual siempre accesible
- Usuario puede ignorar cualquier recomendación
- Historial permite auditar decisiones pasadas

---

## 10. Conclusiones

El proyecto desarrollado cumple completamente con los requisitos del curso: sistema experto funcional con CLIPS (CLIPSPy), 5 reglas de producción con prioridades, encadenamiento hacia adelante, interfaz interactiva con Streamlit, explicabilidad completa, 28 tests automatizados, datos reales vía API, documentación exhaustiva y transparencia en uso de IA.

**Aprendizajes técnicos:**

- Implementación de sistemas expertos con CLIPS y diseño de reglas de producción
- Integración de Python con motores de inferencia y desarrollo de interfaces explicables
- Testing de sistemas basados en conocimiento

**Aprendizajes éticos:**

- Importancia de transparencia en sistemas de IA y declaración de limitaciones
- Responsabilidad del desarrollador vs usuario y necesidad de explicabilidad

**Extensiones futuras:** Integración con sensores reales (DHT22, PIR), Machine Learning para predicción de patrones, sistema multi-habitación, aprendizaje adaptativo, integración IoT con API REST, dashboard de analítica y app móvil.

Este proyecto demuestra que los sistemas expertos basados en reglas siguen siendo valiosos cuando el conocimiento es codificable, la explicabilidad es crucial, se requiere trazabilidad y el espacio de problemas es manejable. La IA debe usarse como herramienta de asistencia, no como sustituto del criterio humano.

---

## 📝 Anexos

### Anexo A: Comandos de Ejecución

```bash
# Instalación
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run run.py

# Ejecutar tests
pytest tests/ -v
```

### Anexo B: Estructura de Archivos

```
termostato_inteligente_sistema_experto/
├── engine/
│   ├── inferencia.py          # Motor CLIPS
│   └── procesador_hechos.py   # Razonador
├── knowledge/
│   ├── datos.py               # Adquisición de datos
│   └── reglas_clips.py        # Base de conocimiento
├── ui/
│   └── app.py                 # Interfaz Streamlit
├── tests/                     # 28 tests automatizados
├── run.py                     # Punto de entrada
└── DOCUMENTO_TECNICO.md       # Este documento
```

### Anexo C: Contacto del Equipo

- **Igor:** Adquisición de datos
- **Bruno:** Procesamiento de hechos
- **Mario:** Base de conocimiento
- **D'Alessandro:** Motor CLIPS y visualización
- **Daniel:** Integración y documentación

---
