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

import os
import shutil
from widgets.interfaces import ElementEditorInterface
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, qVersion, QFile, QDir, qRegisterResourceData, qUnregisterResourceData, pyqtProperty
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QListWidget, QListWidgetItem
from PyQt5.QtQml import qmlRegisterType
from widgets.imageselector import ImageSelector
from widgets.flatbutton import FlatButton
from widgets.item import Item
import plugins.imageeditor_rc


class ImageEditor(ElementEditorInterface):
    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.site = None
        self.animation = ""
        self.class_name = "ImageEditor"
        self.display_name = "Image"
        self.tag_name = "Image"
        self.version = "1.0"
        self.icon = QImage(":/imageeditor.png")

        self.changed = False
        self.setAutoFillBackground(True)

        grid = QGridLayout()

        self.source = QLineEdit()
        self.alt = QLineEdit()
        self.alt.setMaximumWidth(200)
        self.title = QLineEdit()
        self.title.setMaximumWidth(200)
        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)
        seek = QPushButton("...")
        seek.setMaximumWidth(50)
        titleLabel = QLabel("Image Module")
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)
        self.image = ImageSelector()
        self.image.setImage(QImage(":/images/image_placeholder.png"))

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip("Close Editor")

        self.animation_type = QListWidget()
        self.animation_type.addItem("None")
        self.animation_type.addItem("Attention Seekers")
        self.animation_type.addItem("Bouncing Entrances")
        self.animation_type.addItem("Bouncing Exits")
        self.animation_type.addItem("Fading Entrances")
        self.animation_type.addItem("Fading Exits")
        self.animation_type.addItem("Flippers")
        self.animation_type.addItem("Rotating Entrances")
        self.animation_type.addItem("Rotating Exits")
        self.animation_type.addItem("Sliding Entrances")
        self.animation_type.addItem("Sliding Exits")
        self.animation_type.addItem("Zoom Entrances")
        self.animation_type.addItem("Zoom Exits")

        self.animation_subtype = QListWidget()

        grid.addWidget(titleLabel, 0, 0)
        grid.addWidget(close, 0, 3, 1, 1, Qt.AlignRight)
        grid.addWidget(QLabel("Path"), 1, 0)
        grid.addWidget(self.source, 2, 0, 1, 3)
        grid.addWidget(seek, 2, 3)
        grid.addWidget(self.image, 3, 0, 1, 4)
        grid.setRowStretch(3, 1)
        grid.addWidget(QLabel("Alt"), 6, 0)
        grid.addWidget(self.alt, 7, 0)
        grid.addWidget(QLabel("Title"), 8, 0)
        grid.addWidget(self.title, 9, 0)
        grid.addWidget(QLabel("Animation"), 6, 1)
        grid.addWidget(self.animation_type, 7, 1, 6, 1)
        grid.addWidget(self.animation_subtype, 7, 2, 6, 1)
        grid.addWidget(QLabel("Admin Label"), 11, 0)
        grid.addWidget(self.adminlabel, 12, 0)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        self.source.textChanged.connect(self.contentChanged)
        self.alt.textChanged.connect(self.contentChanged)
        self.title.textChanged.connect(self.contentChanged)
        self.adminlabel.textChanged.connect(self.contentChanged)
        seek.clicked.connect(self.seek)
        self.image.clicked.connect(self.seek)
        self.animation_type.currentTextChanged.connect(self.animationTypeChanged)
        self.animation_subtype.currentTextChanged.connect(self.contentChanged)

    def animationTypeChanged(self, type):
        self.contentChanged()
        self.animation_subtype.clear()
        if type == "Attention Seekers":
            self.addSubItem("Bounce", "bounce")
            self.addSubItem("Flash", "flash")
            self.addSubItem("Pulse","pulse")
            self.addSubItem("Shake","shake")
            self.addSubItem("Swing","swing")
            self.addSubItem("Tada","tada")
            self.addSubItem("Wobble","wobble")
        elif type == "Bouncing Entrances":
            self.addSubItem("Bounce In","bounceIn")
            self.addSubItem("Bounce In Down","bounceInDown")
            self.addSubItem("Bounce In Left","bounceInLeft")
            self.addSubItem("Bounce In Right","bounceInRight")
            self.addSubItem("Bounce In Up","bounceInUp")
        elif type == "Bouncing Exits":
            self.addSubItem("Bounce Out","bounceOut")
            self.addSubItem("Bounce Out Down","bounceOutDown")
            self.addSubItem("Bounce Out Left","bounceOutLeft")
            self.addSubItem("Bounce Out Right","bounceOutRight")
            self.addSubItem("Bounce Out Up","bounceOutUp")
        elif type == "Fading Entrances":
            self.addSubItem("Fade In", "fadeIn")
            self.addSubItem("Fade In Down", "fadeInDown")
            self.addSubItem("Fade In Down Big", "fadeInDownBig")
            self.addSubItem("Fade In Left", "fadeInLeft")
            self.addSubItem("Fade In Left Big", "fadeInLeftBig")
            self.addSubItem("Fade In Right", "fadeInRight")
            self.addSubItem("Fade In Right Big", "fadeInRightBig")
            self.addSubItem("Fade In Up", "fadeInUp")
            self.addSubItem("Fade In Up Big", "fadeInUpBig")
        elif type == "Fading Exits":
            self.addSubItem("Fade Out", "fadeOut")
            self.addSubItem("Fade Out Down", "fadeOutDown")
            self.addSubItem("Fade Out Down Big", "fadeOutDownBig")
            self.addSubItem("Fade Out Left", "fadeOutLeft")
            self.addSubItem("Fade Out Left Big", "fadeOutLeftBig")
            self.addSubItem("Fade Out Right", "fadeOutRight")
            self.addSubItem("Fade Out Right Big", "fadeOutRightBig")
            self.addSubItem("Fade Out Up", "fadeOutUp")
            self.addSubItem("Fade Out Up Big", "fadeOutUpBig")
        elif type == "Flippers":
            self.addSubItem("Flip", "flip")
            self.addSubItem("Flip In X", "flipInX")
            self.addSubItem("Flip In Y", "flipInY")
            self.addSubItem("Flip Out X", "flipOutX")
            self.addSubItem("Flip Out Y", "flipOutY")
        elif type == "Rotating Entrances":
            self.addSubItem("Rotate In", "rotateIn")
            self.addSubItem("Rotate In Down Left", "rotateInDownLeft")
            self.addSubItem("Rotate In Down Right", "rotateInDownRight")
            self.addSubItem("Rotate In Up Left", "rotateInUpLeft")
            self.addSubItem("Rotate In Up Right", "rotateInUpRight")
        elif type == "Rotating Exits":
            self.addSubItem("Rotate Out", "rotateOut")
            self.addSubItem("Rotate Out Down Left", "rotateOutDownLeft")
            self.addSubItem("Rotate Out Down Right", "rotateOutDownRight")
            self.addSubItem("Rotate Out Up Left", "rotateOutUpLeft")
            self.addSubItem("Rotate Out Up Right", "rotateOutUpRight")
        elif type == "Sliding Entrances":
            self.addSubItem("Slide In Up", "slideInUp")
            self.addSubItem("Slide In Down", "slideInDown")
            self.addSubItem("Slide In Left", "slideInLeft")
            self.addSubItem("Slide In Right", "slideInRight")
        elif type == "Sliding Exits":
            self.addSubItem("Slide Out Up", "slideOutUp")
            self.addSubItem("Slide Out Down", "slideOutDown")
            self.addSubItem("Slide Out Left", "slideOutLeft")
            self.addSubItem("Slide Out Right", "slideOutRight")
        elif type == "Zoom Entrances":
            self.addSubItem("Zoom In", "zoomIn")
            self.addSubItem("Zoom In Down", "zoomInDown")
            self.addSubItem("Zoom In Left", "zoomInLeft")
            self.addSubItem("Zoom In Right", "zoomInRight")
            self.addSubItem("Zoom In Up", "zoomInUp")
        elif type == "Zoom Exits":
            self.addSubItem("Zoom Out", "zoomOut")
            self.addSubItem("Zoom Out Down", "zoomOutDown")
            self.addSubItem("Zoom Out Left", "zoomOutLeft")
            self.addSubItem("Zoom Out Right", "zoomOutRight")
            self.addSubItem("Zoom Out Up", "zoomOutUp")
    
    def addSubItem(self, title, data):
        item = QListWidgetItem(title)
        item.setData(Qt.UserRole, data)
        self.animation_subtype.addItem(item)

    def closeEditor(self):
        if self.changed:
            self.content.src = self.source.text()
            self.content.alt = self.alt.text()
            self.content.title = self.title.text()
            self.content.adminlabel = self.adminlabel.text()
            if self.animation_type.currentItem():
                self.content.animation_type = self.animation_type.currentItem().data(Qt.DisplayRole)
            if self.animation_subtype.currentItem():
                self.content.animation = self.animation_subtype.currentItem().data(Qt.UserRole)
            else:
                self.content.animation = ""
            #foreach(QString attName, m_attributes.keys())
            #{
            #    stream.writeAttribute(attName, m_attributes.value(attName))
            #}
        self.close.emit()

    def getDefaultContent(self):
        return Image()

    def setContent(self, content):
        self.content = content
        self.source.setText(content.src)
        self.alt.setText(content.alt)
        self.title.setText(content.title)
        self.adminlabel.setText(content.adminlabel)
        if content.src:
            self.image.setImage(QImage(os.path.join(self.site.source_path, "assets", "images", content.src)))
        if self.animation_type:
            index = self.findData(self.animation_type, content.animation_type, Qt.DisplayRole)
            self.animation_type.setCurrentRow(index)
            if self.animation_subtype:
                index = self.findData(self.animation_subtype, content.animation, Qt.UserRole)
                self.animation_subtype.setCurrentRow(index)
        else:
            self.animation_type.setCurrentRow(0)
        self.changed = False

    def findData(self, list, value, role):
        if not value:
            return -1
        for index in range(list.count()):
            item = list.item(index)
            if item.data(role) == value:
                return index
        return -1

    def getContent(self):
        return self.content

    def seek(self):
        fileName = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("Images (*.png *.gif *.jpg)All (*)")
        dialog.setWindowTitle("Load Image")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]
        del dialog
        if not fileName:
            return

        # copy file to assets dir
        name = os.path.basename(fileName).replace(" ", "_")
        path = os.path.join(self.site.source_path, "assets", "images", name)
        self.source.setText(os.path.basename(path))
        try:
            shutil.copy(fileName, path)
        except shutil.SameFileError:
            pass

        # also copy file to deploy dir for previews
        dpath = os.path.join(self.site.source_path, self.site.output, "assets", "images", name)
        shutil.copy(fileName, dpath)

        self.image.setImage(QImage(path))
        self.contentChanged()

    def registerContenType(self):
        qmlRegisterType(Image, 'ImageEditor', 1, 0, 'Image')

    def writeImportString(self, f):
        f.write("import ImageEditor 1.0\n")

    def pluginStyles(self):
        return "<link href=\"assets/plugins/animate/animate.css\" rel=\"stylesheet\" type=\"text/css\"/>\n"

    def installAssets(self, assets_path):
        assets = QDir(assets_path)
        assets.mkdir("plugins")
        assets.cd("plugins")
        assets.mkdir("animate")
        QFile.copy(":/animate.css", assets_path + "/plugins/animate/animate.css")


class Image(Item):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._src = ""
        self._alt = ""
        self._title = ""
        self.tag_name = "Image"
        self._animation = ""
        self._animation_type = ""

    @pyqtProperty('QString')
    def src(self):
        return self._src

    @src.setter
    def src(self, src):
        self._src = src

    @pyqtProperty('QString')
    def alt(self):
        return self._alt

    @alt.setter
    def alt(self, alt):
        self._alt = alt

    @pyqtProperty('QString')
    def animation(self):
        return self._animation

    @animation.setter
    def animation(self, animation):
        self._animation = animation

    @pyqtProperty('QString')
    def animation_type(self):
        return self._animation_type

    @animation_type.setter
    def animation_type(self, animation_type):
        self._animation_type = animation_type

    @pyqtProperty('QString')
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Image {\n")
        self.writeAttribute(f, indent + 4, "src", self.src)
        self.writeAttribute(f, indent + 4, "alt", self.alt)
        self.writeAttribute(f, indent + 4, "title", self.title)
        self.writeAttribute(f, indent + 4, "adminlabel", self._adminlabel)
        self.writeAttribute(f, indent + 4, "animation", self._animation)
        self.writeAttribute(f, indent + 4, "animation_type", self._animation_type)
        f.write(" " * indent + "}\n")

    def getHtml(self): 
        if "/assets/images" in self.src:
            src = self.src[self.src.index("/assets/images") + 14:]
        else:
            src = self.src  
        if self._animation:
            return "<img alt=\"" + self.alt + "\" title=\"" + self.title + "\" class=\"img-responsive animated " + self._animation + " pull-left inner\" src=\"assets/images/" + src + "\">\n"
        else:
            return "<img alt=\"" + self.alt + "\" title=\"" + self.title + "\" class=\"img-responsive pull-left inner\" src=\"assets/images/" + src + "\">\n"
