'''
Módulo dedicado a obtener la información de red del dispositivo.
'''

from src.utils import variables
import socket
import urllib.request
import errno


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
        respuesta = urllib.request.urlopen('https://ident.me', timeout=5)
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



## CÓDIGO DE DEPURACIÓN ##

if __name__ == '__main__':
    print("_______________________________________")
    print("DEPURACIÓN DEL MÓDULO <<DISPOSITIVO>>")
    print("_______________________________________")

    print(f"SISTEMA OPERATIVO: {variables.SO}")
    print(f"IPv4 LOCAL (PRIVADA): {obtener_ip4_privada()}")
    print(f"IPv4 PÚBLICA: {obtener_ip4_publica()}")
    print(f"IPv6 LOCAL (PRIVADA): {obtener_ip6_privada()}")
    print(f"IPv6 PÚBLICA: {obtener_ip6_publica()}")
    