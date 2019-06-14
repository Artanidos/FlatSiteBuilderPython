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
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSignal, Qt


class ImageSelector(QWidget):
    clickedSelector = pyqtSignal(object, int)
    clicked = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.item = None

    def setImage(self, image):
        self.image = image
        self.update()

    def setItem(self, item):
        self.item = item

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        event.accept()
        if self.item:
            self.clickedSelector.emit(self, event.button())
        else:
            self.clicked.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixSize = self.image.size()
        pixSize.scale(event.rect().size(), Qt.KeepAspectRatio)
        scaledImage = self.image.scaled(pixSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        x = (event.rect().size().width() - scaledImage.size().width()) / 2.0
        y = (event.rect().size().height() - scaledImage.size().height()) / 2.0
        painter.drawImage(x, y, scaledImage)
