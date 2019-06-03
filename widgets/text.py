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

from PyQt5.QtCore import pyqtProperty
from widgets.item import Item

class Text(Item):
    def __init__(self, parent = None):
        super().__init__(parent)

    def clone(self):
        txt = Text()
        txt.id = self._id
        txt.text = self._text
        txt.adminlabel = self._adminlabel
        return txt

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Text {\n")
        self.writeAttribute(f, indent + 4, "id", self._id)
        self.writeAttribute(f, indent + 4, "text", self._text.replace("\n", "\\n"))
        self.writeAttribute(f, indent + 4, "adminlabel", self._adminlabel)
        f.write(" " * indent + "}\n")

    def getHtml(self):
        return self.text
