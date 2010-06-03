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
from PyQt4 import QtGui
from ffdraft.main import MainWindow

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

