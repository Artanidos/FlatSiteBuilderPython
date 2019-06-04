#############################################################################
# Copyright (C) 2019 Olaf Japp
#
# self file is part of FlatSiteBuilder.
#
#  FlatSiteBuilder is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FlatSiteBuilder is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FlatSiteBuilder.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from PyQt5.QtCore import pyqtProperty, QObject

class Item(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._adminlabel = ""
        self._text = ""
        self._id = ""

    @pyqtProperty('QString')
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @pyqtProperty('QString')
    def adminlabel(self):
        return self._adminlabel

    @adminlabel.setter
    def adminlabel(self, adminlabel):
        self._adminlabel = adminlabel

    def writeAttribute(self, f, indent, att, value):
        if value: 
            if isinstance(value, str):
                if att == "id":
                    f.write(" " * indent + att + ":  " + value + "\n")
                else:
                    f.write(" " * indent + att + ": \"" + value + "\"\n")
            elif isinstance(value, bool):
                f.write(" " * indent + att + ": true\n")

