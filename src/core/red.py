'''
Módulo dedicado a obtener información sobre la red.
'''

from src.utils import variables
from src.core import dispositivo
import psutil
import socket
import subprocess
import os
import re


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