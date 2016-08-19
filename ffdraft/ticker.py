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

    def set_teams(self, teams, total_rounds=99, rnd=1, idx=0):
        self.ticker.clearTeams()
        self.get_team = self.next_team_gen(teams, total_rounds, rnd, idx)
        while self.ticker.childrenRect().width() < self.width() - 90:
            # Room for another team
            try:
                team = self.get_team.next()
            except StopIteration:
                return
            self.ticker.appendTeam(team)

    def next_team_gen(self, teams, total_rounds, rnd, idx):
        if idx > 0:
            yield { 'is_round': True, 'round': rnd }
            for i in xrange(idx, len(teams)):
                yield teams[i]
            rnd += 1
        while rnd <= total_rounds:
            yield { 'is_round': True, 'round': rnd }
            for team in teams:
                yield team
            rnd += 1
            if rnd > total_rounds: return
            yield { 'is_round': True, 'round': rnd }
            for team in reversed(teams):
                yield team
            rnd += 1

    def set_next_team(self):
        self.ticker.removeTeam(1)
        next_round = self.ticker.isNextRound()
        if next_round:
            self.ticker.removeTeam(0)
        try:
            self.ticker.appendTeam(self.get_team.next())
            if next_round:
                self.ticker.appendTeam(self.get_team.next())
        except StopIteration:
            return

    def resizeEvent(self, ev):
        if self.get_team is not None:
            while self.ticker.childrenRect().width() < self.width() - 90:
                # Room for another team
                try:
                    team = self.get_team.next()
                    self.ticker.appendTeam(team)
                except StopIteration:
                    return
