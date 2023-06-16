import cv2 as cv
import numpy as np
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt
import time
import math

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


    def fileOpenFunction(self):
        # 이미지 개수, pixmap1 초기화
        self.step = 0
        self.atextLabel.setText(' ')
        pixmap1 = QPixmap()
        self.afterLabel.setPixmap(pixmap1)
        
        global fname
        fname = QFileDialog.getOpenFileNames(self, './')
        
        self.img = cv.imread(fname[0][0], 0)
        if self.img is None: sys.exit('파일을 찾을 수 없습니다')
        
        # 이미지 설정
        pixmap = QPixmap(fname[0][0]).scaled(512, 400, Qt.KeepAspectRatio)
        self.beforeLabel.setPixmap(pixmap)
        self.beforeLabel.resize(pixmap.width(), pixmap.height())
        
        # 이미지 하단에 텍스트 설정
        self.btextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
        
    # 수정하기
    def detectFunction(self):
        global fname, pseudo_img, path

        pseudo_img=[]
        path=[]
        for i in range(len(fname[0])):
            pseudo_img.append(pseudo(cv.imread(fname[0][i], 0)))
            path.append('C:/Users/osoyo/.spyder-py3/project/images/'+str(i)+'.tif')
            cv.imwrite(path[i], cv.cvtColor(pseudo_img[i], cv.COLOR_RGB2BGR))
            
        # 이미지 설정
        pixmap1 = QPixmap(path[self.step]).scaled(512, 400, Qt.KeepAspectRatio)
        
        self.afterLabel.setPixmap(pixmap1)
        self.afterLabel.resize(pixmap1.width(), pixmap1.height())
        self.atextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_A and self.step != 0:
            self.step -= 1
            
        elif e.key() == Qt.Key_D and self.step != len(fname[0])-1:
            self.step += 1
        
        pixmap = QPixmap(fname[0][self.step]).scaled(512, 400, Qt.KeepAspectRatio)
        self.beforeLabel.setPixmap(pixmap)
        self.btextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
        pixmap1 = QPixmap(path[self.step]).scaled(512, 400, Qt.KeepAspectRatio)
        self.afterLabel.setPixmap(pixmap1)
        self.atextLabel.setText(str(self.step+1)+"/"+str(len(fname[0])))
        
        
def pseudo(img, flag=0.0):
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
        
    # RD 이미지 생성
    for r in range(20, height - 20):
        for c in range(20, width - 20):
            i = r + 1;
            j = c + 1;
            # 한 픽셀에 대해 주변 40*40 범위의 평균과 표준편차를 구해 주변보다 밀도가 얼마나 차이나는지 구함
            try:
                if img[r, c] < 200:
                    wam = (ps[i + scale][j + scale] - ps[i - scale-1][j + scale] - ps[i + scale][j - scale-1] + ps[i - scale-1][j - scale-1]) / (41 * 41)
                    lam = (ps[i+2][j+2] - ps[i-2-1][j+2] - ps[i+2][j-2-1] + ps[i-2-1][j-2-1]) / (5 * 5)
                    
                    sq_sum = pss[i + scale][j + scale] - pss[i - scale-1][j + scale] - pss[i + scale][j - scale-1] + pss[i - scale-1][j - scale-1]
                    sq_sum_avg = sq_sum / (41 * 41)
                    std = math.sqrt(sq_sum_avg - wam*wam)

                    z = round((lam - wam) / std, 2)
                    s[r, c] = z
                    
                    if 0 < z < flag:
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
            except:
                pass
            
    print('완료')       
    output = np.array(output, dtype=np.uint8)
    return output


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())