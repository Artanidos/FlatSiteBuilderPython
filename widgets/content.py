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

from PyQt5.QtCore import pyqtProperty, QObject, Q_CLASSINFO, QDate
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtQml import QQmlListProperty
from enum import Enum
from widgets.section import Section
from widgets.item import Item


class ContentType(Enum):
    PAGE = 1
    POST = 2


class Content(QObject):
    Q_CLASSINFO('DefaultProperty', 'items')

    def __init__(self, parent = None):
        super().__init__(parent)
        self._title = ""
        self._menu = ""
        self._author = ""
        self._excerpt = ""
        self._keywords = ""
        self._script = ""
        self._layout = ""
        self._date = None
        self.source = ""
        self.content_type = None
        self.attributes = {}
        self._items = []

    @pyqtProperty(QQmlListProperty)
    def items(self):
        return QQmlListProperty(Item, self, self._items)

    @pyqtProperty('QString')
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @pyqtProperty('QString')
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        self._layout = layout

    @pyqtProperty('QString')
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, menu):
        self._menu = menu

    @pyqtProperty('QString')
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    @pyqtProperty('QString')
    def excerpt(self):
        return self._excerpt

    @excerpt.setter
    def excerpt(self, excerpt):
        self._excerpt = excerpt

    @pyqtProperty('QString')
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    @pyqtProperty('QString')
    def script(self):
        return self._script

    @script.setter
    def script(self, script):
        self._script = script

    @pyqtProperty('QDate')
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    def url(self):
        url = self.source
        return url.replace(".qml", ".html")

    def writeAttribute(self, f, indent, att, value):
        if value: 
            if isinstance(value, str):
                f.write(" " * indent + att + ": \"" + value + "\"\n")
            elif isinstance(value, bool):
                f.write(" " * indent + att + ": true\n")
            elif isinstance(value, QDate):
                f.write(" " * indent + att + ": \"" + value.toString("yyyy-MM-dd") + "\"\n")

    def save(self, f):
        f.write("Content {\n")
        self.writeAttribute(f, 4, "title", self.title)
        self.writeAttribute(f, 4, "menu", self.menu)
        self.writeAttribute(f, 4, "author", self.author)
        self.writeAttribute(f, 4, "keywords", self.keywords)
        self.writeAttribute(f, 4, "script", self.script)
        self.writeAttribute(f, 4, "layout", self.layout)
        self.writeAttribute(f, 4, "date", self.date)
        self.writeAttribute(f, 4, "excerpt", self.excerpt)

        for att, value in self.attributes:
            f.writeAttribute(f, 4, att, value) 
            
        for item in self._items:
            item.save(f, 4)

        f.write("}\n")

    def appendSection(self, sec):
        self._items.append(sec)

    def removeSection(self, sec):
        self._items.remove(sec)
