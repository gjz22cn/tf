# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_ClassifyForm.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ClassifyForm(object):
    def setupUi(self, ClassifyForm):
        ClassifyForm.setObjectName("ClassifyForm")
        ClassifyForm.resize(450, 270)
        self.classifyBtn = QtWidgets.QPushButton(ClassifyForm)
        self.classifyBtn.setGeometry(QtCore.QRect(330, 40, 90, 30))
        self.classifyBtn.setObjectName("classifyBtn")
        '''
        self.zhileiBtn = QtWidgets.QPushButton(ClassifyForm)
        self.zhileiBtn.setGeometry(QtCore.QRect(330, 80, 90, 30))
        self.zhileiBtn.setObjectName("zhileiBtn")
        self.boliBtn = QtWidgets.QPushButton(ClassifyForm)
        self.boliBtn.setGeometry(QtCore.QRect(330, 120, 90, 30))
        self.boliBtn.setObjectName("boliBtn")
        self.suliaoBtn = QtWidgets.QPushButton(ClassifyForm)
        self.suliaoBtn.setGeometry(QtCore.QRect(330, 160, 90, 30))
        self.suliaoBtn.setObjectName("suliaoBtn")
        '''
        self.exitBtn = QtWidgets.QPushButton(ClassifyForm)
        self.exitBtn.setGeometry(QtCore.QRect(330, 150, 90, 30))
        self.exitBtn.setObjectName("exitBtn")
        self.imageLabel = QtWidgets.QLabel(ClassifyForm)
        self.imageLabel.setGeometry(QtCore.QRect(40, 10, 240, 240))
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.resultLabel = QtWidgets.QLabel(ClassifyForm)
        self.resultLabel.setGeometry(QtCore.QRect(330, 80, 90, 20))
        self.resultLabel.setObjectName("resultLabel")
        self.closeBtn = QtWidgets.QPushButton(ClassifyForm)
        self.closeBtn.setGeometry(QtCore.QRect(330, 190, 90, 30))
        self.closeBtn.setObjectName("closeBtn")

        self.retranslateUi(ClassifyForm)
        QtCore.QMetaObject.connectSlotsByName(ClassifyForm)

    def retranslateUi(self, ClassifyForm):
        _translate = QtCore.QCoreApplication.translate
        ClassifyForm.setWindowTitle(_translate("ClassifyForm", "分类"))
        self.classifyBtn.setText(_translate("ClassifyForm", "识 别"))
        '''
        self.zhileiBtn.setText(_translate("ClassifyForm", "纸 类"))
        self.boliBtn.setText(_translate("ClassifyForm", "玻 璃"))
        self.suliaoBtn.setText(_translate("ClassifyForm", "塑 料"))
        '''
        self.exitBtn.setText(_translate("ClassifyForm", "退 出"))
        self.resultLabel.setText(_translate("ClassifyForm", "TextLabel"))
        self.closeBtn.setText(_translate("ClassifyForm", "关 机"))

