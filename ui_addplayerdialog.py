# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_addplayerdialog.ui'
#
# Created: Fri Aug 31 20:35:07 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_AddPlayerDialog(object):
    def setupUi(self, AddPlayerDialog):
        AddPlayerDialog.setObjectName("AddPlayerDialog")
        AddPlayerDialog.resize(QtCore.QSize(QtCore.QRect(0,0,353,99).size()).expandedTo(AddPlayerDialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(AddPlayerDialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label_2 = QtGui.QLabel(AddPlayerDialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,1,1,1)

        self.label = QtGui.QLabel(AddPlayerDialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.player_name_field = QtGui.QLineEdit(AddPlayerDialog)
        self.player_name_field.setObjectName("player_name_field")
        self.gridlayout.addWidget(self.player_name_field,1,1,1,1)

        self.position_combo_box = QtGui.QComboBox(AddPlayerDialog)
        self.position_combo_box.setObjectName("position_combo_box")
        self.gridlayout.addWidget(self.position_combo_box,1,0,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(AddPlayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,2,0,1,2)

        self.retranslateUi(AddPlayerDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),AddPlayerDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),AddPlayerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddPlayerDialog)

    def retranslateUi(self, AddPlayerDialog):
        AddPlayerDialog.setWindowTitle(QtGui.QApplication.translate("AddPlayerDialog", "Add Player", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AddPlayerDialog", "Player Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AddPlayerDialog", "Position:", None, QtGui.QApplication.UnicodeUTF8))

