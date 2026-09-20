'''
Pestaña "Dispositivo": muestra la información de red vital del equipo
(IPs públicas/privadas, MAC) y sus puertos locales abiertos.
'''

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from src.core import dispositivo
from src.gui.hilos import HiloTarea


class PestanaDispositivo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hilos = []  # referencias activas para que Qt no las destruya en marcha
        self._construir_interfaz()
        self.actualizar_todo()

    # INTERFAZ
    def _construir_interfaz(self):
        layout = QVBoxLayout(self)

        grupo_info = QGroupBox("Información de red")
        rejilla = QGridLayout(grupo_info)

        self.etiqueta_ip4_privada = self._crear_valor()
        self.etiqueta_ip4_publica = self._crear_valor()
        self.etiqueta_ip6_privada = self._crear_valor()
        self.etiqueta_ip6_publica = self._crear_valor()
        self.etiqueta_macs = self._crear_valor()
        self.etiqueta_macs.setWordWrap(True)

        rejilla.addWidget(QLabel("IPv4 privada:"), 0, 0)
        rejilla.addWidget(self.etiqueta_ip4_privada, 0, 1)
        rejilla.addWidget(QLabel("IPv4 pública:"), 1, 0)
        rejilla.addWidget(self.etiqueta_ip4_publica, 1, 1)
        rejilla.addWidget(QLabel("IPv6 privada:"), 2, 0)
        rejilla.addWidget(self.etiqueta_ip6_privada, 2, 1)
        rejilla.addWidget(QLabel("IPv6 pública:"), 3, 0)
        rejilla.addWidget(self.etiqueta_ip6_publica, 3, 1)
        rejilla.addWidget(QLabel("Direcciones MAC:"), 4, 0, Qt.AlignmentFlag.AlignTop)
        rejilla.addWidget(self.etiqueta_macs, 4, 1)
        rejilla.setColumnStretch(1, 1)

        boton_actualizar_info = QPushButton("Actualizar información")
        boton_actualizar_info.clicked.connect(self.actualizar_info_dispositivo)

        layout.addWidget(grupo_info)
        layout.addWidget(boton_actualizar_info)

        grupo_puertos = QGroupBox("Puertos locales abiertos")
        layout_puertos = QVBoxLayout(grupo_puertos)

        barra_puertos = QHBoxLayout()
        self.boton_actualizar_puertos = QPushButton("Actualizar puertos")
        self.boton_actualizar_puertos.clicked.connect(self.actualizar_puertos)
        self.etiqueta_estado_puertos = QLabel("")
        barra_puertos.addWidget(self.boton_actualizar_puertos)
        barra_puertos.addWidget(self.etiqueta_estado_puertos)
        barra_puertos.addStretch()

        self.tabla_puertos = QTableWidget(0, 4)
        self.tabla_puertos.setHorizontalHeaderLabels(["Puerto", "IP local", "PID", "Proceso"])
        self.tabla_puertos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_puertos.verticalHeader().setVisible(False)
        self.tabla_puertos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_puertos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        nota = QLabel(
            "Nota: en Linux y Windows puede ser necesario ejecutar la aplicación "
            "como administrador para ver todos los procesos asociados."
        )
        nota.setObjectName("nota")
        nota.setWordWrap(True)

        layout_puertos.addLayout(barra_puertos)
        layout_puertos.addWidget(self.tabla_puertos)
        layout_puertos.addWidget(nota)
        layout.addWidget(grupo_puertos, stretch=1)

    def _crear_valor(self):
        etiqueta = QLabel("Cargando...")
        etiqueta.setObjectName("valorInfo")
        return etiqueta

    # LÓGICA
    def actualizar_todo(self):
        self.actualizar_info_dispositivo()
        self.actualizar_puertos()

    def _lanzar(self, funcion, callback, *args):
        hilo = HiloTarea(funcion, *args)
        hilo.terminado.connect(callback)
        hilo.finished.connect(lambda: self._hilos.remove(hilo) if hilo in self._hilos else None)
        self._hilos.append(hilo)
        hilo.start()

    def actualizar_info_dispositivo(self):
        self._lanzar(dispositivo.obtener_ip4_privada, self.etiqueta_ip4_privada.setText)
        self._lanzar(dispositivo.obtener_ip4_publica, self.etiqueta_ip4_publica.setText)
        self._lanzar(dispositivo.obtener_ip6_privada, self.etiqueta_ip6_privada.setText)
        self._lanzar(dispositivo.obtener_ip6_publica, self.etiqueta_ip6_publica.setText)
        self._lanzar(dispositivo.obtener_mac_por_interfaz, self._mostrar_macs)

    def _mostrar_macs(self, macs: dict):
        if not macs:
            self.etiqueta_macs.setText("No se han encontrado interfaces.")
            return
        texto = "\n".join(f"{interfaz}: {mac}" for interfaz, mac in macs.items())
        self.etiqueta_macs.setText(texto)

    def actualizar_puertos(self):
        self.boton_actualizar_puertos.setEnabled(False)
        self.etiqueta_estado_puertos.setText("Escaneando...")
        self._lanzar(dispositivo.obtener_puertos_abiertos, self._mostrar_puertos)

    def _mostrar_puertos(self, puertos: list):
        self.boton_actualizar_puertos.setEnabled(True)
        self.etiqueta_estado_puertos.setText(f"{len(puertos)} puerto(s) encontrados.")

        self.tabla_puertos.setSortingEnabled(False)
        self.tabla_puertos.setRowCount(0)
        for puerto in puertos:
            fila = self.tabla_puertos.rowCount()
            self.tabla_puertos.insertRow(fila)
            self.tabla_puertos.setItem(fila, 0, QTableWidgetItem(str(puerto.get("puerto", ""))))
            self.tabla_puertos.setItem(fila, 1, QTableWidgetItem(str(puerto.get("ip", ""))))
            pid = puerto.get("pid")
            self.tabla_puertos.setItem(fila, 2, QTableWidgetItem(str(pid) if pid is not None else "-"))
            self.tabla_puertos.setItem(fila, 3, QTableWidgetItem(str(puerto.get("proceso", ""))))
