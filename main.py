from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QApplication, QProgressDialog
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
import time
import numpy as np
import sys
import pandas as pd
from scipy import stats
import xlsxwriter
import matplotlib.pyplot as plt
from scipy.stats import linregress
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import re
from regression import RegressionData


# Cargar la interfaz de usuario utilizando loadUiType
Ui_Form, QMainWindow = uic.loadUiType("project_mp25.ui")


class MiVentana(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()

        # Creacion de un dataframe vacio
        self.df = None
        self.mean_time_interval = pd.DataFrame()
        self.time_interval = None
        self.median_time_interval = None
        self.df_moda = None
        self.std_time_interval = None
        self.min_time_interval = None
        self.maximo_time_interval = None
        self.confidence_interval = None
        self.df_mtc_std_ic = None
        self.count = 0
        self.count_clean_data = 0

        # Configurar la interfaz de usuario
        self.setupUi(self)

        # Conectar la señal clicked del botón btnSeleccionarArchivo a un método
        self.btnAbrirFile.clicked.connect(self.seleccionarArchivo)

        # Conectar la señal clicked del botón btnSeleccionarArchivo a un método
        self.btnPromedio.clicked.connect(self.calcularPromedio)

        # Conectar la señal clicked del botón btnEliminarDatos a un método
        self.btnEliminarDatos.clicked.connect(self.EliminarDatos)

        # Conectar la señal clicked del botón btnDescargarFileExcel a un método
        self.btnDescargarFileExcel.clicked.connect(self.DescargarFileExcel)

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

        # Verifica si se seleccionó un archivo
        if archivo:
            # El archivo fue seleccionado
            # Aquí puedes hacer lo que necesites con el archivo
            print(f'Se seleccionó el archivo {archivo}')

            # Mostrar el nombre del archivo seleccionado en un cuadro de texto
            self.txtArchivo.setText(archivo)

            # Conectar la señal clicked del botón btnLeerArchivo a un método
            self.leerArchivo()


        else:
            # El archivo no fue seleccionado
            # Mostrar un mensaje al usuario
            QMessageBox.warning(None, 'Warning', 'You must select a file before continuing.')
        

    def leerArchivo(self):
        # Obtener el nombre del archivo de Excel seleccionado
        archivo = self.txtArchivo.text()

        # Leer el archivo en un objeto DataFrame de Pandas
        self.df = pd.read_excel(archivo)

        self.mostrarDatoTabla(self.df)

    
    def mostrarDatoTabla(self, dataFrame):

        # Configurar la tabla y agregar datos
        self.tblDatos.setRowCount(len(dataFrame.index))
        self.tblDatos.setColumnCount(len(dataFrame.columns))

        for i in range(len(dataFrame.index)):
            for j in range(len(dataFrame.columns)):
                item = QTableWidgetItem(str(dataFrame.iloc[i, j]))
                self.tblDatos.setItem(i, j, item)

        # Personalizar los encabezados de la tabla
        encabezados = list(dataFrame.columns)
        self.tblDatos.setHorizontalHeaderLabels(encabezados)

        # Ajustar el tamaño de las columnas para que se ajusten a los datos
        self.tblDatos.resizeColumnsToContents()

    def mostrarDatoTablaMean(self):

        # Resetear el índice a una columna
        self.mean_time_interval = self.mean_time_interval.reset_index()

        # Configurar la tabla y agregar datos
        self.tableMeanTimeInterval.setRowCount(len(self.mean_time_interval.index))
        self.tableMeanTimeInterval.setColumnCount(len(self.mean_time_interval.columns))

        for i in range(len(self.mean_time_interval.index)):
            for j in range(len(self.mean_time_interval.columns)):
                item = QTableWidgetItem(str(self.mean_time_interval.iloc[i, j]))
                self.tableMeanTimeInterval.setItem(i, j, item)

        # Personalizar los encabezados de la tabla
        encabezados = list(self.mean_time_interval.columns)
        self.tableMeanTimeInterval.setHorizontalHeaderLabels(encabezados)

        # Ajustar el tamaño de las columnas para que se ajusten a los datos
        self.tableMeanTimeInterval.resizeColumnsToContents()


        # Establecer la columna de fechas como índice del dataframe
        self.mean_time_interval.set_index('Fecha_Hora', inplace = True)


    def mostrarDatoMedidasTendenciaCentral(self):

        # Resetear el índice a una columna 
        self.df_mtc_std_ic = self.df_mtc_std_ic.reset_index()

        # Configurar la tabla y agregar datos
        self.tableCentralTendencyMeasures.setRowCount(len(self.df_mtc_std_ic.index))
        self.tableCentralTendencyMeasures.setColumnCount(len(self.df_mtc_std_ic.columns))

        for i in range(len(self.df_mtc_std_ic.index)):
            for j in range(len(self.df_mtc_std_ic.columns)):
                item = QTableWidgetItem(str(self.df_mtc_std_ic.iloc[i, j]))
                self.tableCentralTendencyMeasures.setItem(i, j, item)

        # Personalizar los encabezados de la tabla
        encabezados = list(self.df_mtc_std_ic.columns)
        self.tableCentralTendencyMeasures.setHorizontalHeaderLabels(encabezados)

        # Ajustar el tamaño de las columnas para que se ajusten a los datos
        self.tableCentralTendencyMeasures.resizeColumnsToContents()


        # Establecer la columna de fechas como índice del dataframe
        self.df_mtc_std_ic.set_index('Fecha_Hora', inplace = True)


    def calcularPromedio(self):

        if not self.txtTimeInterval.text(): # Indica que no ingreso valor al campo txt
            self.mostrarMensajeIngresarValor()
        else:

            # Tenemos que validar que haya ingresado muy bien en campo de tiempo
            self.traerIntervaloTiempo()
            if self.validationTimeInterval():
                # El campo en valido

                # Llamamos a la funcion donde calcula el promedio
                self.promedioIntervaloFechas()

                # Llamamos a la funcion para mostrar datos en la tabla tableCentralTendencyMeasures
                self.mostrarDatoTablaMean()

                # Llamamos a la funcion para mostrar las medidas de tendencia central en la tabla
                self.mostrarDatoMedidasTendenciaCentral()

                # Crear el gráfico utilizando Matplotlib
                self.figura = Figure()
                self.grafico = self.figura.add_subplot(111)

                self.grafico.scatter(self.mean_time_interval.index, self.mean_time_interval['mean'], color='red')
                self.grafico.plot(self.mean_time_interval.index, self.mean_time_interval['mean'], color='blue')
                
                # Asignar etiquetas al eje x
                self.grafico.set_xticks(self.mean_time_interval.index)
                self.grafico.set_xticklabels(self.mean_time_interval.index, rotation=90)
                self.grafico.set_xlabel("Date and Hour")
                self.grafico.set_ylabel("PM2.5")
                self.grafico.set_title("Mean for "+ self.time_interval + " of PM2.5")
                # Ajustar posición de subplots para mostrar todas las etiquetas
                self.figura.tight_layout()

                self.grafico.grid()
                

                if self.count == 0:
                    # Agregar el gráfico al widget QVBoxLayout
                    self.canvas = FigureCanvasQTAgg(self.figura)
                    self.frameGrafico.addWidget(self.canvas)
                    self.count += 1 
                else:

                    # para eliminar el objeto de gráfico del QVBoxLayout
                    self.frameGrafico.removeWidget(self.canvas)
                    self.canvas.deleteLater()

                    self.canvas = FigureCanvasQTAgg(self.figura)
                    self.frameGrafico.addWidget(self.canvas)

            else:
                # El campo no es valido
                # Mostrar un mensaje al usuario
                QMessageBox.warning(None, 'Critical', 'Invalid field')


    def promedioIntervaloFechas(self):

        # Antes de pasarle reset_index de self.df
        self.df =  self.df.reset_index()
        self.replacaDataForRegression() #------------------------------------->aqui
        self.messageLoad()
        
        # Resetear el índice fecha a una columna
        self.df_replaced = self.df_replaced.reset_index()
            
        # Convertir la columna de fechas a datetime
        # Estamos cambiando a self.df por self.df_replaced -------------------------------->ojo aqui
        self.df_replaced['Fecha_Hora'] = pd.to_datetime(self.df_replaced['Fecha_Hora'])

        # Establecer la columna de fechas como índice del dataframe
        self.df_replaced.set_index('Fecha_Hora', inplace = True)

        # Agrupar los datos por un intervalo de 1 día y calcular el promedio
        self.mean_time_interval= self.df_replaced.resample(self.time_interval).mean()
        self.mean_time_interval = self.mean_time_interval.rename(columns={'pm25': 'mean'})

        # Agrupar los datos por un intervalo de 1 día y calcular la mediana
        self.median_time_interval = self.df_replaced.resample(self.time_interval).median()
        self.median_time_interval  = self.median_time_interval .rename(columns={'pm25': 'median'})

        # Agrupar los datos por un intervalo de 1 día y calcular la moda
        self.df_replaced = self.df_replaced.reset_index()
        self.df_moda = self.df_replaced.resample(self.time_interval, on='Fecha_Hora')['pm25'].apply(pd.Series.mode)
        self.df_replaced.set_index('Fecha_Hora', inplace = True)

        # Agrupar los datos por un intervalo de 1 día y calcular la desviación estándar
        self.std_time_interval = self.df_replaced.resample(self.time_interval).std()
        self.std_time_interval = self.std_time_interval.rename(columns={'pm25': 'std'})

        self.min_time_interval = self.df_replaced.resample(self.time_interval).min()
        self.min_time_interval = self.min_time_interval.rename(columns={'pm25': 'min'})

        self.maximo_time_interval = self.df_replaced.resample(self.time_interval).max()
        self.maximo_time_interval = self.maximo_time_interval.rename(columns={'pm25': 'max'})

        # LLamamos a la funcion que calcula intervalo de confianza
        self.calcularIntervaloConfianza()

        # Unir dataframe - Concatenar los dataframes
        self.df_mtc_std_ic = pd.concat([self.mean_time_interval, self.median_time_interval, self.std_time_interval, self.min_time_interval, self.maximo_time_interval, self.confidence_interval], axis=1)


    def traerIntervaloTiempo(self):

        # Traer el valor de txt 
        self.time_interval = self.txtTimeInterval.text()
        # Convertimos en mayuscula
        self.time_interval = self.time_interval.upper()


    def validationTimeInterval(self):
        # seconds[S]-minute[T]-hour[H]-day[D]-week[W]-months[M]-year[Y]
        cadena = self.time_interval
        regex =  "^(?:\d+[STHDWMY]|[STHDWMY](?!\w))[STHDWMY]?(?<!\d)$" # Regex para que solo ingrese el formaro indicado
        if re.match(regex, cadena):
            # La cadena es valida
            regex = "^[0-9]*[STHDMYW]{1}$"
            if re.match(regex, cadena):
                return True
        else:
            # La cadena no es valida
            return False
            


    def calcularIntervaloConfianza(self):

        # Resetear el índice a una columna
        self.df_replaced = self.df_replaced.reset_index()

        # Agrupar por semana y calcular el intervalo de confianza del 95%
        self.confidence_interval = self.df_replaced.groupby(pd.Grouper(key='Fecha_Hora', freq=self.time_interval)).agg(lambda x: stats.t.interval(0.95, len(x)-1, loc=x.mean(), scale=stats.sem(x)))
        self.confidence_interval = self.confidence_interval.rename(columns={'pm25': 'confidence_interval 95%'})

        # Establecer la columna de fechas como índice del dataframe
        self.df_replaced.set_index('Fecha_Hora', inplace = True)



    def EliminarDatos(self):

        if not self.txtTimeInterval.text(): # Indica que no ingreso valor al campo txt
            self.mostrarMensajeIngresarValor()

        else: # Si ingreso al campo

            # Tenemos que validar que ingrese bien el campo texto de tiempo
            self.traerIntervaloTiempo()
            if self.validationTimeInterval():
                # El campo valido

                # Eliminar filas que cumplen la condición y asignar el resultado a la misma DataFrame
                #self.df.drop(self.df[(self.df['pm25'] <= 0) | (self.df['pm25']>=99999)].index, inplace=True)

                # Llamamos a la funcion que muestra mensage de proceso
                #self.messageLoad()

                #self.mostrarDatoTabla() 
                
                if self.count_clean_data == 0:
                    # Que es la primera vez
                    self.count_clean_data += 1
                else:
                    self.df =  self.df.reset_index()

                self.replacaDataForRegression()
                self.messageLoad()
                df_3 = self.df_replaced.reset_index()
                self.mostrarDatoTabla(df_3)
            
            else:
                # El campo no es valido
                # Mostrar un mensaje al usuario
                QMessageBox.warning(None, 'Critical', 'Invalid field!!!')


    
    def DescargarFileExcel(self):

        # Verificar si el dataframe está vacío
        if self.mean_time_interval.empty:
            # El dataframe esta vacio y no hay nada que descargar
            # Mostrar un mensaje al usuario
            QMessageBox.warning(None, 'Warning', 'There is no data to download.')

        else:
            # dataframe no esta vacio

            # Resetear el índice a una columna
            self.mean_time_interval = self.mean_time_interval.reset_index() 
            self.df_mtc_std_ic = self.df_mtc_std_ic.reset_index()

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar archivo', '', 'Archivo de Excel (*.xlsx)')
            #file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo Excel", "", "Excel Workbook (*.xlsx)", options=options)
            if file_name:
                writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                sheet_name_1 = 'mean_pm25_' + self.time_interval
                sheet_name_2 = 'central_tendency_measures_' + self.time_interval
                # Guardar los DataFrames en hojas separadas
                self.mean_time_interval.to_excel(writer, sheet_name=sheet_name_1, index=False)
                self.df_mtc_std_ic.to_excel(writer, sheet_name=sheet_name_2, index=False)

                # Cerrar el escritor de Excel
                writer.close()

                # Para descargar la grafica
                self.descargarGrafica(file_name)

            # Establecer la columna de fechas como índice del dataframe
            self.mean_time_interval.set_index('Fecha_Hora', inplace = True)
            self.df_mtc_std_ic.set_index('Fecha_Hora', inplace = True)


    def descargarGrafica(self, file_name):
        route = self.getRutaImges(file_name)
        # Guarda la figura en formato .jpg
        file_image = route+'graph_pm25_'+self.time_interval+'.jpg'
        self.figura.savefig(file_image)

    def getRutaImges(self, file_name):
        list_route = file_name.split("/")
        route = ""
        for i in range(len(list_route)-1):
            route = route + list_route[i] + "/"
        return route

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
            time.sleep(0.010)
            if progress.wasCanceled():
                break
        progress.close()

    
    def replacaDataForRegression(self):
        df_2 = None

        df_2 = self.df

        # Convierte la columna 'Fecha' en un objeto de fecha y hora
        df_2['Fecha_Hora'] = pd.to_datetime(df_2['Fecha_Hora'])

        # Establece el índice como la columna 'Fecha'
        df_2.set_index('Fecha_Hora', inplace=True)

        # Agrupa por día
        grouped = df_2.groupby(pd.Grouper(freq=self.time_interval)) 

        # Definimos la función que reemplaza los datos nulos o atípicos por la regresión de cada grupo
        def replace_outliers(group):
            print("[INFO] estoy entrando a la funcion replace_outliers ....")
            # Calcular los límites inferior y superior del rango aceptable de los valores
            regression_data = RegressionData(group=group)
            return regression_data.getDataCleaned()

        # Aplicamos la función a cada grupo
        self.df_replaced = grouped.apply(replace_outliers)

    def mostrarMensajeIngresarValor(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("The grouping time interval is missing!!!")
        msg.setWindowTitle("Empty field")
        msg.exec_()
            

    def mostrarMensaje(self):
        print("PRESIONANTE EL BUTON SALIR")


if __name__ == "__main__":
    # Crear la aplicación
    app = QtWidgets.QApplication([])

    # Crear la ventana
    ventana = MiVentana()

    # Mostrar la ventana
    ventana.show()

    # Iniciar el bucle de eventos
    app.exec_()
