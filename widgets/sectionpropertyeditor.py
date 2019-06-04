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

from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QScrollArea, QUndoStack,
                             QVBoxLayout, QWidget)

from widgets.content import ContentType
from widgets.elementeditor import ElementEditor, Mode
from widgets.flatbutton import FlatButton
from widgets.hyperlink import HyperLink
from widgets.pageeditor import PageEditor
from widgets.roweditor import RowEditor
from widgets.section import Section
from widgets.sectioneditor import SectionEditor
from widgets.animateableeditor import AnimateableEditor


class SectionPropertyEditor(AnimateableEditor):
    close = pyqtSignal()

    def __init__(self):
        AnimateableEditor.__init__(self)
        self.grid = QGridLayout()
        self.cssclass = QLineEdit()
        self.style = QLineEdit()
        self.attributes = QLineEdit()
        self.id = QLineEdit()
        self.changed = False
        self.setAutoFillBackground(True)

        close = FlatButton("./images/close_normal.png", "./images/close_hover.png")
        close.setToolTip("Close Editor")

        titleLabel = QLabel("Section Module Settings")
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)

        vbox = QVBoxLayout()
        vbox.addStretch()

        self.grid.addWidget(titleLabel, 0, 0)
        self.grid.addWidget(close, 0, 1, 1, 1, Qt.AlignRight)
        self.grid.addWidget(QLabel("CSS Class"), 1, 0)
        self.grid.addWidget(self.cssclass, 2, 0, 1, 2)
        self.grid.addWidget(QLabel("Style"), 3, 0)
        self.grid.addWidget(self.style, 4, 0, 1, 2)
        self.grid.addWidget(QLabel("Aditional Attributes"), 5, 0)
        self.grid.addWidget(self.attributes, 6, 0, 1, 2)
        self.grid.addWidget(QLabel("Id"), 7, 0)
        self.grid.addWidget(self.id, 8, 0, 1, 2)
        self.grid.addLayout(vbox, 10, 0)
        self.setLayout(self.grid)

        close.clicked.connect(self.closeEditor)
        self.cssclass.textChanged.connect(self.contentChanged)
        self.style.textChanged.connect(self.contentChanged)
        self.attributes.textChanged.connect(self.contentChanged)
        self.id.textChanged.connect(self.contentChanged)

    def setSection(self, section):
        self.section = section
        self.id.setText(section.id)
        self.cssclass.setText(section.cssclass)
        self.style.setText(section.style)
        self.attributes.setText(section.attributes)
        self.changed = False

    def closeEditor(self):
        if self.changed:
            self.section.cssclass = self.cssclass.text()
            self.section.sytle = self.style.text()
            self.section.attributes = self.attributes.text()
            self.section.id = self.id.text()
        self.close.emit()

    def contentChanged(self):
        self.changed = True
