# -*- coding: utf-8 -*-

"""
Module implementing ModeSelect.
"""
import sys
import os
import socket
import time
import RPi.GPIO as GPIO
import picamera
import _thread
from PyQt5.QtCore import Qt, pyqtSignal,QCoreApplication
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from Ui_ClassifyForm import Ui_ClassifyForm


class ClassifyWindow(QWidget, Ui_ClassifyForm):
    def __init__(self, parent=None):
        super(ClassifyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Qt.CustomizeWindowHint)
        self.classifyBtn.clicked.connect(self.do_classify)
        self.exitBtn.clicked.connect(QCoreApplication.quit)
        self.closeBtn.clicked.connect(self.do_close)
        
        # BCM 
        self.out_1 = 18
        self.out_2 = 23
        self.out_3 = 24
        self.out_4 = 25
        self.in_1 = 20
        self.in_2 = 21
        self.init_gpio()

        self.camera = picamera.PiCamera()
        self.camera.resolution = (1080,1080)
        self.camera.framerate = 60

        self.server = ('127.0.0.1', 9999)
        self.sock = self.socket_init()
        self.resultLabel.setText("R:")
        self.last_time = time.time()



    def door_callback(self, pin):
        time.sleep(0.01)
        if GPIO.input(pin):
            now_time = time.time()
            if (now_time - self.last_time) > 6:
                print ("%f"%(now_time - self.last_time))
                self.do_classify()
                self.last_time = now_time

    def init_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.out_1, GPIO.OUT)
        GPIO.setup(self.out_2, GPIO.OUT)
        GPIO.setup(self.out_3, GPIO.OUT)
        GPIO.setup(self.out_4, GPIO.OUT)
        GPIO.setup(self.in_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.in_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.in_1, GPIO.RISING, callback=self.door_callback, bouncetime=500)
        GPIO.add_event_detect(self.in_2, GPIO.RISING, callback=self.door_callback, bouncetime=500)

    def on_gpio(self, pin, t_sleep):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(t_sleep)
        GPIO.output(pin, GPIO.LOW)

    def set_gpio(self, pin, v):
        if v:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

    def do_classify(self):
        filename = '/tmp/picture.jpg'
        
        # turn led on
        self.set_gpio(self.out_4, True)

        self.pic_cap(0, filename)
        
        try:
            _thread.start_new_thread(self.query_srv, (filename,))
        except:
            print ("Error: unable to start thread")

        #res = self.query_srv(filename)

        jpg = QtGui.QPixmap(filename).scaled(self.imageLabel.width(), self.imageLabel.height())
        self.imageLabel.setPixmap(jpg)

        # turn led off
        self.set_gpio(self.out_4, False)

        #self.do_action(res)

    def do_action(self, res):
        print ('res='+res)
        self.resultLabel.setText("R: " + res)

        if res != 'ERROR':
            if res == 'trash':
                self.on_gpio(self.out_1, 2);
            else:
                self.on_gpio(self.out_2, 2);
    
    def pic_cap(self, idx, filename):
        #cmd = 'fswebcam -d /dev/video%d -r 1080x1080 --no-banner %s'%(idx, filename)
        #cmd = 'raspistill -t 300 -o %s -w 1080 -h 1080'%(filename)
        #os.system(cmd)
        #self.camera.start_preview()
        self.camera.capture(filename)
        #self.camera.stop_preview()

    def socket_init(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return client

    def query_srv(self, filename):
        t1 = time.time()
        self.sock.sendto(filename.encode('utf-8'), self.server)
        data, server_addr = self.sock.recvfrom(1024)
        t2 = time.time()
        print ("query time=%ds"%(t2-t1))
        res = data.decode()
        res_array = res.split('\n')
        if len(res_array) < 1:
            return 'ERROR'

        result = res_array[0].split(' ')
        if len(result) < 1:
            return 'ERROR'

        self.do_action(result[0])

        return result[0]

    def do_close(self):
        os.system("echo '123456' | sudo -S shutdown -h 0")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    classifyWindow = ClassifyWindow()
    classifyWindow.show()
    sys.exit(app.exec_())
