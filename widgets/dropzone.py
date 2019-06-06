#############################################################################
# Copyright (C) 2019 Olaf Japp
#
# self file is part of FlatSiteBuilder.
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

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor


class DropZone(QWidget):

    def __init__(self, w, h):
        QWidget.__init__(self)
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(self.palette().base().color().name()).lighter().lighter())
        self.setPalette(pal)
        self.setAutoFillBackground(True)
        self.setMinimumWidth(w)
        self.setMaximumWidth(w)
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(QLabel("Drop Here"))
        hbox.addStretch(1)
        self.setLayout(hbox)