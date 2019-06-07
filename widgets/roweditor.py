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
from PyQt5.QtGui import QColor, QPalette, QPixmap, QDrag
from PyQt5.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QScrollArea, QUndoStack,
                             QVBoxLayout, QWidget)
                            
from widgets.columnsdialog import ColumnsDialog
from widgets.column import Column
from widgets.columneditor import ColumnEditor
from widgets.widgetmimedata import WidgetMimeData
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
        self.editButton.setMaximumWidth(24)
        self.copyButton.setMaximumWidth(24)
        self.deleteButton.setMaximumWidth(24)
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
        self.layout.addWidget(self.addColumns, 0, 0, 1, 1, Qt.AlignCenter)
        self.layout.setColumnStretch(0, 1)
        
        layout.addItem(vbox)
        layout.addLayout(self.layout)
        self.setLayout(layout)

        self.deleteButton.clicked.connect(self.delete)
        self.copyButton.clicked.connect(self.copy)
        self.editButton.clicked.connect(self.edit)
        self.addColumns.clicked.connect(self.insertColumns)

    def edit(self):
        ce = self.getContentEditor()
        if ce:
            ce.rowEdit(self)

    def copy(self):
        self.rowEditorCopied.emit(self)

    def delete(self):
        se = self.parentWidget()
        if se:
            se.removeRowEditor(self)
            se.section._items.remove(self.row)
        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Delete Row")  

    def addColumn(self, ce, column):
        if self.addColumns.isVisible():
            self.addColumns.setVisible(False)
            self.layout.removeWidget(self.addColumns)

        self.layout.addWidget(ce, 0, column)
        self.layout.setColumnStretch(column, ce.column.span)

    def load(self, row):
        from widgets.columneditor import ColumnEditor
        
        self.row = row
        i = 0
        for column in self.row.columns:
            ce = ColumnEditor()
            ce.load(column)
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

    def insertColumns(self):
        dlg = ColumnsDialog()
        dlg.exec()
        if dlg.result == 0:
            return

        if dlg.result == 1:  # 1/1
            col = Column()
            col.span = 12
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 0)

        elif dlg.result == 2:  # 1/2 - 1/2
            for i in range(2):
                col = Column()
                col.span = 6
                self.row._columns.append(col)
                ce = ColumnEditor()
                ce.load(col)
                self.addColumn(ce, i)

        elif dlg.result == 3:   # 1/3 - 1/3 - 1/3
            for i in range(3):
                col = Column()
                col.span = 4
                self.row._columns.append(col)
                ce = ColumnEditor()
                ce.load(col)
                self.addColumn(ce, i)

        elif dlg.result == 4:   # 1/4 - 1/4 - 1/4 - 1/4
            for i in range(4):
                col = Column()
                col.span = 3
                self.row._columns.append(col)
                ce = ColumnEditor()
                ce.load(col)
                self.addColumn(ce, i)

        elif dlg.result == 5:  # 2/3 - 1/3
            col = Column()
            col.span = 8
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 0)
            col = Column()
            col.span = 4
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 1)

        elif dlg.result == 6:  # 1/3 - 2/3
            col = Column()
            col.span = 4
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 0)
            col = Column()
            col.span = 8
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 1)

        elif dlg.result == 7:  # 1/4 - 3/4
            col = Column()
            col.span = 2
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 0)
            col = Column()
            col.span = 9
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 1)

        elif dlg.result == 8:  # 3/4 - 1/4
            col = Column()
            col.span = 9
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 0)
            col = Column()
            col.span = 3
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 1)

        elif dlg.result == 9:  # 1/2 - 1/4 - 1/4
            col = Column()
            col.span = 6
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 0)
            col = Column()
            col.span = 3
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 1)
            col = Column()
            col.span = 3
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 2)

        elif dlg.result == 10:  # 1/4 - 1/4 - 1/2
            col = Column()
            col.span = 3
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 0)
            col = Column()
            col.span = 3
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 1)
            col = Column()
            col.span = 6
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 2)
        
        elif dlg.result == 11:  # 1/4 - 1/2 - 1/4
            col = Column()
            col.span = 3
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 0)
            col = Column()
            col.span = 6
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 1)
            col = Column()
            col.span = 3
            self.row._columns.append(col)
            ce = ColumnEditor()
            ce.load(col)
            self.addColumn(ce, 2)
            
        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Add Columns")

    def enableColumnAcceptDrop(self, mode):
        for i in range(self.layout.count()):
            ce = self.layout.itemAt(i).widget()
            if ce:
                ce.setAcceptDrops(mode)
        
    def mousePressEvent(self, event):
        mimeData = WidgetMimeData()
        mimeData.setSize(self.size().width(), self.size().height())
        mimeData.setData(self)

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos())
        drag.setPixmap(pixmap)

        se = self.parentWidget()
        se.removeRowEditor(self)
        pe = se.parentWidget()
        pe.enableColumnAcceptDrop(False)
        self.hide()

        if drag.exec(Qt.MoveAction) == Qt.IgnoreAction:
            se.addRowEditor(self)
            self.show()
        
        pe.enableColumnAcceptDrop(True)
