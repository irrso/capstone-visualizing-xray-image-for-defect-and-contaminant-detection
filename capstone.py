import cv2 as cv
import numpy as np
import sys
from PyQt5.QtWidgets import * #QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class WindowClass(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        
    def setupUI(self):
        # 윈도우 설정
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('농산물')
        
        # 파일 버튼 생성
        self.fileButton = QPushButton('파일', self)
        self.fileButton.setGeometry(10, 10, 100, 30)
        self.fileButton.clicked.connect(self.fileOpenFunction)
        
        # 검출 버튼 생성
        self.detectButton = QPushButton('검출', self)
        self.detectButton.setGeometry(120, 10, 100, 30)
        self.detectButton.clicked.connect(self.detectFunction) # detectFunction 대신 실제 구현
        
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
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setContentsMargins(10, 50, 10, 10)
        self.imageLabel.resize(pixmap.width(), pixmap.height())
        
        # 이미지의 크기에 맞게 윈도우 resize
        self.resize(pixmap.width(), pixmap.height())
    
    # 실제 구현
    def detectFunction(self):
        a = 0
        
    
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