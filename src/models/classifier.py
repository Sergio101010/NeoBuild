import joblib
import numpy as np
from sklearn.naive_bayes import MultinomialNB


def init_classifier(alpha: float, classes: list) -> MultinomialNB:
    clf = MultinomialNB(alpha=alpha)
    clf.partial_fit(np.zeros((1, len(classes))), [classes[0]], classes=classes)
    return clf


def save_model(obj, path: str):
    joblib.dump(obj, path)


def load_model(path: str):
    return joblib.load(path)