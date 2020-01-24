#############################################################################
# Copyright (C) 2020 Olaf Japp
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
from widgets.interfaces import ElementEditorInterface
from widgets.item import Item
from PyQt5.QtWidgets import QUndoStack, QHBoxLayout, QTextEdit, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, QRegExp, pyqtSignal, qVersion, qRegisterResourceData, qUnregisterResourceData
from PyQt5.QtGui import QFont, QFontMetrics, QImage, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtQml import qmlRegisterType
import plugins.shopify_rc


class ShopifyEditor(ElementEditorInterface):
    close = pyqtSignal()

    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.site = None
        self.class_name = "ShopifyEditor"
        self.display_name = "Shopify"
        self.tag_name = "Shopify"
        self.version = "1.0"
        self.icon = QImage(":/shopify.png")
        self.changed = False
        self.setAutoFillBackground(True)

        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(15)

        grid = QGridLayout()

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip("Close Editor")
        self.html = QTextEdit()
        self.html.setFont(font)
        self.html.setAcceptRichText(False)
        self.html.setLineWrapMode(QTextEdit.NoWrap)
        metrics = QFontMetrics(font)
        self.html.setTabStopWidth(4 * metrics.width(' '))

        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)

        self.titleLabel = QLabel("Shopify Module")
        fnt = self.titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        self.titleLabel.setFont(fnt)

        grid.addWidget(self.titleLabel, 0, 0)
        grid.addWidget(close, 0, 1, 1, 1, Qt.AlignRight)
        grid.addWidget(self.html, 1, 0, 1, 2)
        grid.addWidget(QLabel("Admin Label"), 2, 0)
        grid.addWidget(self.adminlabel, 3, 0, 1, 2)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        self.html.textChanged.connect(self.contentChanged)
        self.adminlabel.textChanged.connect(self.contentChanged)

    def setCaption(self, caption):
        self.titleLabel.setText(caption)

    def setText(self, text):
        self.html.setPlainText(text)

    def getText(self):
        return self.html.toPlainText()

    def setContent(self, content):
        self.content = content
        if content:
            if isinstance(content, Shopify):
                self.adminlabel.setText(content.adminlabel)
                self.html.setPlainText(content.text)
            else:
                self.html.setPlainText(content.text)
                self.adminlabel.setText(content.adminlabel)
            self.changed = False

    def getContent(self):
        return self.content

    def getDefaultContent(self):
        return Shopify()

    def setSite(self, site):
        self.site = site

    def closeEditor(self):
        if self.changed:
            if self.content:
                self.content.adminlabel = self.adminlabel.text()
                self.content.text = self.html.toPlainText()
        self.close.emit()

    def registerContenType(self):
        qmlRegisterType(Shopify, 'ShopifyEditor', 1, 0, 'Shopify')

    def writeImportString(self, f):
        f.write("import ShopifyEditor 1.0\n")

    def pluginScripts(self):
        script = "<script src=\"http://sdks.shopifycdn.com/js-buy-sdk/v1/latest/index.umd.min.js\"></script>"
        return script


class Shopify(Item):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tag_name = "Shopify"


    def clone(self):
        txt = Shopify()
        txt.id = self._id
        txt.text = self._text
        txt.adminlabel = self._adminlabel
        return txt

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Shopify {\n")
        self.writeAttribute(f, indent + 4, "id", self._id)
        self.writeAttribute(f, indent + 4, "text", self._text)
        self.writeAttribute(f, indent + 4, "adminlabel", self._adminlabel)
        f.write(" " * indent + "}\n")

    def getHtml(self):
        return html.unescape(self.text)