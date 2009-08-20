#!/usr/bin/python
#
# Copyright (C) 2007-2009 Aaron Brice
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# Read more about GNU General Public License :http://www.gnu.org/licenses/gpl.txt
#
import sys
import re
import yaml
from string import join
from PyQt4 import QtCore, QtGui
from ui_mainwidget import Ui_MainWidget
from ui_teamdialog import Ui_TeamDialog
from ui_addplayerdialog import Ui_AddPlayerDialog

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)
        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.setWindowTitle("Fantasy Football Draft")
        self.version = 1.1

    def createActions(self):
        self.loadAct = QtGui.QAction("&Load", self)
        self.loadAct.setShortcut("Ctrl+L")
        self.loadAct.setStatusTip("Load draft from file")
        self.connect(self.loadAct, QtCore.SIGNAL("triggered()"), self.load)

        self.saveAsAct = QtGui.QAction("Save &As", self)
        self.saveAsAct.setStatusTip("Save draft to file")
        self.connect(self.saveAsAct, QtCore.SIGNAL("triggered()"), self.save_as)

        self.saveAct = QtGui.QAction("&Save", self)
        self.saveAct.setShortcut("Ctrl+S")
        self.saveAct.setStatusTip("Save draft to file")
        self.connect(self.saveAct, QtCore.SIGNAL("triggered()"), self.save)

        self.exportAct = QtGui.QAction("&Export", self)
        self.exportAct.setStatusTip("Export draft results to a text file")
        self.connect(self.exportAct, QtCore.SIGNAL("triggered()"), self.export)

        self.exitAct = QtGui.QAction("E&xit", self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.setStatusTip("Exit the application")
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("close()"))

        self.teamAct = QtGui.QAction("&Configure Teams", self)
        self.teamAct.setStatusTip("Add/Remove teams from the draft")
        self.connect(self.teamAct, QtCore.SIGNAL("triggered()"), self.edit_teams)

        self.keeperAct = QtGui.QAction("&Add Keeper", self)
        self.keeperAct.setStatusTip("Add a player as a keeper from a keeper league")
        self.connect(self.keeperAct, QtCore.SIGNAL("triggered()"), self.add_keeper)
        
        self.extraAct = QtGui.QAction("&Add Extra Player", self)
        self.extraAct.setStatusTip("Add an extra player to a team, outside of the draft")
        self.connect(self.extraAct, QtCore.SIGNAL("triggered()"), self.extra_player)

        self.removeAct = QtGui.QAction("&Remove Player", self)
        self.removeAct.setStatusTip("Remove a player from a team")
        self.connect(self.removeAct, QtCore.SIGNAL("triggered()"), self.remove_player)

        self.draftAct = QtGui.QAction("&Draft Unlisted Player", self)
        self.draftAct.setStatusTip("Draft a player that's not listed in the available player table")
        self.connect(self.draftAct, QtCore.SIGNAL("triggered()"), self.draft_unlisted_player)

        self.aboutAct = QtGui.QAction("About FFD", self)
        self.aboutAct.setStatusTip("About Fantasy Football Draft")
        self.connect(self.aboutAct, QtCore.SIGNAL("triggered()"), self.about)

        self.aboutQtAct = QtGui.QAction("About Qt", self)
        self.aboutQtAct.setStatusTip(self.tr("About the Qt GUI library"))
        self.connect(self.aboutQtAct, QtCore.SIGNAL("triggered()"), QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.loadAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.exportAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.teamAct)
        self.editMenu.addAction(self.extraAct)
        self.editMenu.addAction(self.keeperAct)
        self.editMenu.addAction(self.removeAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.draftAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.playerPopupMenu = QtGui.QMenu(self)
        self.playerPopupMenu.addAction(self.extraAct)
        self.playerPopupMenu.addAction(self.keeperAct)
        self.connect(self.mainWidget.avail_view, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), 
                self.showPlayerMenu)

        self.draftedPopupMenu = QtGui.QMenu(self)
        self.draftedPopupMenu.addAction(self.removeAct)
        self.draftedPopupMenu.addAction(self.draftAct)
        self.connect(self.mainWidget.drafted_view, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), 
                self.showDraftedMenu)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def showPlayerMenu(self, point):
        self.playerPopupMenu.exec_(QtGui.QCursor.pos())

    def showDraftedMenu(self, point):
        self.draftedPopupMenu.exec_(QtGui.QCursor.pos())

    def edit_teams(self):
        self.mainWidget.edit_teams()

    def save_as(self):
        self.mainWidget.save_as()

    def save(self):
        self.mainWidget.save()

    def load(self):
        self.mainWidget.load()

    def load_file(self, file):
        self.mainWidget.load_file(file)

    def export(self):
        self.mainWidget.export()

    def extra_player(self):
        self.mainWidget.extra_player()

    def add_keeper(self):
        self.mainWidget.extra_player(keeper=True)

    def remove_player(self):
        self.mainWidget.remove_player()

    def draft_unlisted_player(self):
        self.mainWidget.draft_unlisted_player()

    def about(self):
        QtGui.QMessageBox.about(self, "About Fantasy Football Draft",
                "Fantasy Football Draft version " + str(self.version) + "\n\n"
                +"Copyright (C) 2007-2009 Aaron Brice (aaron.brice@gmail.com) \n\n"
                +"This program is Free Software, licensed under the GPLv2\n"
                +"See the file COPYING for details\n")


class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

        self.drafted_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.avail_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.avail_view.verticalHeader().hide()
        
        self.timer = EggTimer(self)
        self.autopick = False
        self.connect(self.timer, QtCore.SIGNAL("update(QString)"), self.timerDisplay, QtCore.SLOT("display(QString)"))
        self.connect(self.reset_button, QtCore.SIGNAL("clicked()"), self.timer.reset)
        self.connect(self.pause_button, QtCore.SIGNAL("clicked()"), self.pause_timer)
        self.connect(self.timer, QtCore.SIGNAL("expired()"), self.draft_best_player)

        self.splitter.setSizes([1000, 200])

        # Designer doesn't have QTabBar, only QTabWidget, so I have to insert it manually
        self.tab_bar = QtGui.QTabBar(self)
        self.tab_bar.addTab("All")
        self.tab_bar.addTab("RB")
        self.tab_bar.addTab("QB")
        self.tab_bar.addTab("WR")
        self.tab_bar.addTab("TE")
        self.tab_bar.addTab("K")
        self.tab_bar.addTab("DEF")
        self.vboxlayout2.insertWidget(0, self.tab_bar)

        #self.info_tab_bar = QtGui.QTabBar(self)
        #self.info_tab_bar.addTab("Prev 10 Picks")
        #self.vboxlayout.insertWidget(0, self.info_tab_bar)

        self.avail_model = QtGui.QStandardItemModel()
        self.filtered_model = CustomSortFilterProxyModel()
        self.filtered_model.setSourceModel(self.avail_model)
        self.avail_view.setModel(self.filtered_model)

        self.connect(self.avail_view, QtCore.SIGNAL("doubleClicked(const QModelIndex&)"), self.draft_player)
        self.connect(self.tab_bar, QtCore.SIGNAL("currentChanged(int)"), self.filter_avail)

        self.current_round = 1
        self.current_draft_idx = 0
        self.team_list = []
        self.saved_rows = {}

        self.draft_tmpl = "%02d) %s: %s (Bye: %s)"

        self.save_file = ""
        self.open_file("playerdata.csv")

    def pause_timer(self):
        if self.pause_button.text() == "Start":
            self.timer.start()
            self.pause_button.setText("Pause")
            # If we're starting on player 1 and they have a first round keeper, skip to the next
            self.check_keeper()
        elif self.pause_button.text() == "Pause":
            self.timer.pause()
            self.pause_button.setText("Start")

    def open_file(self, filename):
        lines = []

        f = open(filename)
        for line in f:
            lines.append(line.strip())
        f.close()
        self.load_avail(lines)

    def edit_teams(self):
        dlg = TeamDialog(self.team_list, self.timer.countdown, self.autopick)
        if (dlg.exec_() == QtGui.QDialog.Accepted):
            self.timer.set_countdown(dlg.get_time_limit())
            self.autopick = dlg.get_autopick()
            old_team_list = self.team_list[:]
            self.team_list = dlg.get_team_list()
            diff_list = [ i for i in range(len(old_team_list)) if old_team_list[i] != self.team_list[i] ]
            if diff_list or (len(old_team_list) != len(self.team_list)):
                self.set_draft_view()

    def set_draft_view(self):
        while self.drafted_view.count():
            self.drafted_view.removeItem(0)

        for team in self.team_list:
            list = QtGui.QListWidget(self.drafted_view)
            list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            list.setSortingEnabled(True)
            self.drafted_view.addItem(list, team)

        self.current_round = 1
        self.round_field.setText(str(self.current_round))
        self.current_draft_idx = 0
        self.drafting_field.setText(self.get_team(0))
        self.next_field.setText(self.get_team(1))
        self.previous_picks_list.clear()

    def next_draft_idx(self):
        if self.current_round % 2 != 0:
            # Odd numbered round, index goes up
            if self.current_draft_idx != self.drafted_view.count() - 1:
                return self.current_draft_idx + 1
            else:
                return self.current_draft_idx
        else:
            # Even numbered round, index goes down
            if self.current_draft_idx != 0:
                return self.current_draft_idx - 1
            else:
                return self.current_draft_idx

    def draft_best_player(self):
        if self.autopick:
            name = self.avail_model.data(self.avail_model.index(0,0)).toString()
            position = self.avail_model.data(self.avail_model.index(0,2)).toString()
            bye = self.avail_model.data(self.avail_model.index(0,3)).toString()
            draft_string = self.draft_tmpl % (int(self.current_round), position, name, bye)

            self.drafted_view.widget(self.current_draft_idx).addItem(QtGui.QListWidgetItem(draft_string))
            self.update_pick_list(name, position)

            self.saved_rows[draft_string] = self.avail_model.takeRow(0)
            self.next_team()

    def draft_player(self, filtered_idx):
        filtered_row = filtered_idx.row()
        name = self.filtered_model.data(self.filtered_model.index(filtered_row, 0)).toString()
        position = self.filtered_model.data(self.filtered_model.index(filtered_row, 2)).toString()
        bye = self.filtered_model.data(self.filtered_model.index(filtered_row, 3)).toString()
        draft_string = self.draft_tmpl % (int(self.current_round), position, name, bye)
        
        self.drafted_view.widget(self.current_draft_idx).addItem(QtGui.QListWidgetItem(draft_string))
        self.update_pick_list(name, position)

        avail_idx = self.filtered_model.mapToSource(filtered_idx)
        self.saved_rows[draft_string] = self.avail_model.takeRow(avail_idx.row())
        self.next_team()


    def draft_unlisted_player(self):
        dlg = AddPlayerDialog()
        if (dlg.exec_() != QtGui.QDialog.Accepted):
            return
        name = dlg.player_name_field.text()
        if name == QtCore.QString():
            return
        position = dlg.position_combo_box.currentText()
        draft_string = self.draft_tmpl % (int(self.current_round), position, name, "?")

        self.drafted_view.widget(self.current_draft_idx).addItem(QtGui.QListWidgetItem(draft_string))
        self.update_pick_list(name, position)
        self.next_team()

    def next_team(self):
        next_idx = self.next_draft_idx()
        if next_idx == self.current_draft_idx:
            self.current_round += 1

        self.current_draft_idx = next_idx
        self.round_field.setText(str(self.current_round))
        self.drafting_field.setText(self.get_team())
        self.next_field.setText(self.get_team(self.next_draft_idx()))

        # Make sure the current team is visible in the toolbox
        self.drafted_view.setCurrentIndex(self.current_draft_idx)

        # Reset the timer and start it
        self.timer.reset()
        self.timer.start()
        if self.pause_button.text() == "Start":
            self.pause_button.setText("Pause")
        self.check_keeper()

    def check_keeper(self):
        # See if the current team has already drafted someone this round
        round = "%02d)" % int(self.current_round)
        itemlist = self.drafted_view.widget(self.current_draft_idx).findItems(round, QtCore.Qt.MatchStartsWith)
        if len(itemlist) > 0:
            tmp_string = str(itemlist[0].text())
            m = re.match(r'^\d+\) \w+: (.+)( \(Bye: [\?\d]+\))$', tmp_string)
            if m:
                name = m.group(1)
            msg = "%s automatically selects %s" % (self.drafting_field.text(), name)
            self.timer.pause()
            QtGui.QMessageBox.information(self, "Automatic pick", msg)
            self.timer.start()
            self.next_team()

    def get_team(self, idx=None):
        if idx == None:
            idx = self.current_draft_idx
        item_str = str(self.drafted_view.itemText(idx))
        m = re.match(r'(.+) -- (.+)', item_str)
        if m:
            return m.group(1)
        else:
            return item_str

    def update_pick_list(self, name, position):
        prev = "%s (%s) -- %s" % (name, position, self.get_team())
        self.previous_picks_list.insertItem(0, QtGui.QListWidgetItem(prev))
        while (self.previous_picks_list.count() > 10):
            self.previous_picks_list.takeItem(10)

    def filter_avail(self, tab_idx):
        position = self.tab_bar.tabText(tab_idx)
        if position == "All":
            self.filtered_model.setFilterKeyColumn(2)
            self.filtered_model.setFilterFixedString(QtCore.QString())
        else:
            self.filtered_model.setFilterKeyColumn(2)
            self.filtered_model.setFilterFixedString(position)

    def save_as(self):
        self.save_file = QtGui.QFileDialog.getSaveFileName(None, "Save File", QtCore.QDir.homePath(), "FF Draft (*.ffd)")
        if self.save_file == "":
            return
        self.save()

    def save(self):
        if self.save_file == "":
            self.save_as()
        else:
            f = open(self.save_file, 'w')
            f.write("[State]\n")
            f.write("current_round = " + str(self.current_round) + "\n")
            f.write("current_draft_idx = " + str(self.current_draft_idx) + "\n")
            f.write("drafting_field = " + str(self.drafting_field.text()) + "\n")
            f.write("next_field = " + str(self.next_field.text()) + "\n")
            f.write("team_list = " + join([ str(team) for team in self.team_list ], ',') + "\n")
            f.write("time_limit = " + str(self.timer.countdown) + "\n")
            f.write("autopick = " + str(self.autopick) + "\n")

            f.write("[Drafted]\n")
            team_count = self.drafted_view.count()
            for team_idx in range(team_count):
                team_name = str(self.get_team(team_idx))
                list = self.drafted_view.widget(team_idx)
                drafted_players = [ str(list.item(player_idx).text()) for player_idx in range(list.count()) ]
                drafted_players.insert(0, team_name)
                f.write(join(drafted_players, ",") + "\n")

            f.close()

    def load(self):
        loadfile = QtGui.QFileDialog.getOpenFileName(None, "Open File", QtCore.QDir.homePath(), "FF Draft (*.ffd)")
        if loadfile == QtCore.QString():
            return
        self.load_file(loadfile)

    def load_file(self, file):
        sectionrx = re.compile(r'\[(\w+)\]')
        f = open(file, 'r')
        section = None
        file_lines = {}
        for line in f:
            line = line.strip()
            section_match = sectionrx.match(line)
            if section_match:
                # Start of new section
                section = section_match.group(1)
                file_lines[section] = []
            else:
                file_lines[section].append(line)
        f.close()

        self.load_state(file_lines['State'])
        self.load_draft(file_lines['Drafted'])
        self.update_avail()
        self.save_file = file

    def load_state(self, lines):
        for line in lines:
            (var, value) = line.split(' = ')
            if var == "current_round":
                self.current_round = int(value)
                self.round_field.setText(str(self.current_round))
            elif var == "current_draft_idx":
                self.current_draft_idx = int(value)
            elif var == "drafting_field":
                self.drafting_field.setText(value)
            elif var == "next_field":
                self.next_field.setText(value)
            elif var == "team_list":
                self.team_list = [ QtCore.QString(team) for team in value.split(',') ]
            elif var == "time_limit":
                self.timer.set_countdown(int(value))
            elif var == "autopick":
                self.autopick = bool(value)

    def load_draft(self, lines):
        while self.drafted_view.count():
            self.drafted_view.removeItem(0)

        for line in lines:
            players = line.split(',')
            team = players.pop(0)
            list = QtGui.QListWidget(self.drafted_view)
            list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            list.setSortingEnabled(True)
            self.drafted_view.addItem(list, team)
            for player in players:
                list.addItem(QtGui.QListWidgetItem(player))

    def load_avail(self, lines):
        self.avail_model.clear()

        # First line is headers
        headers = lines.pop(0).strip().split(',')
        self.avail_model.setHorizontalHeaderLabels(headers)

        for line in lines:
            item_list = [ QtGui.QStandardItem(item) for item in line.strip().split(',') ]
            self.avail_model.appendRow(item_list)

        self.avail_view.resizeColumnsToContents()
        self.filtered_model.invalidate()

    def update_avail(self):
        # Loop through the drafted model and remove all the drafted players from the available model
        team_list = [ self.drafted_view.widget(i) for i in range(self.drafted_view.count()) ]
        for list in team_list:
            players = [ str(list.item(i).text()) for i in range(list.count()) ]
            for draft_string in players:
                m = re.match(r'^\d+\) \w+: (.+)( \(Bye: [\?\d]+\))$', draft_string)
                if m:
                    name = m.group(1)
                    item_list = self.avail_model.findItems(name)
                    for item in item_list:
                        self.saved_rows[draft_string] = self.avail_model.takeRow(item.row())

    def extra_player(self, keeper=False):
        # Find the selected player
        filtered_indexes = self.avail_view.selectedIndexes()
        if len(filtered_indexes) == 0:
            QtGui.QMessageBox.warning(self, "Error", "Please select the player to add")
            return
        filtered_idx = filtered_indexes.pop(0)

        # Find the selected team
        drafted_idx = self.drafted_view.currentIndex()
        if drafted_idx == -1:
            QtGui.QMessageBox.warning(self, "Error", "Please select a team to add the player to")
            return

        filtered_row = filtered_idx.row()

        # Determine which round the player is drafted in
        if keeper:
            # For keepers, take the ranking of the player divided by 
            # the number of teams, +1.  So if ranking = 95 and there's 10
            # teams, the player should be a 10th round pick
            (ranking, valid) = self.filtered_model.data(self.filtered_model.index(filtered_row, 4)).toInt()
            if valid:
                round = int(ranking) / int(self.drafted_view.count())
                if (int(ranking) % int(self.drafted_view.count())):
                    round = round + 1
            else:
                round = int(self.current_round)
        else:
            round = int(self.current_round)

        # Add the selected player to the selected team
        name = self.filtered_model.data(self.filtered_model.index(filtered_row, 0)).toString()
        position = self.filtered_model.data(self.filtered_model.index(filtered_row, 2)).toString()
        bye = self.filtered_model.data(self.filtered_model.index(filtered_row, 3)).toString() 
        draft_string = self.draft_tmpl % (round, position, name, bye)
        
        self.drafted_view.widget(drafted_idx).addItem(QtGui.QListWidgetItem(draft_string))

        avail_idx = self.filtered_model.mapToSource(filtered_idx)
        self.saved_rows[draft_string] = self.avail_model.takeRow(avail_idx.row())

    def remove_player(self):
        # Find the selected team's player
        team_idx = self.drafted_view.currentIndex()
        if team_idx == -1:
            QtGui.QMessageBox.warning(self, "Error", "Please select a player to remove")
            return

        list = self.drafted_view.currentWidget()
        selected_players = list.selectedItems()
        for player in selected_players:
            # Remove the player from the team
            draft_string = str(player.text())
            # list.removeItemWidget(player) doesn't seem to work, have to do it
            # the long way?
            for i in reversed(range(list.count())):
                if list.item(i).text() == player.text():
                    list.takeItem(i)

            if self.saved_rows.has_key(draft_string):
                # Restore the player to the available model
                self.avail_model.insertRow(0, self.saved_rows[draft_string])
                del self.saved_rows[draft_string]

    def export(self):
        export_file = QtGui.QFileDialog.getSaveFileName(None, "Export File", QtCore.QDir.homePath(), "Text File (*.txt)")
        if export_file == "":
            return
        f = open(export_file, 'w')
        # Loop through the draft view and write all the drafted players
        for i in range(self.drafted_view.count()):
            team = self.get_team(i)
            list = self.drafted_view.widget(i)
            f.write(str(team) + "\n")
            f.write("-" * len(str(team)))
            f.write("\n")
            players = [ list.item(i).text() for i in range(list.count()) ]
            for player in players:
                f.write(str(player) + "\n")
            f.write("\n\n")
        f.close()

class CustomSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.numrx = re.compile(r'^-?\d+$')
        f = open('datacfg.yaml')
        self.header_data = yaml.load(f)
        f.close()

    def lessThan(self, left, right):
        ldata = str(left.data().toString())
        rdata = str(right.data().toString())
        if ldata == "-":
            return True
        elif rdata == "-":
            return False
        elif self.numrx.match(ldata) != None and self.numrx.match(rdata) != None:
            # Both numbers, do numeric comparison
            return int(ldata) < int(rdata)
        else:
            return ldata < rdata

    def filterAcceptsColumn(self, source_column, source_parent_index):
        column = str(self.sourceModel().headerData(source_column, QtCore.Qt.Horizontal).toString())
        if column in self.header_data['Headers']['All']:
            return True
        position_list = self.header_data['Headers'].keys()
        for position in position_list:
            if self.filterRegExp().indexIn(position) != -1 and column in self.header_data['Headers'][position]:
                return True
        return False

class TeamDialog(QtGui.QDialog, Ui_TeamDialog):
    def __init__(self, team_list = [], timer = 0, autopick = False, parent = None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        self.model = QtGui.QStringListModel()
        self.model.setStringList(team_list)
        self.team_list_view.setModel(self.model)

        self.connect(self.add_button, QtCore.SIGNAL("clicked()"), self.add_team)
        self.connect(self.move_up_button, QtCore.SIGNAL("clicked()"), self.move_team_up)
        self.connect(self.move_down_button, QtCore.SIGNAL("clicked()"), self.move_team_down)

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

class EggTimer(QtCore.QObject):
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)

        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.send_update)
        self.countdown = 0

    def set_countdown(self, countdown):
        self.countdown = countdown
        self.current_time = self.countdown
        self.emit(QtCore.SIGNAL("update(QString)"), self.time_str(self.current_time))

    def reset(self):
        self.current_time = self.countdown
        self.emit(QtCore.SIGNAL("update(QString)"), self.time_str(self.current_time))

    def start(self):
        if self.countdown > 0:
            self.timer.start(1000)

    def pause(self):
        self.timer.stop()

    def send_update(self):
        self.current_time -= 1
        self.emit(QtCore.SIGNAL("update(QString)"), self.time_str(self.current_time))
        if self.current_time == 0:
            self.timer.stop()
            self.emit(QtCore.SIGNAL("expired()"))

    def time_str(self, time):
        hours = str(int(time) / 60)
        minutes = str(int(time) % 60)
        if (int(minutes) < 10):
            minutes = "0" + minutes
        return str(hours) + ":" + str(minutes)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    f = open("ffdraft.css")
    try:
        css = f.read()
        app.setStyleSheet(css);
    finally:
        f.close()
    mainWin = MainWindow()
    mainWin.resize(1200,1000)
    if len(sys.argv) > 1:
        mainWin.load_file(sys.argv[1])
    mainWin.show()
    sys.exit(app.exec_())

