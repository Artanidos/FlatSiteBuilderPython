#############################################################################
# Copyright (C) 2019 Olaf Japp
#
# This file is part of FlatSiteBuilder.
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

from enum import Enum

class ContentType(Enum):
	PAGE = 1
	POST = 2

class Content:

    def __init__(self, type):
        self.content_type = type
        self.attributes = {}
        self.keywords = ""
        self.script = ""
        self.excerpt = ""

    def setSource(self, source):
        self.source = source

    def setExcerpt(self, value):
        self.excerpt = value

    def setTitle(self, value):
        self.title = value

    def setMenu(self, value):
        self.menu = value

    def setAuthor(self, value):
        self.author = value

    def setLayout(self, value):
        self.layout = value

    def setKeywords(self, value):
        self.keywords = value

    def setScript(self, value):
        self.script = value

    def setDate(self, value):
        self.date = value

    def addAttribute(self, att, value):
        self.attributes[att] = value

    def contentType(self):
        return self.content_type

    def url(self):
        url = self.source
        return url.replace(".xml", ".html")