"""
Base de conocimiento: reglas CLIPS del sistema experto.
Responsable: Mario
"""

# Parámetros del dominio
TEMP_BAJA_MAX = 19.9
TEMP_CONFORTABLE_MIN = 20.0
TEMP_CONFORTABLE_MAX = 24.0
TEMP_ALTA_MIN = 24.1

HORA_DIA_INICIO = 6
HORA_NOCHE_INICIO = 22

OCUPACION_INFERENCIA_HORA_INICIO = 8
OCUPACION_INFERENCIA_HORA_FIN = 22

# Templates CLIPS

TEMPLATE_ESTADO = """(deftemplate estado
    (slot temperatura (type FLOAT))
    (slot ocupada (type SYMBOL) (allowed-symbols TRUE FALSE))
    (slot hora (type INTEGER))
    (slot categoria-temp (type SYMBOL))
    (slot horario (type SYMBOL)))"""

TEMPLATE_RESULTADO = """(deftemplate resultado
    (slot modo (type SYMBOL))
    (slot razon (type STRING))
    (slot prioridad (type INTEGER)))"""


# Reglas de producción CLIPS
# Prioridades: 11=APAGADO, 10=CALOR/FRIO, 9=ECO desocupada, 8=ECO confortable

REGLA_MODO_CALOR = """(defrule modo-calor
    "Activa calefacción cuando hace frío y hay personas"
    (estado (ocupada TRUE) (categoria-temp temperatura_baja))
    =>
    (assert (resultado 
        (modo CALOR) 
        (razon "Habitación ocupada con temperatura baja") 
        (prioridad 10))))"""

REGLA_MODO_FRIO = """(defrule modo-frio
    "Activa aire acondicionado cuando hace calor y hay personas"
    (estado (ocupada TRUE) (categoria-temp temperatura_alta))
    =>
    (assert (resultado 
        (modo FRIO) 
        (razon "Habitación ocupada con temperatura alta") 
        (prioridad 10))))"""

REGLA_MODO_ECO_DESOCUPADA = """(defrule modo-eco-desocupada
    "Modo ahorro cuando no hay personas (independiente de temperatura)"
    (estado (ocupada FALSE))
    =>
    (assert (resultado 
        (modo ECO) 
        (razon "Habitación desocupada - ahorro de energía") 
        (prioridad 9))))"""

REGLA_MODO_ECO_CONFORTABLE = """(defrule modo-eco-confortable
    "Mantiene temperatura cuando está en rango confortable"
    (estado (ocupada TRUE) (categoria-temp temperatura_confortable))
    =>
    (assert (resultado 
        (modo ECO) 
        (razon "Temperatura confortable - ahorro de energía") 
        (prioridad 8))))"""

REGLA_MODO_APAGADO = """(defrule modo-apagado
    "Apaga completamente en horario nocturno sin ocupación"
    (estado (ocupada FALSE) (horario horario_noche))
    =>
    (assert (resultado 
        (modo APAGADO) 
        (razon "Horario nocturno sin ocupación") 
        (prioridad 11))))"""


# Lista de todas las reglas del sistema
TODAS_LAS_REGLAS = [
    REGLA_MODO_APAGADO,
    REGLA_MODO_CALOR,
    REGLA_MODO_FRIO,
    REGLA_MODO_ECO_DESOCUPADA,
    REGLA_MODO_ECO_CONFORTABLE,
]

# Categorías del dominio

# Categorías de temperatura
CATEGORIAS_TEMPERATURA = {
    'temperatura_baja': {
        'rango': f'< {TEMP_BAJA_MAX}°C',
        'descripcion': 'Temperatura fría que requiere calefacción',
        'accion_recomendada': 'calentar'
    },
    'temperatura_confortable': {
        'rango': f'{TEMP_CONFORTABLE_MIN}°C - {TEMP_CONFORTABLE_MAX}°C',
        'descripcion': 'Temperatura ideal para confort humano',
        'accion_recomendada': 'mantener'
    },
    'temperatura_alta': {
        'rango': f'> {TEMP_ALTA_MIN}°C',
        'descripcion': 'Temperatura cálida que requiere enfriamiento',
        'accion_recomendada': 'enfriar'
    }
}

# Categorías de horario
CATEGORIAS_HORARIO = {
    'horario_dia': {
        'rango': f'{HORA_DIA_INICIO}:00 - {HORA_NOCHE_INICIO-1}:59',
        'descripcion': 'Horario de actividad normal',
        'ocupacion_esperada': True
    },
    'horario_noche': {
        'rango': f'{HORA_NOCHE_INICIO}:00 - {HORA_DIA_INICIO-1}:59',
        'descripcion': 'Horario de descanso nocturno',
        'ocupacion_esperada': False
    }
}

# Modos del termostato
MODOS_TERMOSTATO = {
    'CALOR': {
        'icono': '🔥',
        'descripcion': 'Calefacción activa',
        'consumo_energetico': 'alto',
        'confort': 'óptimo'
    },
    'FRIO': {
        'icono': '❄️',
        'descripcion': 'Aire acondicionado activo',
        'consumo_energetico': 'alto',
        'confort': 'óptimo'
    },
    'ECO': {
        'icono': '🌱',
        'descripcion': 'Modo ahorro de energía',
        'consumo_energetico': 'bajo',
        'confort': 'bueno'
    },
    'APAGADO': {
        'icono': '⚫',
        'descripcion': 'Sistema apagado',
        'consumo_energetico': 'nulo',
        'confort': 'ninguno'
    }
}


# Funciones de utilidad

def clasificar_temperatura(temp: float) -> str:
    """Clasifica temperatura en categoría (baja, confortable, alta)."""
    if temp <= TEMP_BAJA_MAX:
        return "temperatura_baja"
    elif TEMP_CONFORTABLE_MIN <= temp <= TEMP_CONFORTABLE_MAX:
        return "temperatura_confortable"
    else:
        return "temperatura_alta"


def clasificar_horario(hora: int) -> str:
    """Clasifica hora en categoría (día o noche)."""
    if HORA_NOCHE_INICIO <= hora <= 23 or 0 <= hora < HORA_DIA_INICIO:
        return "horario_noche"
    return "horario_dia"


def inferir_ocupacion_por_hora(hora: int) -> bool:
    """Infiere ocupación basándose en la hora (para cuando no hay sensor)."""
    return OCUPACION_INFERENCIA_HORA_INICIO <= hora <= OCUPACION_INFERENCIA_HORA_FIN


def obtener_info_modo(modo: str) -> dict:
    """Obtiene información sobre un modo específico."""
    return MODOS_TERMOSTATO.get(modo.upper())


if __name__ == "__main__":
    print("BASE DE CONOCIMIENTO - TERMOSTATO INTELIGENTE")
    
    print("\n📋 REGLAS DEFINIDAS:")
    print(f"Total de reglas: {len(TODAS_LAS_REGLAS)}")
    
    print("\n🌡️ CATEGORÍAS DE TEMPERATURA:")
    for categoria, info in CATEGORIAS_TEMPERATURA.items():
        print(f"  - {categoria}: {info['rango']}")
    
    print("\n🕐 CATEGORÍAS DE HORARIO:")
    for categoria, info in CATEGORIAS_HORARIO.items():
        print(f"  - {categoria}: {info['rango']}")
    
    print("\n⚙️ MODOS DEL TERMOSTATO:")
    for modo, info in MODOS_TERMOSTATO.items():
        print(f"  {info['icono']} {modo}: {info['descripcion']}")
    
    print("\n✅ Base de conocimiento cargada correctamente")
    print("=" * 60)

