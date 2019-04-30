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

class MenuItem:

    def __init__(self):
        self.title = ""
        self.url = ""
        self.icon = ""
        self.attributes = {}
        self.items = []
        self.parentItem = None

    def setTitle(self, title):
        self.title = title

    def setUrl(self, url):
        self.url = url

    def setIcon(self, icon):
        self.icon = icon

    def addAttribute(self, key, value):
        self.attributes[key] = value

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
    
