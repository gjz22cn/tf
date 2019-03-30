# -*- coding: utf-8 -*-

"""
Module implementing ModeSelect.
"""
import sys
import os
import numpy as np
import cv2
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_ClassifyForm import Ui_ClassifyForm

class ClassifyWindow(QWidget, Ui_ClassifyForm):
    def __init__(self, parent=None):
        super(ClassifyWindow, self).__init__(parent)
        self.setupUi(self)
        self.classifyBtn.clicked.connect(self.do_classify)

    def do_classify(self):
        filename, ext = QFileDialog.getOpenFileName(self, 'open file', '')
        print(filename, ext)
        jpg = QtGui.QPixmap(filename).scaled(self.imageLabel.width(), self.imageLabel.height())
        self.imageLabel.setPixmap(jpg)
        self.resultLabel.setText("结果")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    classifyWindow = ClassifyWindow()
    classifyWindow.show()
    sys.exit(app.exec_())
