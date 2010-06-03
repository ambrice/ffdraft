#!/usr/bin/python

import re
import yaml
from PyQt4 import QtCore, QtGui

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

