# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface.ui'
#
# Created: Sat Feb  7 13:01:39 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setAutoFillBackground(False)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Interface_groupBox = QtGui.QGroupBox(Dialog)
        self.Interface_groupBox.setObjectName("Interface_groupBox")
        self.interface_comboBox = QtGui.QComboBox(self.Interface_groupBox)
        self.interface_comboBox.setGeometry(QtCore.QRect(0, 70, 141, 31))
        self.interface_comboBox.setObjectName("interface_comboBox")
        self.Interface_label = QtGui.QLabel(self.Interface_groupBox)
        self.Interface_label.setGeometry(QtCore.QRect(0, 20, 141, 41))
        self.Interface_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Interface_label.setWordWrap(True)
        self.Interface_label.setObjectName("Interface_label")
        self.label = QtGui.QLabel(self.Interface_groupBox)
        self.label.setGeometry(QtCore.QRect(0, 100, 161, 121))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.Interface_groupBox)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.monitor_comboBox = QtGui.QComboBox(self.groupBox)
        self.monitor_comboBox.setGeometry(QtCore.QRect(0, 70, 151, 31))
        self.monitor_comboBox.setObjectName("monitor_comboBox")
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(0, 20, 181, 41))
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 161, 111))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.Interface_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.Interface_label.setText(QtGui.QApplication.translate("Dialog", "Select Interface for this attack", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "The interface you select will be put in monitor mode and used for this attack.", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Monitor Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Interface already in monitor mode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "You may select one of the interface(s) already in monitor mode. An attempt will be made to anonimize it.", None, QtGui.QApplication.UnicodeUTF8))

