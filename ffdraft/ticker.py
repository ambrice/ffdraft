from PyQt4 import QtCore, QtGui, QtDeclarative

class Ticker(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.get_team = None
        sp = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setSizePolicy(sp)

        view = QtDeclarative.QDeclarativeView()
        view.setSource(QtCore.QUrl.fromLocalFile('ffdraft/qml/Ticker.qml'))
        self.ticker = view.rootObject()

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(view)
        self.setLayout(hbox)

    def set_teams(self, teams, rnd=1, idx=0):
        self.ticker.clearTeams()
        self.get_team = self.next_team_gen(teams, rnd, idx)
        while self.ticker.childrenRect().width() < self.width() - 90:
            # Room for another team
            team = self.get_team.next()
            self.ticker.appendTeam(team)

    def next_team_gen(self, teams, rnd, idx):
        if idx > 0:
            yield { 'is_round': True, 'round': rnd }
            for i in xrange(idx, len(teams)):
                yield teams[i]
            rnd += 1
        while True:
            yield { 'is_round': True, 'round': rnd }
            for team in teams:
                yield team
            rnd += 1
            yield { 'is_round': True, 'round': rnd }
            for team in reversed(teams):
                yield team
            rnd += 1

    def set_next_team(self):
        self.ticker.removeTeam(1)
        self.ticker.appendTeam(self.get_team.next())
        if self.ticker.isNextRound().toBool():
            self.ticker.removeTeam(0)
            self.ticker.appendTeam(self.get_team.next())

    def resizeEvent(self, ev):
        if self.get_team is not None:
            while self.ticker.childrenRect().width() < self.width() - 90:
                # Room for another team
                team = self.get_team.next()
                self.ticker.appendTeam(team)
