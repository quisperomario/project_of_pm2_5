from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
import pandas as pd
import sys

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PyQt5.QtWidgets import QApplication, QProgressDialog
from PyQt5.QtCore import QCoreApplication
import time

from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.QtCore import Qt


# Cargar la interfaz de usuario utilizando loadUiType
Ui_Form, QMainWindow = uic.loadUiType("project_mp25.ui")


class MiVentana(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()

        # Creacion de un dataframe vacio
        self.df = df = pd.DataFrame()
        self.mean_time_interval = pd.DataFrame()
        self.time_interval = ""

        # Configurar la interfaz de usuario
        self.setupUi(self)

        # Conectar la señal clicked del botón btnSeleccionarArchivo a un método
        self.btnAbrirFile.clicked.connect(self.seleccionarArchivo)

        # Conectar la señal clicked del botón btnSeleccionarArchivo a un método
        self.btnPromedio.clicked.connect(self.calcularPromedio)

        # Conectar la señal clicked del botón btnEliminarDatos a un método
        self.btnEliminarDatos.clicked.connect(self.EliminarDatos)

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

        self.mostrarDatoTabla()

    
    def mostrarDatoTabla(self):

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


    def calcularPromedio(self):
        # Llamamos a la funcion donde calcula el promedio
        self.promedioIntervaloFechas()

        # Crear el gráfico utilizando Matplotlib
        self.figura = Figure()
        self.grafico = self.figura.add_subplot(1,1,1)

        #x = self.mean_time_interval.index
        #y = self.mean_time_interval['pm25']
        self.grafico.scatter(self.mean_time_interval.index, self.mean_time_interval['pm25'])
        self.grafico.plot(self.mean_time_interval.index, self.mean_time_interval['pm25'])
        
        # Asignar etiquetas al eje x
        self.grafico.set_xticks(self.mean_time_interval.index)
        self.grafico.set_xticklabels(self.mean_time_interval.index, rotation=90)
        self.grafico.set_xlabel("Date and Hour")
        self.grafico.set_ylabel("PM2.5")
        self.grafico.set_title("Mean for Week of PM2.5")
        # Ajustar posición de subplots para mostrar todas las etiquetas
        self.figura.tight_layout()

        self.grafico.grid()

        # Agregar el gráfico al widget QVBoxLayout
        self.canvas = FigureCanvasQTAgg(self.figura)
        self.frameGrafico.addWidget(self.canvas)

        print("[INFO] Llegue a este punto de graficas....")


    def  promedioIntervaloFechas(self): # time interval ['1D','W' como 'H' ,para 1 hora, 'T' para 1 minuto, 'S' ,para 1 segundo]

        # ------------------------------------------------------------------> AQUI TRAEMOS LA FECHA DEL CAMPO TXT
        self.traerIntervaloTiempo()

        # Convertir la columna de fechas a datetime
        self.df['Fecha_Hora'] = pd.to_datetime(self.df['Fecha_Hora'])

        # Establecer la columna de fechas como índice del dataframe
        self.df.set_index('Fecha_Hora', inplace=True)

        # Agrupar los datos por un intervalo de 1 día y calcular el promedio
        self.mean_time_interval = self.df.resample(self.time_interval).mean()

        # Mostrar los promedios por día
        print(self.mean_time_interval)

    def traerIntervaloTiempo(self):
        # Traer el valor de txt 
        self.time_interval = self.txtTimeInterval.text()
        # Convertimos en mayuscula
        self.time_interval = self.time_interval.upper()



    def EliminarDatos(self):

        print(self.df.info())

        # Eliminar filas que cumplen la condición y asignar el resultado a la misma DataFrame
        self.df.drop(self.df[(self.df['pm25'] <= 0) | (self.df['pm25']>=99999)].index, inplace=True)

        print(self.df.head())

        # Llamamos a la funcion que muestra mensage de proceso
        self.messageLoad()

        self.mostrarDatoTabla()

        print("[INFO] Borramos los datos del dataFrame.")

    def messageLoad(self):
        
        progress = QProgressDialog("Cargando...", "Cancelar", 0, 100)
        progress.setWindowTitle("Progreso")
        progress.setWindowModality(2)
        progress.setAutoReset(False)
        progress.setAutoClose(False)
        progress.show()

        for i in range(101):
            progress.setValue(i)
            QCoreApplication.processEvents()
            time.sleep(0.025)
            if progress.wasCanceled():
                break

        progress.close()

    def mostrarMensaje(self):
        # print(self.df)
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
