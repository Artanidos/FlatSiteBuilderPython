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
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal


class TableCellButtons(QWidget):
    deleteItem = pyqtSignal(object)
    editItem = pyqtSignal(object)

    def __init__(self):
        QWidget.__init__(self)
        self.delete = FlatButton("./images/trash_normal.png", "./images/trash_hover.png")
        self.edit = FlatButton("./images/edit_normal.png", "./images/edit_hover.png")
        self.edit.setToolTip("Edit Item")
        self.delete.setToolTip("Delete Item")
        self.item = None

        hbox = QHBoxLayout()
        hbox.addWidget(self.edit)
        hbox.addWidget(self.delete)
        self.setLayout(hbox)

        self.delete.clicked.connect(self.deleteItemClicked)
        self.edit.clicked.connect(self.editItemClicked)

    def setItem(self, item):
        self.item = item

    def deleteItemClicked(self):
        self.deleteItem.emit(self.item)

    def editItemClicked(self):
        self.editItem.emit(self.item)
