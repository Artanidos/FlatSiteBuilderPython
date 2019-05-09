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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtProperty


class AnimateableEditor(QWidget):
    closes = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)

    @pyqtProperty('int')
    def x(self):
        return super.x()

    @x.setter
    def x(self, value):
        self.move(value, super.y())

    @pyqtProperty('int')
    def y(self):
        return super.y()

    @y.setter
    def y(self, value):
        self.move(super.x(), value)

    @pyqtProperty('int')
    def width(self):
        return super.width()

    @width.setter
    def width(self, value):
        self.resize(value, super.height())

    @pyqtProperty('int')
    def height(self):
        return super.height()

    @height.setter
    def height(self, value):
        self.resize(super.width(), value)
