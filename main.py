# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:31:55 2020

@author: NeoSixMan
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_project import Ui_MainWindow

import cv2

import numpy as np

class CurrentData():
    def __init__(self):
        self.growth = np.loadtxt('image/20200329/rates_20_04_2020.csv', delimiter=',')
        self.classes = np.loadtxt('image/20200329/class_10_04_2020.csv', delimiter=',')
        
    def change(self, day):
        self.growth = np.loadtxt('image/20200329/rates_20_04_2020.csv', delimiter=',')
        self.classes = np.loadtxt('image/20200329/class_10_04_2020.csv', delimiter=',')
    
    def data_prep1(self, g):
        if g > 120:
            return 'Error'
        elif g > 95 and g <= 120:
            return 'Available'
        return str(g) + ' %'
    
    def data_prep2(self, c):
        if c == 0:
            return 'Healthy'
        return 'Spoiled'


class TestUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # May change position
        self.batch_x = [17, 17+97, 17+97*2, 17+97*3, 17+97*4, 17+97*5, 580]
        self.batch_y = [0, 53, 53+101, 53+101*2, 53+101*3, 53+101*4, self.ui.batch.height()]
        
        self.path_main = 'image/viz_2020-03-29_'
        self.day = '11'
        self.png = '.png'
        
        self.path_sub = 'image/20200329/'
        
        img1 = QPixmap('image/h.png')
        img2 = QPixmap('image/r.png')
        img3 = QPixmap('image/next.png')
        #current image
        nm = self.path_main + self.day + self.png
        img0 = QPixmap(nm)
        
        self.ns = self.path_sub + self.day + '/2' + self.png
        self.img = QPixmap(self.ns)
        
        self.data = CurrentData()
        viz = self.draw(img0)
        self.ui.label.setPixmap(img1)
        self.ui.label_2.setPixmap(img2)
        self.ui.label_4.setPixmap(img3.scaled(self.ui.label_4.size(),Qt.KeepAspectRatio))
        #current image
        self.ui.batch.setPixmap(viz.scaled(self.ui.batch.size(),Qt.KeepAspectRatio))
        self.ui.sample_image.setPixmap(self.img.scaled(self.ui.sample_image.size(),Qt.KeepAspectRatio))
        
        self.ui.status_value.setText(self.data.data_prep2(self.data.classes[0][1]))
        self.ui.rate_value.setText(self.data.data_prep1(self.data.growth[0][1]))
        #self.ui.rate_value.setText(self.data_prep1(growth[1]))
        
        self.ui.status_value_2.setText('01/05/2020')
        self.ui.status_value_3.setText('10')
        
        #Event
        self.ui.label_4.mousePressEvent = self.previous
        self.ui.batch.mousePressEvent = self.select
        self.ui.current_button.clicked.connect(self.current)
        
    def draw(self, img):
        p = QPainter(img)
        
        # set rectangle color and thickness
        pRedRect = QPen(Qt.red)
        pRedRect.setWidth(15)
        pGreenRect = QPen(Qt.green)
        pGreenRect.setWidth(15)
        
        # opimize values
        p.setPen(pGreenRect)
        scaleX = 4.15
        scaleY = 3.9
        delayX = 10
        delayY = 15
        
        for i in range(6):
            for j in range(6):
                if i*6+j not in [0, 5, 30, 35]:
                    x = scaleX*(self.batch_x[i] + delayX*i)
                    y = scaleY*(self.batch_y[j] + delayY*j)
                    w = scaleX*(self.batch_x[i+1] - self.batch_x[i])
                    h = scaleY*(self.batch_y[j+1] - self.batch_y[j])
                    if self.data.classes[i][j]:
                        p.setPen(pRedRect)
                    else:
                        p.setPen(pGreenRect)
                    p.drawRect(x,y,w,h)
        p.end()
        return img
        
    def previous(self, event):
        if self.ui.prev_back_label.text() == "see previous":
            self.ui.prev_back_label.setText("back to current")
            self.change_batch('-')
        else:
            self.ui.prev_back_label.setText("see previous")
            self.change_batch('+')
            
    def change_batch(self, assign):
        if assign == '+':
            num = int(self.day) + 1
        else:
            num = int(self.day) - 1
        self.day = '' + str(num)
        if num >= 0:
            #Change day
            #self.data.change(num)
            
            name = self.path_main + self.day + self.png
            temp = QPixmap(name)
            viz = self.draw(temp)
            self.ui.batch.setPixmap(viz.scaled(self.ui.batch.size(),Qt.KeepAspectRatio))
        else:
            print("First day")
        
    def select(self, event):
        # size = (611*521)
        #print(event.x(), event.y())
        #w = self.ui.batch.width()
        #h = self.ui.batch.height()

        i = next(x[0] for x in enumerate(self.batch_x) if x[1] >= event.x())
        j = next(y[0] for y in enumerate(self.batch_y) if y[1] >= event.y())
        pic_num = (j-1)*6 + i
        if i > 0 and j > 0 and pic_num not in [1, 6, 31, 36]:
            self.ui.status_value.setText(self.data.data_prep2(self.data.classes[i-1][j-1]))
            self.ui.rate_value.setText(self.data.data_prep1(self.data.growth[i-1][j-1]))
            
            self.ns = self.path_sub + self.day + '/' + str(pic_num) + self.png
            self.img = QPixmap(self.ns)
            self.ui.sample_image.setPixmap(self.img.scaled(self.ui.sample_image.size(),Qt.KeepAspectRatio))
        elif pic_num in [1, 6, 31, 36]:
            print("Excluded observation")
        
    def current(self, event):
        print(event)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestUI()
    w.show()
    sys.exit(app.exec_())