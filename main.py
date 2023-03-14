from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
import pandas as pd
import sys

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


# Cargar la interfaz de usuario utilizando loadUiType
Ui_Form, QMainWindow = uic.loadUiType("project_mp25.ui")


class MiVentana(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()

        # Creacion de un dataframe vacio
        self.df = df = pd.DataFrame()

        # Configurar la interfaz de usuario
        self.setupUi(self)

        # Conectar la señal clicked del botón btnSeleccionarArchivo a un método
        self.btnAbrirFile.clicked.connect(self.seleccionarArchivo)

        # Conectar la señal clicked del botón btnSeleccionarArchivo a un método
        self.btnMostrarFile.clicked.connect(self.mostrarGrafica)

        # Conectar la señal clicked del botón btnSalir a un método
        self.btnSalir.clicked.connect(self.mostrarMensaje)

    def seleccionarArchivo(self):
        # Mostrar un cuadro de diálogo para seleccionar el archivo de Excel
        archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de Excel",
            "",
            "Archivos de Excel (*.xlsx *.xls)"
        )
        # Mostrar el nombre del archivo seleccionado en un cuadro de texto
        self.txtArchivo.setText(archivo)

        # Conectar la señal clicked del botón btnLeerArchivo a un método
        self.leerArchivo()

    def leerArchivo(self):
        # Obtener el nombre del archivo de Excel seleccionado
        archivo = self.txtArchivo.text()

        # Leer el archivo en un objeto DataFrame de Pandas
        self.df = pd.read_excel(archivo)

        # Configurar la tabla y agregar datos
        self.tblDatos.setRowCount(len(self.df.index))
        self.tblDatos.setColumnCount(len(self.df.columns))

        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                item = QTableWidgetItem(str(self.df.iloc[i, j]))
                self.tblDatos.setItem(i, j, item)

        # Personalizar los encabezados de la tabla
        encabezados = list(self.df.columns)
        self.tblDatos.setHorizontalHeaderLabels(encabezados)

        # Ajustar el tamaño de las columnas para que se ajusten a los datos
        self.tblDatos.resizeColumnsToContents()

    def mostrarGrafica(self):
        # Crear el gráfico utilizando Matplotlib
        self.figura = Figure()
        self.grafico = self.figura.add_subplot(111)
        x = np.linspace(0, 10, 1000)
        y = np.sin(x)
        self.grafico.plot(x, y)
        
        # Agregar el gráfico al widget QFrame
        self.canvas = FigureCanvasQTAgg(self.figura)
        self.canvas.setParent(self.frameGrafico)

    def mostrarMensaje(self):
        print(self.df)
        print("Hola, presionaste el button Salir")



if __name__ == "__main__":
    # Crear la aplicación
    app = QtWidgets.QApplication([])

    # Crear la ventana
    ventana = MiVentana()

    # Mostrar la ventana
    ventana.show()

    # Iniciar el bucle de eventos
    app.exec_()
