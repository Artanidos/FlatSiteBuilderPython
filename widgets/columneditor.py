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

        # connect(ee, SIGNAL(elementEnabled()), this, SLOT(addElement()));
        # connect(ee, SIGNAL(elementDragged()), this, SLOT(addElement()));
        # connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)));

    def addElement(self):
        ee = ElementEditor()
        self.layout.addWidget(ee, 0, Qt.AlignTop)

        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Add Element")

        ee.elementEnabled.connect(self.addElement)
        # connect(ee, SIGNAL(elementEnabled()), this, SLOT(addElement()));
        # connect(ee, SIGNAL(elementDragged()), this, SLOT(addElement()));
        # connect(ee, SIGNAL(elementCopied(ElementEditor*)), this, SLOT(copyElement(ElementEditor*)));

    def addElement(self, ee):
        self.layout.insertWidget(self.layout.count() - 1, ee, 0, Qt.AlignTop)
        ee.elementEnabled.connect(self.addElement)
        #connect(ee, SIGNAL(elementEnabled()), this, SLOT(addElement()));
        #connect(ee, SIGNAL(elementDragged()), this, SLOT(addElement()));
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
            self.layout.insertWidget(self.layout.count() - 1, ee, 0, Qt.AlignTop)
