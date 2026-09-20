'''
Pestaña "Tráfico": monitor en tiempo real de las conexiones de red
(TCP/UDP e ICMP) entrantes y salientes del dispositivo.
'''

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QColor
from src.core.conexiones import EventoConexion, EventoError, Sentido
from src.gui.hilos import HiloTrafico

MAXIMO_FILAS = 300  # evita que la tabla crezca de forma indefinida


class PestanaTrafico(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hilo_trafico = None
        self._construir_interfaz()

    def _construir_interfaz(self):
        layout = QVBoxLayout(self)

        barra = QHBoxLayout()
        self.boton_iniciar = QPushButton("▶ Iniciar captura")
        self.boton_detener = QPushButton("■ Detener captura")
        self.boton_detener.setEnabled(False)
        self.boton_iniciar.clicked.connect(self.iniciar_captura)
        self.boton_detener.clicked.connect(self.detener_captura)

        self.etiqueta_estado = QLabel("Captura detenida.")

        barra.addWidget(self.boton_iniciar)
        barra.addWidget(self.boton_detener)
        barra.addWidget(self.etiqueta_estado, stretch=1)

        self.tabla = QTableWidget(0, 6)
        self.tabla.setHorizontalHeaderLabels(
            ["Hora", "Protocolo", "Sentido", "IP remota", "PID", "Proceso"]
        )
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        nota = QLabel(
            "Nota: requiere permisos de administrador para capturar ICMP y "
            "asociar cada conexión a su proceso."
        )
        nota.setObjectName("nota")

        layout.addLayout(barra)
        layout.addWidget(self.tabla)
        layout.addWidget(nota)

    # CONTROL DE CAPTURA
    def iniciar_captura(self):
        self.boton_iniciar.setEnabled(False)
        self.boton_detener.setEnabled(True)
        self.etiqueta_estado.setText("Capturando tráfico...")

        self._hilo_trafico = HiloTrafico(espera_tcp_udp=2.0)
        self._hilo_trafico.evento_recibido.connect(self._procesar_evento)
        self._hilo_trafico.start()

    def detener_captura(self):
        if self._hilo_trafico is not None:
            hilo = self._hilo_trafico
            hilo.detener()
            # El generador del backend solo comprueba la señal de parada
            # al recibir un evento; si no hay tráfico en ese instante puede
            # tardar. Como red de seguridad, si no termina enseguida se
            # fuerza su finalización para no dejar hilos colgados al cerrar.
            if not hilo.wait(1500):
                hilo.terminate()
                hilo.wait(500)
            self._hilo_trafico = None

        self.boton_iniciar.setEnabled(True)
        self.boton_detener.setEnabled(False)
        self.etiqueta_estado.setText("Captura detenida.")

    # PROCESADO DE EVENTOS
    def _procesar_evento(self, evento):
        if isinstance(evento, EventoError):
            self.etiqueta_estado.setText(f"⚠ {evento}")
            return

        if isinstance(evento, EventoConexion):
            self._insertar_fila(evento)

    def _insertar_fila(self, evento: EventoConexion):
        self.tabla.insertRow(0)  # las conexiones más recientes, arriba
        valores = [
            evento.momento.strftime("%H:%M:%S"),
            evento.protocolo.value,
            evento.sentido.value,
            evento.ip_remota,
            evento.pid,
            evento.proceso,
        ]
        color = QColor("#c0392b") if evento.sentido == Sentido.ENTRANTE else QColor("#1f6f4a")
        for columna, valor in enumerate(valores):
            item = QTableWidgetItem(str(valor))
            item.setForeground(color)
            self.tabla.setItem(0, columna, item)

        while self.tabla.rowCount() > MAXIMO_FILAS:
            self.tabla.removeRow(self.tabla.rowCount() - 1)

    def cerrar(self):
        """Debe llamarse al cerrar la ventana para detener el hilo de captura."""
        self.detener_captura()
