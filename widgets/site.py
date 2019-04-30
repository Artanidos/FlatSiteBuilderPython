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

import os, datetime
from widgets.content import ContentType, Content
from widgets.menu import Menu
from widgets.menuitem import MenuItem
from xml.sax import make_parser, handler
from xml.etree import ElementTree as et
from PySide2.QtCore import QFileInfo

class Site:

    def __init__(self, win, filename):
        info = QFileInfo(filename)
        self.filename = info.fileName()
        self.win = win
        self.source_path = info.path()
        self.publisher = ""
        self.copyright = ""
        self.keywords = ""
        self.description = ""
        self.author = ""
        self.theme = ""
        self.attributes = {}
        self.pages = []
        self.posts = []
        self.menus = []
        self.title = ""

    def load(self):
        parser = make_parser()
        parser.setContentHandler(SiteHandler(self))
        parser.parse(self.source_path + "/Site.xml")
        self.win.statusBar().showMessage("Site has been loaded")
    
    def save(self):
        site = et.Element("Site")
        site.attrib["theme"] = self.theme
        site.attrib["title"] = self.title
        site.attrib["description"] = self.description
        site.attrib["copyright"] = self.copyright
        site.attrib["keywords"] = self.keywords
        site.attrib["author"] = self.author
        site.attrib["publisher"] = self.publisher

        for att, value in self.attributes.items():
            site.attrib[att] = value

        tree = et.ElementTree(site)
        tree.write(self.source_path + "/Site.xml", encoding = "utf-8", method = "xml", xml_declaration = True)
        self.win.statusBar().showMessage("Site has been saved")


    def saveMenus(self):
        menus = et.Element("Menus")
        for menu in self.menus:
            m = et.SubElement(menus, "Menu")
            m.attrib["name"] = menu.name
            for item in menu.items:
                i = et.SubElement(m, "Item")
                i.attrib["title"] = item.title
                i.attrib["url"] = item.url 
                i.attrib["icon"] = item.icon
                for att, value in item.attributes.items():
                    i.attrib[att] = value
                for subitem in item.items:
                    si = et.SubElement(i, "Item")
                    si.attrib["title"] = si.title
                    si.attrib["url"] = si.url
                    si.attrib["icon"] = si.icon
                    for att, value in subitem.attributes.items():
                       si.attrib[att] = value
        tree = et.ElementTree(menus)
        tree.write(self.source_path + "/Menus.xml", encoding = "utf-8", method = "xml", xml_declaration = True)                 
        self.win.statusBar().showMessage("Menus have been saved")

        
    def addMenu(self, menu):
        self.menus.append(menu)

    def loadMenus(self):    
        self.menus.clear()
        parser = make_parser()
        parser.setContentHandler(MenuHandler(self))
        parser.parse(self.source_path + "/Menus.xml")        
        self.win.statusBar().showMessage("Menus have been loaded")

    def removeMenu(self, menu):
        self.menus.remove(menu)
    
    def publisher(self):
        return self.publisher

    def setPublisher(self, arg):
        self.publisher = arg

    def copyright(self):
        return self.copyright

    def setCopyright(self, copyright):
        self.copyright = copyright

    def keywords(self):
        return self.keywords

    def setKeywords(self, keywords):
        self.keywords = keywords

    def description(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def author(self):
        return self.author

    def setAuthor(self, author):
        self.author = author

    def seTheme(self, theme):
        self.theme = theme

    def theme(self):
        return self.theme

    def addAttribute(self, key, value):
        self.attributes[key] = value

    def addPage(self, page):
        self.pages.append(page)

    def loadPages(self):
        self.pages.clear()
        for r, d, files in os.walk(self.source_path + "/pages"):
            for filename in files:  
                parser = make_parser()
                parser.setContentHandler(ContentHandler(self, filename, ContentType.PAGE))
                parser.parse(self.source_path + "/pages/" + filename)           

        self.win.statusBar().showMessage("Pages have been loaded")

    def loadPosts(self):
        self.posts.clear()
        for r, d, files in os.walk(self.source_path + "/posts"):
            for filename in files:  
                parser = make_parser()
                parser.setContentHandler(ContentHandler(self, filename, ContentType.POST))
                parser.parse(self.source_path + "/posts/" + filename)           

        self.win.statusBar().showMessage("Pages have been loaded")
        

class SiteHandler(handler.ContentHandler):
    def __init__(self, site):
        self.site = site

    def startElement(self, name, attrs):
        if name == "Site":
            for att, value in attrs.items():
                if att == "theme":
                    self.site.theme = value
                elif att == "description":
                    self.site.description = value
                elif att == "copyright":
                    self.site.copyright = value
                elif att == "title":
                    self.site.title = value
                elif att == "keywords":
                    self.site.keywords = value
                elif att == "author":
                    self.site.author = value
                elif att == "publisher":
                    self.site.publisher = value
                else:
                    self.site.addAttribute(att, value)


class ContentHandler(handler.ContentHandler):

    def __init__(self, site, filename, type):
        self.site = site
        self.filename = filename
        self.type = type

    def startElement(self, name, attrs):
        if name == "Content":
            content = Content(type)
            content.setSource(self.filename)
            self.site.addPage(content)
            for att, value in attrs.items():
                if att == "excerpt":
                    content.setExerpt(value)
                elif att == "title":
                    content.setTitle(value)
                elif att == "menu":
                    content.setMenu(value)
                elif att == "author":
                    content.setAuthor(value)
                elif att == "layout":
                    content.setLayout(value)
                elif att == "keywords":
                    content.setKeywords(value)
                elif att == "date":
                    content.setDate(datetime.datetime.strptime(value, "%d.%m.%Y"))
                else:
                    content.addAttribute(att, value)
            

class MenuHandler(handler.ContentHandler):
    def __init__(self, site):
        self.site = site
        self.id = 0
        self.current_menu = None
        self.current_item = None

    def startElement(self, name, attrs):
        if name == "Menus":
            pass
        elif name == "Menu":
            self.id += 1
            self.current_menu = Menu()
            self.current_menu.setId(self.id)
            self.current_menu.setName(attrs["name"])
        elif name == "Item":
            if self.current_item: # sub menu item
                tmp_item = MenuItem()
                self.current_item.addMenuItem(tmp_item)
                self.current_item = tmp_item
            else:
                self.current_item = MenuItem()
            for att, value in attrs.items():
                if att == "title":
                    self.current_item.setTitle(value)
                elif att == "url":
                    self.current_item.setUrl(value)
                elif att == "icon":
                    self.current_item.setIcon(value)
                else: # set additional html attributes like class="scrollTo"
                    self.current_item.addAttribute(att, value)
        else:
            print("Unknown tag name in MenuHandler:", name)
    
                    
    def endElement(self, name):
        if name == "Item":
            self.current_menu.addMenuItem(self.current_item)
            self.current_item = None
        elif name == "Menu":
            self.site.addMenu(self.current_menu)
            self.current_menu = None

                                
                                
        #                            if(menu.name() == "Item")                                    
        #                                MenuItem *subitem = MenuItem()
        #                                subitem.setSubitem(True)
        #                                foreach(QXmlStreamAttribute att, menu.attributes())
        #                                
        #                                    QString attName = att.name().toString()
        #                                    QString value = att.value().toString()
        #                                    if(attName == "title")
        #                                        subitem.setTitle(value)
        #                                    else if(attName == "url")
        #                                        subitem.setUrl(value)
        #                                    else if(attName == "icon")
        #                                        subitem.setIcon(value)
        #                                    else //set additional html attributes like class="scrollTo"
        #                                        subitem.addAttribute(attName, value)
        #                                
        #                                item.addMenuitem(subitem)
        #                                menu.readNext()
        #                            
        #                            else
        #                                menu.skipCurrentElement()
        #                        m.addMenuitem(item)
        #                        menu.readNext()                    
        #                    else
        #                        menu.skipCurrentElement()
        #                
        #                addMenu(m)
                    
        #            else
        #                menu.skipCurrentElement()
                
            
