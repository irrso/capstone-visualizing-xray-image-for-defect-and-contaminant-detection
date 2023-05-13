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
        self.detectBtn.clicked.connect(self.detectFunction)
        
        # 이미지 개수(* 변수명 변경하기)
        self.step = 0


    def fileOpenFunction(self):
        global fname
        fname = QFileDialog.getOpenFileNames(self, './')
        
        self.img = cv.imread(fname[0][0])
        if self.img is None: sys.exit('파일을 찾을 수 없습니다')
        
        # 이미지 설정
        pixmap = QPixmap(fname[0][0]).scaled(512, 400, Qt.KeepAspectRatio)
        self.beforeLabel.setPixmap(pixmap)
        self.beforeLabel.resize(pixmap.width(), pixmap.height())
        
        # 이미지 하단에 텍스트 설정
        self.btextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
        
    # 수정하기
    def detectFunction(self):
        global fname1
        fname1 = QFileDialog.getOpenFileNames(self, './')
         
        self.img1 = cv.imread(fname1[0][0])
        if self.img1 is None: sys.exit('파일을 찾을 수 없습니다')
         
        # 이미지 설정
        pixmap1 = QPixmap(fname1[0][0]).scaled(512, 400, Qt.KeepAspectRatio)
        self.afterLabel.setPixmap(pixmap1)
        self.afterLabel.resize(pixmap1.width(), pixmap1.height())
         
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_A and self.step != 0:
            self.step -= 1
            
        elif e.key() == Qt.Key_D and self.step != len(fname[0])-1:
            self.step += 1
        
        pixmap = QPixmap(fname[0][self.step]).scaled(512, 400, Qt.KeepAspectRatio)
        self.beforeLabel.setPixmap(pixmap)
        self.btextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())