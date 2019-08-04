# -*- coding: utf-8 -*-
import sys
import os
from socket import *
import requests
import _thread
import datetime
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
from Ui_ClassifyForm import Ui_ClassifyForm


class ClassifyWindow(QWidget, Ui_ClassifyForm):
    def __init__(self, parent=None):
        super(ClassifyWindow, self).__init__(parent)
        self.setupUi(self)
        self.udpServer = None
        self.imgPath = Path(r'D:\trash')
        self.imageDirInit()
        self.udpServerInit()
        self.startUpdServerLoop()

    def closeEvent(self, event):
        print("closeEvent")
        self.udpServerClose()
        event.accept()

    def startUpdServerLoop(self):
        try:
            _thread.start_new_thread(self.updServerLoop, ())
        except:
            print("Error: unable to start upd_server_loop thread")

    def udpServerInit(self):
        host = ''
        port = 6666
        addr = (host, port)
        udpServer = socket(AF_INET, SOCK_DGRAM)
        udpServer.bind(addr)
        self.udpServer = udpServer
        print("udpServerInit")

    def udpServerClose(self):
        self.udpServer.close()

    def updServerLoop(self):
        bufsize = 1024
        while True:
            print('Waiting for connection...')
            try:
                data, addr = self.udpServer.recvfrom(bufsize)
                data = data.decode(encoding='utf-8')
                result = data.split('-')
                if len(result) == 2:
                    self.resultLabel.setText(result[0])
                    self.startLoadNetPic(result[1], result[0])
            except:
                self.udpServerClose()
                self.resultLabel.setText("接收端异常，请重新打开！")
                break

    def startLoadNetPic(self, filename, label):
        try:
            _thread.start_new_thread(self.loadNetPic, (filename, label,))
        except Exception as e:
            print("Error: unable to start loadNetPic thread, %s"%e)

    def loadNetPic(self, filename, label):
        url = 'http://10.10.10.1/'+filename
        #url = 'https://raw.githubusercontent.com/gjz22cn/tf/master/img_classify/data/pre_image/glass34.jpg'
        req = requests.get(url)
        photo = QPixmap()
        photo.loadFromData(req.content)
        jpg = photo.scaled(self.imageLabel.width(), self.imageLabel.height())
        self.imageLabel.setPixmap(jpg)

        dir_path = os.path.join(self.imgPath, label)
        if not dir_path.is_dir():
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg')
        with open(file_path, 'wb') as f:
            f.write(req.content)

    def imageDirInit(self):
        if not self.imgPath.is_dir():
            os.makedirs(self.imgPath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    classifyWindow = ClassifyWindow()
    classifyWindow.show()
    sys.exit(app.exec_())
