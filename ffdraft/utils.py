#!/usr/bin/python

from PyQt4 import QtCore, QtGui

class EggTimer(QtCore.QObject):
    update = QtCore.pyqtSignal(QtCore.QString)
    expired = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.send_update)
        self.countdown = 0

    def set_countdown(self, countdown):
        self.countdown = countdown
        self.current_time = self.countdown
        self.update.emit(self.time_str(self.current_time))

    def reset(self):
        self.current_time = self.countdown
        self.update.emit(self.time_str(self.current_time))

    def start(self):
        if self.countdown > 0:
            self.timer.start(1000)

    def pause(self):
        self.timer.stop()

    def send_update(self):
        self.current_time -= 1
        self.update.emit(self.time_str(self.current_time))
        if self.current_time == 0:
            self.timer.stop()
            self.expired.emit()

    def time_str(self, time):
        hours = str(int(time) / 60)
        minutes = str(int(time) % 60)
        if (int(minutes) < 10):
            minutes = "0" + minutes
        return str(hours) + ":" + str(minutes)


class SelectionOrder(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        sp = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setSizePolicy(sp)
        self.hbox = QtGui.QHBoxLayout()
        self.setLayout(self.hbox)

    def set_teams(self, teams, icons):
        self.teams = teams
        self.icons = icons
        for i, team in enumerate(teams):
            button = QtGui.QLabel(self)
            button.setPixmap(icons[i])
            self.hbox.addWidget(button)

    def sizeHint(self):
        return QtCore.QSize(60, 60)

