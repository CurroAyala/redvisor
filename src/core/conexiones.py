'''
Módulo dedicado a monitorizar en tiempo real el tráfico de red del
dispositivo, mediante sondeo (polling) con psutil y socket.
'''

from typing import Any, Union
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from src.core.dispositivo import obtener_puertos_abiertos
from src.utils.variables import SO
import socket
import psutil
import queue
import threading
import struct


## CLASES AUXILIARES ##
class Protocolo(str, Enum):
    TCP_UDP = "TCP/UDP"
    ICMP = "ICMP"

class Sentido(str, Enum):
    """
    Sentido de la conexión
    """
    ENTRANTE = "ENTRANTE"
    SALIENTE = "SALIENTE"

@dataclass(frozen=True) 
# Frozen = True evita que un objeto de este tipo pueda ser modificado
class EventoConexion:
    """
    Evento para representar una única conexión detectada.
    """
    momento: datetime
    protocolo: Protocolo
    sentido: Sentido
    ip_remota: str
    pid: str = ""
    proceso: str = "Desconocido"

    def __str__(self) -> str:
        return (
            f"[{self.momento:%H:%M:%S}] ({self.protocolo.value}) {self.sentido.value}"
            f" - IP remota: {self.ip_remota} PID: {self.pid} (Proceso: {self.proceso})"
        )

@dataclass(frozen=True) 
class EventoError:
    """
    Evento para informar sobre fallos.
    """
    momento: datetime
    protocolo: Protocolo
    mensaje: str

    def __str__(self) -> str:
        return f"[{self.momento:%H:%M:%S}] ADVERTENCIA ({self.protocolo.value}): {self.mensaje}"

Evento = Union[EventoConexion, EventoError]



## CAPTURA DE TRÁFICO TCP / UDP (capa de transporte) ##

# MÉTODOS AUXILIARES
def _parsear_conexion(conn:Any): 
    # Any porque el tipo <conn> es privado de la biblioteca psutil
    """
    Devuelve una tupla con los valores de una conexión:
        - IP local: string
        - Puerto local: int
        - IP remota: string
        - Puerto remoto: int
        - Protocolo: string
    Devuelve None si la conexión no tiene IP remota.
    """
    if not conn.raddr or not conn.laddr:
        return None

    protocolo = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
    return (conn.laddr.ip, conn.laddr.port, conn.raddr.ip, conn.raddr.port, protocolo)

def _escanear_puertos():
    """
    Devuelve el conjunto de conexiones de tipo ESTABLISHED en este instante.
    """
    conexiones = set()
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_ESTABLISHED:
            conexion = _parsear_conexion(conn)
            if conexion: conexiones.add(conexion)

    return conexiones

def _localizar_proceso(
        ip_local: str, puerto_local: int, ip_remota: str, puerto_remoto: int):
    """
    Asocia un pid y el nombre de su proceso a una conexión detectada.
    """
    try:
        for conn in psutil.net_connections(kind='inet'):
            if (
                conn.raddr
                and conn.laddr
                and conn.laddr.ip == ip_local
                and conn.laddr.port == puerto_local
                and conn.raddr.ip == ip_remota
                and conn.raddr.port == puerto_remoto
            ):
                if conn.pid is None:
                    return None, "Desconocido"
                try:
                    return conn.pid, psutil.Process(conn.pid).name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return conn.pid, "Inaccesible"
    except psutil.AccessDenied:
        pass
    return None


# MÉTODO PRINCIPAL (TCP y UDP)
def monitorizar_puertos(
    cola: queue.Queue[Evento], 
    evento_parada: threading.Event,
    espera: float = 1.0): # espera de 1 segundo por defecto
    """
    Escanea los puertos abiertos en busca de conexiones TCP o UDP
    que se establecen a partir del momento en el que se inicia
    la captura.
    """

    try:
        conexiones_previas = _escanear_puertos()
    except psutil.AccessDenied:
        cola.put(EventoError(
            momento=datetime.now(),
            protocolo=Protocolo.TCP_UDP,
            mensaje="Permiso denegado al leer conexiones de red."
        ))
        return
    except Exception as exc:
        cola.put(EventoError(
            momento=datetime.now(),
            protocolo=Protocolo.TCP_UDP,
            mensaje=f"Error inesperado: {exc}"
        ))

    while not evento_parada.is_set():
        evento_parada.wait(timeout=espera)
        if evento_parada.is_set():
            break

        try:
            conexiones_actuales = _escanear_puertos()
            puertos_abiertos = {p["puerto"] for p in obtener_puertos_abiertos()}
        except psutil.AccessDenied:
            cola.put(EventoError(
                momento=datetime.now(),
                protocolo=Protocolo.TCP_UDP,
                mensaje="Permiso denegado al obtener los permisos abiertos."
            ))
            return
        except Exception as exc:
            cola.put(EventoError(
                momento=datetime.now(),
                protocolo=Protocolo.TCP_UDP,
                mensaje=f"Error inesperado: {exc}"
            ))
            continue

        nuevas_conexiones = conexiones_actuales - conexiones_previas

        for ip_local, puerto_local, ip_remota, puerto_remoto, protocolo in nuevas_conexiones:
            sentido = Sentido.ENTRANTE if puerto_local in puertos_abiertos else Sentido.SALIENTE
            pid_asociado, proceso_asociado = _localizar_proceso(ip_local, puerto_local, ip_remota, puerto_remoto)

            cola.put(EventoConexion(
                momento=datetime.now(),
                protocolo=Protocolo.TCP_UDP,
                sentido=sentido,
                ip_remota=ip_remota,
                pid=pid_asociado,
                proceso=proceso_asociado
            ))

        conexiones_previas = conexiones_actuales



## CAPTURA DE TRÁFICO ICMP (capa de red) CON sockets ##

# CONSTANTES
_ICMP_ECHO_REQUEST = 8
_ICMP_ECHO_REPLY = 0
_ICMP_TIPOS = {
    0: "Echo replay",
    3: "Destination unreachable",
    5: "Redirect",
    8: "Echo request",
    11: "Time exceeded"
}


# MÉTODOS AUXILIARES
def _parsear_paquete_icmp(datos:bytes):
    '''
    Extrae (tipo_icmp, codigo_icmp, descripcion) de un datagrama IP crudo que
    contiene un mensaje ICMP.
    Devuelve None si el paquete es demasiado corto o no puede interpretarse.
    '''
    if len(datos) < 20:
        return None

    
    # Se alcula la longitud de la cabecera IP (IHL) en bytes y se valida que el 
    # paquete no esté cortado: debe contener la cabecera completa más, al menos,
    # 8 bytes de la capa de transporte. Si no, lo descarta.
    ihl = (datos[0] & 0x0F) * 4
    if len(datos) < ihl + 8:
        return None

    tipo_icmp, codigo_icmp = struct.unpack("!BB", datos[ihl:ihl + 2])
    descripcion = _ICMP_TIPOS.get(tipo_icmp, f"Tipo {tipo_icmp}")
    return tipo_icmp, codigo_icmp, descripcion

def _crear_socket_icmp():
    '''
    Crea una conexión de red a bajo nivel (raw socket) que se salta los procesos
    automáticos del sistema operativo, devolviendo la información "en crudo".
    El socket se incializa para capturar los mensajes ICMP.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    if  SO == "Windows":
        ip_local = socket.gethostbyname(socket.gethostname())
        sock.bind((ip_local, 0))
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    else:
        sock.bind(("0.0.0.0", 0))

    sock.settimeout(1.0)
    return sock


# MÉTODO PRINCIPAL (ICMP)
def monitorizar_icmp(
    cola: queue.Queue[Evento],
    evento_parada: threading.Event):
    """
    Abre un raw socket para capturar de forma continua los paquetes ICMP.
    """
    try:
        sock = _crear_socket_icmp()
    except PermissionError:
        cola.put(EventoError(
            momento=datetime.now(),
            protocolo=Protocolo.ICMP,
            mensaje="Acceso denegado al abrir socket ICMP."
        ))
        return
    except OSError as exc:
        cola.put(EventoError(
            momento=datetime.now(),
            protocolo=Protocolo.ICMP,
            mensaje=f"Error inesperado al abrir socket ICMP: {exc}."
        ))

    try:
        while not evento_parada.is_set():
            try:
                datos, direccion_origen = sock.recvfrom(65535)
                # lee los datos entrantes, hasta 65535 bytes
            except socket.timeout:
                continue
            except OSError as exc:
                cola.put(EventoError(
                    momento=datetime.now(),
                    protocolo=Protocolo.ICMP,
                    mensaje=f"Error de lectura: {exc}"
                ))
                break

            paquete = _parsear_paquete_icmp(datos)
            if paquete is None:
                continue
            tipo_icmp, _codigo, _descripcion = paquete

            if tipo_icmp not in (_ICMP_ECHO_REQUEST,_ICMP_ECHO_REPLY):
                continue

            if tipo_icmp == _ICMP_ECHO_REQUEST:
                sentido=Sentido.ENTRANTE
            else:
                sentido=Sentido.SALIENTE

            cola.put(EventoConexion(
                momento=datetime.now(),
                protocolo=Protocolo.ICMP,
                sentido=sentido,
                ip_remota=direccion_origen[0],
                proceso="Sistema"
            ))
    finally:
        if SO == "Windows":
            try:
                sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            except OSError:
                pass
        sock.close()



## ORQUESTADOR ##
'''
El orquestador aúna la monitorización de ambas capas (TCP/UDP e ICMP).
'''
def monitorizar_trafico(espera_tcp_udp: float = 2.0):
    cola = queue.Queue()
    evento_parada = threading.Event()

    hilo_tcp_udp = threading.Thread(
        target=monitorizar_puertos, args=(cola, evento_parada, espera_tcp_udp),
        name="Monitorizar puertos", daemon=True
    )
    hilo_icmp = threading.Thread(
        target=monitorizar_icmp, args=(cola,evento_parada),
        name="Monitorizar ICMP", daemon=True
    )
    # daemon=True manda ese hilo a segundo plano

    hilo_tcp_udp.start()
    hilo_icmp.start()

    try:
        while True:
            try:
                evento = cola.get(timeout=0.5)
            except queue.Empty:
                continue
            yield evento # devuelve el valor sin destruir el método
    finally:
        evento_parada.set()
        hilo_tcp_udp.join(timeout=2.0)
        hilo_icmp.join(timeout=2.0)




## CÓDIGO DE DEPURACIÓN ##
if __name__ == "__main__":
    print("_______________________________________")
    print("DEPURACIÓN DEL MÓDULO <<TRAFICO>>")
    print("_______________________________________")
    print("Pulsar Ctrl+C para detener.\n")

    generador = monitorizar_trafico(espera_tcp_udp=2.0)
    try:
        for evento in generador:
            print(evento)
    except KeyboardInterrupt:
        print("\nMonitorización detenida por el usuario.")
    finally:
        generador.close()
