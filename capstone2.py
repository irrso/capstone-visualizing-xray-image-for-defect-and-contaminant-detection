import cv2 as cv
import numpy as np
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import * #QMainWindow, QLabel, QPushButton, QApplication, QMainWindow 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


form_class = uic.loadUiType("./test.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('x-ray detection program')
        
        # 열기 버튼 클릭 이벤트
        self.openBtn.clicked.connect(self.fileOpenFunction)
                
        # 검출 버튼 클릭 이벤트
        #self.detectBtn.clicked.connect(self.btnClick)
        
        # 이미지를 추가할 라벨
        self.imageLabel = QLabel(self)
        
        # 이미지 개수(* 변수명 변경하기)
        self.step = 0

    def fileOpenFunction(self):
        global fname
        fname = QFileDialog.getOpenFileNames(self, './')
        
        self.img = cv.imread(fname[0][0])
        if self.img is None: sys.exit('파일을 찾을 수 없습니다')
        
        # 이미지 설정
        pixmap = QPixmap(fname[0][0])
        pixmap = pixmap.scaled(512, 400, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setContentsMargins(10, 55, 10, 10)
        self.imageLabel.resize(pixmap.width(), pixmap.height())
        
        # 이미지의 크기에 맞게 윈도우 resize
        self.resize(pixmap.width(), pixmap.height())
        
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_A and self.step != 0:
            self.step -= 1
            
        elif e.key() == Qt.Key_D and self.step != len(fname[0])-1:
            self.step += 1
        
        pixmap = QPixmap(fname[0][self.step])
        self.imageLabel.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())