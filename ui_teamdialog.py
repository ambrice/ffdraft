# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_teamdialog.ui'
#
# Created: Tue Aug 21 20:15:51 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_TeamDialog(object):
    def setupUi(self, TeamDialog):
        TeamDialog.setObjectName("TeamDialog")
        TeamDialog.resize(QtCore.QSize(QtCore.QRect(0,0,452,304).size()).expandedTo(TeamDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(TeamDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(TeamDialog)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.team_name_field = QtGui.QLineEdit(TeamDialog)
        self.team_name_field.setObjectName("team_name_field")
        self.vboxlayout1.addWidget(self.team_name_field)

        self.label_2 = QtGui.QLabel(TeamDialog)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)

        self.manager_name_field = QtGui.QLineEdit(TeamDialog)
        self.manager_name_field.setObjectName("manager_name_field")
        self.vboxlayout1.addWidget(self.manager_name_field)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)

        self.add_button = QtGui.QPushButton(TeamDialog)
        self.add_button.setObjectName("add_button")
        self.vboxlayout1.addWidget(self.add_button)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.team_list_view = QtGui.QListView(TeamDialog)
        self.team_list_view.setObjectName("team_list_view")
        self.hboxlayout.addWidget(self.team_list_view)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem1)

        self.move_up_button = QtGui.QPushButton(TeamDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.move_up_button.sizePolicy().hasHeightForWidth())
        self.move_up_button.setSizePolicy(sizePolicy)
        self.move_up_button.setMaximumSize(QtCore.QSize(21,27))
        self.move_up_button.setObjectName("move_up_button")
        self.vboxlayout2.addWidget(self.move_up_button)

        self.move_down_button = QtGui.QPushButton(TeamDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.move_down_button.sizePolicy().hasHeightForWidth())
        self.move_down_button.setSizePolicy(sizePolicy)
        self.move_down_button.setMaximumSize(QtCore.QSize(21,27))
        self.move_down_button.setObjectName("move_down_button")
        self.vboxlayout2.addWidget(self.move_down_button)

        spacerItem2 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem2)
        self.hboxlayout.addLayout(self.vboxlayout2)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.buttonBox = QtGui.QDialogButtonBox(TeamDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(TeamDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),TeamDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),TeamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TeamDialog)

    def retranslateUi(self, TeamDialog):
        TeamDialog.setWindowTitle(QtGui.QApplication.translate("TeamDialog", "Team Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TeamDialog", "Team Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("TeamDialog", "Manager Name", None, QtGui.QApplication.UnicodeUTF8))
        self.add_button.setText(QtGui.QApplication.translate("TeamDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.move_up_button.setText(QtGui.QApplication.translate("TeamDialog", "/\\", None, QtGui.QApplication.UnicodeUTF8))
        self.move_down_button.setText(QtGui.QApplication.translate("TeamDialog", "\\/", None, QtGui.QApplication.UnicodeUTF8))

