# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_addplayerdialog.ui'
#
# Created: Thu Sep  1 08:52:32 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AddPlayerDialog(object):
    def setupUi(self, AddPlayerDialog):
        AddPlayerDialog.setObjectName(_fromUtf8("AddPlayerDialog"))
        AddPlayerDialog.resize(353, 99)
        AddPlayerDialog.setWindowTitle(QtGui.QApplication.translate("AddPlayerDialog", "Add Player", None, QtGui.QApplication.UnicodeUTF8))
        self.gridlayout = QtGui.QGridLayout(AddPlayerDialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label_2 = QtGui.QLabel(AddPlayerDialog)
        self.label_2.setText(QtGui.QApplication.translate("AddPlayerDialog", "Player Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtGui.QLabel(AddPlayerDialog)
        self.label.setText(QtGui.QApplication.translate("AddPlayerDialog", "Position:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.player_name_field = QtGui.QLineEdit(AddPlayerDialog)
        self.player_name_field.setObjectName(_fromUtf8("player_name_field"))
        self.gridlayout.addWidget(self.player_name_field, 1, 1, 1, 1)
        self.position_combo_box = QtGui.QComboBox(AddPlayerDialog)
        self.position_combo_box.setObjectName(_fromUtf8("position_combo_box"))
        self.gridlayout.addWidget(self.position_combo_box, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AddPlayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(AddPlayerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddPlayerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddPlayerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddPlayerDialog)

    def retranslateUi(self, AddPlayerDialog):
        pass

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwidget.ui'
#
# Created: Thu Sep  1 08:52:32 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName(_fromUtf8("MainWidget"))
        MainWidget.resize(1093, 600)
        MainWidget.setWindowTitle(QtGui.QApplication.translate("MainWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(MainWidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.splitter = QtGui.QSplitter(MainWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label.setFrameShadow(QtGui.QFrame.Sunken)
        self.label.setLineWidth(3)
        self.label.setText(QtGui.QApplication.translate("MainWidget", "Round:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.round_field = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.round_field.sizePolicy().hasHeightForWidth())
        self.round_field.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(18)
        self.round_field.setFont(font)
        self.round_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.round_field.setText(_fromUtf8(""))
        self.round_field.setFrame(True)
        self.round_field.setReadOnly(True)
        self.round_field.setObjectName(_fromUtf8("round_field"))
        self.gridlayout.addWidget(self.round_field, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_2.setLineWidth(3)
        self.label_2.setText(QtGui.QApplication.translate("MainWidget", "Drafting: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.drafting_field = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drafting_field.sizePolicy().hasHeightForWidth())
        self.drafting_field.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.drafting_field.setFont(font)
        self.drafting_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.drafting_field.setText(_fromUtf8(""))
        self.drafting_field.setReadOnly(True)
        self.drafting_field.setObjectName(_fromUtf8("drafting_field"))
        self.gridlayout.addWidget(self.drafting_field, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_3.setLineWidth(3)
        self.label_3.setText(QtGui.QApplication.translate("MainWidget", "Next:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.next_field = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_field.sizePolicy().hasHeightForWidth())
        self.next_field.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.next_field.setFont(font)
        self.next_field.setFocusPolicy(QtCore.Qt.NoFocus)
        self.next_field.setText(_fromUtf8(""))
        self.next_field.setReadOnly(True)
        self.next_field.setObjectName(_fromUtf8("next_field"))
        self.gridlayout.addWidget(self.next_field, 2, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridlayout)
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.previous_picks_list = QtGui.QListWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_picks_list.sizePolicy().hasHeightForWidth())
        self.previous_picks_list.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.previous_picks_list.setFont(font)
        self.previous_picks_list.setLineWidth(3)
        self.previous_picks_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.previous_picks_list.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.previous_picks_list.setViewMode(QtGui.QListView.ListMode)
        self.previous_picks_list.setObjectName(_fromUtf8("previous_picks_list"))
        self.vboxlayout.addWidget(self.previous_picks_list)
        self.horizontalLayout.addLayout(self.vboxlayout)
        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.timerDisplay = QtGui.QLCDNumber(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerDisplay.sizePolicy().hasHeightForWidth())
        self.timerDisplay.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.timerDisplay.setFont(font)
        self.timerDisplay.setFrameShape(QtGui.QFrame.StyledPanel)
        self.timerDisplay.setFrameShadow(QtGui.QFrame.Sunken)
        self.timerDisplay.setLineWidth(3)
        self.timerDisplay.setSmallDecimalPoint(False)
        self.timerDisplay.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.timerDisplay.setProperty("value", 0.0)
        self.timerDisplay.setObjectName(_fromUtf8("timerDisplay"))
        self.vboxlayout1.addWidget(self.timerDisplay)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.reset_button = QtGui.QPushButton(self.layoutWidget)
        self.reset_button.setText(QtGui.QApplication.translate("MainWidget", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.reset_button.setObjectName(_fromUtf8("reset_button"))
        self.hboxlayout.addWidget(self.reset_button)
        self.pause_button = QtGui.QPushButton(self.layoutWidget)
        self.pause_button.setText(QtGui.QApplication.translate("MainWidget", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.pause_button.setObjectName(_fromUtf8("pause_button"))
        self.hboxlayout.addWidget(self.pause_button)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.horizontalLayout.addLayout(self.vboxlayout1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        self.avail_view = QtGui.QTableView(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.avail_view.sizePolicy().hasHeightForWidth())
        self.avail_view.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.avail_view.setFont(font)
        self.avail_view.setLineWidth(3)
        self.avail_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.avail_view.setAlternatingRowColors(True)
        self.avail_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.avail_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.avail_view.setShowGrid(False)
        self.avail_view.setSortingEnabled(True)
        self.avail_view.setObjectName(_fromUtf8("avail_view"))
        self.vboxlayout2.addWidget(self.avail_view)
        self.verticalLayout.addLayout(self.vboxlayout2)
        self.drafted_view = QtGui.QToolBox(self.splitter)
        self.drafted_view.setObjectName(_fromUtf8("drafted_view"))
        self.horizontalLayout_2.addWidget(self.splitter)

        self.retranslateUi(MainWidget)
        self.drafted_view.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        pass

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_teamdialog.ui'
#
# Created: Thu Sep  1 08:52:33 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TeamDialog(object):
    def setupUi(self, TeamDialog):
        TeamDialog.setObjectName(_fromUtf8("TeamDialog"))
        TeamDialog.resize(452, 477)
        TeamDialog.setWindowTitle(QtGui.QApplication.translate("TeamDialog", "Team Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.vboxlayout = QtGui.QVBoxLayout(TeamDialog)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.label = QtGui.QLabel(TeamDialog)
        self.label.setText(QtGui.QApplication.translate("TeamDialog", "Team Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout1.addWidget(self.label)
        self.team_name_field = QtGui.QLineEdit(TeamDialog)
        self.team_name_field.setObjectName(_fromUtf8("team_name_field"))
        self.vboxlayout1.addWidget(self.team_name_field)
        self.label_2 = QtGui.QLabel(TeamDialog)
        self.label_2.setText(QtGui.QApplication.translate("TeamDialog", "Manager Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.vboxlayout1.addWidget(self.label_2)
        self.manager_name_field = QtGui.QLineEdit(TeamDialog)
        self.manager_name_field.setObjectName(_fromUtf8("manager_name_field"))
        self.vboxlayout1.addWidget(self.manager_name_field)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.add_button = QtGui.QPushButton(TeamDialog)
        self.add_button.setText(QtGui.QApplication.translate("TeamDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.add_button.setObjectName(_fromUtf8("add_button"))
        self.vboxlayout1.addWidget(self.add_button)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.team_list_view = QtGui.QListView(TeamDialog)
        self.team_list_view.setObjectName(_fromUtf8("team_list_view"))
        self.hboxlayout.addWidget(self.team_list_view)
        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem1)
        self.move_up_button = QtGui.QPushButton(TeamDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.move_up_button.sizePolicy().hasHeightForWidth())
        self.move_up_button.setSizePolicy(sizePolicy)
        self.move_up_button.setMaximumSize(QtCore.QSize(21, 27))
        self.move_up_button.setText(QtGui.QApplication.translate("TeamDialog", "/\\", None, QtGui.QApplication.UnicodeUTF8))
        self.move_up_button.setObjectName(_fromUtf8("move_up_button"))
        self.vboxlayout2.addWidget(self.move_up_button)
        self.move_down_button = QtGui.QPushButton(TeamDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.move_down_button.sizePolicy().hasHeightForWidth())
        self.move_down_button.setSizePolicy(sizePolicy)
        self.move_down_button.setMaximumSize(QtCore.QSize(21, 27))
        self.move_down_button.setText(QtGui.QApplication.translate("TeamDialog", "\\/", None, QtGui.QApplication.UnicodeUTF8))
        self.move_down_button.setObjectName(_fromUtf8("move_down_button"))
        self.vboxlayout2.addWidget(self.move_down_button)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem2)
        self.hboxlayout.addLayout(self.vboxlayout2)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.line = QtGui.QFrame(TeamDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.vboxlayout.addWidget(self.line)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label_3 = QtGui.QLabel(TeamDialog)
        self.label_3.setText(QtGui.QApplication.translate("TeamDialog", "Pick Time Limit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.hboxlayout1.addWidget(self.label_3)
        self.timeEdit = QtGui.QTimeEdit(TeamDialog)
        self.timeEdit.setMaximumTime(QtCore.QTime(13, 0, 59))
        self.timeEdit.setDisplayFormat(QtGui.QApplication.translate("TeamDialog", "m:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.hboxlayout1.addWidget(self.timeEdit)
        self.autoPick = QtGui.QCheckBox(TeamDialog)
        self.autoPick.setToolTip(QtGui.QApplication.translate("TeamDialog", "Automatically take top-rated player when timer expires", None, QtGui.QApplication.UnicodeUTF8))
        self.autoPick.setText(QtGui.QApplication.translate("TeamDialog", "Auto-pick on expire?", None, QtGui.QApplication.UnicodeUTF8))
        self.autoPick.setObjectName(_fromUtf8("autoPick"))
        self.hboxlayout1.addWidget(self.autoPick)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem3)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.buttonBox = QtGui.QDialogButtonBox(TeamDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(TeamDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TeamDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TeamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TeamDialog)

    def retranslateUi(self, TeamDialog):
        pass

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_webauth.ui'
#
# Created: Thu Sep  1 08:52:33 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_WebAuthDialog(object):
    def setupUi(self, WebAuthDialog):
        WebAuthDialog.setObjectName(_fromUtf8("WebAuthDialog"))
        WebAuthDialog.resize(385, 604)
        WebAuthDialog.setWindowTitle(QtGui.QApplication.translate("WebAuthDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(WebAuthDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.webView = QtWebKit.QWebView(WebAuthDialog)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)
        self.label = QtGui.QLabel(WebAuthDialog)
        self.label.setText(QtGui.QApplication.translate("WebAuthDialog", "1. Log in to Yahoo!\n"
"2.Allow ffdraft access to fantasy sports\n"
"3.Enter verification code below:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.verification_edit = QtGui.QLineEdit(WebAuthDialog)
        self.verification_edit.setObjectName(_fromUtf8("verification_edit"))
        self.verticalLayout.addWidget(self.verification_edit)
        self.buttonBox = QtGui.QDialogButtonBox(WebAuthDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(WebAuthDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), WebAuthDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), WebAuthDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(WebAuthDialog)

    def retranslateUi(self, WebAuthDialog):
        pass

from PyQt4 import QtWebKit
