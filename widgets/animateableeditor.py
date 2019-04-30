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

from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Signal, Property

class AnimateableEditor(QWidget):
    closes = Signal()

    def __init__(self):
        QWidget.__init__(self)

    def readX(self):
        return super.x()
    
    def setX(self, value):
        self.move(value, super.y())

    def readY(self):
        return super.y()

    def setY(self, value):
        self.move(super.x(), value)

    def readWidth(self):
        return super.width()

    def setWidth(self, value):
        self.resize(value, super.height())

    def readHeight(self):
        return super.height()

    def setHeight(slef, value):
        self.resize(super.width(), value)
    
    x = Property(int, readX, setX)
    y = Property(int, readY, setY)
    width = Property(int, readWidth, setWidth)
    height = Property(int, readHeight, setHeight)
    
    