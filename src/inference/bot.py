import os
import json
import random
import joblib
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from src.data.load_data import log_interaccion

# Asegurarse de que los recursos de NLTK estén disponibles
nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("spanish"))

# Cargar el modelo y el vectorizador entrenado
MODELO_PATH = os.path.join("data", "models", "modelo_nb.pkl")
VECTORIZER_PATH = os.path.join("data", "models", "vectorizer.pkl")

modelo = joblib.load(MODELO_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# Cargar intenciones desde el archivo intents.json
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

# Procesamiento básico de texto
def limpiar_texto(texto):
    texto = texto.lower()
    texto = texto.translate(str.maketrans("", "", string.punctuation))
    tokens = texto.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(tokens)

# Obtener respuesta basada en la intención
def obtener_respuesta(intencion_predicha):
    for intent in intents:
        if intent["tag"] == intencion_predicha:
            return random.choice(intent["responses"])
    return "Lo siento, no entiendo lo que me estás preguntando."

# Función principal para manejar el flujo del bot
def responder(pregunta_usuario):
    texto_limpio = limpiar_texto(pregunta_usuario)
    X_input = vectorizer.transform([texto_limpio])
    prediccion = modelo.predict(X_input)[0]

    respuesta = obtener_respuesta(prediccion)

    log_interaccion(pregunta_usuario, prediccion, respuesta)

    return respuesta
