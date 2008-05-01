# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwidget.ui'
#
# Created: Thu May  1 00:00:11 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(QtCore.QSize(QtCore.QRect(0,0,800,600).size()).expandedTo(MainWidget.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(MainWidget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter = QtGui.QSplitter(MainWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.widget)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setFrameShape(QtGui.QFrame.Panel)
        self.label.setFrameShadow(QtGui.QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.round_field = QtGui.QLineEdit(self.widget)

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        self.round_field.setFont(font)
        self.round_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.round_field.setFrame(True)
        self.round_field.setReadOnly(True)
        self.round_field.setObjectName("round_field")
        self.gridlayout.addWidget(self.round_field,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.widget)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtGui.QFrame.Panel)
        self.label_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.drafting_field = QtGui.QLineEdit(self.widget)

        font = QtGui.QFont()
        font.setPointSize(12)
        self.drafting_field.setFont(font)
        self.drafting_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.drafting_field.setReadOnly(True)
        self.drafting_field.setObjectName("drafting_field")
        self.gridlayout.addWidget(self.drafting_field,1,1,1,1)

        self.label_3 = QtGui.QLabel(self.widget)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtGui.QFrame.Panel)
        self.label_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.next_field = QtGui.QLineEdit(self.widget)

        font = QtGui.QFont()
        font.setPointSize(12)
        self.next_field.setFont(font)
        self.next_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.next_field.setReadOnly(True)
        self.next_field.setObjectName("next_field")
        self.gridlayout.addWidget(self.next_field,2,1,1,1)
        self.hboxlayout.addLayout(self.gridlayout)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.timerDisplay = QtGui.QLCDNumber(self.widget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerDisplay.sizePolicy().hasHeightForWidth())
        self.timerDisplay.setSizePolicy(sizePolicy)
        self.timerDisplay.setSmallDecimalPoint(False)
        self.timerDisplay.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.timerDisplay.setProperty("value",QtCore.QVariant(0.0))
        self.timerDisplay.setObjectName("timerDisplay")
        self.vboxlayout2.addWidget(self.timerDisplay)

        self.pause_button = QtGui.QPushButton(self.widget)
        self.pause_button.setObjectName("pause_button")
        self.vboxlayout2.addWidget(self.pause_button)
        self.hboxlayout.addLayout(self.vboxlayout2)
        self.vboxlayout1.addLayout(self.hboxlayout)

        self.avail_view = QtGui.QTableView(self.widget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
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

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
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
        self.label.setText(QtGui.QApplication.translate("MainWidget", "Round:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWidget", "Drafting: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWidget", "Next:", None, QtGui.QApplication.UnicodeUTF8))
        self.pause_button.setText(QtGui.QApplication.translate("MainWidget", "Start", None, QtGui.QApplication.UnicodeUTF8))

