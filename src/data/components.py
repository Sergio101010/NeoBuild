# src/data/components.py

componentes = {
    "CPU": [
        {"nombre": "Ryzen 5 5600G", "marca": "AMD", "precio": 129, "rendimiento": 72, "socket": "AM4", "nucleos": 6, "uso": ["oficina", "basico"]},
        {"nombre": "Core i5-13400", "marca": "Intel", "precio": 199, "rendimiento": 85, "socket": "LGA1700", "nucleos": 10, "uso": ["gaming", "streaming"]},
        {"nombre": "Ryzen 9 7950X", "marca": "AMD", "precio": 699, "rendimiento": 98, "socket": "AM5", "nucleos": 16, "uso": ["streaming", "edicion"]},
        {"nombre": "Core i9-13900K", "marca": "Intel", "precio": 589, "rendimiento": 100, "socket": "LGA1700", "nucleos": 24, "uso": ["edicion", "rendimiento"]},
        {"nombre": "Ryzen 7 5800X3D", "marca": "AMD", "precio": 449, "rendimiento": 95, "socket": "AM4", "nucleos": 8, "uso": ["gaming", "streaming"]},
    ],
    "GPU": [
        {"nombre": "RTX 3060", "marca": "NVIDIA", "precio": 299, "vram": 12, "consumo": 170, "uso": ["gaming", "streaming"]},
        {"nombre": "RX 6600", "marca": "AMD", "precio": 249, "vram": 8, "consumo": 132, "uso": ["gaming", "basico"]},
        {"nombre": "RTX 4090", "marca": "NVIDIA", "precio": 1599, "vram": 24, "consumo": 450, "uso": ["4k", "rendimiento"]},
        {"nombre": "RX 7900 XTX", "marca": "AMD", "precio": 999, "vram": 24, "consumo": 355, "uso": ["4k", "gaming"]},
        {"nombre": "RTX 4070", "marca": "NVIDIA", "precio": 599, "vram": 12, "consumo": 200, "uso": ["gaming", "streaming"]},
    ],
    "Motherboard": [
        {"nombre": "ASUS ROG Strix B550-F", "socket": "AM4", "precio": 179, "formato": "ATX", "ram_slots": 4},
        {"nombre": "MSI MAG B660 Tomahawk", "socket": "LGA1700", "precio": 189, "formato": "ATX", "ram_slots": 4},
        {"nombre": "Gigabyte X670 AORUS Elite", "socket": "AM5", "precio": 299, "formato": "ATX", "ram_slots": 4},
    ],
    "RAM": [
        {"nombre": "Corsair Vengeance 16GB DDR4", "precio": 49, "velocidad": 3200, "tipo": "DDR4"},
        {"nombre": "G.Skill Trident Z 32GB DDR5", "precio": 129, "velocidad": 6000, "tipo": "DDR5"},
    ],

    "Almacenamiento": [
        {"nombre": "Samsung 970 EVO 1TB", "tipo": "SSD", "precio": 99, "velocidad": 3500},
        {"nombre": "Seagate Barracuda 2TB", "tipo": "HDD", "precio": 59, "velocidad": 7200},
    ],
    "Fuente": [
        {"nombre": "Corsair RM750x", "potencia": 750, "precio": 129, "certificacion": "80 Plus Gold"},
        {"nombre": "EVGA 600 W1", "potencia": 600, "precio": 49, "certificacion": "80 Plus White"},
    ],
    "Caja": [
        {"nombre": "NZXT H510", "precio": 69, "formato": "ATX", "ventiladores": 2},
        {"nombre": "Cooler Master MasterBox Q300L", "precio": 49, "formato": "Micro-ATX", "ventiladores": 1},
    ],
    "Refrigeracion": [
        {"nombre": "Cooler Master Hyper 212", "tipo": "Aire", "precio": 39, "rendimiento": 150},
        {"nombre": "NZXT Kraken X63", "tipo": "Agua", "precio": 129, "rendimiento": 280},
    ],
    "Monitor": [
        {"nombre": "Dell UltraSharp U2720Q", "precio": 599, "tamaño": 27, "resolucion": "4K", "uso": ["oficina", "edicion"]},
        {"nombre": "ASUS ROG Swift PG259QN", "precio": 799, "tamaño": 24.5, "resolucion": "Full HD", "uso": ["gaming"]},
    ],
    "Teclado": [
        {"nombre": "Logitech G Pro X", "precio": 149, "tipo": "Mecanico", "uso": ["gaming", "oficina"]},
        {"nombre": "Corsair K55 RGB", "precio": 49, "tipo": "Membrana", "uso": ["oficina"]},
    ],
    "Mouse": [
        {"nombre": "Logitech G502 HERO", "precio": 79, "tipo": "Optico", "uso": ["gaming", "oficina"]},
        {"nombre": "Razer DeathAdder V2", "precio": 69, "tipo": "Optico", "uso": ["gaming"]},
    ],
    "Audio": [
        {"nombre": "HyperX Cloud II", "precio": 99, "tipo": "Auriculares", "uso": ["gaming", "oficina"]},
        {"nombre": "Logitech G560", "precio": 199, "tipo": "Altavoces", "uso": ["gaming", "oficina"]},
    ],
    "Webcam": [
        {"nombre": "Logitech C920", "precio": 79, "resolucion": "1080p", "uso": ["streaming", "oficina"]},
        {"nombre": "Razer Kiyo", "precio": 99, "resolucion": "1080p", "uso": ["streaming"]},
    ],
    "Microfono": [
        {"nombre": "Blue Yeti", "precio": 129, "tipo": "USB", "uso": ["streaming", "oficina"]},
        {"nombre": "Audio-Technica AT2020", "precio": 99, "tipo": "XLR", "uso": ["streaming", "oficina"]},
    ],
    "Capturadora": [
        {"nombre": "Elgato HD60 S", "precio": 179, "resolucion": "1080p", "uso": ["streaming"]},
        {"nombre": "AVerMedia Live Gamer Mini", "precio": 99, "resolucion": "1080p", "uso": ["streaming"]},
    ],
    
}