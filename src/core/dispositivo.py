'''
Módulo dedicado a obtener la información de red del dispositivo.
'''

from src.utils import variables
import socket
import urllib.request
import errno
import psutil


# OBTENER LA IPv4 privada
def obtener_ip4_privada():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # AF_INET: estable el tipo de IP en v4
        # SOCK_DGRAM: define el protocolo de transporte en UDP
        s.connect(("8.8.8.8", 80))
        ip4_privada = s.getsockname()[0]
        s.close()
        return ip4_privada
    except Exception:
        return "Desconocida"

# OBTENER LA IPv4 PÚBLICA
def obtener_ip4_publica():
    try:
        respuesta = urllib.request.urlopen('https://4.ident.me', timeout=5)
        ip4_publica = respuesta.read().decode('utf8')
        return ip4_publica
    except Exception:
        return "Desconocida"


# OBTENER LA IPv6 privada
def obtener_ip6_privada():
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # AF_INET6: estable el tipo de IP en v6
        # SOCK_DGRAM: define el protocolo de transporte en UDP
        s.connect(("2001:4860:4860::8888", 80))
        # IPv6 de los servidores DNS de Google: 2001:4860:4860::8888
        ip6_privada = s.getsockname()[0]
        s.close()
        return ip6_privada
    except OSError as e:
        if e.errno in (errno.ENETUNREACH, 10051):
            return "IPv6 privada no asignada"
        else:
            return "Desconocida"
    except Exception:
            return "Desconocida"

# OBTENER LA IPv6 PÚBLICA
def obtener_ip6_publica():
    try:
        respuesta = urllib.request.urlopen('https://6.ident.me', timeout=5)
        ip6_publica = respuesta.read().decode('utf8')
        return ip6_publica
    except urllib.error.URLError as e:
        return "IPv6 pública no asignada"
    except Exception:
        return "Desconocida"


# OBTENER MACS
def obtener_mac_por_interfaz():
    interfaces = psutil.net_if_addrs()
    # net_if_addrs devuelve las direcciones asociadas a cada tarjeta de red.
    macs = {}

    if variables.SO == 'Linux':
        familia_mac = socket.AF_PACKET
    else:
        familia_mac = psutil.AF_LINK

    for interfaz, direcciones in interfaces.items():
        for direccion in direcciones:
            if direccion.family == familia_mac:
                macs[interfaz] = direccion.address

    return macs


# OBTENER PUERTOS ABIERTOS
def obtener_puertos_abiertos():
    puertos = []

    try: 
        conexiones = psutil.net_connections(kind='inet')
    except psutil.AccessDenied:
        return puertos

    for conn in conexiones:
        if conn.status == psutil.CONN_LISTEN:
            puerto = {
                'puerto': conn.laddr.port,
                'ip': conn.laddr.ip,
                'pid': conn.pid,
                'proceso': 'Desconocido'
            }

            if conn.pid is not None:
                try:
                    proceso = psutil.Process(conn.pid)
                    puerto['proceso'] = proceso.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    puerto['proceso'] = 'Protegido / Inaccesible'

            puertos.append(puerto)

    return sorted(puertos, key=lambda x: x['puerto'])



## CÓDIGO DE DEPURACIÓN ##

if __name__ == '__main__':
    print("_______________________________________")
    print("DEPURACIÓN DEL MÓDULO <<DISPOSITIVO>>")
    print("_______________________________________")

    print(f"SISTEMA OPERATIVO: {variables.SO}")

    print(f"> IPv4 LOCAL (PRIVADA): {obtener_ip4_privada()}")
    print(f"> IPv4 PÚBLICA: {obtener_ip4_publica()}")
    print(f"> IPv6 LOCAL (PRIVADA): {obtener_ip6_privada()}")
    print(f"> IPv6 PÚBLICA: {obtener_ip6_publica()}")

    print("> MACs ENCONTRADAS:")
    for interfaz,direccion in obtener_mac_por_interfaz().items():
        print("\t>> ",interfaz,": ", direccion)

    print("> PUERTOS ABIERTOS")
    for puerto in obtener_puertos_abiertos():
        for info in puerto.items():
            print("\t>> ",info)
        print("")
    