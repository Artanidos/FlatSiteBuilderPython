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
#  along with FlatSiteBuilder.  If not, see <http.//www.gnu.org/licenses/>.
#
#############################################################################

from widgets.interfaces import ElementEditorInterface
from widgets.item import Item
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtCore import pyqtProperty



class SlideEditor(ElementEditorInterface):
    def __init__(self):
        ElementEditorInterface.__init__(self)

    def closeEditor(self):
        if self.changed:
            if self.content:
                self.content.adminlabel = self.adminlabel.text()
                self.content.text = html.escape(self.html.toPlainText())
        self.close.emit()

    def registerContenType(self):
        qmlRegisterType(Slide, 'Slide', 1, 0, 'Slide')

    def writeImportString(self, f):
        f.write("import Slide 1.0\n")


class Slide(Item):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tag_name = "Slide"
        self._src = ""
    
    @pyqtProperty('QString')
    def src(self):
        return self._src

    @src.setter
    def src(self, src):
        self._src = src