import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog

from PyQt5.uic import loadUi
from mainWindows import Ui_MainWindowDetectObject

import torch
import numpy as np
import pandas
import requests


# Cargar el modelo previamente entrenado
#model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
#model = torch.hub.load('ultralytics/yolov5','custom',path='C:/Users/ROMAR/Desktop/PROGRAMACION/Project Neural Network/Vision Artificial/Deteccion Objetos/detect_object_v2/best.pt')
#self.label_map = {0: 'casco_de_seguridad',1: 'arnes_de_seguridad',2: 'cono_de_seguridad',3: 'escalera'}


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/ROMAR/Desktop/PROGRAMACION/Project Neural Network/Vision Artificial/Deteccion Objetos/detect_object_v2/best.pt')

        # Configurar la interfaz gráfica 
        self.ui = Ui_MainWindowDetectObject()
        self.ui.setupUi(self)

        self.cap = cv2.VideoCapture(0)  # abriendo la camara
        
        self.video_size = QtCore.QSize(640, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.ui.btnStart.clicked.connect(self.start_video)
        self.ui.btnStop.clicked.connect(self.stop_video)

        # Actualizar el contenido de la ventana de forma constante
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_frame)
        self.timer.start(30)

    def start_video(self):
        self.cap = cv2.VideoCapture(0)
        self.ui.btnStart.setEnabled(False)
        self.ui.btnStop.setEnabled(True)

    def stop_video(self):
        self.cap.release()
        self.ui.lblVideoCapture.clear()
        self.ui.btnStart.setEnabled(True)
        self.ui.btnStop.setEnabled(False)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # Escalar la imagen para que se ajuste al QLabel
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            pixmap = pixmap.scaled(self.ui.lblVideoCapture.size(), Qt.KeepAspectRatio)
            
            # Mostrar la imagen en el QLabel
            self.ui.lblVideoCapture.setPixmap(pixmap)        
            self.ui.lblVideoCapture.setPixmap(QPixmap.fromImage(convert_to_qt_format))
    
    def detect_objects(self, frame):
        results = self.model(frame)
        labels = results.xyxyn[0][:, -1].numpy()
        info = results.pandas().xyxy[0]
        print(info)
        return labels

    @pyqtSlot()
    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            labels = self.detect_objects(frame)
            print(labels)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            
            '''
            # Escalar la imagen para que se ajuste al QLabel
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            pixmap = pixmap.scaled(self.ui.lblVideoCapture.size(), Qt.KeepAspectRatio)
            
            # Mostrar la imagen en el QLabel
            self.ui.lblVideoCapture.setPixmap(pixmap)        
            self.ui.lblVideoCapture.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
            self.ui.lblVideoCapture.setText(f"Objects detected: {labels}")
            '''
            
            pixmap = QtGui.QPixmap.fromImage(convert_to_Qt_format)
            self.ui.lblVideoCapture.setPixmap(pixmap)
            #self.ui.lblVideoCapture.setText(f"Objects detected: {labels}")  
                  

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())