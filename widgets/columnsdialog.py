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
import resources
from widgets.flatbutton import FlatButton

class ColumnsDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.result = 0
        self.setWindowTitle("Insert Columns")
        grid = QGridLayout()
        b1 = FlatButton(":/images/columns1.png", ":/images/columns1_hover.png")
        b2 = FlatButton(":/images/columns2.png", ":/images/columns2_hover.png")
        b3 = FlatButton(":/images/columns3.png", ":/images/columns3_hover.png")
        b4 = FlatButton(":/images/columns4.png", ":/images/columns4_hover.png")
        b5 = FlatButton(":/images/columns5.png", ":/images/columns5_hover.png")
        b6 = FlatButton(":/images/columns6.png", ":/images/columns6_hover.png")
        b7 = FlatButton(":/images/columns7.png", ":/images/columns7_hover.png")
        b8 = FlatButton(":/images/columns8.png", ":/images/columns8_hover.png")
        b9 = FlatButton(":/images/columns9.png", ":/images/columns9_hover.png")
        b10 = FlatButton(":/images/columns10.png", ":/images/columns10_hover.png")
        b11 = FlatButton(":/images/columns11.png", ":/images/columns11_hover.png")
        grid.addWidget(b1, 0, 0)
        grid.addWidget(b2, 0, 1)
        grid.addWidget(b3, 0, 2)
        grid.addWidget(b4, 1, 0)
        grid.addWidget(b5, 1, 1)
        grid.addWidget(b6, 1, 2)
        grid.addWidget(b7, 3, 0)
        grid.addWidget(b8, 3, 1)
        grid.addWidget(b9, 3, 2)
        grid.addWidget(b10, 4, 0)
        grid.addWidget(b11, 4, 1)

        closeButton = QPushButton("Close")

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(closeButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(grid)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)
        self.setLayout(mainLayout)

        closeButton.clicked.connect(self.close)
        b1.clicked.connect(self.close1)
        b2.clicked.connect(self.close2)
        b3.clicked.connect(self.close3)
        b4.clicked.connect(self.close4)
        b5.clicked.connect(self.close5)
        b6.clicked.connect(self.close6)
        b7.clicked.connect(self.close7)
        b8.clicked.connect(self.close8)
        b9.clicked.connect(self.close9)
        b10.clicked.connect(self.close10)
        b11.clicked.connect(self.close11)

    def close1(self):
        self.result = 1
        self.close()

    def close2(self):
        self.result = 2
        self.close()

    def close3(self):
        self.result = 3
        self.close()
    
    def close4(self):
        self.result = 4
        self.close()

    def close5(self):
        self.result = 5
        self.close()

    def close6(self):
        self.result = 6
        self.close()

    def close7(self):
        self.result = 7
        self.close()

    def close8(self):
        self.result = 8
        self.close()

    def close9(self):
        self.result = 9
        self.close()

    def close10(self):
        self.result = 10
        self.close()

    def close11(self):
        self.result = 11
        self.close()