# scripts/retrain_model.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Asegura que la carpeta raíz esté en sys.path
PROYECTO_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROYECTO_RAIZ not in sys.path:
    sys.path.insert(0, PROYECTO_RAIZ)

import yaml
from src.data.load_data import seed_historial
from src.training.train import initial_train

def main():
    # Carga configuración
    cfg_path = os.path.join(PROYECTO_RAIZ, 'config', 'settings.yaml')
    with open(cfg_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 1. Sembrar historial si está vacío
    seed_historial(config['data']['raw'])

    # 2. Entrenamiento inicial
    initial_train(config)
    print("✅ Modelo entrenado y guardado en data/models/")

if __name__ == '__main__':
    main()
