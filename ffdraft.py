#!/usr/bin/python2
#
# Copyright (C) 2007-2011 Aaron Brice
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
import os
import sys
import ConfigParser
from PyQt4 import QtGui
from ffdraft.main import MainWindow

if __name__ == "__main__":
    try:
        cfgfile = open(os.path.join(sys.path[0], 'ffdraft.cfg'))
        config = ConfigParser.RawConfigParser()
        config.readfp(cfgfile)
        consumer_key = config.get('apikey', 'consumer_key')
        consumer_secret = config.get('apikey', 'consumer_secret')
    except:
        print('No API keys found in ffdraft.cfg, see README')
        sys.exit(0)

    app = QtGui.QApplication(sys.argv)
    f = open(os.path.join(sys.path[0], 'ffdraft.css'))
    try:
        css = f.read()
        app.setStyleSheet(css);
    finally:
        f.close()
    db = sys.argv[1] if len(sys.argv) > 1 else None
    mainWin = MainWindow(db, consumer_key, consumer_secret)
    mainWin.resize(1600,1000)
    mainWin.show()
    sys.exit(app.exec_())

