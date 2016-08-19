#!/usr/bin/python

import re
import ffdraft.models as models
import os
from xml.etree import ElementTree
from PyQt4 import QtCore, QtGui
from ffdraft.utils import EggTimer
from ffdraft.ticker import Ticker
from ffdraft.dialogs import TeamDialog, AddPlayerDialog, WebAuthDialog
from ffdraft.yahoo.auth import OAuthWrapper

YAHOO_URL = 'http://fantasysports.yahooapis.com/fantasy/v2'
# 359 is the id for NFL season 2016, each year have to update that from
# http://developer.yahoo.com/fantasysports/guide/game-resource.html
YAHOO_LAST_SEASON_ID = 348

class MainWindow(QtGui.QMainWindow):
    def __init__(self, dbfile=None, consumer_key=None, consumer_secret=None):
        QtGui.QMainWindow.__init__(self)

        self.mainWidget = MainWidget(dbfile, None, consumer_key, consumer_secret)
        self.setCentralWidget(self.mainWidget)
        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.setWindowTitle('Fantasy Football Draft')
        self.version = '2016-08'

    def createActions(self):
        self.newAct = QtGui.QAction('&New Session', self)
        self.newAct.setStatusTip('Start a New Fantasy Football Draft session')
        self.newAct.triggered.connect(self.mainWidget.newdb)

        self.openAct = QtGui.QAction('&Open Session', self)
        self.openAct.setStatusTip('Open a previous Fantasy Football Draft session')
        self.openAct.triggered.connect(self.mainWidget.opendb)

        self.leagueAct = QtGui.QAction('&Select League', self)
        self.leagueAct.setStatusTip('Select from multiple leagues')
        self.leagueAct.triggered.connect(self.mainWidget.switch_league)

        self.yahooAct = QtGui.QAction('&Import From Yahoo', self)
        self.yahooAct.setStatusTip('Import League information from Yahoo')
        self.yahooAct.triggered.connect(self.mainWidget.import_from_yahoo)

        self.exportAct = QtGui.QAction('&Export', self)
        self.exportAct.setStatusTip('Export draft results to a text file')
        self.exportAct.triggered.connect(self.mainWidget.export)

        self.exitAct = QtGui.QAction('E&xit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit the application')
        self.exitAct.triggered.connect(self.close)

        self.teamAct = QtGui.QAction('&Configure Teams', self)
        self.teamAct.setStatusTip('Add/Remove teams from the draft')
        self.teamAct.triggered.connect(self.mainWidget.edit_teams)

        self.keeperAct = QtGui.QAction('&Add Keeper', self)
        self.keeperAct.setStatusTip('Add a player as a keeper from a keeper league')
        self.keeperAct.triggered.connect(self.add_keeper)
        
        self.extraAct = QtGui.QAction('&Add Extra Player', self)
        self.extraAct.setStatusTip('Add an extra player to a team, outside of the draft')
        self.extraAct.triggered.connect(self.mainWidget.extra_player)

        self.removeAct = QtGui.QAction('&Remove Player', self)
        self.removeAct.setStatusTip('Remove a player from a team')
        self.removeAct.triggered.connect(self.mainWidget.remove_player)

        self.draftAct = QtGui.QAction('&Draft Unlisted Player', self)
        self.draftAct.setStatusTip('Draft a player not listed in the available player table')
        self.draftAct.triggered.connect(self.mainWidget.draft_unlisted_player)

        self.aboutAct = QtGui.QAction('About FFD', self)
        self.aboutAct.setStatusTip('About Fantasy Football Draft')
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QtGui.QAction('About Qt', self)
        self.aboutQtAct.setStatusTip(self.tr('About the Qt GUI library'))
        self.aboutQtAct.triggered.connect(QtGui.qApp.aboutQt)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.yahooAct)
        self.fileMenu.addAction(self.leagueAct)
        self.fileMenu.addAction(self.exportAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu('&Edit')
        self.editMenu.addAction(self.teamAct)
        self.editMenu.addAction(self.extraAct)
        self.editMenu.addAction(self.keeperAct)
        self.editMenu.addAction(self.removeAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.draftAct)

        self.helpMenu = self.menuBar().addMenu('&Help')
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
        self.statusBar().showMessage('Ready')

    def showPlayerMenu(self, point):
        self.playerPopupMenu.exec_(QtGui.QCursor.pos())

    def showDraftedMenu(self, point):
        self.draftedPopupMenu.exec_(QtGui.QCursor.pos())

    def add_keeper(self):
        self.mainWidget.extra_player(keeper=True)

    def about(self):
        QtGui.QMessageBox.about(self, 'About Fantasy Football Draft',
                'Fantasy Football Draft version ' + self.version + '\n\n'
                +'Copyright (C) 2007-2016 Aaron Brice (aaron.brice@gmail.com) \n\n'
                +'This program is Free Software, licensed under the GPLv2\n'
                +'See the file COPYING for details\n')


class MainWidget(QtGui.QWidget):
    def __init__(self, dbfile=None, parent=None, consumer_key=None, consumer_secret=None):
        QtGui.QWidget.__init__(self, parent)

        self.setup_ui()

        self.timer = EggTimer(self)
        self.timer.update.connect(self.timer_display.display)
        self.timer.expired.connect(self.draft_best_player)

        self.reset_button.clicked.connect(self.timer.reset)
        self.pause_button.clicked.connect(self.pause_timer)

        self.avail_view.doubleClicked.connect(self.draft_player)
        self.tab_bar.currentChanged.connect(self.filter_avail)

        self.stat_categories = None
        self.timer.set_countdown(60)
        self.team_list = []
        self.drafted_model = {}

        self.league = models.League('Unnamed')

        # Yahoo OAuth stuff
        self.yahoo = OAuthWrapper(consumer_key, consumer_secret)
        self.yahoo.add_token_update_callback(self.update_access_token)

        if dbfile:
            self.opendb(dbfile)
            self.init_league()

        self.player_image = {}
        self.player_stats = {}

    def setup_ui(self):
        self.pause_button = QtGui.QPushButton('Start', self)
        self.reset_button = QtGui.QPushButton('Reset', self)
        button_layout = QtGui.QVBoxLayout()
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)

        self.timer_display = QtGui.QLCDNumber(self)
        self.timer_display.setMinimumWidth(140)
        self.ticker = Ticker()
        
        banner_layout = QtGui.QHBoxLayout()
        banner_layout.addSpacing(140)
        banner_layout.addWidget(self.timer_display)
        banner_layout.addLayout(button_layout)
        banner_layout.addWidget(self.ticker)
        banner_layout.addSpacing(140)

        player_widget = self.setup_player_ui()
        avail_widget = self.setup_avail_ui()
        drafted_widget = self.setup_drafted_ui()

        splitter = QtGui.QSplitter(self)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.addWidget(player_widget)
        splitter.addWidget(avail_widget)
        splitter.addWidget(drafted_widget)
        #splitter.setSizes([200, 600, 200])

        top_layout = QtGui.QVBoxLayout()
        top_layout.addSpacing(20)
        top_layout.addLayout(banner_layout)
        top_layout.addWidget(splitter)
        top_layout.addSpacing(10)
        self.setLayout(top_layout)

    def setup_player_ui(self):
        widget = QtGui.QWidget(self)

        self.player_image_view = QtGui.QLabel(widget)
        self.player_image_view.setAlignment(QtCore.Qt.AlignCenter)
        self.player_label = QtGui.QLabel('Player', widget)
        self.player_label.setAlignment(QtCore.Qt.AlignHCenter)
        statistics_label = QtGui.QLabel('2015 Statistics', widget)
        self.player_stats_table = QtGui.QTableWidget(widget)
        self.player_stats_table.setAlternatingRowColors(True)
        self.player_stats_table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.player_stats_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.player_stats_table.setShowGrid(False)
        self.player_stats_table.setGridStyle(QtCore.Qt.NoPen)
        self.player_stats_table.setRowCount(0)
        self.player_stats_table.setColumnCount(2)
        self.player_stats_table.verticalHeader().hide()
        self.player_stats_table.horizontalHeader().hide()

        layout = QtGui.QVBoxLayout()
        layout.addSpacing(10)
        layout.addWidget(self.player_image_view)
        layout.addWidget(self.player_label)
        layout.addSpacing(10)
        layout.addWidget(statistics_label)
        layout.addWidget(self.player_stats_table)
        widget.setLayout(layout)

        return widget

    def setup_avail_ui(self):
        widget = QtGui.QWidget(self)

        self.tab_bar = QtGui.QTabBar(self)
        self.tab_bar.addTab('All')
        self.tab_bar.addTab('RB')
        self.tab_bar.addTab('QB')
        self.tab_bar.addTab('WR')
        self.tab_bar.addTab('TE')
        self.tab_bar.addTab('K')
        self.tab_bar.addTab('DEF')

        self.avail_view = QtGui.QTableView(widget)
        self.avail_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.avail_view.verticalHeader().hide()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.tab_bar)
        layout.addWidget(self.avail_view)
        widget.setLayout(layout)

        return widget

    def setup_drafted_ui(self):
        widget = QtGui.QWidget(self)

        self.previous_picks_list = QtGui.QListWidget(widget)
        self.previous_picks_list.setLineWidth(3)
        self.previous_picks_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.previous_picks_list.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.previous_picks_list.setViewMode(QtGui.QListView.ListMode)

        self.drafted_view = QtGui.QToolBox(widget)
        self.drafted_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.drafted_view.setCurrentIndex(-1)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.previous_picks_list)
        layout.addWidget(self.drafted_view)
        layout.setStretch(0, 1)
        layout.setStretch(1, 5)
        widget.setLayout(layout)

        return widget

    def pause_timer(self):
        if self.pause_button.text() == 'Start':
            self.timer.start()
            self.pause_button.setText('Pause')
            # If we're starting on player 1 and they have a first round keeper, skip to the next
            self.check_keeper()
        elif self.pause_button.text() == 'Pause':
            self.timer.pause()
            self.pause_button.setText('Start')

    def open_file(self, filename):
        # TODO
        self.load_avail(filename)

    def edit_teams(self):
        dlg = TeamDialog(self.league.name, self.team_list, self.timer.countdown, self.league.autopick)
        if (dlg.exec_() == QtGui.QDialog.Accepted):
            self.league.time_limit = dlg.get_time_limit()
            self.league.autopick = dlg.get_autopick()
            self.timer.set_countdown(self.league.time_limit)
            old_team_list = self.team_list[:]
            self.team_list = dlg.get_team_list()
            if len(old_team_list) != len(self.team_list) or any(i != j for i, j in zip(old_team_list, self.team_list)):
                self.set_draft_view()
                ticker_model = []
                for team in self.team_list:
                    img_url = models.Team.find_by_name(team).img_url
                    ticker_model.append( { 'name': team, 'img_url': img_url } )
                self.ticker.set_teams(ticker_model, self.league.roster_count)

    def set_draft_view(self):
        while self.drafted_view.count():
            self.drafted_view.removeItem(0)

        self.drafted_model = {}

        for team in self.team_list:
            self.drafted_model[team] = models.DraftedPlayerModel(team)
            tview = QtGui.QListView(self.drafted_view)
            tview.setModel(self.drafted_model[team])
            tview.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            self.drafted_view.addItem(tview, team)

        self.league.current_round = 1
        self.league.current_draft_index = 0
        self.league.save()
        self.previous_picks_list.clear()

    def next_draft_idx(self):
        if self.league.current_round % 2 != 0:
            # Odd numbered round, index goes up
            if self.league.current_draft_index != self.drafted_view.count() - 1:
                return self.league.current_draft_index + 1
            else:
                return self.league.current_draft_index
        else:
            # Even numbered round, index goes down
            if self.league.current_draft_index != 0:
                return self.league.current_draft_index - 1
            else:
                return self.league.current_draft_index

    def draft_best_player(self):
        if self.league.autopick:
            player = self.filtered_model[0]
            team = self.get_team()
            self.drafted_model[team].draft(player, self.league.current_round)
            self.filtered_model.draft(player)
            self.avail_view.hideColumn(0)
            self.avail_view.hideColumn(1)
            self.update_pick_list(player.name, player.position)
            self.next_team()

    def draft_player(self, filtered_idx):
        player = self.filtered_model[filtered_idx.row()]
        team = self.get_team()
        self.drafted_model[team].draft(player, self.league.current_round)
        self.filtered_model.draft(player)
        self.avail_view.hideColumn(0)
        self.avail_view.hideColumn(1)
        self.update_pick_list(player.name, player.position)
        self.next_team()


    def draft_unlisted_player(self):
        # TODO: search yahoo API for player
        dlg = AddPlayerDialog()
        if (dlg.exec_() != QtGui.QDialog.Accepted):
            return
        name = str(dlg.player_name_field.text())
        if name == '':
            return
        position = str(dlg.position_combo_box.currentText())
        player = models.Player(0, 0, name, '?', 0, position, None)
        self.avail_model.add_player(player)

        team = self.get_team()
        self.drafted_model[team].draft(player, self.league.current_round)
        self.filtered_model.draft(player)
        self.avail_view.hideColumn(0)
        self.avail_view.hideColumn(1)
        self.update_pick_list(name, position)
        self.next_team()

    def next_team(self):
        next_idx = self.next_draft_idx()
        if next_idx == self.league.current_draft_index:
            self.league.current_round += 1

        self.league.current_draft_index = next_idx
        self.league.save()
        self.ticker.set_next_team()

        if self.league.current_round > self.league.roster_count:
            self.timer.pause()
            return

        # Make sure the current team is visible in the toolbox
        self.drafted_view.setCurrentIndex(self.league.current_draft_index)

        # Reset the timer and start it
        self.timer.reset()
        self.timer.start()
        if self.pause_button.text() == 'Start':
            self.pause_button.setText('Pause')
        self.check_keeper()

    def check_keeper(self):
        # See if the current team has already drafted someone this round
        team = self.get_team()
        player = self.drafted_model[team].has_drafted(self.league.current_round)
        if player:
            msg = '{0} automatically selects {1}'.format(team, player.name)
            self.timer.pause()
            QtGui.QMessageBox.information(self, 'Automatic pick', msg)
            self.timer.start()
            self.update_pick_list(player.name, player.position, automatic=True)
            self.next_team()

    def get_team(self, idx=None):
        if idx == None:
            idx = self.league.current_draft_index
        item_str = str(self.drafted_view.itemText(idx))
        m = re.match(r'(.+) -- (.+)', item_str)
        if m:
            return m.group(1)
        else:
            return item_str

    def update_pick_list(self, name, position, team=None, automatic=False):
        if team == None:
            team = self.get_team()
        prev = '%s (%s) -- %s' % (name, position, team)
        if (automatic):
            prev = ' '.join([prev, ' / Auto'])
        self.previous_picks_list.insertItem(0, QtGui.QListWidgetItem(prev))
        while (self.previous_picks_list.count() > 10):
            self.previous_picks_list.takeItem(10)

    def remove_pick_list(self, name, position, team):
        prev = '%s (%s) -- %s' % (name, position, team)
        for i in reversed(xrange(self.previous_picks_list.count())):
            if self.previous_picks_list.item(i).text() == prev:
                self.previous_picks_list.takeItem(i)

    def filter_avail(self, tab_idx):
        position = self.tab_bar.tabText(tab_idx)
        self.filtered_model.set_position(position)
        self.filtered_model.invalidate()
        self.avail_view.hideColumn(0)
        self.avail_view.hideColumn(1)

    def load_avail(self, filename):
        self.avail_model.load(filename)
        self.filtered_model.invalidate()
        self.avail_view.hideColumn(0)
        self.avail_view.hideColumn(1)

    def extra_player(self, keeper=False):
        # Find the selected player
        filtered_indexes = self.avail_view.selectedIndexes()
        if len(filtered_indexes) == 0:
            QtGui.QMessageBox.warning(self, 'Error', 'Please select the player to add')
            return
        filtered_idx = filtered_indexes.pop(0)

        # Find the selected team
        drafted_idx = self.drafted_view.currentIndex()
        if drafted_idx == -1:
            QtGui.QMessageBox.warning(self, 'Error', 'Please select a team to add the player to')
            return

        drafted_team = self.get_team(drafted_idx)
        filtered_row = filtered_idx.row()

        # Determine which round the player is drafted in
        if keeper:
            # For keepers, take the ranking of the player divided by 
            # the number of teams, +1.  So if ranking = 95 and there's 10
            # teams, the player should be a 10th round pick
            player = self.filtered_model[filtered_row]
            round = player.rank / int(self.drafted_view.count())
            if (player.rank % int(self.drafted_view.count())):
                round = round + 1
            # See if they already have a player in this round, add it to the next round
            while any(drafted.round == round for drafted in self.drafted_model[drafted_team].team.drafted):
                round += 1
        else:
            round = self.league.current_round

        # Add the selected player to the selected team
        player = self.filtered_model[filtered_row]
        self.drafted_model[drafted_team].draft(player, round)
        self.filtered_model.draft(player)
        self.avail_view.hideColumn(0)
        self.avail_view.hideColumn(1)
        self.update_pick_list(player.name, player.position, self.drafted_model[drafted_team].team.name)

    def remove_player(self):
        # Find the selected team's player
        team_idx = self.drafted_view.currentIndex()
        if team_idx == -1:
            QtGui.QMessageBox.warning(self, 'Error', 'Please select a player to remove')
            return
        team = self.get_team(team_idx)

        indexes = self.drafted_view.widget(team_idx).selectedIndexes()
        for index in indexes:
            # Remove the player from the team
            p = self.drafted_model[team][index.row()].player
            self.drafted_model[team].removeRows(index.row(), 1)
            self.filtered_model.remove_draft(p)
            self.remove_pick_list(p.name, p.position, p.team)

    def export(self):
        export_file = QtGui.QFileDialog.getSaveFileName(None, 'Export File', QtCore.QDir.homePath(), 'Text File (*.txt)')
        if export_file == '':
            return
        f = open(export_file, 'w')
        # Loop through the draft view and write all the drafted players
        for i in xrange(self.drafted_view.count()):
            team = self.get_team(i)
            mylist = self.drafted_view.widget(i).model()
            f.write(str(team) + '\n')
            f.write('-' * len(str(team)))
            f.write('\n')
            players = [ mylist.index(i, 0).data().toString() for i in xrange(mylist.count()) ]
            for player in players:
                f.write(str(player) + '\n')
            f.write('\n\n')
        f.close()

    def newdb(self):
        dbfile = QtGui.QFileDialog.getSaveFileName(None, "Create Session", QtCore.QDir.homePath(), "FF Draft (*.ffd)")
        if dbfile != '':
            try:
                os.remove(dbfile)
            except OSError:
                pass
            open(dbfile, 'w').close()
            self.opendb(dbfile)

    def opendb(self, loadfile=None):
        if not loadfile:
            loadfile = QtGui.QFileDialog.getOpenFileName(None, "Open Session", QtCore.QDir.homePath(), "FF Draft (*.ffd)")
        if loadfile != '' and os.access(loadfile, os.R_OK|os.W_OK):
            models.set_database(loadfile)
            if models.League.total_count() > 0:
                self.league = models.League.active_league()
            self.avail_model = models.PlayerModel()
            self.filtered_model = models.PlayerFilterProxyModel()
            self.filtered_model.setSourceModel(self.avail_model)
            self.avail_view.setModel(self.filtered_model)
            self.avail_view.selectionModel().currentRowChanged.connect(self.update_stats)
            self.avail_view.hideColumn(0)
            self.avail_view.hideColumn(1)
            self.avail_view.resizeColumnsToContents()

    def import_from_yahoo(self):
        self.get_access_token()
        self.progress = QtGui.QProgressDialog('Importing data from Yahoo!...', QtCore.QString(), 0, 34)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.setValue(0)
        url = '{0}/users;use_login=1/games;game_keys=nfl/leagues'.format(YAHOO_URL)
        self.progress.setValue(1)
        leaguesxml = self.yahoo.request(url)
        self.update_leagues(leaguesxml)

    def update_leagues(self, leaguesxml):
        leagues = models.League.load_from_xml(leaguesxml)
        # TODO: handle 0 or 1 leagues
        league_names = [ league.name for league in leagues ]
        league_name, accepted = QtGui.QInputDialog.getItem( self, 'Select League', 'Leagues', league_names, 0, False)
        if accepted:
            self.league = models.League.find_by_name(league_name)
            self.league.activate()
        else:
            self.league = leagues[0]
            self.league.activate()
        for league in leagues:
            url = '{0}/league/nfl.l.{1}/teams'.format(YAHOO_URL, league.yahoo_id)
            self.progress.setValue(2)
            teamsxml = self.yahoo.request(url)
            models.Team.load_from_xml(teamsxml)
            url = '{0}/league/nfl.l.{1}/settings'.format(YAHOO_URL, league.yahoo_id)
            settingsxml = self.yahoo.request(url)
            models.League.set_roster(settingsxml)
        models.Player.clear()
        for start in xrange(0,800,25):
            self.progress.setValue(self.progress.value() + 1)
            url = '{0}/league/nfl.l.{1}/players;sort=OR;count=25;start={2}/'.format(YAHOO_URL, self.league.yahoo_id, start)
            playersxml = self.yahoo.request(url)
            models.Player.append_from_xml(playersxml, start)
        self.avail_model = models.PlayerModel()
        self.filtered_model = models.PlayerFilterProxyModel()
        self.filtered_model.setSourceModel(self.avail_model)
        self.avail_view.setModel(self.filtered_model)
        self.avail_view.selectionModel().currentRowChanged.connect(self.update_stats)
        self.avail_view.hideColumn(0)
        self.avail_view.hideColumn(1)
        self.avail_view.resizeColumnsToContents()
        self.init_league()

    def init_league(self):
        while self.drafted_view.count():
            self.drafted_view.removeItem(0)

        self.timer.set_countdown(self.league.time_limit)
        team_model = models.TeamModel(self.league.name)
        self.team_list = team_model.team_names()
        self.last_round = self.league.roster_count

        ticker_model = []
        self.drafted_model = {}
        for team in self.team_list:
            self.drafted_model[team] = models.DraftedPlayerModel(team)
            tview = QtGui.QListView(self.drafted_view)
            tview.setModel(self.drafted_model[team])
            tview.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            self.drafted_view.addItem(tview, team)
            img_url = models.Team.find_by_name(team).img_url
            ticker_model.append( { 'name': team, 'img_url': img_url } )

        self.ticker.set_teams(ticker_model, self.league.roster_count, self.league.current_round, self.league.current_draft_index)
        self.previous_picks_list.clear()

    def switch_league(self):
        league_names = models.League.names()
        league_name, accepted = QtGui.QInputDialog.getItem( self, 'Select League', 'Leagues', league_names, 0, False)
        if accepted:
            self.league = models.League.find_by_name(league_name)
            self.league.activate()
            self.init_league()

    def get_access_token(self):
        if models.YahooAuth.total_count() == 0:
            request_token = self.yahoo.get_request_token()
            dlg = WebAuthDialog(request_token.get_callback_url())
            if (dlg.exec_() != QtGui.QDialog.Accepted):
                return
            verification = dlg.verification_edit.text()
            self.yahoo.access_token, self.yahoo.session_handle, self.yahoo.access_expires  = self.yahoo.get_access_token(request_token, verification)
            auth = models.YahooAuth(self.yahoo.access_token.key, self.yahoo.access_token.secret, self.yahoo.session_handle, self.yahoo.access_expires)
            auth.save()
        else:
            auth = models.YahooAuth.first()
            self.yahoo.set_access(auth.access_token_key, auth.access_token_secret, auth.session_handle, auth.access_expires)

    def update_access_token(self, key, secret, handle, expires):
        auth = models.YahooAuth.first()
        auth.access_token_key = key
        auth.access_token_secret = secret
        auth.session_handle = handle
        auth.access_expires = expires
        auth.save()

    def update_stats(self, index):
        if not self.stat_categories:
            self.get_stat_categories()
        player = self.filtered_model[index.row()]
        if self.player_image.has_key(player.id) and self.player_stats.has_key(player.id):
            self.show_player_data(player)
        if not self.player_image.has_key(player.id):
            q = player.img_url.rfind('http')
            if q != -1:
                url = player.img_url[q:]
            else:
                url = player.img_url
            self.yahoo.request_async(url, lambda x: self.read_image(player, x), skip_auth=True)
        if not self.player_stats.has_key(player.id):
            url = '{0}/player/{1}.p.{2}/stats'.format(YAHOO_URL, YAHOO_LAST_SEASON_ID, player.yahoo_id)
            self.yahoo.request_async(url, lambda x: self.read_stats(player, x))

    def read_image(self, player, image):
        try:
            self.player_image[player.id] = QtGui.QPixmap()
            self.player_image[player.id].loadFromData(image)
            self.player_image[player.id] = self.player_image[player.id].scaledToHeight(600)
            if self.player_stats.has_key(player.id):
                self.show_player_data(player)
        except Exception as e:
            print 'Error reading image ' + str(e)
            del self.player_image[player.id]

    def read_stats(self, player, statsxml):
        statsxml = str(statsxml)
        root = ElementTree.fromstring(statsxml)
        models.remove_namespace(root, '{0}/base.rng'.format(YAHOO_URL))
        self.player_stats[player.id] = []
        try:
            for stat in root.findall('player/player_stats/stats/stat'):
                stat_id = stat.findtext('stat_id')
                stat_value = stat.findtext('value')
                if int(stat_value) != 0:
                    self.player_stats[player.id].append( (stat_id, stat_value) )
            if self.player_image.has_key(player.id):
                self.show_player_data(player)
        except Exception as e:
            print 'Error reading stats ' + str(e)
            del self.player_stats[player.id]


    def show_player_data(self, player):
        self.player_label.setText(player.name)
        self.player_image_view.setPixmap(self.player_image[player.id])
        self.player_stats_table.clear()
        self.player_stats_table.setRowCount(len(self.player_stats[player.id]))
        for row, stat in enumerate(self.player_stats[player.id]):
            item = QtGui.QTableWidgetItem(self.stat_categories[stat[0]])
            self.player_stats_table.setItem(row, 0, item)
            item = QtGui.QTableWidgetItem(stat[1])
            self.player_stats_table.setItem(row, 1, item)
        self.player_stats_table.resizeColumnsToContents()

    def get_stat_categories(self):
        self.get_access_token()
        url = '{0}/game/{1}/stat_categories'.format(YAHOO_URL, YAHOO_LAST_SEASON_ID)
        statsxml = self.yahoo.request(url)
        self.read_stat_categories(statsxml)

    def read_stat_categories(self, statsxml):
        root = ElementTree.fromstring(statsxml)
        models.remove_namespace(root, '{0}/base.rng'.format(YAHOO_URL))
        self.stat_categories = {}
        for stat in root.findall('game/stat_categories/stats/stat'):
            stat_id = stat.findtext('stat_id')
            stat_name = stat.findtext('name')
            self.stat_categories[stat_id] = stat_name
