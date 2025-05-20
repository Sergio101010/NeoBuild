# src/data/load_data.py

import os
import json
from datetime import datetime
import pandas as pd
from .seed_data import training_data

def load_raw(path: str) -> pd.DataFrame:
    """Carga un archivo JSONL de historial y retorna un DataFrame."""
    registros = []
    with open(path, encoding='utf-8') as f:
        for linea in f:
            registros.append(json.loads(linea))
    return pd.DataFrame(registros)

def save_processed(df: pd.DataFrame, path: str):
    """Guarda el DataFrame procesado como CSV."""
    df.to_csv(path, index=False, encoding='utf-8')

def log_interaccion(path: str, pregunta: str, intencion: str):
    """
    Registra cada interacción de usuario en formato JSON Lines (JSONL).
    Cada línea: {"timestamp": "...", "pregunta": ..., "intencion": ...}
    """
    registro = {
        "timestamp": datetime.utcnow().isoformat(),
        "pregunta": pregunta,
        "intencion": intencion
    }
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

def seed_historial(path: str):
    """
    Si el historial está vacío o no existe, lo llena con training_data.
    """
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        with open(path, 'w', encoding='utf-8') as f:
            for pregunta, intencion in training_data:
                registro = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "pregunta": pregunta,
                    "intencion": intencion
                }
                f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        print(f"✅ Sembrado historial con {len(training_data)} ejemplos en {path}")
    else:
        print(f"ℹ Historial ya contiene datos: {path}")
