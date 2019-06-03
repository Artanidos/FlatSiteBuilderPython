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

from PyQt5.QtCore import pyqtProperty, QObject, Q_CLASSINFO
from PyQt5.QtQml import QQmlListProperty
from widgets.row import Row
from widgets.item import Item

class Section(Item):
    Q_CLASSINFO('DefaultProperty', 'items')

    def __init__(self, parent = None):
        super().__init__(parent)
        self._fullwidth = False
        self._cssclass = ""
        self._style = ""
        self._attributes = ""
        self._items = []

    @pyqtProperty(QQmlListProperty)
    def items(self):
        return QQmlListProperty(Item, self, self._items)

    @pyqtProperty('bool')
    def fullwidth(self):
        return self._fullwidth

    @fullwidth.setter
    def fullwidth(self, fullwidth):
        self._fullwidth = fullwidth

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Section {\n")
        self.writeAttribute(f, indent + 4, "id", self._id)
        self.writeAttribute(f, indent + 4, "cssclass", self._cssclass)
        self.writeAttribute(f, indent + 4, "style", self._style)
        self.writeAttribute(f, indent + 4, "attributes", self._attributes)
        self.writeAttribute(f, indent + 4, "fullwidth", self._fullwidth)
        for item in self._items:
            item.save(f, indent + 4)
        f.write(" " * indent + "}\n")

    def getHtml(self):
        html = ""
        if self.fullwidth:
            for item in self._items:
                html += item.getHtml() + "\n"
        else:
            html += "<section"
            if self._cssclass:
                cssclass = self._cssclass
            else:
                cssclass = "container"
            html += " class=\"" + cssclass + "\""
            if self._id:
                html += " id=\"" + self._id +"\""
            if self._style:
                html += " style=\"" + self._style + "\""
            if self._attributes:
                html += " " + self._attributes
            html += ">\n"
            for item in self._items:
                html += item.getHtml()
        return html