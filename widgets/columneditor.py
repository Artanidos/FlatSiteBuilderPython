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

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QScrollArea, QUndoStack,
                             QVBoxLayout, QWidget)

from widgets.content import ContentType
from widgets.dropzone import DropZone
from widgets.elementeditor import ElementEditor, Mode
from widgets.flatbutton import FlatButton
from widgets.hyperlink import HyperLink
from widgets.section import Section


class ColumnEditor(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.column = None
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(self.palette().base().color().name()).lighter())
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.setAcceptDrops(True)

        ee = ElementEditor()
        self.layout.addWidget(ee, 0, Qt.AlignTop)
        ee.elementEnabled.connect(self.addElement)
        ee.elementDragged.connect(self.addElement)
        # connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)));

    def addElement(self):
        ee = ElementEditor()
        self.layout.addWidget(ee, 0, Qt.AlignTop)

        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Add Element")

        ee.elementEnabled.connect(self.addElement)
        ee.elementDragged.connect(self.addElement)
        
        # connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)));

    def addElementEditor(self, ee):
        self.layout.insertWidget(self.layout.count() - 1, ee, 0, Qt.AlignTop)
        ee.elementEnabled.connect(self.addElement)
        ee.elementDragged.connect(self.addElement)
        
        #connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)));
        
    def getContentEditor(self):
        from widgets.pageeditor import PageEditor
        from widgets.roweditor import RowEditor
        from widgets.sectioneditor import SectionEditor
        re = self.parentWidget()
        if isinstance(re, RowEditor):
            se = re.parentWidget()
            if isinstance(se, SectionEditor):
                pe = se.parentWidget()
                if isinstance(pe, PageEditor):
                    sa = pe.parentWidget()
                    if sa:
                        vp = sa.parentWidget()
                        if vp:
                            cee = vp.parentWidget()
                            if cee:
                                return cee

        return None

    def load(self, column):
        self.column = column
        for item in self.column.items:
            ee = ElementEditor()
            ee.setMode(Mode.ENABLED)
            ee.setContent(item)
            ee.elementEnabled.connect(self.addElement)
            ee.elementDragged.connect(self.addElement)
        
            #connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)));
            self.layout.insertWidget(self.layout.count() - 1, ee, 0, Qt.AlignTop)

    def dragEnterEvent(self, event):
        myData = event.mimeData()
        if myData:
            ee = myData.getData()
            if isinstance(ee, ElementEditor):
                for  i in range(self.layout.count()):
                    editor = self.layout.itemAt(i).widget()
                    if isinstance(editor, ElementEditor) and editor.mode == Mode.EMPTY:
                        editor.setMode(Mode.DROPZONE)
                        break
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        for i in range(self.layout.count()):
            editor = self.layout.itemAt(i).widget()
            if isinstance(editor, ElementEditor) and editor.mode == Mode.DROPZONE:
                # put editor to the end of the list
                editor.setMode(Mode.EMPTY)
                self.layout.removeWidget(editor)
                self.layout.addWidget(editor)
                break
        event.accept()

    def dragMoveEvent(self, event):
        myData = event.mimeData()
        if myData:
            ee = myData.getData()
            if isinstance(ee, ElementEditor):
                row = event.pos().y() / 50 #+ self.layout.margin())
                for i in range(self.layout.count()):
                    editor = self.layout.itemAt(i).widget()
                    if isinstance(editor, ElementEditor) and editor.mode == Mode.DROPZONE:
                        if i != row:
                            # put dropzone under mouse pointer
                            self.layout.insertWidget(row, editor)
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
            ee = myData.getData()
            if isinstance(ee, ElementEditor):
                for i in range(self.layout.count()):
                    dz = self.layout.itemAt(i).widget()
                    if isinstance(dz, ElementEditor) and dz.mode == Mode.DROPZONE:
                        # remove widget if it belongs to this layout
                        self.layout.removeWidget(ee)

                        # replace dropzone with dragged element
                        self.layout.replaceWidget(dz, ee)
                        new_pos = i
                        # and put dropzone to the end of the list
                        dz.setMode(Mode.EMPTY)
                        self.layout.removeWidget(dz)
                        self.layout.addWidget(dz)
                        break
                ee.dropped()
                ee.show()
                ee.elementEnabled.disconnect()
                ee.elementDragged.disconnect()
                # ee.copied.disconnect(self.copyElement)
                ce = self.getContentEditor()
                if ce:
                    myData.source_list.remove(ee.content)
                    self.column.insertElement(ee.content, new_pos)
                    ce.editChanged("Move Element")
                ee.elementEnabled.connect(self.addElement)
                ee.elementDragged.connect(self.addElement)
                # ee.elementCopied.connectself.copyElement)
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def removeElement(self, content):
        self.column._items.remove(content)
