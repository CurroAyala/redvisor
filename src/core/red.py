'''
Módulo dedicado a obtener información sobre la red.
'''

from src.utils import variables, equivalencias, servicios
from src.core import dispositivo
import psutil
import socket
import subprocess
import os
import re
import ipaddress
import csv
import concurrent.futures


# OBTENER EL NOMBRE (SSID) DE LA RED WIFI
def obtener_ssid():
    try: 
        if variables.SO == 'Linux':
            # Se fuerza el idioma del entorno para tratar la salida
            entorno = os.environ.copy()
            entorno['LC_ALL'] = 'C' # Inglés


            salida_comando = subprocess.check_output(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'], text=True, env=entorno)
            for linea in salida_comando.split('\n'):
                if linea.startswith('yes:'):
                    return linea.split(':')[1].strip()
            return "Conexión por cable / Desconectado"
        
        elif variables.SO == 'Windows':
            salida_comando = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], text=True)
            for linea in salida_comando.split('\n'):
                if " SSID " in linea and "BSSID" not in linea:
                    return linea.split(':')[1].strip()
            return "Conexión por cable / Desconectado"
    except Exception:
        return "Desconectado"


# OBTENER LA MÁSCARA DE LA RED
def obtener_mascara_red():
    # Primero, se obtiene la IP local
    ip_local = dispositivo.obtener_ip4_privada()

    if ip_local != 'Desconocida':
        interfaces = psutil.net_if_addrs()
        for interfaz, direcciones in interfaces.items():
            for direccion in direcciones:
                if direccion.family == socket.AF_INET and direccion.address == ip_local:
                    return direccion.netmask

    return "Desconectado"


# OBTENER PROTOCOLO DE CIFRADO PARA CONEXIONES WIFI
def obtener_seguridad_wifi():
    try:
        if variables.SO == 'Linux':
            entorno = os.environ.copy()
            entorno['LC_ALL'] = 'C'
            
            salida_comando = subprocess.check_output(
                ['nmcli', '-t', '-f', 'active,security', 'dev', 'wifi'], 
                text=True, env=entorno
            )
            for linea in salida_comando.split('\n'):
                if linea.startswith('yes:'):
                    seguridad = linea.split(':')[1].strip()
                    return seguridad if seguridad else "Sin cifrado"
            return "Conexión por cable / Desconectado"
            
        elif variables.SO == 'Windows':
            salida_comando = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], text=True)
            
            patron = r'(WPA3?-Personal|WPA3?-Enterprise|WPA2?-Personal|WPA2?-Enterprise|WPA-Personal|WPA-Enterprise|WEP|802\.1X)'
            match = re.search(patron, salida_comando, re.IGNORECASE)
            
            if match:
                return match.group(1).upper()
            
            if " BSSID " in salida_comando:
                return "Sin cifrado"
                
            return "Conexión por cable / Desconectado"
            
    except Exception:
        return "Desconectado"

# EVALUAR EL PROTOCOLO DE CIFRADO
def evaluar_seguridad(protocolo):
    protocolo_upper = protocolo.upper()
    
    if "SIN CIFRADO" in protocolo_upper or "WEP" in protocolo_upper:
        return {
            "riesgo": "Crítico",
            "color": "red",
            "descripcion": "Tráfico sin cifrar o cifrado obsoleto."
        }
        
    elif "WPA2" not in protocolo_upper and "WPA3" not in protocolo_upper and "WPA" in protocolo_upper:
        return {
            "riesgo": "Alto",
            "color": "orange",
            "descripcion": "Cifrado obsoleto."
        }
    
    elif "WPA2" in protocolo_upper:
        return {
            "riesgo": "Bajo",
            "color": "green",
            "descripcion": "Estándar seguro."
        }
        
    elif "WPA3" in protocolo_upper:
        return {
            "riesgo": "Mínimo",
            "color": "darkgreen",
            "descripcion": "Máxima seguridad actual."
        }
        
    elif "CABLE" in protocolo_upper:
        return {
            "riesgo": "Físico",
            "color": "gray",
            "descripcion": "Conexión Ethernet o desconectado de la red."
        }
        
    # 6. Desconocido o fallos
    return {
        "riesgo": "Desconocido",
        "color": "yellow",
        "descripcion": f"Protocolo no reconocido: ({protocolo})."
    }



## ESCANEO DE RED ##

# CONSTANTES
MAX_HOSTS_DESCUBRIMIENTO            = 512
MAX_HILOS_DESCUBRIMIENTO            = 200
PUERTOS_DESCUBRIMIENTO              = [80, 443, 22, 445, 139, 8080]
TIMEOUT_CONEXION_DESCUBRIMIENTO     = 0.25
TIMEOUT_TOTAL_DESCUBRIMIENTO        = 25

TIMEOUT_BANNER                      = 1.0
TIMEOUT_CONEXION_PUERTO             = 0.6
MAX_HILOS_ESCANEO_PUERTOS           = 100
PUERTOS_ESCANEO = [
    21, 22, 23, 25, 53, 67, 68, 69, 80, 88, 110, 111, 123, 135, 137, 138,
    139, 143, 161, 162, 179, 389, 443, 445, 465, 514, 515, 548, 554, 587,
    631, 636, 873, 993, 995, 1080, 1194, 1433, 1521, 1723, 1883, 2049,
    2181, 3000, 3128, 3268, 3306, 3389, 3690, 4443, 5000, 5060, 5432,
    5601, 5900, 5985, 5986, 6379, 6443, 6667, 7001, 7070, 7077, 7443,
    8000, 8008, 8080, 8081, 8086, 8088, 8090, 8443, 8888, 9000, 9042,
    9090, 9092, 9200, 9300, 9418, 10000, 11211, 15672, 27017, 27018, 32400
]
TIMEOUT_TOTAL_ESCANEO_PUERTOS       = 25


# MÉTODOS AUXILIARES
def _obtener_red_local():
    """
    Determina la red local (w.x.y.z/a) a partir de la IP privada y
    la máscara de red.
    Devuelve un objeto ipaddress.IPv4Network o None si no se puede determinar.
    """
    ip_local = dispositivo.obtener_ip4_privada()
    mascara = obtener_mascara_red()
 
    if ip_local == "Desconocida" or mascara == "Desconectado":
        return None
 
    try:
        return ipaddress.IPv4Interface(f"{ip_local}/{mascara}").network
    except ValueError:
        return None

def _limitar_rango_red(red):
    """
    Para aevitar desbordamientos, si la red local contiene mas direcciones
    de las que se consideran seguras de escanear de una sola vez
    (MAX_HOSTS_DESCUBRIMIENTO), se recorta a una subred mas pequeña que
    incluya la IP del equipo.

    Devuelve una tupla (red_a_escanear, fue_recortada: bool).
    """
    total_direcciones = red.num_addresses
 
    if total_direcciones <= MAX_HOSTS_DESCUBRIMIENTO:
        return red, False
 
    # Cálculo del prefijo minimo necesario para no superar el limite
    bits_host = max(1, (MAX_HOSTS_DESCUBRIMIENTO - 1).bit_length())
    nuevo_prefijo = min(32 - bits_host, 32)
 
    ip_local = dispositivo.obtener_ip4_privada()
    red_recortada = ipaddress.ip_interface(f"{ip_local}/{nuevo_prefijo}").network
 
    return red_recortada, True

def _host_vivo(ip):
    """
    Comprueba si un host responde en alguno de los PUERTOS_DESCUBRIMIENTO.
    Tanto si la conexion se establece (puerto abierto) como si es
    rechazada activamente (puerto cerrado, pero el host contesta), se
    considera que el host existe. Si ningun puerto responde en el tiempo
    dado, se asume que no hay dispositivo en esa IP (o esta detrás de un
    firewall que descarta todo).
    """
    for puerto in PUERTOS_DESCUBRIMIENTO:
        try:
            with socket.create_connection((ip, puerto), timeout=TIMEOUT_CONEXION_DESCUBRIMIENTO):
                return True
        except ConnectionRefusedError:
            return True
        except OSError:
            continue
    return False

def _leer_tabla_arp():
    """
    Devuelve un diccionario {ip: mac} a partir de la tabla ARP del propio
    sistema. Para que otro dispositivo aparezca aquí, el equipo debe haberle
    hablado antes (esto ocurre en el escaneo de dispositivos).
    """
    tabla = {}
 
    try:
        if variables.SO == 'Linux':
            with open('/proc/net/arp', 'r') as f:
                lineas = f.readlines()[1:]
            for linea in lineas:
                columnas = linea.split()
                if len(columnas) >= 4:
                    ip, mac = columnas[0], columnas[3]
                    if mac != '00:00:00:00:00:00':
                        tabla[ip] = mac.upper()
 
        elif variables.SO == 'Windows':
            salida = subprocess.check_output(['arp', '-a'], text=True)
            for linea in salida.split('\n'):
                coincidencia = re.match(r'\s*(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})', linea)
                if coincidencia:
                    ip = coincidencia.group(1)
                    mac = coincidencia.group(2).replace('-', ':').upper()
                    tabla[ip] = mac
    except Exception:
        pass
 
    return tabla

def _cargar_tabla_fabricantes():
    """
    A partir del archivo <oui.csv> (IEEE), devuelve un diccionario
    que relaciona el código OUI (primera mitad de la dirección MAC)
    con un fabricante.
    """
    tabla = {}

    directorio_src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_csv = os.path.join(directorio_src, 'utils', 'oui.csv')
    if os.path.isfile(ruta_csv):
        try:
            with open(ruta_csv, newline='', encoding='utf-8', errors='ignore') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    prefijo = fila.get('Assignment', '').strip().upper()
                    nombre = fila.get('Organization Name', '').strip()
                    if len(prefijo) == 6 and nombre:
                        tabla[prefijo] = nombre
        except Exception:
            pass
 
    return tabla

TABLA_FABRICANTES = _cargar_tabla_fabricantes()

def _obtener_fabricante(mac):
    """
    Devuelve el nombre del fabricante asociado al OUI de una MAC.
    """
    if not mac:
        return "Desconocido"
 
    oui = mac.upper().replace(':', '').replace('-', '')[:6]
    if oui[1] in '26AE': # detectar si es una MAC aleatoria
        return "MAC generada aleatoriamente"

    return TABLA_FABRICANTES.get(oui, "Desconocido")

def _aproximar_so(fabricante):
    """
    Traduce el fabricante de la tarjeta de red a una aproximacion del tipo
    de sistema operativo o dispositivo.
    No tratar como dato fiable.
    """
    if fabricante == "Desconocido":
        return "Desconocido"
 
    nombre = fabricante.lower()
 
    for claves, resultado in equivalencias.CLASIFICACION_FABRICANTES:
        if any(clave in nombre for clave in claves):
            return resultado
 
    return f"Desconocido (fabricante: {fabricante})"


def _banner_grabbing(sock):
    """
    Intenta identificar el servicio de un puerto ya abierto:
      1. Escucha pasivamente un breve instante por si el servicio envía un
         banner nada más conectar (SSH, FTP, SMTP, POP3, IMAP...).
      2. Si no llega nada, envia una peticion HTTP mínima por si se trata
         de un servidor web, y lee la cabecera 'Server' de la respuesta.
    Devuelve el texto encontrado, o None si no se ha podido identificar.
    """
    try:
        sock.settimeout(TIMEOUT_BANNER)
        datos = sock.recv(256) # banner grabbing pasivo
        if datos:
            return datos.decode(errors='ignore').strip().splitlines()[0][:120]
    except socket.timeout:
        pass
    except OSError:
        return None
 
    try: # banner grabbing activo
        sock.sendall(b'HEAD / HTTP/1.0\r\n\r\n')
        sock.settimeout(TIMEOUT_BANNER)
        datos = sock.recv(512).decode(errors='ignore')
        for linea in datos.split('\r\n'):
            if linea.lower().startswith('server:'):
                return linea.split(':', 1)[1].strip()
        if datos.startswith('HTTP/'):
            return "Servidor HTTP (sin cabecera 'Server')"
    except OSError:
        pass
 
    return None

def _analizar_puerto(ip, puerto):
    """Comprueba un unico puerto TCP: si esta abierto, intenta identificar el servicio."""
    try:
        with socket.create_connection((ip, puerto), timeout=TIMEOUT_CONEXION_PUERTO) as sock:
            banner = _banner_grabbing(sock)
    except OSError:
        return None
 
    return {
        "puerto": puerto,
        "protocolo": "tcp",
        "servicio": servicios.SERVICIOS_CONOCIDOS.get(puerto, "Desconocido"),
        "banner": banner
    }


# DESCRUBIMIENTO DE DISPOSITIVOS
def escanear_dispositivos():
    """
    Realiza un barrido TCP para descubrir los dispositivos activos en la red local,
    aproximando el tipo de dispositivo o SO a partir del fabricante.
    Devuelve un diccionario con la forma:
        {
            "<ip>": {
                "ip": "<ip>",
                "mac": "<mac o 'Desconocida'>",
                "fabricante": "<fabricante o 'Desconocido'>",
                "sistema_operativo": "<aproximacion>"
            },
            ...
            # Claves opcionales de control (no representan dispositivos):
            "_error": "<mensaje si algo ha fallado>",
            "_aviso": "<mensaje si la red se ha recortado por ser muy grande>"
        }
    """
    dispositivos = {}

    red_local = _obtener_red_local()

    if red_local is None:
        dispositivos["_error"] = "No se ha podido determinar la red local."
        return dispositivos

    red_a_escanear, recortada = _limitar_rango_red(red_local)
    candidatos = [str(ip) for ip in red_a_escanear.hosts()]
 
    ips_vivas = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_HILOS_DESCUBRIMIENTO)
    try:
        futuros = {executor.submit(_host_vivo, ip): ip for ip in candidatos}
        completados, _pendientes = concurrent.futures.wait(
            futuros, timeout=TIMEOUT_TOTAL_DESCUBRIMIENTO
        )
        for futuro in completados:
            try:
                if futuro.result():
                    ips_vivas.append(futuros[futuro])
            except Exception:
                pass
    finally:
        executor.shutdown(wait=False)
 
    tabla_arp = _leer_tabla_arp()
 
    for ip in ips_vivas:
        mac = tabla_arp.get(ip)
        fabricante = _obtener_fabricante(mac)
        dispositivos[ip] = {
            "ip": ip,
            "mac": mac if mac else "Desconocida",
            "fabricante": fabricante,
            "sistema_operativo": _aproximar_so(fabricante)
        }
 
    if recortada:
        dispositivos["_aviso"] = (
            f"La red detectada supera los {MAX_HOSTS_DESCUBRIMIENTO} dispositivos; "
            f"el escaneo se ha limitado a la subred {red_a_escanear} para evitar sobrecargas."
        )
 
    return dispositivos


# ESCANEO DE PUERTOS
def escanear_puertos_dispositivo(ip):
    """
    Dado un dispositivo de la red (por IP), escanea sus puertos TCP más
    habituales e intenta identificar el servicio que aloja cada uno.
 
    Devuelve una lista de diccionarios con la forma:
        [
            {
                "puerto": 22,
                "protocolo": "tcp",
                "servicio": "ssh",
                "banner": "SSH-2.0-OpenSSH_8.4p1"
            },
            ...
        ]
    o una lista vacía si la IP no es válida, el host no responde en ningún
    puerto comprobado, o todos estan cerrados/filtrados.
    """
    puertos_abiertos = []
 
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return puertos_abiertos
 
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_HILOS_ESCANEO_PUERTOS)
    try:
        futuros = [executor.submit(_analizar_puerto, ip, puerto) for puerto in PUERTOS_ESCANEO]
        completados, _pendientes = concurrent.futures.wait(
            futuros, timeout=TIMEOUT_TOTAL_ESCANEO_PUERTOS
        )
        for futuro in completados:
            try:
                resultado = futuro.result()
                if resultado is not None:
                    puertos_abiertos.append(resultado)
            except Exception:
                pass
    finally:
        executor.shutdown(wait=False)
 
    return sorted(puertos_abiertos, key=lambda p: p['puerto'])




## CÓDIGO DE DEPURACIÓN ##

if __name__ == '__main__':
    print("_______________________________________")
    print("DEPURACIÓN DEL MÓDULO <<RED>>")
    print("_______________________________________")

    print(f"> NOMBRE DE LA RED: {obtener_ssid()}")
    print(f"> MÁSCARA DE RED: {obtener_mascara_red()}")
    protocolo = obtener_seguridad_wifi()
    print(f"> PROTOCOLO DE CIFRADO (WIFI): {protocolo}")
    print(f"> EVALUACIÓN DEL PROTOCOLO: {evaluar_seguridad(protocolo)}")

    print("> ESCANEO DE RED:")
    for clave, valor in escanear_dispositivos().items():
        print(f"\t>> {clave}:")
        for _clave, _valor in valor.items():
            print(f"\t\t>>> {_clave}: {_valor if _valor!="Desconocida" else "Este dispositivo"}")

    ip = str(input("> IP A ESCANEAR: "))
    print(f"> ESCANEO DEL DISPOSITIVO <{ip}>")
    puertos = escanear_puertos_dispositivo(ip)
    print(puertos)
    for puerto in puertos:
        print(f"\t>> PUERTO {puerto.get("puerto")}")
        print(f"\t\t>>> PROTOCOLO: {puerto.get("protocolo")}")
        print(f"\t\t>>> SERVICIO: {puerto.get("servicio")}")
        print(f"\t\t>>> BANNER: {puerto.get("banner")}")