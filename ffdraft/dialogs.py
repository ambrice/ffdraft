#!/usr/bin/python

import models
from PyQt4 import QtCore, QtGui
from ffdraft.ui import Ui_TeamDialog, Ui_AddPlayerDialog, Ui_WebAuthDialog

class TeamDialog(QtGui.QDialog, Ui_TeamDialog):
    def __init__(self, league_name, team_list = [], timer = 0, autopick = False, parent = None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        self.model = models.TeamModel(league_name)
        self.team_list_view.setModel(self.model)

        self.add_button.clicked.connect(self.add_team)
        self.move_up_button.clicked.connect(self.move_team_up)
        self.move_down_button.clicked.connect(self.move_team_down)

        time = QtCore.QTime()
        min = int(timer) / 60
        sec = timer % 60
        time.setHMS(0, min, sec)
        self.timeEdit.setTime(time)
        self.autoPick.setChecked(True)

    def add_team(self):
        team = str(self.team_name_field.text())
        manager = str(self.manager_name_field.text())
        if team == '':
            return
        self.model.append_team(team, manager)
        self.team_name_field.clear()
        self.manager_name_field.clear()
        self.team_name_field.setFocus()

    def move_team_down(self):
        row = self.team_list_view.selectedIndexes().pop(0).row()
        if row == self.model.rowCount() - 1:
            # Already at bottom of list
            return
        self.model.move_down(row)
        self.team_list_view.selectionModel().select(self.model.index(row + 1, 0), QtGui.QItemSelectionModel.ClearAndSelect)

    def move_team_up(self):
        row = self.team_list_view.selectedIndexes().pop(0).row()
        if row == 0:
            # Already at top of list
            return
        self.model.move_up(row)
        self.team_list_view.selectionModel().select(self.model.index(row - 1, 0), QtGui.QItemSelectionModel.ClearAndSelect)

    def get_team_list(self):
        return self.model.team_names()

    def get_time_limit(self):
        sec = self.timeEdit.time().second()
        min = self.timeEdit.time().minute()
        return min * 60 + sec

    def get_autopick(self):
        return self.autoPick.isChecked()


class AddPlayerDialog(QtGui.QDialog, Ui_AddPlayerDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        self.position_combo_box.addItem("RB")
        self.position_combo_box.addItem("QB")
        self.position_combo_box.addItem("WR")
        self.position_combo_box.addItem("TE")
        self.position_combo_box.addItem("K")
        self.position_combo_box.addItem("DEF")

class WebAuthDialog(QtGui.QDialog, Ui_WebAuthDialog):
    def __init__(self, url=None, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)
        self.resize(512, 649)
        if url:
            self.webView.load(QtCore.QUrl(url))

    def resizeEvent(self, e):
        #print 'Dialog: {0}x{1}'.format(e.size().width(), e.size().height())
        QtGui.QDialog.resizeEvent(self, e)
