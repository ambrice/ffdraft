#!/usr/bin/python

import re
from string import join
from PyQt4 import QtCore, QtGui
from ffdraft.ui import Ui_MainWidget
from ffdraft.utils import EggTimer
from ffdraft.dialogs import TeamDialog, AddPlayerDialog
from ffdraft.models import CustomSortFilterProxyModel

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
        self.loadAct.triggered.connect(self.load)

        self.saveAsAct = QtGui.QAction("Save &As", self)
        self.saveAsAct.setStatusTip("Save draft to file")
        self.saveAsAct.triggered.connect(self.save_as)

        self.saveAct = QtGui.QAction("&Save", self)
        self.saveAct.setShortcut("Ctrl+S")
        self.saveAct.setStatusTip("Save draft to file")
        self.saveAct.triggered.connect(self.save)

        self.exportAct = QtGui.QAction("&Export", self)
        self.exportAct.setStatusTip("Export draft results to a text file")
        self.exportAct.triggered.connect(self.export)

        self.exitAct = QtGui.QAction("E&xit", self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.setStatusTip("Exit the application")
        self.exitAct.triggered.connect(self.close)

        self.teamAct = QtGui.QAction("&Configure Teams", self)
        self.teamAct.setStatusTip("Add/Remove teams from the draft")
        self.teamAct.triggered.connect(self.edit_teams)

        self.keeperAct = QtGui.QAction("&Add Keeper", self)
        self.keeperAct.setStatusTip("Add a player as a keeper from a keeper league")
        self.keeperAct.triggered.connect(self.add_keeper)
        
        self.extraAct = QtGui.QAction("&Add Extra Player", self)
        self.extraAct.setStatusTip("Add an extra player to a team, outside of the draft")
        self.extraAct.triggered.connect(self.extra_player)

        self.removeAct = QtGui.QAction("&Remove Player", self)
        self.removeAct.setStatusTip("Remove a player from a team")
        self.removeAct.triggered.connect(self.remove_player)

        self.draftAct = QtGui.QAction("&Draft Unlisted Player", self)
        self.draftAct.setStatusTip("Draft a player that's not listed in the available player table")
        self.draftAct.triggered.connect(self.draft_unlisted_player)

        self.aboutAct = QtGui.QAction("About FFD", self)
        self.aboutAct.setStatusTip("About Fantasy Football Draft")
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QtGui.QAction("About Qt", self)
        self.aboutQtAct.setStatusTip(self.tr("About the Qt GUI library"))
        self.aboutQtAct.triggered.connect(QtGui.qApp.aboutQt)


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
        self.mainWidget.avail_view.customContextMenuRequested.connect(self.showPlayerMenu)

        self.draftedPopupMenu = QtGui.QMenu(self)
        self.draftedPopupMenu.addAction(self.removeAct)
        self.draftedPopupMenu.addAction(self.draftAct)
        self.mainWidget.drafted_view.customContextMenuRequested.connect(self.showDraftedMenu)

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
        self.timer.update.connect(self.timerDisplay.display)
        self.timer.expired.connect(self.draft_best_player)
        self.reset_button.clicked.connect(self.timer.reset)
        self.pause_button.clicked.connect(self.pause_timer)

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

        self.avail_view.doubleClicked.connect(self.draft_player)
        self.tab_bar.currentChanged.connect(self.filter_avail)

        self.current_round = 1
        self.current_draft_idx = 0
        self.team_list = []
        self.saved_rows = {}

        self.draft_tmpl = "%02d) %s: %s (Bye: %s)"
        self.draft_re = re.compile(r'^(\d+)\) (\w+): (.+)( \(Bye: [\?\d]+\))$')

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
            m = self.draft_re.match(tmp_string)
            if m:
                position = m.group(2)
                name = m.group(3)
            msg = "%s automatically selects %s" % (self.drafting_field.text(), name)
            self.timer.pause()
            QtGui.QMessageBox.information(self, "Automatic pick", msg)
            self.timer.start()
            self.update_pick_list(name, position, automatic=True)
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

    def update_pick_list(self, name, position, team=None, automatic=False):
        if team == None:
            team = self.get_team()
        prev = "%s (%s) -- %s" % (name, position, team)
        if (automatic):
            prev = ' '.join([prev, ' / Auto'])
        self.previous_picks_list.insertItem(0, QtGui.QListWidgetItem(prev))
        while (self.previous_picks_list.count() > 10):
            self.previous_picks_list.takeItem(10)

    def remove_pick_list(self, name, position, team):
        prev = "%s (%s) -- %s" % (name, position, team)
        for i in reversed(range(self.previous_picks_list.count())):
            if self.previous_picks_list.item(i).text() == prev:
                self.previous_picks_list.takeItem(i)

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
            # See if they already have a player in this round, add it to the next round
            round_string = "%02d)" % (round)
            while (len(self.drafted_view.widget(drafted_idx).findItems(round_string, QtCore.Qt.MatchStartsWith)) > 0):
                round += 1
                round_string = "%02d)" % (round)
        else:
            round = int(self.current_round)

        # Add the selected player to the selected team
        name = self.filtered_model.data(self.filtered_model.index(filtered_row, 0)).toString()
        position = self.filtered_model.data(self.filtered_model.index(filtered_row, 2)).toString()
        bye = self.filtered_model.data(self.filtered_model.index(filtered_row, 3)).toString() 
        draft_string = self.draft_tmpl % (round, position, name, bye)
        
        self.drafted_view.widget(drafted_idx).addItem(QtGui.QListWidgetItem(draft_string))
        self.update_pick_list(name, position, self.get_team(drafted_idx))

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
                    m = self.draft_re.match(draft_string)
                    if m:
                        position = m.group(2)
                        name = m.group(3)
                        team = self.get_team(team_idx)
                        self.remove_pick_list(name, position, team)
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

