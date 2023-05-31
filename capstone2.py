import cv2 as cv
import numpy as np
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import * #QMainWindow, QLabel, QPushButton, QApplication, QMainWindow 
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

from matplotlib import pyplot as plt
import time
import math

def psudo(img, flag=156):
    print(img.shape)
    height, width = img.shape
    s = np.zeros((height, width)).astype('float')

    alpha = 100 # 색상 선택을 위한 용도
    scale = 20 # n x n WAM 필터의 크기
    output = np.ones(shape=(height, width, 3), dtype=int) * 255 # 출력용 이미지
    
    pss = np.zeros((height+1, width+1), dtype=np.int64)
    ps = np.zeros((height+1, width+1), dtype=np.int64)
    
    
    for i in range(1, height+1):
        for j in range(1, width+1):
            ps[i, j] = ps[i-1][j] + ps[i][j-1] - ps[i-1][j-1] + img[i-1, j-1]
            pss[i, j] = pss[i-1][j] + pss[i][j-1] - pss[i-1][j-1] + np.int64(img[i-1, j-1])*img[i-1, j-1]
        
#     print(ps)
    
    # RD 이미지 생성
    for r in range(20, height - 20):
        for c in range(20, width - 20):
            i = r + 1;
            j = c + 1;
            # 한 픽셀에 대해 주변 40*40 범위의 평균과 표준편차를 구해 주변보다 밀도가 얼마나 차이나는지 구함
            if img[r, c] < flag: # 40000
                wam = (ps[i + scale][j + scale] - ps[i - scale-1][j + scale] - ps[i + scale][j - scale-1] + ps[i - scale-1][j - scale-1]) / (41 * 41)
                lam = (ps[i+2][j+2] - ps[i-2-1][j+2] - ps[i+2][j-2-1] + ps[i-2-1][j-2-1]) / (5 * 5)
                
#                     print(r, c, wam, lam)
#                     return output
                
                sq_sum = pss[i + scale][j + scale] - pss[i - scale-1][j + scale] - pss[i + scale][j - scale-1] + pss[i - scale-1][j - scale-1]
                sq_sum_avg = sq_sum / (41 * 41)
                std = math.sqrt(sq_sum_avg - wam*wam)
            
#                     wam = np.mean(img[r - scale + 1:r + scale, c - scale:c + scale + 1])
#                     lam = np.mean(img[r - 2:r + 3, c - 2:c + 3])
#                     std = np.std(img[r - scale:r + scale + 1, c - scale:c + scale + 1])
                z = round((lam - wam) / std, 2)
                s[r, c] = z
        
                if 0 < z <= 1.5:
                    z *= -1.0
    
                if z > 0:  # Red
                    v = max(0, 255 - int(alpha * z))
                    output[r, c, 0] = 255  # R
                    output[r, c, 1] = v  # G
                    output[r, c, 2] = v  # B
                else:
                    v = max(0, 255 + int(alpha * z))
                    output[r, c, 0] = v  # R
                    output[r, c, 1] = v  # G
                    output[r, c, 2] = 255  # B
    
    output = np.array(output, dtype=np.uint8)
    return output




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
        
        self.img = cv.imread(fname[0][0], 0)
        if self.img is None: sys.exit('파일을 찾을 수 없습니다')
        
        
        # 이미지 설정
        pixmap = QPixmap(fname[0][0]).scaled(512, 400, Qt.KeepAspectRatio)
        self.beforeLabel.setPixmap(pixmap)
        self.beforeLabel.resize(pixmap.width(), pixmap.height())
        
        print(pixmap)
        # 이미지 하단에 텍스트 설정
        self.btextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
        
    # 수정하기
    def detectFunction(self):
        global fname, psudo_img
        
        psudo_img = self.img
        psudo_img = psudo(self.img)
        
        path = r'C:\Users\osoyo\.spyder-py3\project\images\sibal.tif'
        # path = r'C:\Users\osoyo\OneDrive\바탕 화면\fdas\sibal.tif'
        
        # time.sleep(30)
        
        print(psudo_img.shape)
        print(psudo_img[400, 600])
        # cv.imshow('psudo_img', psudo_img)
        
        cv.imwrite(path, cv.cvtColor(psudo_img, cv.COLOR_RGB2BGR))
        
        print(1)
        
        # 이미지 설정
        pixmap1 = QPixmap(path).scaled(512, 400, Qt.KeepAspectRatio)
        
        # print(psudo_img.shape)
        # h, w = psudo_img.shape[:2]
        # bytesPerLine = 3*w
        # pixmap1 = QImage(psudo_img.data, w, h, bytesPerLine, QImage.Format_RGB888)
        # pixmap1 = QPixmap.fromImage(pixmap1)
        # pixmap1 = pixmap1.scaled(512, 400, Qt.KeepAspectRatio)
        
        # pixmap1 = qimage2ndarray.array2qimage(psudo_img, normalize=False)
        self.afterLabel.setPixmap(pixmap1)
        self.afterLabel.resize(pixmap1.width(), pixmap1.height())
        
        self.atextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Left and self.step != 0:
            self.step -= 1
            
        elif e.key() == Qt.Key_Right and self.step != len(fname[0])-1:
            self.step += 1
        
        pixmap = QPixmap(fname[0][self.step]).scaled(512, 400, Qt.KeepAspectRatio)
        self.beforeLabel.setPixmap(pixmap)
        self.btextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
        pixmap1 = QPixmap(fname1[0][self.step]).scaled(512, 400, Qt.KeepAspectRatio)
        self.afterLabel.setPixmap(pixmap1)
        self.atextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())