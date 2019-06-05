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

from widgets.interfaces import ElementEditorInterface
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton, QLabel
from widgets.imageselector import ImageSelector
from widgets.flatbutton import FlatButton
from widgets.item import Item


class ImageEditor(ElementEditorInterface):
    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.class_name = "ImageEditor"
        self.display_name = "Image"
        self.tag_name = "Image"
        self.version = "2.0.0"
        self.icon = QImage("./plugins/imageeditor.png")

        self.changed = False
        self.setAutoFillBackground(True)

        grid = QGridLayout()

        self.source = QLineEdit()
        self.alt = QLineEdit()
        self.alt.setMaximumWidth(200)
        self.title = QLineEdit()
        self.title.setMaximumWidth(200)
        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)
        seek = QPushButton("...")
        seek.setMaximumWidth(50)
        titleLabel = QLabel("Image Module Plugin")
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)
        self.image = ImageSelector()
        self.image.setImage(QImage(":/images/image_placeholder.png"))

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip("Close Editor")

        grid.addWidget(titleLabel, 0, 0)
        grid.addWidget(close, 0, 3, 1, 1, Qt.AlignRight)
        grid.addWidget(QLabel("Path"), 1, 0)
        grid.addWidget(self.source, 2, 0, 1, 3)
        grid.addWidget(seek, 2, 3)
        grid.addWidget(self.image, 3, 0, 1, 4)
        grid.setRowStretch(3, 1)
        grid.addWidget(QLabel("Alt"), 6, 0)
        grid.addWidget(self.alt, 7, 0)
        grid.addWidget(QLabel("Title"), 8, 0)
        grid.addWidget(self.title, 9, 0)
        grid.addWidget(QLabel("Admin Label"), 10, 0)
        grid.addWidget(self.adminlabel, 11, 0)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        # connect(self.source, SIGNAL(textChanged(QString)), this, SLOT(contentChanged()))
        # connect(self.alt, SIGNAL(textChanged(QString)), this, SLOT(contentChanged()))
        # connect(self.title, SIGNAL(textChanged(QString)), this, SLOT(contentChanged()))
        # connect(self.adminlabel, SIGNAL(textChanged(QString)), this, SLOT(contentChanged()))
        # connect(self.image, SIGNAL(clicked()), this, SLOT(seek()))
        # connect(seek, SIGNAL(clicked()), this, SLOT(seek()))
        # connect(close, SIGNAL(clicked()), this, SLOT(closeEditor()))

    def closeEditor(self):
        if self.changed:
            self.content.src = self.source.text()
            self.content.alt = self.alt.text()
            self.content.title = self.title.text()
            self.content.adminlabel = self.adminlabel.text()
            #foreach(QString attName, m_attributes.keys())
            #{
            #    stream.writeAttribute(attName, m_attributes.value(attName));
            #}
        self.close.emit()

    def getHtml(self):
        return "<img src=\"\">\n"

    def getDefaultContent(self):
        return Image()

    def setContent(self, content):
        self.content = content
        self.changed = False


class Image(Item):
    def __init__(self, parent = None):
        super().__init__(parent)