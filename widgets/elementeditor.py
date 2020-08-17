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
from widgets.plugins import Plugins
from widgets.moduldialog import ModulDialog
from widgets.widgetmimedata import WidgetMimeData
from PyQt5.QtWidgets import QUndoStack, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QPixmap, QDrag
from enum import Enum
import resources

class Mode(Enum):
    EMPTY = 1
    ENABLED = 2
    DROPZONE = 3


class ElementEditor(QWidget):
    elementCopied = pyqtSignal(object)
    elementEnabled = pyqtSignal()
    elementDragged = pyqtSignal()

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
        from widgets.columneditor import ColumnEditor
        from widgets.sectioneditor import SectionEditor
        dlg = ModulDialog()
        dlg.exec()

        if not dlg.result:
            return
        editor = Plugins.element_plugins[dlg.result]
        self.content = editor.getDefaultContent()
        if isinstance(self.parentWidget(), ColumnEditor):
            self.parentWidget().column._items.append(self.content)
        elif isinstance(self.parentWidget(), SectionEditor):
            self.parentWidget().section._items.append(self.content)
        self.type = editor.tag_name
        self.text.setText(editor.tag_name)

        self.setMode(Mode.ENABLED)
        self.elementEnabled.emit()
        self.edit()
        
    def copy(self):
        self.elementCopied.emit(self)

    def delete(self):
        self.parentWidget().removeElement(self.content)
        self.parentWidget().layout.removeWidget(self)
        self.hide()
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
        print(content)
        self.type = content.tag_name
        if content.adminlabel:
            self.text.setText(content.adminlabel)
        else:
            self.text.setText(content.tag_name)

    def mousePressEvent(self, event):
        from widgets.columneditor import ColumnEditor
        from widgets.sectioneditor import SectionEditor
        if self.mode != Mode.ENABLED or event.button() != Qt.LeftButton:
            return

        if self.parentWidget().layout.count() == 1:
            self.elementDragged.emit()

        mimeData = WidgetMimeData()
        mimeData.setData(self)
        parent = self.parentWidget()
        if isinstance(parent, ColumnEditor):
            mimeData.source_list = parent.column._items
        elif isinstance(parent, SectionEditor):
            mimeData.source_list = parent.section._items

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos())
        drag.setPixmap(pixmap)
        self.hide()

        if drag.exec(Qt.MoveAction) == Qt.IgnoreAction:
            self.show()

    def dropped(self):
        #seems to be a bug that after dropping the item the bgcolor changes
        self.setColor(self.enabledColor)