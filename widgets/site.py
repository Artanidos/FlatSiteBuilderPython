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

import datetime
import os
from widgets.content import ContentType, Content
from widgets.menu import Menu
from widgets.menuitem import Menuitem
from widgets.generator import Generator
from PyQt5.QtCore import QFileInfo, QObject, pyqtProperty, QUrl
from PyQt5.QtQml import QQmlEngine, QQmlComponent


class Site(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filename = ""
        self.win = None
        self.source_path = ""
        self.deploy_path = ""
        self._publisher = ""
        self._copyright = ""
        self._keywords = ""
        self._description = ""
        self._author = ""
        self._theme = ""
        self._title = ""
        self._logo = ""
        self.attributes = {}
        self.pages = []
        self.posts = []
        self.menus = None

    @pyqtProperty('QString')
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        self._publisher = publisher

    @pyqtProperty('QString')
    def copyright(self):
        return self._copyright

    @copyright.setter
    def copyright(self, copyright):
        self._copyright = copyright

    @pyqtProperty('QString')
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    @pyqtProperty('QString')
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self.deploy_path = os.path.join(Generator.sitesPath(), title)

    @pyqtProperty('QString')
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @pyqtProperty('QString')
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    @pyqtProperty('QString')
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, theme):
        self._theme = theme

    @pyqtProperty('QString')
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, logo):
        self._logo = logo

    def setFilename(self, filename):
        info = QFileInfo(filename)
        self.filename = info.fileName()
        self.source_path = info.path()

    def filename(self):
        return self.filename

    def setWindow(self, win):
        self.win = win

    def save(self):
        with open(os.path.join(self.source_path, "Site.qml"), "w") as f:
            f.write("import FlatSiteBuilder 2.0\n\n")
            f.write("Site {\n")
            f.write("   title: '" + self.title + "'\n")
            f.write("   theme: '" + self.theme + "'\n")
            f.write("   description: '" + self.description + "'\n")
            f.write("   copyright: '" + self.copyright + "'\n")
            f.write("   keywords: '" + self.keywords + "'\n")
            f.write("   author: '" + self.author + "'\n")
            f.write("   logo: '" + self.logo + "'\n")
            f.write("   publisher: '" + self.publisher + "'\n")
            f.write("}\n")
        self.win.statusBar().showMessage("Site has been saved")

    def saveMenus(self):
        with open(os.path.join(self.source_path, "Menus.qml"), "w") as f:
            f.write("import FlatSiteBuilder 2.0\n\n")
            f.write("Menus {\n")
            for menu in self.menus.menus:
                f.write("    Menu {\n")
                f.write("        name: '" + menu.name + "'\n")
                for item in menu.items:
                    f.write("        Menuitem {\n")
                    f.write("            title: '" + item.title + "'\n")
                    f.write("            url: '" + item.url + "'\n")
                    f.write("            icon: '" + item.icon + "'\n")
                    for subitem in item.items:
                        f.write("            Menuitem {\n")
                        f.write("                title: '" + subitem.title + "'\n")
                        f.write("                url: '" + subitem.url + "'\n")
                        f.write("                icon: '" + subitem.icon + "'\n")
                        f.write("            }\n")
                    f.write("        }\n")
                f.write("    }\n")
            f.write("}\n")
        self.win.statusBar().showMessage("Menus have been saved")

    def addMenu(self, menu):
        self.menus.menus.append(menu)

    def loadMenus(self):
        engine = QQmlEngine()
        component = QQmlComponent(engine)
        component.loadUrl(QUrl(os.path.join(self.source_path, "Menus.qml")))
        self.menus = component.create()
        if self.menus is not None:
            self.win.statusBar().showMessage("Menus have been loaded")
        else:
            for error in component.errors():
                print(error.toString())
        del engine

    def removeMenu(self, menu):
        self.menus.remove(menu)

    def addAttribute(self, key, value):
        self.attributes[key] = value

    def addPage(self, page):
        self.pages.append(page)

    def loadPages(self):
        self.pages.clear()
        for root, dirs, files in os.walk(os.path.join(self.source_path, "pages")):
            for file in files:
                page = self.loadContent(file, ContentType.PAGE)
                self.pages.append(page)
        self.win.statusBar().showMessage("Pages have been loaded")

    def loadContent(self, source, type):
        if type == ContentType.PAGE:
            sub = "pages"
        else:
            sub = "posts"
        engine = QQmlEngine()
        component = QQmlComponent(engine)
        component.loadUrl(QUrl(os.path.join(self.source_path, sub, source)))
        content = component.create()
        if content is not None:
            content.source = source
            content.content_type = type
        else:
            for error in component.errors():
                print(error.toString())
        return content

    def loadPosts(self):
        self.posts.clear()
        for root, dirs, files in os.walk(os.path.join(self.source_path, "posts")):
            for file in files:
                post = self.loadContent(file, ContentType.POST)
                self.posts.append(post)
        self.win.statusBar().showMessage("Posts have been loaded")
