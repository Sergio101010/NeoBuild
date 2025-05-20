# src/small_talk.py

import random

# ------------------
# Frases de small talk
# ------------------

# Saludos para iniciar la conversación
SALUDOS = [
    "¡Hola! ¿En qué puedo ayudarte con tu PC hoy?",
    "¡Buenas! ¿Listo para hablar de hardware?",
    "¡Hey! ¿Qué aspecto del PC te interesa hoy?",
    "¡Hola! ¿Cómo puedo asistirte en tu configuración de PC?"
]

# Mensajes de transición cuando el bot está "pensando"
TRANSICIONES = [
    "Un momento, por favor…",
    "Dame un segundo mientras busco…",
    "Permíteme un momento para revisar…",
    "Ahora mismo lo estoy comprobando…"
]

# Despedidas para cerrar la conversación
DESPEDIDAS = [
    "¡Hasta luego! Si necesitas más ayuda, aquí estaré.",
    "¡Nos vemos! Que disfrutes tu nueva configuración.",
    "¡Chau! ¡Que tengas buen ensamblaje!",
    "¡Adiós! Espero haber sido de ayuda."
]

# Agradecimientos y respuestas a “gracias”
RESPUESTAS_AGRADECIMIENTO = [
    "¡Para eso estoy!",
    "¡Con gusto!",
    "¡Encantado de ayudar!",
    "¡De nada!"
]

# ------------------
# Funciones para obtener frases aleatorias
# ------------------

def saludo() -> str:
    """Devuelve un saludo aleatorio."""
    return random.choice(SALUDOS)

def transicion() -> str:
    """Devuelve un mensaje de transición aleatorio."""
    return random.choice(TRANSICIONES)

def despedida() -> str:
    """Devuelve una despedida aleatoria."""
    return random.choice(DESPEDIDAS)

def agradecimiento() -> str:
    """Devuelve una respuesta aleatoria para agradecimientos."""
    return random.choice(RESPUESTAS_AGRADECIMIENTO)
