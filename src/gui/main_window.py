'''
Ventana principal de REDvisor: aúna las tres pestañas de la aplicación
(Dispositivo, Red y Tráfico) dentro de un QTabWidget.
'''

from PySide6.QtWidgets import QMainWindow, QTabWidget
from src.gui.pestana_dispositivo import PestanaDispositivo
from src.gui.pestana_red import PestanaRed
from src.gui.pestana_trafico import PestanaTrafico


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("REDvisor")
        self.resize(900, 650)

        self.pestana_trafico = PestanaTrafico()

        pestanas = QTabWidget()
        pestanas.addTab(PestanaDispositivo(), "💻 Dispositivo")
        pestanas.addTab(PestanaRed(), "📡 Red")
        pestanas.addTab(self.pestana_trafico, "🚦 Tráfico")

        self.setCentralWidget(pestanas)

    def closeEvent(self, evento):
        self.pestana_trafico.cerrar()
        evento.accept()
