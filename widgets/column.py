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
from widgets.item import Item

class Column(Item):
    Q_CLASSINFO('DefaultProperty', 'items')

    def __init__(self, parent = None):
        super().__init__(parent)
        self._items = []
        self._span = 0

    @pyqtProperty(QQmlListProperty)
    def items(self):
        return QQmlListProperty(Item, self, self._items)

    @pyqtProperty(int)
    def span(self):
        return self._span

    @span.setter
    def span(self, span):
        self._span = span

    def clone(self):
        col = Column()
        col.span = self._span
        for item in self._items:
            col._items.append(item.clone())
        return col

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Column {\n")
        self.writeAttribute(f, indent + 4, "span", self._span)
        for item in self._items:
            item.save(f, indent + 4)
        f.write(" " * indent + "}\n")

    def getHtml(self):
        html = "<div class=\"col-md-" + str(self._span) + "\">\n"
        for item in self._items:
            html += item.getHtml()
        return html + "\n</div>\n"

    def collectPluginNames(self, list):
        for item in self._items:
            if not item.tag_name in list:
                list.append(item.tag_name)     