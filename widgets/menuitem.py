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

from PyQt5.QtCore import QObject, pyqtProperty, Q_CLASSINFO
from PyQt5.QtQml import QQmlListProperty


class Menuitem(QObject):
    Q_CLASSINFO('DefaultProperty', 'items')

    def __init__(self, parent = None):
        super().__init__(parent)
        self._title = ""
        self._url = ""
        self._icon = ""
        #self._attr = ""
        self._attributes = ""
        #self.attributes = {}
        self._items = []
        self.parentItem = None

    @pyqtProperty(QQmlListProperty)
    def items(self):
        return QQmlListProperty(Menuitem, self, self._items)

    @pyqtProperty('QString')
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @pyqtProperty('QString')
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @pyqtProperty('QString')
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon):
        self._icon = icon

    @pyqtProperty('QString')
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

 #   def addAttribute(self, key, value):
 #       self.attributes[key] = value

    def isSubitem(self):
        return self.isSubitem

    def setSubitem(self, sub):
        self.isSubitem = sub

    def addMenuitem(self, item):
        self.items.append(item)
        item.setParentItem(self)

    def removeMenuitem(self, item):
        self.items.remove(item)
        item.setParentItem(None)

    def setParentItem(self, parent):
        self.parentItem = parent
