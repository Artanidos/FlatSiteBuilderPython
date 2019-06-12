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

import html
from widgets.hyperlink import HyperLink
from widgets.flatbutton import FlatButton
from widgets.animateableeditor import AnimateableEditor
from widgets.section import Section
from widgets.pageeditor import PageEditor
from widgets.sectioneditor import SectionEditor
from widgets.roweditor import RowEditor
from widgets.columneditor import ColumnEditor
from widgets.elementeditor import ElementEditor, Mode
from widgets.content import ContentType
from widgets.xmlhighlighter import XmlHighlighter
from widgets.interfaces import ElementEditorInterface
from widgets.item import Item
from PyQt5.QtWidgets import QUndoStack, QHBoxLayout, QTextEdit, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, qVersion, qRegisterResourceData, qUnregisterResourceData
from PyQt5.QtGui import QFont, QFontMetrics, QImage
from PyQt5.QtQml import qmlRegisterType
import resources

class TextEditor(ElementEditorInterface):
    close = pyqtSignal()

    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.site = None
        self.class_name = "TextEditor"
        self.display_name = "Text"
        self.tag_name = "Text"
        self.version = "1.0"
        self.icon = QImage(":/texteditor.png")
        self.changed = False
        self.setAutoFillBackground(True)
        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(12)

        grid = QGridLayout()

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip("Close Editor")
        self.html = QTextEdit()
        self.html.setFont(font)
        self.html.setAcceptRichText(False)
        self.html.setLineWrapMode(QTextEdit.NoWrap)
        metrics = QFontMetrics(font)
        self.html.setTabStopWidth(4 * metrics.width(' '))

        self.highlighter = XmlHighlighter(self.html.document())

        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)

        titleLabel = QLabel("Text Module")
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)

        grid.addWidget(titleLabel, 0, 0)
        grid.addWidget(close, 0, 1, 1, 1, Qt.AlignRight)
        grid.addWidget(self.html, 1, 0, 1, 2)
        grid.addWidget(QLabel("Admin Label"), 2, 0)
        grid.addWidget(self.adminlabel, 3, 0, 1, 2)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        self.html.textChanged.connect(self.contentChanged)
        self.adminlabel.textChanged.connect(self.contentChanged)

    def setText(self, text):
        self.html.setPlainText(html.unescape(text))

    def getText(self):
        return html.escape(self.html.toPlainText())

    def setContent(self, content):
        self.content = content
        if isinstance(content, Text):
            self.adminlabel.setText(content.adminlabel)
            self.html.setPlainText(html.unescape(content.text))
        else:
            self.html.setPlainText(html.unescape(content.text))
            self.adminlabel.setText(content.adminlabel)
        self.changed = False

    def getContent(self):
        return self.content

    def getDefaultContent(self):
        return Text()

    def setSite(self, site):
        self.site = site

    def closeEditor(self):
        if self.changed:
            if self.content:
                self.content.adminlabel = self.adminlabel.text()
                self.content.text = self.html.toPlainText()
        self.close.emit()

    def registerContenType(self):
        qmlRegisterType(Text, 'TextEditor', 1, 0, 'Text')

    def writeImportString(self, f):
        f.write("import TextEditor 1.0\n")


class Text(Item):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tag_name = "Text"

    def clone(self):
        txt = Text()
        txt.id = self._id
        txt.text = self._text
        txt.adminlabel = self._adminlabel
        return txt

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Text {\n")
        self.writeAttribute(f, indent + 4, "id", self._id)
        self.writeAttribute(f, indent + 4, "text", html.escape(self._text))
        self.writeAttribute(f, indent + 4, "adminlabel", self._adminlabel)
        f.write(" " * indent + "}\n")

    def getHtml(self):
        return html.unescape(self.text)


qt_resource_data = b"\
\x00\x00\x01\xdb\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x20\x00\x00\x00\x20\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\
\x00\x00\x00\x04\x73\x42\x49\x54\x08\x08\x08\x08\x7c\x08\x64\x88\
\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0d\xd7\x00\x00\x0d\xd7\
\x01\x42\x28\x9b\x78\x00\x00\x00\x19\x74\x45\x58\x74\x53\x6f\x66\
\x74\x77\x61\x72\x65\x00\x77\x77\x77\x2e\x69\x6e\x6b\x73\x63\x61\
\x70\x65\x2e\x6f\x72\x67\x9b\xee\x3c\x1a\x00\x00\x01\x58\x49\x44\
\x41\x54\x58\x85\xc5\x97\x4b\xaa\xc2\x30\x18\x46\xcf\xff\x1b\x5a\
\x44\x10\x0c\x0e\x14\x0a\x82\xd5\xe2\x02\x04\x57\xe0\x62\xdc\xa9\
\x13\x37\x20\x38\xf3\x81\x82\x03\x3b\xb4\x68\xee\xc0\xfb\x82\x4b\
\xb1\x17\x9a\xe6\x1b\x15\x12\x72\x0e\xe4\x23\x49\x65\xb5\x5a\xb9\
\xfd\x7e\x4f\x9d\x11\x11\xb2\x2c\x63\x3a\x9d\xbe\x9d\xab\x87\xc3\
\xa1\x56\x38\x80\x73\x8e\xe3\xf1\x58\x69\xae\x3a\xe7\x6a\x17\x00\
\x78\x3e\x9f\xd5\x04\xbc\xd0\xff\x11\x6d\xb5\x5a\x5e\x16\xae\xba\
\xae\xc9\xb2\x8c\xd3\xe9\x54\xbb\xc0\x78\x3c\xae\x26\x90\xa6\x29\
\x69\x9a\xd6\x2e\x50\x35\xc1\x3b\x60\x8a\xa2\xe0\x76\xbb\x35\x06\
\x14\x11\xac\xb5\x88\xc8\x4b\x60\xbd\x5e\x37\x2a\x00\x30\x99\x4c\
\x98\xcd\x66\x00\x68\x9e\xe7\x8d\xc2\x01\x7e\x33\xbd\x1d\x44\x55\
\x13\xbc\x84\x1a\x45\x51\xe3\xd0\x38\x8e\xbf\xbf\xcd\x7c\x3e\xe7\
\x7c\x3e\x37\x06\x57\x55\x46\xa3\xd1\x8f\x80\xb5\x16\x6b\x6d\x63\
\x02\x7f\x84\x82\x91\x3f\x63\xae\xd7\x2b\x97\xcb\xc5\x1b\xa0\xd7\
\xeb\x31\x18\x0c\xca\x05\x36\x9b\x0d\xf7\xfb\xdd\x9b\x80\x88\xb0\
\x5c\x2e\x29\x2b\xbb\xfa\x84\xc3\xeb\x75\x54\x14\x45\xe9\x78\xf0\
\x0e\xe8\xd7\xa5\x10\x4c\xa0\xdb\xed\x7a\x05\xc4\x71\x4c\xbb\xdd\
\x2e\x1d\x37\x8b\xc5\x02\x9f\x17\x52\xa7\xd3\x41\xb5\x7c\xa7\x4d\
\x14\x45\xf4\xfb\x7d\x6f\x02\xef\x12\xbc\x84\x66\xb7\xdb\x79\x79\
\x94\x56\xc9\x70\x38\xc4\x6c\xb7\x5b\x1e\x8f\x47\x10\x81\x3c\xcf\
\xd1\x50\x70\x78\xfd\x3d\x05\xef\x40\xd0\x83\x48\x44\xd0\x24\x49\
\x82\x09\x24\x49\xc2\x07\xe7\x55\x5f\xe0\xcc\x66\xb1\x3a\x00\x00\
\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x0e\
\x02\x90\x3f\xe7\
\x00\x74\
\x00\x65\x00\x78\x00\x74\x00\x65\x00\x64\x00\x69\x00\x74\x00\x6f\x00\x72\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x66\x1a\xed\xe4\x10\
"

qt_version = [int(v) for v in qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
