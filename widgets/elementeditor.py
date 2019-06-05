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
from widgets.hyperlink import HyperLink
from widgets.section import Section
from widgets.content import ContentType
from widgets.text import Text
from widgets.plugins import Plugins
from widgets.moduldialog import ModulDialog
from PyQt5.QtWidgets import QUndoStack, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from enum import Enum
import resources

class Mode(Enum):
    EMPTY = 1
    ENABLED = 2
    DROPZONE = 3


class ElementEditor(QWidget):
    elementCopied = pyqtSignal(object)
    elementEnabled = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.content = None
        self.type = ""
        self.setAutoFillBackground(True)
        self.setMinimumWidth(120)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.zoom = False

        self.mode = Mode.EMPTY
        self.normalColor = QColor(self.palette().base().color().name()).lighter().name()
        self.enabledColor = self.palette().base().color().name()
        self.dropColor = QColor(self.palette().base().color().name()).lighter().lighter().name()
        self.setColor(self.normalColor)
        self.link = HyperLink("(+) Insert Module")

        self.editButton = FlatButton(":/images/edit_normal.png", ":/images/edit_hover.png")
        self.copyButton = FlatButton(":/images/copy_normal.png", ":/images/copy_hover.png")
        self.deleteButton = FlatButton(":/images/trash_normal.png", ":/images/trash_hover.png")
        self.editButton.setVisible(False)
        self.copyButton.setVisible(False)
        self.deleteButton.setVisible(False)
        self.editButton.setToolTip("Edit Element")
        self.deleteButton.setToolTip("Delete Element")
        self.copyButton.setToolTip("Copy Element")
        self.text = QLabel("Text")
        self.text.setVisible(False)
        layout= QHBoxLayout()
        layout.addWidget(self.link, 0, Qt.AlignCenter)
        layout.addWidget(self.editButton)
        layout.addWidget(self.copyButton)
        layout.addWidget(self.text, 1, Qt.AlignCenter)
        layout.addWidget(self.deleteButton)
        self.setLayout(layout)

        self.editButton.clicked.connect(self.edit)
        self.deleteButton.clicked.connect(self.delete)
        self.copyButton.clicked.connect(self.copy)
        self.link.clicked.connect(self.enable)

    def enable(self):
        dlg = ModulDialog()
        dlg.exec()

        if not dlg.result:
            return

        editor = Plugins.element_plugins[dlg.result]
        self.text.setText(editor.display_name)
        self.content = editor.getDefaultContent()
        self.type = editor.class_name

        self.setMode(Mode.ENABLED)
        self.elementEnabled.emit()
        self.edit()
        
    def copy(self):
        self.elementCopied.emit(self)

    def delete(self):
        self.parentWidget().layout.removeWidget(self)

        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Delete Element")

    def edit(self):
        ce = self.getContentEditor()
        if ce:
            ce.elementEdit(self)

    def setColor(self, name):
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(name))
        self.setPalette(pal)

    def load(self, content):
        self.content = content

    def setMode(self, mode):
        self.mode = mode
        if mode == Mode.EMPTY:
            self.link.setVisible(True)
            self.editButton.setVisible(False)
            self.copyButton.setVisible(False)
            self.deleteButton.setVisible(False)
            self.text.setVisible(False)
            self.setColor(self.normalColor)
        elif mode == Mode.ENABLED:
            self.link.setVisible(False)
            self.editButton.setVisible(True)
            self.copyButton.setVisible(True)
            self.deleteButton.setVisible(True)
            self.text.setVisible(True)
            self.setColor(self.enabledColor)
        elif mode == Mode.DROPZONE:
            self.link.setVisible(False)
            self.editButton.setVisible(False)
            self.copyButton.setVisible(False)
            self.deleteButton.setVisible(False)
            self.text.setVisible(True)
            self.text.setText("Drop Here")
            self.setColor(self.dropColor)
        
    def getContentEditor(self):
        se = self.getSectionEditor()
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

    def getSectionEditor(self):
        from widgets.sectioneditor import SectionEditor
        from widgets.columneditor import ColumnEditor
        se = self.parentWidget()
        if isinstance(se, SectionEditor):
            return se
        elif isinstance(se, ColumnEditor):
            re = se.parentWidget()
            if re:
                se = re.parentWidget()
                if se:
                    return se
        return None

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content
        if content.adminlabel:
            self.text.setText(content.adminlabel)
        else:
            self.text.setText("Text")
