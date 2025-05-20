# src/data/feedback.py

import json
import datetime
from pathlib import Path

# Ruta al archivo de feedback
FEEDBACK_PATH = Path("data/feedback.jsonl")

def log_feedback(pregunta: str, intencion: str, feedback: str) -> None:
    """
    Registra en un archivo JSONL la retroalimentación del usuario sobre una respuesta.

    Cada línea del archivo es un objeto JSON con:
    - timestamp: fecha y hora en ISO 8601
    - pregunta: el texto original de la consulta del usuario
    - intencion: la intención que se le asignó a esa consulta
    - feedback: 's' o 'n' según si la respuesta fue útil o no

    Si la carpeta 'data' no existe, se crea automáticamente.
    """
    registro = {
        "timestamp": datetime.datetime.now().isoformat(),
        "pregunta": pregunta,
        "intencion": intencion,
        "feedback": feedback.lower()
    }

    # Asegurarse de que la carpeta exista
    FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Escribir el registro en modo append, con un salto de línea
    with FEEDBACK_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        #print(f"Feedback registrado: {registro}")
    