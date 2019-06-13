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

from widgets.menuitem import Menuitem
from PyQt5.QtCore import QObject, pyqtProperty, Q_CLASSINFO
from PyQt5.QtQml import QQmlListProperty


class Menu(QObject):
    Q_CLASSINFO('DefaultProperty', 'items')

    def __init__(self, parent = None):
        super().__init__(parent)
        self.id = 0
        self._name = ""
        self._items = []

    def setId(self, id):
        self.id = id

    @pyqtProperty(QQmlListProperty)
    def items(self):
        return QQmlListProperty(Menuitem, self, self._items)

    @pyqtProperty('QString')
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def addMenuItem(self, item):
        self._items.append(item)
