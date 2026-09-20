'''
Hilos (QThread) encargados de ejecutar en segundo plano las funciones del
backend, que pueden bloquear (llamadas de red, subprocess, sockets...),
para no congelar nunca la interfaz gráfica.
'''

from PySide6.QtCore import QThread, Signal
from src.core import conexiones


class HiloTarea(QThread):
    """
    Hilo genérico para ejecutar una única función del backend y emitir
    su resultado al terminar. Sirve para cualquier llamada "de una vez"
    (obtener una IP, escanear la red, escanear puertos de un host...).
    """
    terminado = Signal(object)

    def __init__(self, funcion, *args, parent=None, **kwargs):
        super().__init__(parent)
        self._funcion = funcion
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            resultado = self._funcion(*self._args, **self._kwargs)
        except Exception as exc:
            resultado = {"_error": f"Error inesperado: {exc}"}
        self.terminado.emit(resultado)


class HiloTrafico(QThread):
    """
    Hilo que consume el generador monitorizar_trafico() del módulo
    conexiones.py y emite cada evento (EventoConexion o EventoError) a
    medida que llega, sin bloquear la interfaz.
    """
    evento_recibido = Signal(object)

    def __init__(self, espera_tcp_udp: float = 2.0, parent=None):
        super().__init__(parent)
        self._espera_tcp_udp = espera_tcp_udp
        self._detener = False

    def run(self):
        generador = conexiones.monitorizar_trafico(espera_tcp_udp=self._espera_tcp_udp)
        try:
            for evento in generador:
                if self._detener:
                    break
                self.evento_recibido.emit(evento)
        finally:
            # generador.close() dispara el "finally" interno de
            # monitorizar_trafico(), deteniendo los hilos de escucha.
            generador.close()

    def detener(self):
        self._detener = True
