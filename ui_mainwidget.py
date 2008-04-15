# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwidget.ui'
#
# Created: Fri Aug 17 00:43:56 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(QtCore.QSize(QtCore.QRect(0,0,800,600).size()).expandedTo(MainWidget.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(MainWidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter = QtGui.QSplitter(MainWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label_2 = QtGui.QLabel(self.layoutWidget)

        font = QtGui.QFont(self.label_2.font())
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtGui.QFrame.Panel)
        self.label_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.next_field = QtGui.QLineEdit(self.layoutWidget)

        font = QtGui.QFont(self.next_field.font())
        font.setPointSize(12)
        self.next_field.setFont(font)
        self.next_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.next_field.setReadOnly(True)
        self.next_field.setObjectName("next_field")
        self.gridlayout.addWidget(self.next_field,2,1,1,1)

        self.drafting_field = QtGui.QLineEdit(self.layoutWidget)

        font = QtGui.QFont(self.drafting_field.font())
        font.setPointSize(12)
        self.drafting_field.setFont(font)
        self.drafting_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.drafting_field.setReadOnly(True)
        self.drafting_field.setObjectName("drafting_field")
        self.gridlayout.addWidget(self.drafting_field,1,1,1,1)

        self.label_3 = QtGui.QLabel(self.layoutWidget)

        font = QtGui.QFont(self.label_3.font())
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtGui.QFrame.Panel)
        self.label_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.label = QtGui.QLabel(self.layoutWidget)

        font = QtGui.QFont(self.label.font())
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setFrameShape(QtGui.QFrame.Panel)
        self.label.setFrameShadow(QtGui.QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.round_field = QtGui.QLineEdit(self.layoutWidget)

        font = QtGui.QFont(self.round_field.font())
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        self.round_field.setFont(font)
        self.round_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.round_field.setFrame(True)
        self.round_field.setReadOnly(True)
        self.round_field.setObjectName("round_field")
        self.gridlayout.addWidget(self.round_field,0,1,1,1)
        self.vboxlayout1.addLayout(self.gridlayout)

        self.avail_view = QtGui.QTableView(self.layoutWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.avail_view.sizePolicy().hasHeightForWidth())
        self.avail_view.setSizePolicy(sizePolicy)
        self.avail_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.avail_view.setAlternatingRowColors(True)
        self.avail_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.avail_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.avail_view.setSortingEnabled(True)
        self.avail_view.setObjectName("avail_view")
        self.vboxlayout1.addWidget(self.avail_view)

        self.drafted_view = QtGui.QTreeView(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drafted_view.sizePolicy().hasHeightForWidth())
        self.drafted_view.setSizePolicy(sizePolicy)
        self.drafted_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.drafted_view.setObjectName("drafted_view")
        self.vboxlayout.addWidget(self.splitter)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QtGui.QApplication.translate("MainWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWidget", "Drafting: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWidget", "Next:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWidget", "Round:", None, QtGui.QApplication.UnicodeUTF8))

