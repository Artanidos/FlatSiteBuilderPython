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
from widgets.column import Column
from widgets.item import Item


class Row(Item):
    Q_CLASSINFO('DefaultProperty', 'columns')

    def __init__(self, parent = None):
        super().__init__(parent)
        self._columns = []

    @pyqtProperty(QQmlListProperty)
    def columns(self):
        return QQmlListProperty(Column, self, self._columns)

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Row {\n")
        for item in self._columns:
            item.save(f, indent + 4)
        f.write(" " * indent + "}\n")