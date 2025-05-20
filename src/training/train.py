import joblib
from src.data.load_data import load_raw
from src.models.classifier import init_classifier, save_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import numpy as np

def initial_train(config: dict):
    """Reentrena desde cero usando todo el historial."""
    df = load_raw(config['data']['raw'])
    X = df['pregunta'].tolist()
    y = df['intencion'].tolist()

    # Vectorizador TF-IDF
    vectorizer = TfidfVectorizer(
        ngram_range=tuple(config['model']['tfidf']['ngram_range']),
        analyzer=config['model']['tfidf']['analyzer'],
        max_features=config['model']['tfidf']['max_features']
    )
    X_vec = vectorizer.fit_transform(X)

    # Clasificador
    clases = sorted(set(y))
    clf = init_classifier(config['model']['alpha'], clases)
    clf.fit(X_vec, y)

    # Guardar artefactos
    save_model(vectorizer, f"{config['data']['models']}/vectorizer.pkl")
    save_model(clf,       f"{config['data']['models']}/modelo_nb.pkl")

def incremental_train(pregunta: str, etiqueta: str, config: dict):
    """Actualiza el modelo con un solo ejemplo."""
    vectorizer = joblib.load(f"{config['data']['models']}/vectorizer.pkl")
    clf = joblib.load(f"{config['data']['models']}/modelo_nb.pkl")

    X_new = vectorizer.transform([pregunta])
    clf.partial_fit(X_new, [etiqueta])

    save_model(clf, f"{config['data']['models']}/modelo_nb.pkl")
