
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

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import QParallelAnimationGroup, QPropertyAnimation, Qt, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QImage, QPalette, QPixmap, QColor


class Expander(QWidget):
    expanded = pyqtSignal(object)
    clicked = pyqtSignal()

    def __init__(self, header, normal_icon="", hovered_icon="", selected_icon=""):
        QWidget.__init__(self)
        self.is_expanded = False
        self.text = header
        self.label_normal_color = self.palette().link().color().name()
        self.label_hovered_color = self.palette().highlight().color().name()
        self.label_selected_color = self.palette().highlightedText().color().name()
        self.normal_color = self.palette().base().color().name()
        self.selected_color = self.palette().highlight().color()
        self.hovered_color = self.palette().alternateBase().color()

        self.setCursor(Qt.PointingHandCursor)

        if normal_icon:
            self.normal_icon = QImage(normal_icon)
        if hovered_icon:
            self.hovered_icon = QImage(hovered_icon)
        if selected_icon:
            self.selected_icon = QImage(selected_icon)

        self.setAttribute(Qt.WA_Hover, True)

        self.color = self.normal_color
        self.setAutoFillBackground(True)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.icon = QLabel()
        self.icon.setPixmap(QPixmap.fromImage(self.normal_icon))
        self.hyper = QLabel()
        self.hyper.setText("<a style=\"color: " + self.label_normal_color + " text-decoration: none\" href=\"#\">" + self.text + "</a>")
        hbox.addWidget(self.icon)
        hbox.addSpacing(5)
        hbox.addWidget(self.hyper)
        hbox.addStretch()
        hbox.setContentsMargins(8, 8, 8, 8)
        vbox.addLayout(hbox)
        self.content = QWidget()
        self.content.setStyleSheet("background-color: " + self.palette().base().color().name())
        self.content.setMaximumHeight(0)

        vbox.addWidget(self.content)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        self.hyper.linkActivated.connect(self.buttonClicked)

        self.anim = QParallelAnimationGroup()
        self.height_anim = QPropertyAnimation(self.content, "maximumHeight".encode("utf-8"))
        self.color_anim = QPropertyAnimation(self, "color".encode("utf-8"))
        self.height_anim.setDuration(200)
        self.color_anim.setDuration(200)
        self.anim.addAnimation(self.height_anim)
        self.anim.addAnimation(self.color_anim)

    def setExpanded(self, value):
        if value == self.is_expanded:
            return

        if value:
            self.is_expanded = True
            pal = self.palette()
            pal.setColor(QPalette.Background, self.selected_color)
            self.setPalette(pal)
            self.icon.setPixmap(QPixmap.fromImage(self.selected_icon))
            self.hyper.setText("<a style=\"color: " + self.label_selected_color + "; text-decoration: none;\" href=\"#\">" + self.text + "</a>")
        else:
            self.is_expanded = False
            pal = self.palette()
            pal.setColor(QPalette.Background, QColor(self.normal_color))
            self.setPalette(pal)
            self.icon.setPixmap(QPixmap.fromImage(self.normal_icon))
            self.hyper.setText("<a style=\"color: " + self.label_normal_color + "; text-decoration: none;\" href=\"#\">" + self.text + "</a>")

        if self.is_expanded:
            self.expandContent()
        else:
            self.collapseContent()
        self.expanded.emit(self.is_expanded)

    def addLayout(self, layout):
        self.content.setLayout(layout)

    @pyqtProperty('QColor')
    def color(self):
        return Qt.black

    @color.setter
    def color(self, color):
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(color))
        self.setPalette(pal)

    def mouseReleaseEvent(self, me):
        self.setExpanded(not self.is_expanded)
        if self.is_expanded:
            self.clicked.emit()

    def expandContent(self):
        if self.content.layout():
            self.height_anim.setEndValue(self.content.layout().sizeHint().height())
        else:
            self.height_anim.setEndValue(0)
        self.height_anim.setStartValue(0)
        self.color_anim.setStartValue(self.normal_color)
        self.color_anim.setEndValue(self.selected_color)
        self.anim.start()

    def collapseContent(self):
        if self.content.layout():
            self.height_anim.setStartValue(self.content.layout().sizeHint().height())
        else:
            self.height_anim.setStartValue(0)
        self.height_anim.setEndValue(0)
        self.color_anim.setStartValue(self.selected_color)
        self.color_anim.setEndValue(self.normal_color)
        self.anim.start()

    def buttonClicked(self):
        self.setExpanded(not self.is_expanded)
        if self.is_expanded:
            self.clicked.emit()
