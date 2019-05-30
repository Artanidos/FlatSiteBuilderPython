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

from PyQt5.QtCore import QRect, Qt, QUrl
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QScrollArea, QUndoStack,
                             QVBoxLayout, QWidget)


class RowEditor(QWidget):

    def __init__(self, row ,clone = False):
        QWidget.__init__(self)

        from widgets.content import ContentType
        from widgets.flatbutton import FlatButton
        from widgets.hyperlink import HyperLink
        from widgets.section import Section

        self.row = row
        self.editButton = FlatButton("./images/edit_normal.png", "./images/edit_hover.png")
        self.copyButton = FlatButton("./images/copy_normal.png", "./images/copy_hover.png")
        self.closeButton = FlatButton("./images/trash_normal.png", "./images/trash_hover.png")
        self.addColumns = HyperLink("(+) Add Columns")
        self.editButton.setToolTip("Edit Row")
        self.closeButton.setToolTip("Delete Row")
        self.copyButton.setToolTip("Copy Row")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(5)
        vbox.addWidget(self.editButton)
        vbox.addWidget(self.copyButton)
        vbox.addWidget(self.closeButton, 0, Qt.AlignBottom)
        layout = QHBoxLayout()

        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(self.palette().alternateBase().color()))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        self.highlightedRect = QRect()
        self.layout = QGridLayout()
        if not clone:
            s1 = QHBoxLayout()
            s1.addStretch()
            s2 = QHBoxLayout()
            s2.addStretch()
            self.layout.addLayout(s1, 0, 0)
            self.layout.addWidget(self.addColumns, 0, 1, 1, 1, Qt.AlignCenter)
            self.layout.addLayout(s2, 0, 2)
        
        layout.addItem(vbox)
        layout.addLayout(self.layout)
        self.setLayout(layout)

        # connect(self.closeButton, SIGNAL(clicked()), this, SLOT(close()))
        # connect(self.copyButton, SIGNAL(clicked()), this, SLOT(copy()))
        # connect(self.editButton, SIGNAL(clicked()), this, SLOT(edit()))
        # connect(self.addColumns, SIGNAL(clicked()), this, SLOT(addColumns()))

        self.load()

    def addColumn(self, ce, column):
        if self.addColumns:
            self.layout.removeItem(self.layout.itemAt(2))
            self.layout.removeItem(self.layout.itemAt(0))
            self.layout.removeWidget(self.addColumns)
            del self.addColumns
            self.addColumns = None

        self.layout.addWidget(ce, 0, column)
        self.layout.setColumnStretch(column, ce.span())

    def clone(self):
        nre = RowEditor(True)
        # nre->setCssClass(m_cssclass);
        for i in range(self.layout.count()):
            ce = self.layout.itemAt(i).widget()
            if isinstance(ce, Column):
                nre.addColumn(ce.clone(), i)
        return nre

    def load(self):
        from widgets.columneditor import ColumnEditor
        
        i = 0
        for column in self.row.columns:
            ce = ColumnEditor(column)
            self.addColumn(ce, i)
            i = i + 1
