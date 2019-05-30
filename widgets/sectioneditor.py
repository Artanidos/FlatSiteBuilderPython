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

from PyQt5.QtWidgets import QUndoStack, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette, QColor
from widgets.row import Row
from widgets.text import Text


class SectionEditor(QWidget):

    def __init__(self, section):
        QWidget.__init__(self)
        from widgets.hyperlink import HyperLink
        from widgets.flatbutton import FlatButton
        from widgets.section import Section
        from widgets.content import ContentType
        from widgets.elementeditor import ElementEditor, Mode

        self.section = section
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)
        self.setBGColor()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(5)
        self.edit_button = FlatButton("./images/edit_normal.png", "./images/edit_hover.png")
        self.copyButton = FlatButton("./images/copy_normal.png", "./images/copy_hover.png")
        self.closeButton = FlatButton("./images/trash_normal.png", "./images/trash_hover.png")
        self.edit_button.setToolTip("Edit Section")
        self.closeButton.setToolTip("Delete Section")
        self.copyButton.setToolTip("Copy Section")
        vbox.addWidget(self.edit_button)
        vbox.addWidget(self.copyButton)
        vbox.addWidget(self.closeButton)

        vboxRight = QVBoxLayout()
        vboxRight.setAlignment(Qt.AlignLeft)
        layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        layout.addLayout(vbox)
        addRow = HyperLink("(+) Add Row")
        vboxRight.addLayout(self.layout)

        if self.section.fullwidth:
            ee = ElementEditor(section.items[0])
            # connect(ee, SIGNAL(elementEnabled()), this, SLOT(addElement()))
            # connect(ee, SIGNAL(elementDragged()), this, SLOT(addElement()))
            # connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)))

            self.layout.addWidget(ee, 0, Qt.AlignTop)
        else:
            vboxRight.addWidget(addRow)
        layout.addLayout(vboxRight)
        self.setLayout(layout)

        # connect(addRow, SIGNAL(clicked()), this, SLOT(addRow()))
        # connect(self.closeButton, SIGNAL(clicked()), this, SLOT(close()))
        # connect(self.copyButton, SIGNAL(clicked()), this, SLOT(copy()))
        # connect(self.edit_button, SIGNAL(clicked()), this, SLOT(edit()))

        self.load()


    def setBGColor(self):
        pal = self.palette()
        if self.section.fullwidth:
            pal.setColor(QPalette.Background, QColor("#800080"))
        else:
            pal.setColor(QPalette.Background, QColor(self.palette().base().color().name()))
        self.setPalette(pal)

    def addElement(self, ee):
        # connect(ee, SIGNAL(elementEnabled()), this, SLOT(addElement()));
        # connect(ee, SIGNAL(elementDragged()), this, SLOT(addElement()));
        # connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)));
        self.layout.insertWidget(self.layout.count() - 1, ee, 0, Qt.AlignTop)

    def addRow(self, re):
        # connect(re, SIGNAL(rowEditorCopied(RowEditor*)), this, SLOT(copyRowEditor(RowEditor *)));
        self.layout.addWidget(re)

    def load(self):
        from widgets.elementeditor import ElementEditor, Mode
        from widgets.roweditor import RowEditor

        for item in self.section.items:
            if isinstance(item, Row):
                re = RowEditor(item)
                self.addRow(re)
            elif isinstance(item, Text):
                ee = ElementEditor(item)
                ee.setMode(Mode.ENABLED)
                self.addElement(ee)
