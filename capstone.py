import cv2 as cv
import numpy as np
import sys
from PyQt5.QtWidgets import * #QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap

class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        
    def setupUI(self):
        # 윈도우 설정
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('농산물')
        
        # 버튼 생성
        self.fileButton = QPushButton('파일', self)
        self.fileButton.setGeometry(10, 10, 100, 30)
        self.fileButton.clicked.connect(self.fileOpenFunction)
        
        # 이미지를 추가할 라벨
        self.imageLabel = QLabel(self)
        
    def fileOpenFunction(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file>', './')
        self.img=cv.imread(fname[0])
        if self.img is None: sys.exit('파일을 찾을 수 없습니다')
        
        # 이미지 설정
        pixmap = QPixmap(fname[0])
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setContentsMargins(10, 50, 10, 10)
        self.imageLabel.resize(pixmap.width(), pixmap.height())
        
        # 이미지의 크기에 맞게 윈도우 resize
        self.resize(pixmap.width(), pixmap.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())