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

from widgets.animateableeditor import AnimateableEditor
from widgets.undoableeditor import UndoableEditor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class ElementEditorInterface(AnimateableEditor):
    close = pyqtSignal()

    def __init__(self):
        AnimateableEditor.__init__(self)
        self.class_name = ""
        self.display_name = ""
        self.tag_name = ""
        self.icon = None
        self.version = ""
        self.content = None
    
    def registerContenType(self):
        pass

    def setContent(self, content):
        pass
    
    def pluginStyles(self):
        return ""

    def pluginScripts(self):
        return ""

    def installAssets(self, assets_path):
        pass

    def getDefaultContent(self):
        return Item()

    def writeImportString(self, f):
        pass


class ThemeEditorInterface(UndoableEditor):
    def __init__(self):
        UndoableEditor.__init__(self)
        self.class_name = ""
        self.display_name = ""
        self.theme_name = ""
        self.version = ""
        self.theme_vars = {}
        self._source_path = ""

    def setSourcePath(self, path):
        self._source_path = path


class PublisherInterface(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.class_name = ""
        self.display_name = ""
        self.version = ""
        self._site_path = ""

    def setSitePath(self, path):
        self._site_path = path
