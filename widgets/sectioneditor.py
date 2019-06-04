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
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QPalette, QColor
from widgets.row import Row
from widgets.text import Text
from widgets.roweditor import RowEditor
import resources

class SectionEditor(QWidget):
    sectionEditorCopied = pyqtSignal(object)

    def __init__(self, fullwidth):
        QWidget.__init__(self)
        from widgets.hyperlink import HyperLink
        from widgets.flatbutton import FlatButton
        from widgets.section import Section
        from widgets.content import ContentType
        from widgets.elementeditor import ElementEditor, Mode

        self.fullwidth = fullwidth
        self.section = None
        self.id = None
        self.cssclass = None
        self.style = None
        self.attributes = None
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)
        self.setBGColor()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(5)
        self.edit_button = FlatButton(":/images/edit_normal.png", ":/images/edit_hover.png")
        self.copyButton = FlatButton(":/images/copy_normal.png", ":/images/copy_hover.png")
        self.deleteButton = FlatButton(":/images/trash_normal.png", ":/images/trash_hover.png")
        self.edit_button.setToolTip("Edit Section")
        self.deleteButton.setToolTip("Delete Section")
        self.copyButton.setToolTip("Copy Section")
        vbox.addWidget(self.edit_button)
        vbox.addWidget(self.copyButton)
        vbox.addWidget(self.deleteButton)

        vboxRight = QVBoxLayout()
        vboxRight.setAlignment(Qt.AlignLeft)
        layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        layout.addLayout(vbox)
        addRow = HyperLink("(+) Add Row")
        vboxRight.addLayout(self.layout)

        if self.fullwidth:
            ee = ElementEditor()
            # connect(ee, SIGNAL(elementEnabled()), this, SLOT(addElement()))
            # connect(ee, SIGNAL(elementDragged()), this, SLOT(addElement()))
            # connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)))

            self.layout.addWidget(ee, 0, Qt.AlignTop)
        else:
            vboxRight.addWidget(addRow)
        layout.addLayout(vboxRight)
        self.setLayout(layout)

        self.deleteButton.clicked.connect(self.delete)
        self.copyButton.clicked.connect(self.copy)
        addRow.clicked.connect(self.addRow)
        self.edit_button.clicked.connect(self.edit)

    def edit(self):
        ce = self.getContentEditor()
        if ce:
            ce.sectionEdit(self)

    def addRow(self):
        row = Row()
        self.section._items.append(row)
        re = RowEditor()
        re.load(row)
        self.addRowEditor(re)
        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Add Row")

    def addRowEditor(self, re):
        re.rowEditorCopied.connect(self.copyRowEditor)
        self.layout.addWidget(re)

    def copyRowEditor(self, re):
        ren = RowEditor()
        row = re.row.clone()
        ren.load(row)
        self.section._items.append(row)
        self.addRowEditor(ren)
        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Copy Row")

    def copy(self):
        self.sectionEditorCopied.emit(self)

    def delete(self):
        pe = self.parentWidget()
        if pe:
            pe.removeSection(self)

    def setBGColor(self):
        pal = self.palette()
        if self.fullwidth:
            pal.setColor(QPalette.Background, QColor("#800080"))
        else:
            pal.setColor(QPalette.Background, QColor(self.palette().base().color().name()))
        self.setPalette(pal)

    def addElement(self, ee):
        # connect(ee, SIGNAL(elementEnabled()), this, SLOT(addElement()));
        # connect(ee, SIGNAL(elementDragged()), this, SLOT(addElement()));
        # connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)));
        self.layout.insertWidget(self.layout.count() - 1, ee, 0, Qt.AlignTop)

    def setSection(self, section):
        self.section = section

    def removeRowEditor(self, re):
        re.setVisible(False)
        self.section._items.remove(re.row)
        self.layout.removeWidget(re)

    def load(self, section):
        from widgets.elementeditor import ElementEditor, Mode
        from widgets.roweditor import RowEditor

        self.section = section
        for item in self.section.items:
            if isinstance(item, Row):
                re = RowEditor()
                re.load(item)
                self.addRowEditor(re)
            elif isinstance(item, Text):
                ee = ElementEditor()
                ee.load(item)
                ee.setMode(Mode.ENABLED)
                self.addElement(ee)

    def getContentEditor(self):
        pe = self.parentWidget()
        if pe:
            sa = pe.parentWidget()
            if sa:
                vp = sa.parentWidget()
                if vp:
                    cee = vp.parentWidget()
                    if cee:
                        return cee

        return None
