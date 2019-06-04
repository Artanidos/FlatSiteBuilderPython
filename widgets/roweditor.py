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

from PyQt5.QtCore import QRect, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QScrollArea, QUndoStack,
                             QVBoxLayout, QWidget)
import resources

class RowEditor(QWidget):
    rowEditorCopied = pyqtSignal(object)

    def __init__(self):
        QWidget.__init__(self)

        from widgets.content import ContentType
        from widgets.flatbutton import FlatButton
        from widgets.hyperlink import HyperLink
        from widgets.section import Section

        self.editButton = FlatButton(":/images/edit_normal.png", ":/images/edit_hover.png")
        self.copyButton = FlatButton(":/images/copy_normal.png", ":/images/copy_hover.png")
        self.deleteButton = FlatButton(":/images/trash_normal.png", ":/images/trash_hover.png")
        self.addColumns = HyperLink("(+) Add Columns")
        self.editButton.setToolTip("Edit Row")
        self.deleteButton.setToolTip("Delete Row")
        self.copyButton.setToolTip("Copy Row")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(5)
        vbox.addWidget(self.editButton)
        vbox.addWidget(self.copyButton)
        vbox.addWidget(self.deleteButton, 0, Qt.AlignBottom)
        layout = QHBoxLayout()

        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(self.palette().alternateBase().color()))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        self.highlightedRect = QRect()
        self.layout = QGridLayout()
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

        self.deleteButton.clicked.connect(self.delete)
        self.copyButton.clicked.connect(self.copy)
        
        # connect(self.copyButton, SIGNAL(clicked()), this, SLOT(copy()))
        # connect(self.editButton, SIGNAL(clicked()), this, SLOT(edit()))
        # connect(self.addColumns, SIGNAL(clicked()), this, SLOT(addColumns()))

    def copy(self):
        self.rowEditorCopied.emit(self)

    def delete(self):
        se = self.parentWidget()
        if se:
            se.removeRowEditor(self)
        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Delete Row");  

    def addColumn(self, ce, column):
        if self.addColumns:
            self.layout.removeItem(self.layout.itemAt(2))
            self.layout.removeItem(self.layout.itemAt(0))
            self.layout.removeWidget(self.addColumns)
            del self.addColumns
            self.addColumns = None

        self.layout.addWidget(ce, 0, column)
        self.layout.setColumnStretch(column, ce.span())

    def load(self, row):
        from widgets.columneditor import ColumnEditor
        
        self.row = row
        i = 0
        for column in self.row.columns:
            ce = ColumnEditor(column)
            self.addColumn(ce, i)
            i = i + 1

    def getContentEditor(self):
        se = self.parentWidget()
        if se:
            pe = se.parentWidget()
            if pe:
                sa = pe.parentWidget()
                if sa:
                    vp = sa.parentWidget()
                    if vp:
                        cee = vp.parentWidget()
                        if cee:
                            return cee
        return None