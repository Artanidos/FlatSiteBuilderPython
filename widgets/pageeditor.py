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
from PyQt5.QtWidgets import QUndoStack, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl


class PageEditor(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignLeft)
        hbox.setSpacing(10)
        addSection = HyperLink("(+) Add Section")
        addFullSection = HyperLink("(+) Add Full Width Section")
        self.layout = QVBoxLayout()
        hbox.addWidget(addSection)
        hbox.addWidget(addFullSection)
        self.layout.addLayout(hbox)
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.setAcceptDrops(True)
        # connect(addSection, SIGNAL(clicked()), this, SLOT(addSection()))
        # connect(addFullSection, SIGNAL(clicked()), this, SLOT(addFullSection()))

    def addSection(self, se):
        #connect(se, SIGNAL(sectionEditorCopied(SectionEditor*)), this, SLOT(copySection(SectionEditor*)));
        self.layout.insertWidget(self.layout.count() - 2, se)

    def sections(self):
        list = []
        for i in range(self.layout.count()):
            se = self.layout.itemAt(i).widget()
            if isinstance(se, SectionEditor):
                list.append(se)
        return list
