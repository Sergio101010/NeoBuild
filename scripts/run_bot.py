#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import joblib
import logging
import argparse
import re

# Añade la carpeta raíz al path para importar src.*
PROYECTO_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROYECTO_RAIZ not in sys.path:
    sys.path.insert(0, PROYECTO_RAIZ)

from src.data.load_data import log_interaccion
from src.data.feedback import log_feedback
from src.features.preprocess import extract_entities
from src.models.classifier import load_model
from src.training.train import incremental_train
from src.utils.context import Contexto
from src.data.components import componentes
from src.templates import (
    RESPUESTA_RECOMENDACION,
    RESPUESTA_COMPATIBILIDAD,
    RESPUESTA_PRESUPUESTO,
    RESPUESTA_USO
)
from src.small_talk import saludo, despedida, agradecimiento

def setup_argparse():
    p = argparse.ArgumentParser(description="Ejecutar Asistente NeoBuild 1")
    p.add_argument("-c", "--config", default="config/settings.yaml",
                   help="Ruta al archivo YAML de configuración")
    p.add_argument("-t", "--threshold", type=float,
                   help="Umbral de confianza (opcional)")
    return p.parse_args()

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler("run_bot.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def limpiar_referencias(texto: str, contexto: Contexto) -> str:
    ultimo = contexto.obtener_ultimo_componente()
    if ultimo:
        return re.sub(r"\b(esa|esta|el anterior|la anterior)\b",
                      ultimo.lower(), texto, flags=re.IGNORECASE)
    return texto

def generar_propuesta_presupuesto(presupuesto: int, contexto: Contexto) -> str:
    uso = contexto.obtener("uso") or "general"
    distribuciones = {
        "general":   {"CPU":0.25,"GPU":0.35,"Motherboard":0.10,"RAM":0.10,"Almacenamiento":0.10,"Fuente":0.05,"Caja":0.05},
        "gaming":    {"CPU":0.30,"GPU":0.40,"Motherboard":0.10,"RAM":0.10,"Almacenamiento":0.05,"Fuente":0.03,"Caja":0.02},
        "oficina":   {"CPU":0.30,"GPU":0.20,"Motherboard":0.10,"RAM":0.15,"Almacenamiento":0.15,"Fuente":0.05,"Caja":0.05},
    }
    pct = distribuciones.get(uso, distribuciones["general"])

    proposal, total = {}, 0
    for comp, frac in pct.items():
        bud = presupuesto * frac
        opts = [c for c in componentes.get(comp, []) if c["precio"] <= bud] or componentes.get(comp, [])
        key = "rendimiento" if comp=="CPU" else "vram" if comp=="GPU" else "precio"
        pick = sorted(opts, key=lambda x: x.get(key,0), reverse=True)[0]
        proposal[comp] = pick
        total += pick["precio"]

    orden = ["Caja","Fuente","Almacenamiento","Motherboard","RAM","GPU","CPU"]
    for comp in orden:
        if total <= presupuesto:
            break
        pick = proposal.get(comp)
        if not pick:
            continue
        opts = sorted(componentes.get(comp, []), key=lambda x: x["precio"])
        cheaper = next((o for o in opts if o["precio"] < pick["precio"]), None)
        if cheaper:
            total -= (pick["precio"] - cheaper["precio"])
            proposal[comp] = cheaper
        else:
            total -= pick["precio"]
            del proposal[comp]

    lines = [f"- {c}: {i['nombre']} (${i['precio']})" for c, i in proposal.items()]
    return "Aquí tienes una propuesta optimizada:\n" + "\n".join(lines) + f"\nTotal aproximado: ${total}"

def responder(texto: str, intent: str, contexto: Contexto) -> str:
    """Genera la respuesta basada en intención, entidades y contexto."""

    # 1) Small talk
    if intent == "saludo":
        return saludo()
    if intent == "despedida":
        return despedida()
    if intent == "agradecimiento":
        return agradecimiento()

    # 2) Extraer entidades y actualizar contexto
    entidades = extract_entities(texto)
    contexto.actualizar(entidades)
    uso = contexto.obtener("uso")
    pres = contexto.obtener("presupuesto")
    marca = contexto.obtener("marca")
    comp = entidades.get("componente")

    # 3) Recomendaciones de componentes
    if intent.startswith("recomendacion_"):
        # Determina el tipo (CPU, GPU, etc.)
        tipo = intent.split("_", 1)[1].upper()
        opciones = componentes.get(tipo, [])
        # Aplica filtros progresivos
        if uso:
            opciones = [c for c in opciones if uso in c.get("uso", [])]
        if marca:
            opciones = [c for c in opciones if c.get("marca", "").lower() == marca.lower()]
        if pres:
            opciones = [c for c in opciones if c["precio"] <= pres]
        # Selecciona la mejor según rendimiento o VRAM
        key = "rendimiento" if tipo == "CPU" else "vram" if tipo == "GPU" else "precio"
        opciones = sorted(opciones, key=lambda x: x.get(key, 0), reverse=True)
        if opciones:
            elegido = opciones[0]
            # Construye el detalle de filtros usados
            filtros = []
            if uso:   filtros.append(f"uso={uso}")
            if marca: filtros.append(f"marca={marca}")
            if pres:  filtros.append(f"precio<={pres}")
            detalle = f" (filtros: {', '.join(filtros)})" if filtros else ""
            return (
                f"Para{' '+uso if uso else ''}, te recomiendo el {tipo} "
                f"«{elegido['nombre']}» de {elegido['marca']} "
                f"por ${elegido['precio']}{detalle}."
            )
        else:
            return f"No he encontrado ningún {tipo} que cumpla tus criterios."

    # 4) Compatibilidad
    if intent == "compatibilidad":
        if comp == "CPU":
            sockets = ", ".join(sorted({c["socket"] for c in componentes["CPU"]}))
            return f"Los sockets disponibles para CPU son: {sockets}."
        if comp == "GPU":
            return "Las GPUs se conectan por PCIe 4.0/5.0."
        if comp == "RAM":
            tipos = ", ".join(sorted({c["tipo"] for c in componentes["RAM"]}))
            return f"Las memorias RAM soportadas son: {tipos}."
        return "Dime a qué componente te refieres para ver compatibilidad."

    # 5) Presupuesto
    if intent == "presupuesto":
        if pres:
            return f"Perfecto, tengo tu presupuesto de ${pres}. ¿Quieres una propuesta de configuración completa? (s/n)"
        else:
            return "Por favor, indícame tu presupuesto en dólares, p.ej. «Tengo $600»."

    # 6) Uso específico
    if intent == "uso_especifico":
        uso_texto = uso or "uso general"
        return f"Entendido, elaboración de una configuración para {uso_texto}."

    # 7) Fallback
    return (
        "Lo siento, no tengo la información precisa para eso. "
        "Puedes pedirme recomendaciones de componentes (CPU, GPU, RAM…), "
        "consultar compatibilidad o definir un presupuesto."
    )

def main():
    args = setup_argparse()
    init_logging()
    cfg = load_config(args.config)
    threshold = args.threshold or cfg["model"]["proba_threshold"]

    contexto = Contexto()
    vec_path = os.path.join(PROYECTO_RAIZ, cfg["data"]["models"], "vectorizer.pkl")
    mod_path = os.path.join(PROYECTO_RAIZ, cfg["data"]["models"], "modelo_nb.pkl")
    vectorizer = load_model(vec_path)
    clf = load_model(mod_path)

    print(responder("", "saludo", contexto))
    print("Escribe 'salir' para terminar.\n")

    awaiting_conf = False
    awaiting_budget = False
    last_text = last_intent = ""

    while True:
        user_input = input("👤 Tú: ").strip()
        if user_input.lower() in ["salir","exit","adios"]:
            print(responder("", "despedida", contexto))
            break

        # Confirmación de presupuesto
        if awaiting_budget:
            if user_input.lower() in ["s","si","y","yes"]:
                pres = contexto.obtener("presupuesto")
                propuesta = generar_propuesta_presupuesto(pres, contexto)
                print(f"🤖 {propuesta}\n")
                fb = input("¿Te resultó útil esta propuesta? (s/n): ").strip().lower()
                log_feedback(user_input, last_intent, fb)
               # evita reclasificar este "s"
             # ¡RESET del flag para volver al flujo normal!
                awaiting_budget = False
                continue
            else:
                print("🤖 De acuerdo, no genero propuesta.\n")
                awaiting_budget = False
                continue


        # Confirmación por baja confianza
        if awaiting_conf:
            if user_input.lower() in ["s","si","y","yes"]:
                log_interaccion(os.path.join("data","raw","historial.jsonl"), last_text, last_intent)
                resp = responder(last_text, last_intent, contexto)
                print(f"🤖 {resp}\n")
                incremental_train(last_text, last_intent, cfg)
                fb = input("¿Te resultó útil esta respuesta? (s/n): ").strip().lower()
                log_feedback(last_text, last_intent, fb)
                continue
            else:
                print("👍 Entendido, no lo guardaré.\n")
                awaiting_conf = False
                continue

        # Flujo normal: limpieza y clasificación
        cleaned = limpiar_referencias(user_input, contexto)
        vec = vectorizer.transform([cleaned])
        probs = clf.predict_proba(vec)[0]
        idx = probs.argmax()
        intent = clf.classes_[idx]
        conf = probs[idx]
        logging.info(f"Entrada: '{user_input}' => {intent} ({conf:.2f})")

        last_text, last_intent = user_input, intent

        if conf < threshold:
            print(f"🤔 No estoy segur@ ({conf:.2f}). ¿Te refieres a '{intent}'? (s/n)")
            awaiting_conf = True
            continue

        log_interaccion(os.path.join("data","raw","historial.jsonl"), user_input, intent)
        respuesta = responder(cleaned, intent, contexto)
        print(f"🤖 {respuesta}\n")

        # Si es presupuesto, preguntar confirmación antes de feedback
        if intent == "presupuesto" and contexto.obtener("presupuesto") is not None:
            awaiting_budget = True
            continue

        # Feedback de respuestas normales
        fb = input("¿Te resultó útil esta respuesta? (s/n): ").strip().lower()
        log_feedback(user_input, intent, fb)
        print("👍 Gracias por tu feedback!\n")

        # Entrenamiento incremental
        incremental_train(user_input, intent, cfg)
        #print("🤖 Gracias por tu feedback!\n")

if __name__ == "__main__":
    main()
