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

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, QDate, QPoint, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
import resources
from widgets.flatbutton import FlatButton
from widgets.plugins import Plugins


class ModulDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)

        self.result = ""
        self.setWindowTitle("Insert Module")
        self.grid = QGridLayout()
        textButton = self.createButton(QImage(":/images/text.png"), "Text")
        self.grid.addWidget(textButton, 0, 0)

        cancelButton = QPushButton("Cancel")
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(cancelButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.grid)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)
        self.setLayout(mainLayout)

        row = 0
        col = 1

        for name in Plugins.elementPluginNames():
            plugin = Plugins.element_plugins[name]
            btn = self.createButton(plugin.icon, plugin.display_name)
            btn.returncode = name
            self.grid.addWidget(btn, row, col)
            col = col + 1
            btn.clickedWithReturn.connect(self.close2)
            if col == 4:
                row = row + 1
                col = 0
            
        cancelButton.clicked.connect(self.close)
        textButton.clicked.connect(self.close1)

    def close1(self):
        self.result = "TextEditor"
        self.close()

    def close2(self, result):
        self.result = result
        self.close()

    def createButton(self, icon, text):
        btn = FlatButton()
        pmNormal = QPixmap.fromImage(QImage(":/images/module_normal.png"))
        pmHover = QPixmap.fromImage(QImage(":/images/module_hover.png"))
        title = QLabel()
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor("#999999"))
        pal.setColor(QPalette.Foreground, QColor("#000000"))
        title.setPalette(pal)
        title.setText(text)
        title.setFixedWidth(90)
        title.render(pmNormal, QPoint(80, 40))
        title.render(pmHover, QPoint(80, 40))

        iconLabel = QLabel()
        iconLabel.setPixmap(QPixmap.fromImage(icon))
        iconLabel.render(pmNormal, QPoint(33, 33))
        iconLabel.render(pmHover, QPoint(33, 33))

        btn.setNormalPixmap(pmNormal)
        btn.setHoverPixmap(pmHover)
        return btn