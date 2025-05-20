# src/utils/context.py

class Contexto:
    """
    Maneja el contexto de la conversación:
      - Guarda valores clave (presupuesto, uso, componente, marca)
      - Historial de últimas interacciones
      - Seguimiento de última intención y último componente para referencias implícitas
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia todo el contexto a valores iniciales."""
        self.data = {
            "presupuesto": None,
            "uso": None,
            "componente": None,
            "marca": None,
            "historial": [],
            "ultimo_componente": None,
            "ultimo_intent": None
        }

    def actualizar(self, entidades: dict):
        """
        Actualiza el contexto con nuevas entidades detectadas:
          - Añade al historial (máximo 5 entradas)
          - Actualiza presupuesto, uso, componente o marca si aparecen
          - Actualiza último componente
        """
        # Historial (máximo 5)
        if len(self.data["historial"]) >= 5:
            self.data["historial"].pop(0)
        self.data["historial"].append(entidades)

        # Campos principales
        for key in ["precio", "uso", "componente", "marca"]:
            if entidades.get(key) is not None:
                # Precio guardamos en "presupuesto" por consistencia
                if key == "precio":
                    self.data["presupuesto"] = entidades["precio"]
                else:
                    self.data[key] = entidades[key]

        # Último componente mencionado (para referencias implícitas)
        if entidades.get("componente"):
            self.data["ultimo_componente"] = entidades["componente"]

    def establecer_ultimo_intent(self, intent: str):
        """Guarda la última intención predicha (para flujos de confirmación)."""
        self.data["ultimo_intent"] = intent

    def obtener(self, key: str):
        """Recupera un valor del contexto por su clave."""
        return self.data.get(key)

    def obtener_ultimo_componente(self):
        """Devuelve el último componente mencionado en la conversación."""
        return self.data.get("ultimo_componente")

    def obtener_ultimo_intent(self):
        """Devuelve la última intención predicha."""
        return self.data.get("ultimo_intent")

    def obtener_historial(self):
        """Devuelve el historial de las últimas entidades procesadas."""
        return list(self.data["historial"])
