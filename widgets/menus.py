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

from widgets.menu import Menu
from PyQt5.QtCore import QObject, pyqtProperty, Q_CLASSINFO
from PyQt5.QtQml import QQmlListProperty


class Menus(QObject):
    Q_CLASSINFO('DefaultProperty', 'menus')

    def __init__(self, parent = None):
        super().__init__(parent)

        self._menus = []

    @pyqtProperty(QQmlListProperty)
    def menus(self):
        return QQmlListProperty(Menu, self, self._menus)
