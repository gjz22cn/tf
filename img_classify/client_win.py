# -*- coding: utf-8 -*-

"""
Module implementing ModeSelect.
"""
import sys
import os
import socket
import time
import RPi.GPIO as GPIO
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from Ui_ClassifyForm import Ui_ClassifyForm


class ClassifyWindow(QWidget, Ui_ClassifyForm):
    def __init__(self, parent=None):
        super(ClassifyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Qt.CustomizeWindowHint)
        self.classifyBtn.clicked.connect(self.do_classify)
        self.closeBtn.clicked.connect(self.do_close)
        
        self.pin_1 = 18 # GPIO PIN 18
        self.pin_2 = 23 # GPIO PIN 23
        self.pin_3 = 24 # GPIO PIN 24
        self.pin_4 = 25 # GPIO PIN 25
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.init_gpio()

        self.server = ('127.0.0.1', 9999)
        self.sock = self.socket_init()
        self.resultLabel.setText("Res:")

    def init_gpio(self):
        GPIO.setup(self.pin_1, GPIO.OUT)
        GPIO.setup(self.pin_2, GPIO.OUT)
        GPIO.setup(self.pin_3, GPIO.OUT)
        GPIO.setup(self.pin_4, GPIO.OUT)

    def on_gpio(self, pin, t_sleep):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(t_sleep)
        GPIO.output(pin, GPIO.LOW)

    def do_classify(self):
        #filename, ext = QFileDialog.getOpenFileName(self, 'open file', '')
        #print(filename, ext)
        filename = '/tmp/picture.jpg'
        self.pic_cap(0, filename)
        #time.sleep(0.5)

        res = self.query_srv(filename)

        if res != 'ERROR':
            if res == 'Other':
                self.on_gpio(self.pin_1, 2);
                self.on_gpio(self.pin_2, 2);
            else:
                self.on_gpio(self.pin_3, 2);
                self.on_gpio(self.pin_4, 2);

        jpg = QtGui.QPixmap(filename).scaled(self.imageLabel.width(), self.imageLabel.height())
        self.imageLabel.setPixmap(jpg)
        self.resultLabel.setText("Res: " + res)
    
    def pic_cap(self, idx, filename):
        #cmd = 'fswebcam -d /dev/video%d -r 1080x1080 --no-banner %s'%(idx, filename)
        #cmd = 'raspistill -t 1 -o %s -w 1080 -h 1080'%(filename)
        cmd = 'raspistill -t 300 -o %s -w 1080 -h 1080'%(filename)
        os.system(cmd)

    def socket_init(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return client

    def query_srv(self, filename):
        self.sock.sendto(filename.encode('utf-8'), self.server)
        data, server_addr = self.sock.recvfrom(1024)
        res = data.decode()
        res_array = res.split('\n')
        if len(res_array) < 1:
            return 'ERROR'

        result = res_array[0].split(' ')
        if len(result) < 1:
            return 'ERROR'

        return result[0]

    def do_close(self):
        os.system("echo '123456' | sudo -S shutdown -h 0")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    classifyWindow = ClassifyWindow()
    classifyWindow.show()
    sys.exit(app.exec_())
