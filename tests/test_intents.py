# tests/test_intents.py

import pytest
import yaml
import joblib
from src.features.preprocess import build_vectorizer
from src.models.classifier import init_classifier

# Ruta al config
CONFIG_PATH = 'config/settings.yaml'

@pytest.fixture(scope='module')
def config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope='module')
def vectorizer_and_clf(config):
    # Carga artefactos ya entrenados
    vec = joblib.load(f"{config['data']['models']}/vectorizer.pkl")
    clf = joblib.load(f"{config['data']['models']}/modelo_nb.pkl")
    return vec, clf

@pytest.mark.parametrize("entrada,esperado", [
    ("quiero una cpu para gaming",        "recomendacion_cpu"),
    ("¿es compatible esta ram?",           "compatibilidad"),
    ("tengo 500 dólares",                  "presupuesto"),
    ("necesito algo para transmisiones",   "uso_especifico"),
    ("hola, ¿qué tal?",                    "general"),
])
def test_intents(vectorizer_and_clf, entrada, esperado):
    vec, clf = vectorizer_and_clf
    etiquetas = clf.predict(vec.transform([entrada]))
    assert etiquetas[0] == esperado
