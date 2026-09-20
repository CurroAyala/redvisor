'''
Punto de entrada de la aplicación REDvisor.
Ejecutar desde la raíz del proyecto (donde vive el paquete `src`).
'''

import sys
from PySide6.QtWidgets import QApplication
from src.gui.main_window import VentanaPrincipal
from src.gui.estilo import HOJA_DE_ESTILOS


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(HOJA_DE_ESTILOS)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
