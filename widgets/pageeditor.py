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

from widgets.hyperlink import HyperLink
from widgets.flatbutton import FlatButton
from widgets.hyperlink import HyperLink
from widgets.section import Section
from widgets.sectioneditor import SectionEditor
from widgets.content import ContentType
from widgets.columneditor import ColumnEditor
from widgets.dropzone import DropZone
from PyQt5.QtWidgets import QUndoStack, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl


class PageEditor(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.placeholder = QWidget()
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignLeft)
        hbox.setSpacing(10)
        addSection = HyperLink("(+) Add Section")
        addFullSection = HyperLink("(+) Add Full Width Section")
        l = QVBoxLayout()
        self.layout = QVBoxLayout()
        l.addLayout(self.layout)
        l.addWidget(self.placeholder)
        hbox.addWidget(addSection)
        hbox.addWidget(addFullSection)
        self.layout.addLayout(hbox)
        self.layout.addStretch()
        self.setLayout(l)
        self.setAcceptDrops(True)
        addSection.clicked.connect(self.addNormalSection)
        addFullSection.clicked.connect(self.addFullSection)

    def enableColumnAcceptDrop(self, mode):
        for i in range(self.layout.count()):
            ce = self.layout.itemAt(i).widget()
            if isinstance(ce, ColumnEditor):
                ce.enableColumnAcceptDrop(mode)

    def enableSectionAcceptDrop(self, mode):
       for i in range(self.layout.count()):
            se = self.layout.itemAt(i).widget()
            if isinstance(se, SectionEditor):
                se.enableColumnAcceptDrop(mode)

    def addFullSection(self):
        se = SectionEditor(True)
        self.addSection(se)
        ce = self.getContentEditor()
        if ce:
            sec = Section()
            sec.fullwidth = True
            se.load(sec)
            ce.content.appendSection(sec)
            ce.editChanged("Add Section")

    def addNormalSection(self):
        se = SectionEditor(False)
        self.addSection(se)
        ce = self.getContentEditor()
        if ce:
            sec = Section()
            sec.fullwidth = False
            se.load(sec)
            ce.content.appendSection(sec)
            ce.editChanged("Add Section")

    def addSection(self, se):
        se.sectionEditorCopied.connect(self.copySection)
        self.layout.insertWidget(self.layout.count() - 2, se)

    def sections(self):
        list = []
        for i in range(self.layout.count()):
            se = self.layout.itemAt(i).widget()
            if isinstance(se, SectionEditor):
                list.append(se)
        return list

    def removeSectionEditor(self, se):
        self.layout.removeWidget(se)

    def removeSection(self, se):
        sec = se.section
        se.hide()
        self.layout.removeWidget(se)
        del se
        ce = self.getContentEditor()
        if ce:
            ce.content.removeSection(sec)
            ce.editChanged("Delete Section")

    def copySection(self, se):
        see = SectionEditor(se.fullwidth)
        self.addSection(see)
        ce = self.getContentEditor()
        if ce:
            sec = se.section.clone()
            see.load(sec)
            ce.content.appendSection(sec)
            ce.editChanged("Copy Section")

    def getContentEditor(self):
        sa = self.parentWidget()
        if sa:
            vp = sa.parentWidget()
            if vp:
                cee = vp.parentWidget()
                if cee:
                    return cee
        return None

    def dragEnterEvent(self, event):
        myData = event.mimeData()
        if myData:
            se = myData.getData()
            if isinstance(se, SectionEditor):
                # insert a dropzone at the end
                self.layout.addWidget(DropZone(myData.width, myData.height))
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # remove dropzones
        for i in  range(self.layout.count()):
            dz = self.layout.itemAt(i).widget()
            if isinstance(dz, DropZone):
                dz.hide()
                self.layout.removeWidget(dz)
                del dz
                break
        event.accept()

    def dragMoveEvent(self, event):
        myData = event.mimeData()
        if myData:
            se = myData.getData()
            if isinstance(se, SectionEditor):
                height = 0
                row = 0

                # evaluate position for the dropzone to be placed
                for i in range(self.layout.count()):
                    editor = self.layout.itemAt(i).widget()
                    if isinstance(editor, SectionEditor):
                        if event.pos().y() > height and event.pos().y() < height + editor.height():
                            break
                        height += editor.height();
                        row = row + 1

                # find dropzone and replace it to new location
                for i in range(self.layout.count()):
                    dz = self.layout.itemAt(i).widget()
                    if isinstance(dz, DropZone):
                        if i != row:
                            self.layout.insertWidget(row, dz)
                        break
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        myData = event.mimeData()
        if myData:
            se = myData.getData()
            if isinstance(se, SectionEditor):
                # place the dragged SectionEditor to the place where DropZone is now
                for i in range(self.layout.count()):
                    dz = self.layout.itemAt(i).widget()
                    if isinstance(dz, DropZone):
                        dz.hide()
                        self.layout.replaceWidget(dz, se)
                        new_pos = i
                        se.show()
                        del dz
                        break
                ce = self.getContentEditor()
                if ce:
                    ce.content.changeSectionPos(se.section, new_pos)
                    ce.editChanged("Move Section")
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

