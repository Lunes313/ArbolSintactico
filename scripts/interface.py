from PyQt5 import QtWidgets, uic

class interfaz(QtWidgets.QMainWindow):
    def __init__(self):
        super(interfaz, self).__init__()
        uic.loadUi("../design/interface.ui", self)  # Cargar la interfaz desde el archivo .ui
        self.setWindowTitle("   Gramatica y Arboles Sintacticos  ")  # Título de la ventana

        self.btnSalir.clicked.connect(self.close)