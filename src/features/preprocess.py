import re

def extract_entities(texto):
    """Extrae uso, marca, componente y precio del texto del usuario."""
    entidades = {}
    texto_limpio = texto.lower()

    # Usos
    usos = ["oficina", "gaming", "edición", "servidor", "render", "tareas básicas"]
    for uso in usos:
        if uso in texto_limpio:
            entidades["uso"] = uso
            break

    # Marcas
    marcas = ["amd", "intel", "nvidia", "asus", "msi", "gigabyte", "corsair"]
    for marca in marcas:
        if marca in texto_limpio:
            entidades["marca"] = marca
            break

    # Componentes
    comps = {
        "CPU": ["cpu", "procesador"],
        "GPU": ["gpu", "tarjeta gráfica", "gráfica"],
        "RAM": ["ram", "memoria"],
        "MOTHERBOARD": ["motherboard", "placa madre", "placa base"],
        "ALMACENAMIENTO": ["ssd", "hdd", "almacenamiento"],
        "FUENTE": ["fuente", "psu"],
        "CAJA": ["caja", "chasis"],
        "REFRIGERACION": ["refrigeración", "cooler", "ventilador"]
    }
    for key, kws in comps.items():
        if any(kw in texto_limpio for kw in kws):
            entidades["componente"] = key
            break

    # Precio
    match_precio = re.search(
        r"(?:tengo\s+)?(?:un\s+)?(?:presupuesto\s+de\s+)?\$?\s?(\d{2,5})(?:\s*(usd|dólares)?)?",
        texto_limpio
    )
    if match_precio:
        valor = re.sub(r"[^\d]", "", match_precio.group(1))
        if valor.isdigit():
            entidades["precio"] = int(valor)

    return entidades
