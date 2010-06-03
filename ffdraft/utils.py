#!/usr/bin/python

from PyQt4 import QtCore

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

