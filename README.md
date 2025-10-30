# 🌡️ Termostato Inteligente - Sistema Experto

Sistema experto para control automático de temperatura utilizando el motor de inferencia **CLIPS** con encadenamiento hacia adelante.

## 📋 Descripción

Este sistema experto determina automáticamente el modo óptimo de un termostato basándose en condiciones del entorno como temperatura, ocupación de la habitación y horario del día. Utiliza inteligencia artificial basada en reglas para optimizar el balance entre confort térmico y eficiencia energética.

**Características principales:**

- 🌡️ Obtención de temperatura en tiempo real vía API meteorológica
- 👥 Detección manual de ocupación de la habitación
- 🕐 Consideración de horarios (día/noche) para optimización
- 🧠 Motor de inferencia CLIPS con 5 reglas de producción
- 📊 Interfaz web interactiva con Streamlit
- 🔍 Explicabilidad completa de las decisiones tomadas

## 🎯 Modos del Termostato

El sistema puede recomendar 4 modos diferentes según las condiciones:

- **🔥 CALOR**: Activa calefacción cuando hay personas y la temperatura es baja (< 20°C)
- **❄️ FRIO**: Activa aire acondicionado cuando hay personas y la temperatura es alta (> 24°C)
- **🌱 ECO**: Modo eficiente cuando la temperatura es confortable (20-24°C) o la habitación está vacía
- **⚫ APAGADO**: Desactiva el sistema en horario nocturno (22:00-6:00) sin ocupación

## 🚀 Instalación Local

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

**1. Clonar el repositorio:**

```bash
git clone <url-del-repositorio>
cd termostato_inteligente_sistema_experto
```

**2. Crear entorno virtual (recomendado):**

_Windows (PowerShell):_

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

_Windows (CMD):_

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

_Linux/Mac:_

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar dependencias:**

```bash
pip install -r requirements.txt
```

Esto instalará las siguientes bibliotecas:

- `streamlit` - Framework para la interfaz web
- `clipspy` - Motor de inferencia CLIPS para Python
- `requests` - Consultas a API meteorológica
- `pytest` - Framework de testing

## 💻 Ejecutar la Aplicación

Una vez instaladas las dependencias, ejecuta la aplicación con uno de estos métodos:

**Opción 1: Usando run.py (recomendado)**

```bash
streamlit run run.py
```

**Opción 2: Directamente desde ui/app.py**

```bash
streamlit run ui/app.py
```

**Opción 3: Con módulo Python**

```bash
python -m streamlit run run.py
```

La aplicación se abrirá automáticamente en tu navegador en **http://localhost:8501**

Si el puerto 8501 está ocupado, puedes usar otro puerto:

```bash
streamlit run run.py --server.port 8502
```

## 🧪 Ejecutar Pruebas

El proyecto incluye 28 pruebas automatizadas que validan el correcto funcionamiento del sistema:

**Ejecutar todas las pruebas:**

```bash
pytest tests/ -v
```

**Ejecutar pruebas con más detalle (ver prints):**

```bash
pytest tests/ -v -s
```

**Ejecutar pruebas de un módulo específico:**

```bash
# Pruebas del módulo de datos
pytest tests/test_datos.py -v

# Pruebas del procesador de hechos
pytest tests/test_hechos.py -v

# Pruebas de inferencia con CLIPS
pytest tests/test_inferencia.py -v

# Pruebas de la base de conocimiento
pytest tests/test_reglas.py -v
```

**Ejecutar una prueba específica:**

```bash
pytest tests/test_inferencia.py::test_inferencia_modo_calor -v
```

### ¿Qué prueban los tests?

- **test_datos.py**: Verifica que los datos se obtienen correctamente desde la API
- **test_hechos.py**: Valida la transformación de datos en hechos estructurados
- **test_inferencia.py**: Prueba que CLIPS dispara las reglas correctas según las condiciones
- **test_reglas.py**: Verifica que las reglas y parámetros del dominio estén bien definidos

**Nota:** Si pytest no está instalado, se instaló automáticamente con `requirements.txt`

## 📖 Manual de Usuario

### Pasos para Usar la Aplicación

**1. Abrir la aplicación**

- Ejecuta `streamlit run run.py` en tu terminal
- Se abrirá automáticamente en tu navegador

**2. Actualizar datos del entorno**

- Haz clic en el botón **"🔄 Actualizar Datos"** en el panel lateral
- El sistema obtendrá la temperatura actual de Trujillo, Perú desde la API meteorológica
- Se mostrarán los datos actuales: temperatura, hora, día, estación

**3. Configurar ocupación**

- En el panel lateral, marca o desmarca **"¿Habitación ocupada?"**
- Esto indica al sistema si hay personas presentes en la habitación

**4. Ejecutar el sistema experto**

- Haz clic en **"▶️ Ejecutar Sistema Experto"** en la sección principal
- El motor CLIPS analizará los datos y determinará el modo óptimo

**5. Interpretar los resultados**

- El sistema mostrará el **modo recomendado** (CALOR, FRIO, ECO o APAGADO)
- Expandir la sección de **"Explicación del razonamiento"** para ver:
  - Hechos evaluados
  - Reglas que se dispararon
  - Razón de la decisión
- Revisar las **recomendaciones adicionales** según el modo

### Modo Manual (Simulación)

Para probar diferentes escenarios sin esperar a que cambien las condiciones reales:

1. En el panel lateral, marca **"Modo Manual"**
2. Ajusta los controles:
   - **Temperatura**: Deslizador de 0 a 40°C
   - **Ocupación**: Checkbox manual
   - **Hora**: Deslizador de 0 a 23
3. Haz clic en **"✔️ Aplicar datos manuales"**
4. Ejecuta el sistema experto para ver qué modo recomienda

**Ejemplo de uso manual:**

- Temperatura: 17°C, Ocupada: Sí → Sistema recomienda **CALOR** 🔥
- Temperatura: 30°C, Ocupada: Sí → Sistema recomienda **FRIO** ❄️
- Temperatura: 22°C, Ocupada: No → Sistema recomienda **ECO** 🌱
- Temperatura: 22°C, Ocupada: No, Hora: 23:00 → Sistema recomienda **APAGADO** ⚫

### Historial de Decisiones

La aplicación mantiene un registro de las últimas ejecuciones:

- Ver **estadísticas** del historial (total de ejecuciones, modo más usado)
- Expandir el historial completo para ver cada decisión tomada
- Cada entrada muestra: timestamp, temperatura, ocupación, modo recomendado

### Limpiar Resultados

Si quieres empezar de nuevo:

- Botón **"🗑️ Limpiar"**: Elimina los resultados actuales
- Botón **"🗑️ Limpiar historial"**: Borra todo el historial de ejecuciones

## 🏗️ Arquitectura del Sistema

El sistema está compuesto por 5 módulos principales:

### 1. **knowledge/datos.py**

Obtiene datos del entorno (temperatura de API, hora del sistema, estación).

### 2. **engine/procesador_hechos.py**

Transforma datos brutos en hechos estructurados (clasifica temperatura, horarios, ocupación).

### 3. **knowledge/reglas_clips.py**

Define las 5 reglas CLIPS y parámetros del dominio (temperaturas, horarios, prioridades).

### 4. **engine/inferencia.py**

Motor de inferencia CLIPS que ejecuta las reglas y determina el modo óptimo.

### 5. **ui/app.py**

Interfaz web Streamlit que integra todos los módulos y presenta resultados al usuario.

## 🔧 Tecnologías

- **Python 3.8+** - Lenguaje principal
- **CLIPS (CLIPSPy)** - Motor de inferencia con reglas de producción
- **Streamlit** - Framework para interfaz web
- **Requests** - API meteorológica Open-Meteo
- **pytest** - Framework de testing

## 🐛 Solución de Problemas

**Error: "ModuleNotFoundError"**

```bash
pip install -r requirements.txt --force-reinstall
```

**Error con CLIPS en Windows**
CLIPSPy requiere Microsoft Visual C++ 14.0 o superior.
Descarga e instala desde: https://visualstudio.microsoft.com/downloads/

**Puerto 8501 ocupado**

```bash
streamlit run run.py --server.port 8502
```

**No se detecta Python**

- Verifica que Python esté instalado: `python --version`
- Asegúrate de tener Python 3.8 o superior instalado

**Error al activar entorno virtual en Windows**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta activar de nuevo: `.\venv\Scripts\Activate.ps1`

## ⚠️ Aviso Importante

Este sistema experto es una **herramienta de asistencia**. Las recomendaciones deben ser evaluadas por el usuario final. El sistema no se conecta directamente a termostatos reales sin supervisión humana.

**No está diseñado para:**

- Uso médico o ambientes críticos (hospitales, laboratorios)
- Situaciones de emergencia extrema
- Funcionamiento completamente autónomo sin supervisión

**Sí está diseñado para:**

- Asistencia en hogares residenciales
- Usuarios que buscan optimizar confort y ahorro energético
- Aprendizaje sobre sistemas expertos basados en reglas

## 👥 Equipo

**Igor** - Adquisición de datos  
**Bruno** - Procesamiento de hechos  
**Mario** - Base de conocimiento  
**D'Alessandro** - Motor CLIPS y visualización  
**Daniel** - Integración y documentación

## 📚 Documentación Adicional

Para más información técnica, consulta:

- `DOCUMENTO_TECNICO.md` - Documentación técnica completa

---

**Proyecto educativo** desarrollado para el curso de Sistemas Inteligentes
