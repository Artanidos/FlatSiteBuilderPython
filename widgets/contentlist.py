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

import datetime
from widgets.content import ContentType
from widgets.flatbutton import FlatButton
from widgets.tablecellbuttons import TableCellButtons
from PyQt5.QtWidgets import QWidget, QUndoStack, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QTableWidget, QAbstractItemView, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt, QFileInfo
import resources

class ContentList(QWidget):
    editContent = pyqtSignal(object)

    def __init__(self, site, type):
        QWidget.__init__(self)
        self.site = site
        self.addedContentName = ""
        self.type = type
        self.undoStack = QUndoStack()
        vbox = QVBoxLayout()
        layout = QGridLayout()
        titleLabel = QLabel()
        button = QPushButton()
        if self.type == ContentType.PAGE:
            button.setText("Add Page")
        else:
            button.setText("Add Post")
        button.setMaximumWidth(120)
        if self.type == ContentType.PAGE:
            titleLabel.setText("Pages")
        else:
            titleLabel.setText("Posts")
        fnt = titleLabel.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        titleLabel.setFont(fnt)

        self.undo = FlatButton(":/images/undo_normal.png", ":/images/undo_hover.png", "", ":/images/undo_disabled.png")
        self.redo = FlatButton(":/images/redo_normal.png", ":/images/redo_hover.png", "", ":/images/redo_disabled.png")
        self.undo.setToolTip("Undo")
        self.redo.setToolTip("Redo")
        self.undo.setEnabled(False)
        self.redo.setEnabled(False)
        hbox = QHBoxLayout()
        hbox.addStretch(0)
        hbox.addWidget(self.undo)
        hbox.addWidget(self.redo)

        self.list = QTableWidget(0, 6, self)
        self.list.verticalHeader().hide()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.list.setToolTip("Double click to edit item")
        labels = ["", "Name", "Source", "Layout", "Author", "Date"]
        self.list.setHorizontalHeaderLabels(labels)

        self.reload()

        layout.addWidget(titleLabel, 0, 0)
        layout.addLayout(hbox, 0, 2)
        layout.addWidget(button, 1, 0)
        layout.addWidget(self.list, 2, 0, 1, 3)
        vbox.addLayout(layout)
        self.setLayout(vbox)

        button.clicked.connect(self.buttonClicked)
        self.list.cellDoubleClicked.connect(self.tableDoubleClicked)
        self.redo.clicked.connect(self.doredo)
        self.undo.clicked.connect(self.doundo)
        self.undoStack.canUndoChanged.connect(self.canUndoChanged)
        self.undoStack.canRedoChanged.connect(self.canRedoChanged)
        self.undoStack.redoTextChanged.connect(self.redoTextChanged)

    def reload(self):
        self.list.setRowCount(0)
        row = -1

        contentToEdit = None
        if self.type == ContentType.PAGE:
            self.site.loadPages()
            for i in range(len(self.site.pages)):
                content = self.site.pages[i]
                if content.source == self.addedContentName:
                    contentToEdit = content
                    row = self.list.rowCount()
                self.addListItem(content)
        else:
            self.site.loadPosts()
            for i in range(0, len(self.site.posts)):
                content = self.site.posts[i]
                if content.source == self.addedContentName:
                    contentToEdit = content
                    row = self.list.rowCount()
                self.addListItem(content)

        if contentToEdit:
            self.addedContentName = ""
            self.list.selectRow(row)
            self.editContent(contentToEdit)

    def addListItem(self, content):
        rows = self.list.rowCount()
        self.list.setRowCount(rows + 1)
        tcb = TableCellButtons()
        tcb.setItem(content)
        #connect(tcb, SIGNAL(deleteItem(QObject*)), self, SLOT(deleteContent(QObject*)))
        #connect(tcb, SIGNAL(editItem(QObject*)), self, SLOT(editContent(QObject*)))
        self.list.setCellWidget(rows, 0, tcb)
        self.list.setRowHeight(rows, tcb.sizeHint().height())
        titleItem = QTableWidgetItem(content.title)
        titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
        titleItem.setData(Qt.UserRole, content)
        self.list.setItem(rows, 1, titleItem)

        sourceItem = QTableWidgetItem(content.source)
        sourceItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
        self.list.setItem(rows, 2, sourceItem)

        layoutItem = QTableWidgetItem(content.layout)
        layoutItem.setFlags(layoutItem.flags() ^ Qt.ItemIsEditable)
        self.list.setItem(rows, 3, layoutItem)

        authorItem = QTableWidgetItem(content.author)
        authorItem.setFlags(authorItem.flags() ^ Qt.ItemIsEditable)
        self.list.setItem(rows, 4, authorItem)
        dateItem = QTableWidgetItem(content.date.toString("dd.MM.yyyy"))
        dateItem.setFlags(dateItem.flags() ^ Qt.ItemIsEditable)
        self.list.setItem(rows, 5, dateItem)

    def canUndoChanged(self, can):
        self.undo.setEnabled(can)

    def canRedoChanged(self, can):
        self.redo.setEnabled(can)

    def undoTextChanged(self, text):
        self.undo.setToolTip("Undo " + text)

    def redoTextChanged(self, text):
        self.redo.setToolTip("Redo " + text)

    def doundo(self):
        self.undoStack.undo()

    def doredo(self):
        self.undoStack.redo()

    def buttonClicked(self):
        pass
        #self.addedContentName = self.site.createTemporaryContent(self.type)
        #info = QFileInfo(self.addedContentName)
        #self.addedContentName = info.fileName()
        #reload()

    def tableDoubleClicked(self, r, i):
        item = self.list.item(r, 1)
        self.undoStack.clear()
        self.editContent.emit(item)
