'''
Pestaña "Red": información de la red local (Wi-Fi o cableada), con
evaluación visual de seguridad, y escáner de dispositivos conectados
a la misma red (con escaneo de puertos por dispositivo).
'''

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog,
    QProgressBar, QMessageBox
)
from src.core import red
from src.gui.hilos import HiloTarea


class DialogoPuertosDispositivo(QDialog):
    """
    Ventana emergente que lanza y muestra el resultado del escaneo de
    puertos de un dispositivo remoto de la red (puede tardar hasta
    unos 25 segundos, según red.TIMEOUT_TOTAL_ESCANEO_PUERTOS).
    """

    def __init__(self, ip: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Puertos de {ip}")
        self.resize(520, 420)
        self._hilo = None

        layout = QVBoxLayout(self)

        self.etiqueta_estado = QLabel(
            f"Escaneando puertos de {ip}... (puede tardar hasta 25 segundos)"
        )
        self.etiqueta_estado.setWordWrap(True)

        self.barra_progreso = QProgressBar()
        self.barra_progreso.setRange(0, 0)  # indeterminado

        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(["Puerto", "Protocolo", "Servicio", "Banner"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.clicked.connect(self.close)

        layout.addWidget(self.etiqueta_estado)
        layout.addWidget(self.barra_progreso)
        layout.addWidget(self.tabla)
        layout.addWidget(boton_cerrar)

        self._escanear(ip)

    def _escanear(self, ip):
        self._hilo = HiloTarea(red.escanear_puertos_dispositivo, ip)
        self._hilo.terminado.connect(self._mostrar_resultado)
        self._hilo.start()

    def _mostrar_resultado(self, puertos: list):
        self.barra_progreso.hide()
        if not puertos:
            self.etiqueta_estado.setText(
                "No se han encontrado puertos abiertos (o el dispositivo no responde)."
            )
            return

        self.etiqueta_estado.setText(f"{len(puertos)} puerto(s) abierto(s) encontrados:")
        for puerto in puertos:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(puerto.get("puerto", ""))))
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(puerto.get("protocolo", ""))))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(puerto.get("servicio", ""))))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(puerto.get("banner") or "-")))


class PestanaRed(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hilos = []
        self._construir_interfaz()
        self.actualizar_info_red()

    # INTERFAZ
    def _construir_interfaz(self):
        layout = QVBoxLayout(self)

        grupo_info = QGroupBox("Red actual")
        rejilla = QGridLayout(grupo_info)

        self.etiqueta_ssid = QLabel("Cargando...")
        self.etiqueta_mascara = QLabel("Cargando...")
        self.etiqueta_seguridad = QLabel("Cargando...")
        self.etiqueta_riesgo = QLabel("")
        self.etiqueta_riesgo.setObjectName("insignia")

        rejilla.addWidget(QLabel("Red (SSID):"), 0, 0)
        rejilla.addWidget(self.etiqueta_ssid, 0, 1)
        rejilla.addWidget(QLabel("Máscara de red:"), 1, 0)
        rejilla.addWidget(self.etiqueta_mascara, 1, 1)
        rejilla.addWidget(QLabel("Cifrado:"), 2, 0)
        rejilla.addWidget(self.etiqueta_seguridad, 2, 1)
        rejilla.addWidget(QLabel("Nivel de riesgo:"), 3, 0)
        rejilla.addWidget(self.etiqueta_riesgo, 3, 1)
        rejilla.setColumnStretch(1, 1)

        boton_actualizar_red = QPushButton("Actualizar información de red")
        boton_actualizar_red.clicked.connect(self.actualizar_info_red)

        layout.addWidget(grupo_info)
        layout.addWidget(boton_actualizar_red)

        grupo_escaner = QGroupBox("Escáner de red")
        layout_escaner = QVBoxLayout(grupo_escaner)

        barra_escaner = QHBoxLayout()
        self.boton_escanear_red = QPushButton("Escanear red")
        self.boton_escanear_red.clicked.connect(self.escanear_red)
        self.etiqueta_estado_escaner = QLabel("")
        self.etiqueta_estado_escaner.setWordWrap(True)
        barra_escaner.addWidget(self.boton_escanear_red)
        barra_escaner.addWidget(self.etiqueta_estado_escaner, stretch=1)

        self.tabla_dispositivos = QTableWidget(0, 4)
        self.tabla_dispositivos.setHorizontalHeaderLabels(["IP", "MAC", "Fabricante", "SO estimado"])
        self.tabla_dispositivos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_dispositivos.verticalHeader().setVisible(False)
        self.tabla_dispositivos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_dispositivos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_dispositivos.doubleClicked.connect(self._al_hacer_doble_clic)

        nota = QLabel("Doble clic sobre un dispositivo para escanear sus puertos.")
        nota.setObjectName("nota")

        layout_escaner.addLayout(barra_escaner)
        layout_escaner.addWidget(self.tabla_dispositivos)
        layout_escaner.addWidget(nota)
        layout.addWidget(grupo_escaner, stretch=1)

    # LÓGICA: INFORMACIÓN DE RED
    def _lanzar(self, funcion, callback, *args):
        hilo = HiloTarea(funcion, *args)
        hilo.terminado.connect(callback)
        hilo.finished.connect(lambda: self._hilos.remove(hilo) if hilo in self._hilos else None)
        self._hilos.append(hilo)
        hilo.start()

    def actualizar_info_red(self):
        self._lanzar(red.obtener_ssid, self.etiqueta_ssid.setText)
        self._lanzar(red.obtener_mascara_red, self.etiqueta_mascara.setText)
        self._lanzar(red.obtener_seguridad_wifi, self._mostrar_seguridad)

    def _mostrar_seguridad(self, protocolo):
        self.etiqueta_seguridad.setText(protocolo)
        evaluacion = red.evaluar_seguridad(protocolo)
        self.etiqueta_riesgo.setText(f"  {evaluacion['riesgo']} — {evaluacion['descripcion']}  ")
        self.etiqueta_riesgo.setStyleSheet(
            f"background-color: {evaluacion['color']}; color: white;"
            f"border-radius: 4px; padding: 2px 6px; font-weight: 600;"
        )

    # LÓGICA: ESCÁNER DE RED
    def escanear_red(self):
        self.boton_escanear_red.setEnabled(False)
        self.etiqueta_estado_escaner.setText("Escaneando red local (puede tardar varios segundos)...")
        self.tabla_dispositivos.setRowCount(0)
        self._lanzar(red.escanear_dispositivos, self._mostrar_dispositivos)

    def _mostrar_dispositivos(self, dispositivos: dict):
        self.boton_escanear_red.setEnabled(True)

        # las claves de control no representan dispositivos
        error = dispositivos.pop("_error", None)
        aviso = dispositivos.pop("_aviso", None)

        if error:
            self.etiqueta_estado_escaner.setText(f"⚠ {error}")
            QMessageBox.warning(self, "Error de escaneo", error)
            return

        self.tabla_dispositivos.setSortingEnabled(False)
        for ip, info in dispositivos.items():
            fila = self.tabla_dispositivos.rowCount()
            self.tabla_dispositivos.insertRow(fila)
            self.tabla_dispositivos.setItem(fila, 0, QTableWidgetItem(ip))
            self.tabla_dispositivos.setItem(fila, 1, QTableWidgetItem(info.get("mac", "Desconocida")))
            self.tabla_dispositivos.setItem(fila, 2, QTableWidgetItem(info.get("fabricante", "Desconocido")))
            self.tabla_dispositivos.setItem(fila, 3, QTableWidgetItem(info.get("sistema_operativo", "Desconocido")))

        mensaje = f"{len(dispositivos)} dispositivo(s) encontrados."
        if aviso:
            mensaje += f" ⚠ {aviso}"
        self.etiqueta_estado_escaner.setText(mensaje)

    def _al_hacer_doble_clic(self, indice):
        fila = indice.row()
        item_ip = self.tabla_dispositivos.item(fila, 0)
        if item_ip is None:
            return
        dialogo = DialogoPuertosDispositivo(item_ip.text(), self)
        dialogo.exec()
