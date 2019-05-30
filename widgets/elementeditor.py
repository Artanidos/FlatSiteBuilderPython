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

from widgets.flatbutton import FlatButton
from widgets.hyperlink import HyperLink
from widgets.section import Section
from widgets.content import ContentType
from PyQt5.QtWidgets import QUndoStack, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QColor, QPalette
from enum import Enum


class Mode(Enum):
    EMPTY = 1
    ENABLED = 2
    DROPZONE = 3


class ElementEditor(QWidget):

    def __init__(self, element):
        QWidget.__init__(self)
        self.element = element
        self.setAutoFillBackground(True)
        self.setMinimumWidth(120)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.zoom = False

        self.mode = Mode.EMPTY
        self.normalColor = QColor(self.palette().base().color().name()).lighter().name()
        self.enabledColor = self.palette().base().color().name()
        self.dropColor = QColor(self.palette().base().color().name()).lighter().lighter().name()
        self.setColor(self.normalColor)
        self.link = HyperLink("(+) Insert Module")

        self.editButton = FlatButton("./images/edit_normal.png", "./images/edit_hover.png")
        self.copyButton = FlatButton("./images/copy_normal.png", "./images/copy_hover.png")
        self.closeButton = FlatButton("./images/trash_normal.png", "./images/trash_hover.png")
        self.editButton.setVisible(False)
        self.copyButton.setVisible(False)
        self.closeButton.setVisible(False)
        self.editButton.setToolTip("Edit Element")
        self.closeButton.setToolTip("Delete Element")
        self.copyButton.setToolTip("Copy Element")
        self.text = QLabel("Text")
        self.text.setVisible(False)
        layout= QHBoxLayout()
        layout.addWidget(self.link, 0, Qt.AlignCenter)
        layout.addWidget(self.editButton)
        layout.addWidget(self.copyButton)
        layout.addWidget(self.text, 1, Qt.AlignCenter)
        layout.addWidget(self.closeButton)
        self.setLayout(layout)

        # connect(self.link, SIGNAL(clicked()), this, SLOT(enable()))
        # connect(self.editButton, SIGNAL(clicked()), this, SLOT(edit()))
        # connect(self.copyButton, SIGNAL(clicked()), this, SLOT(copy()))
        # connect(self.closeButton, SIGNAL(clicked()), this, SLOT(close()))

        self.load()

    def setColor(self, name):
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(name))
        self.setPalette(pal)

    def load(self):
        print("impl load")

    def setMode(self, mode):
        self.mode = mode
        if mode == Mode.EMPTY:
            self.link.setVisible(True)
            self.editButton.setVisible(False)
            self.copyButton.setVisible(False)
            self.closeButton.setVisible(False)
            self.text.setVisible(False)
            self.setColor(self.normalColor)
        elif mode == Mode.ENABLED:
            self.link.setVisible(False)
            self.editButton.setVisible(True)
            self.copyButton.setVisible(True)
            self.closeButton.setVisible(True)
            self.text.setVisible(True)
            self.setColor(self.enabledColor)
        elif mode == Mode.DROPZONE:
            self.link.setVisible(False)
            self.editButton.setVisible(False)
            self.copyButton.setVisible(False)
            self.closeButton.setVisible(False)
            self.text.setVisible(True)
            self.text.setText("Drop Here")
            self.setColor(self.dropColor)
        