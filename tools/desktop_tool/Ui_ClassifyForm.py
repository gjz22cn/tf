# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_ClassifyForm.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClassifyForm(object):
    def setupUi(self, ClassifyForm):
        ClassifyForm.setObjectName("ClassifyForm")
        ClassifyForm.resize(420, 430)
        self.imageLabel = QtWidgets.QLabel(ClassifyForm)
        self.imageLabel.setGeometry(QtCore.QRect(50, 90, 320, 320))
        self.imageLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.resultLabel = QtWidgets.QLabel(ClassifyForm)
        self.resultLabel.setGeometry(QtCore.QRect(50, 20, 320, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.resultLabel.setFont(font)
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLabel.setObjectName("resultLabel")

        self.retranslateUi(ClassifyForm)
        QtCore.QMetaObject.connectSlotsByName(ClassifyForm)

    def retranslateUi(self, ClassifyForm):
        _translate = QtCore.QCoreApplication.translate
        ClassifyForm.setWindowTitle(_translate("ClassifyForm", "垃圾分类"))
        self.resultLabel.setText(_translate("ClassifyForm", "分类结果"))


