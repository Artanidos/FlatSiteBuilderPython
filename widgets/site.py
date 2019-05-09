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
from PyQt5.QtCore import QFileInfo, QObject, pyqtProperty, QUrl
from PyQt5.QtQml import QQmlEngine, QQmlComponent


class Site(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filename = ""
        self.win = None
        self.source_path = ""
        self._publisher = ""
        self._copyright = ""
        self._keywords = ""
        self._description = ""
        self._author = ""
        self._theme = ""
        self._title = ""
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

    def removeMenu(self, menu):
        self.menus.remove(menu)

    def addAttribute(self, key, value):
        self.attributes[key] = value

    def addPage(self, page):
        self.pages.append(page)

    def loadPages(self):
        pass
        # self.pages.clear()
        # for r, d, files in os.walk(os.path.join(self.source_path, "pages")):
        #     for filename in files:
        #         parser = make_parser()
        #         parser.setContentHandler(ContentHandler(self, filename, ContentType.PAGE))
        #         parser.parse(os.path.join(self.source_path, "pages", filename))

        # self.win.statusBar().showMessage("Pages have been loaded")

    def loadPosts(self):
        pass
        # self.posts.clear()
        # for r, d, files in os.walk(os.path.join(self.source_path, "posts")):
        #     for filename in files:
        #         parser = make_parser()
        #         parser.setContentHandler(ContentHandler(self, filename, ContentType.POST))
        #         parser.parse(os.path.join(self.source_path, "posts", filename))

        # self.win.statusBar().showMessage("Pages have been loaded")


# class SiteHandler(handler.ContentHandler):
#     def __init__(self, site):
#         self.site = site

#     def startElement(self, name, attrs):
#         if name == "Site":
#             for att, value in attrs.items():
#                 if att == "theme":
#                     self.site.theme = value
#                 elif att == "description":
#                     self.site.description = value
#                 elif att == "copyright":
#                     self.site.copyright = value
#                 elif att == "title":
#                     self.site.title = value
#                 elif att == "keywords":
#                     self.site.keywords = value
#                 elif att == "author":
#                     self.site.author = value
#                 elif att == "publisher":
#                     self.site.publisher = value
#                 else:
#                     self.site.addAttribute(att, value)


# class ContentHandler(handler.ContentHandler):

#     def __init__(self, site, filename, t):
#         self.site = site
#         self.filename = filename
#         self.type = t

#     def startElement(self, name, attrs):
#         if name == "Content":
#             content = Content(self.type)
#             content.setSource(self.filename)
#             self.site.addPage(content)
#             for att, value in attrs.items():
#                 if att == "excerpt":
#                     content.setExerpt(value)
#                 elif att == "title":
#                     content.setTitle(value)
#                 elif att == "menu":
#                     content.setMenu(value)
#                 elif att == "author":
#                     content.setAuthor(value)
#                 elif att == "layout":
#                     content.setLayout(value)
#                 elif att == "keywords":
#                     content.setKeywords(value)
#                 elif att == "date":
#                     content.setDate(datetime.datetime.strptime(value, "%d.%m.%Y"))
#                 else:
#                     content.addAttribute(att, value)

