'''
Catálogo de clasificación de fabricantes por dirección MAC.
'''

CLASIFICACION_FABRICANTES = [
    # Móviles, Tablets y Ecosistemas Móviles
    (("apple",), "iOS / macOS (Apple)"),
    (("google",), "Android / ChromeOS (Google)"),
    (("samsung",), "Android (Samsung)"),
    (("huawei", "xiaomi", "oneplus", "oppo", "vivo", "realme", "motorola", "zte", "nokia", "lenovo", "htc", "itel"), "Dispositivo móvil / Tablet (Android)"),
    
    # Entretenimiento: Smart TVs, Consolas y Set-Top Boxes
    (("sony", "nintendo"), "Consola de videojuegos"),
    (("lg electronics", "lg "), "Smart TV / Electrodoméstico (LG)"),
    (("amazon",), "Fire OS / Echo (Amazon)"),
    (("roku",), "Reproductor multimedia"),
    
    # PCs, Portátiles y Placas Base
    (("microsoft",), "Windows / Xbox (Microsoft)"),
    (("intel", "realtek", "hon hai", "foxconn", "dell", "hewlett packard", "asus", "acer", "msi", "gigabyte"), "PC / Portátil genérico"),
    (("raspberry pi",), "Linux (Raspberry Pi)"),
    (("azurewave", "liteon", "murata"), "Tarjeta de red genérica (Portátil/TV)"),
    
    # Máquinas Virtuales
    (("vmware", "virtualbox", "oracle vm", "qemu", "xen", "parallels"), "Máquina virtual"),
    
    # Routers, Switches y Equipos de Operadora
    (("sagemcom", "arcadyan", "mitrastar", "sercomm", "commscope", "arris", "technicolor", "vantiva", "humax"), "Router de operadora / Módem"),
    (("tp-link", "d-link", "netgear", "asus", "ubiquiti", "mikrotik", "cisco", "zyxel", "linksys", "huawei technologies", "juniper", "aruba"), "Infraestructura de red"),
    
    # IoT, Domótica y Sensores
    (("sonos", "nest", "ring", "shelly", "tuya", "dreame", "irobot", "philips", "belkin", "dyson"), "IoT / Domótica inteligente"),
    (("texas instruments", "silicon laboratories", "espressif"), "Chip IoT / Placa de desarrollo"),
    
    # Videovigilancia
    (("hikvision", "dahua", "axis", "reolink"), "Cámara de seguridad"),
    
    # Impresoras
    (("epson", "canon", "brother", "lexmark"), "Impresora de red")
]