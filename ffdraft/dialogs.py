#!/usr/bin/python

from PyQt4 import QtCore, QtGui
from ffdraft.ui import Ui_TeamDialog, Ui_AddPlayerDialog

class TeamDialog(QtGui.QDialog, Ui_TeamDialog):
    def __init__(self, team_list = [], timer = 0, autopick = False, parent = None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        self.model = QtGui.QStringListModel()
        self.model.setStringList(team_list)
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
        team = self.team_name_field.text()
        manager = self.manager_name_field.text()

        if team == "":
            return

        full_name = team + " (" + manager + ")"

        new_row = self.model.rowCount()
        self.model.insertRows(new_row, 1)
        idx = self.model.index(new_row)
        self.model.setData(idx, QtCore.QVariant(full_name))
        self.team_name_field.clear()
        self.manager_name_field.clear()
        self.team_name_field.setFocus()

    def move_team_down(self):
        row = self.team_list_view.selectedIndexes().pop(0).row()
        if row == self.model.rowCount() - 1:
            # Already at bottom of list
            return
        old_idx = self.model.createIndex(row, 0)
        new_idx = self.model.createIndex(row + 1, 0)
        old_value = self.model.data(old_idx, QtCore.Qt.EditRole)
        new_value = self.model.data(new_idx, QtCore.Qt.EditRole)
        self.model.setData(old_idx, new_value)
        self.model.setData(new_idx, old_value)
        self.team_list_view.selectionModel().select(new_idx, QtGui.QItemSelectionModel.ClearAndSelect)

    def move_team_up(self):
        row = self.team_list_view.selectedIndexes().pop(0).row()
        if row == 0:
            # Already at top of list
            return
        old_idx = self.model.createIndex(row, 0)
        new_idx = self.model.createIndex(row - 1, 0)
        old_value = self.model.data(old_idx, QtCore.Qt.EditRole)
        new_value = self.model.data(new_idx, QtCore.Qt.EditRole)
        self.model.setData(old_idx, new_value)
        self.model.setData(new_idx, old_value)
        self.team_list_view.selectionModel().select(new_idx, QtGui.QItemSelectionModel.ClearAndSelect)

    def get_team_list(self):
        return self.model.stringList()

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

