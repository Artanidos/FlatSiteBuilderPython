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

from widgets.hyperlink import HyperLink
from widgets.flatbutton import FlatButton
from widgets.animateableeditor import AnimateableEditor
from widgets.section import Section
from widgets.text import Text
from widgets.pageeditor import PageEditor
from widgets.sectioneditor import SectionEditor
from widgets.roweditor import RowEditor
from widgets.columneditor import ColumnEditor
from widgets.elementeditor import ElementEditor, Mode
from widgets.content import ContentType
from widgets.xmlhighlighter import XmlHighlighter
from PyQt5.QtWidgets import QUndoStack, QHBoxLayout, QTextEdit, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QFont, QFontMetrics
import resources

class TextEditor(AnimateableEditor):
    close = pyqtSignal()

    def __init__(self):
        AnimateableEditor.__init__(self)
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

    def setContent(self, content):
        self.content = content
        if isinstance(content, Text):
            self.adminlabel.setText(content.adminlabel)
            self.html.setPlainText(content.text)
        else:
            self.html.setPlainText(content.text)
            self.adminlabel.setText(content.adminlabel)
        self.changed = False

    def getContent(self):
        return self.content

    def setSite(self, site):
        self.site = site

    def closeEditor(self):
        if self.changed:
            self.content.adminlabel = self.adminlabel.text()
            self.content.text = self.html.toPlainText() 
        self.close.emit()