'''
Hoja de estilos (QSS) para dar a REDvisor un aspecto moderno y minimalista.
'''

HOJA_DE_ESTILOS = """
QWidget {
    background-color: #f4f6f8;
    color: #202a33;
    font-family: "Segoe UI", "Cantarell", sans-serif;
    font-size: 13px;
}

QMainWindow {
    background-color: #f4f6f8;
}

QTabWidget::pane {
    border: 1px solid #dde2e6;
    border-radius: 8px;
    background-color: #ffffff;
    top: -1px;
}

QTabBar::tab {
    background-color: transparent;
    padding: 8px 18px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: #5a6672;
    font-weight: 600;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #0f9d8c;
    border: 1px solid #dde2e6;
    border-bottom: none;
}

QGroupBox {
    background-color: #ffffff;
    border: 1px solid #e1e5e9;
    border-radius: 10px;
    margin-top: 14px;
    padding: 14px 10px 10px 10px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px;
    color: #0f9d8c;
}

QLabel#valorInfo {
    font-weight: 600;
}

QLabel#nota {
    color: #8a94a0;
    font-style: italic;
}

QPushButton {
    background-color: #0f9d8c;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 7px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #0d8a7b;
}

QPushButton:pressed {
    background-color: #0b7669;
}

QPushButton:disabled {
    background-color: #b7bfc6;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e1e5e9;
    border-radius: 6px;
    gridline-color: #eef1f3;
    selection-background-color: #d7f2ee;
    selection-color: #0b3b34;
}

QHeaderView::section {
    background-color: #f0f3f5;
    color: #4a5561;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #dde2e6;
    font-weight: 600;
}

QProgressBar {
    border: 1px solid #dde2e6;
    border-radius: 6px;
    background-color: #eef1f3;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #0f9d8c;
    border-radius: 6px;
}

QDialog {
    background-color: #f4f6f8;
}
"""
