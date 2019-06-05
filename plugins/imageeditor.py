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
from PyQt5.QtCore import Qt, qVersion, qRegisterResourceData, qUnregisterResourceData, pyqtProperty
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtQml import qmlRegisterType
from widgets.imageselector import ImageSelector
from widgets.flatbutton import FlatButton
from widgets.item import Item


class ImageEditor(ElementEditorInterface):
    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.site = None
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
        titleLabel = QLabel("Image Module Plugin")
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)
        self.image = ImageSelector()
        self.image.setImage(QImage(":/images/image_placeholder.png"))

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip("Close Editor")

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
        grid.addWidget(QLabel("Admin Label"), 10, 0)
        grid.addWidget(self.adminlabel, 11, 0)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        self.source.textChanged.connect(self.contentChanged)
        self.alt.textChanged.connect(self.contentChanged)
        self.title.textChanged.connect(self.contentChanged)
        self.adminlabel.textChanged.connect(self.contentChanged)
        seek.clicked.connect(self.seek)
        self.image.clicked.connect(self.seek)

    def closeEditor(self):
        if self.changed:
            self.content.src = self.source.text()
            self.content.alt = self.alt.text()
            self.content.title = self.title.text()
            self.content.adminlabel = self.adminlabel.text()
            #foreach(QString attName, m_attributes.keys())
            #{
            #    stream.writeAttribute(attName, m_attributes.value(attName));
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
            self.image.setImage(QImage(content.src))
        self.changed = False

    def getContent(self):
        return self.content

    def seek(self):
        fileName = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("Images (*.png *.gif *.jpg);;All (*)")
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
        self.source.setText(path)
        shutil.copy(fileName, path)

        # also copy file to deploy dir for previews
        dpath = os.path.join(self.site.deploy_path, "assets", "images", name)
        shutil.copy(fileName, dpath)

        self.image.setImage(QImage(path))
        self.contentChanged()

    def registerContenType(self):
        qmlRegisterType(Image, 'ImageEditor', 1, 0, 'Image')

    def writeImportString(self, f):
        f.write("import ImageEditor 1.0\n")


class Image(Item):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._src = ""
        self._alt = ""
        self._title = ""
        self.tag_name = "Image"

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
        f.write(" " * indent + "}\n")

    def getHtml(self):
        html = "<img"
        classValue = "img-responsive pull-left inner"
        html += " src=\"" + self.src + "\""
        html += " alt=\"" + self.alt + "\""
        html += " title=\"" + self.title + "\""
        html += " class=\"" + classValue + "\">\n"
        return html


qt_resource_data = b"\
\x00\x00\x02\x96\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x20\x00\x00\x00\x20\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\
\x00\x00\x00\x04\x73\x42\x49\x54\x08\x08\x08\x08\x7c\x08\x64\x88\
\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0d\xd7\x00\x00\x0d\xd7\
\x01\x42\x28\x9b\x78\x00\x00\x00\x19\x74\x45\x58\x74\x53\x6f\x66\
\x74\x77\x61\x72\x65\x00\x77\x77\x77\x2e\x69\x6e\x6b\x73\x63\x61\
\x70\x65\x2e\x6f\x72\x67\x9b\xee\x3c\x1a\x00\x00\x02\x13\x49\x44\
\x41\x54\x58\x85\xed\x95\xdb\xae\xe9\x50\x14\x86\xff\x3a\xa4\x8d\
\x44\xdc\x10\x91\xe0\x19\xc4\x03\xb8\xf2\x08\x1e\xd6\x0b\xb8\x21\
\x84\x6a\x51\x82\x46\x5a\x71\x8a\xc6\xa9\xf4\x38\xf7\xcd\xde\xcd\
\xee\xee\x2a\xb5\x56\x53\x37\xfb\xbf\x1b\xc3\x18\xf3\xff\x8c\x79\
\x28\xd5\x68\x34\x88\xa6\x69\xf8\x84\x68\x9a\x46\xec\x53\xe6\x00\
\xa0\x69\x1a\x62\x1f\x73\xff\xad\xc4\xdf\x41\x2a\x95\x8a\xc4\x54\
\x55\xd5\xaf\x01\x6a\xb5\x1a\x12\x89\x84\xa7\x21\x4c\x99\xa6\x89\
\x66\xb3\xe9\xc4\x1f\xdf\x82\xd0\x01\x08\x21\xd0\x75\x3d\x70\x7d\
\xa8\xf3\x56\x14\x05\x9d\x4e\x07\xba\xae\x23\x9f\xcf\xa3\x5a\xad\
\x22\x1e\x8f\x3f\xed\x09\x6d\x02\x84\x10\x0c\x06\x03\xe7\xdf\x6f\
\xb7\x5b\xac\x56\xab\x97\x7d\xa1\x01\x68\x9a\x86\xeb\xf5\xea\xca\
\xed\xf7\xfb\xe8\x00\x08\x21\x9e\x1c\x45\x51\xd1\x01\x30\x0c\x83\
\x74\x3a\xed\xca\xe5\x72\xb9\xe8\x00\x28\x8a\x42\xa5\x52\x01\xc3\
\x30\xa0\x28\x0a\x85\x42\x01\xe5\x72\xf9\x65\x5f\xe0\x5b\x20\x49\
\x12\x8a\xc5\xe2\xd3\x9a\x4c\x26\x83\x7a\xbd\x0e\xc3\x30\x90\x4c\
\x26\x03\xad\x1b\x68\x02\x87\xc3\x01\xfd\x7e\x1f\xeb\xf5\x3a\xd0\
\xa2\x41\xcd\x03\x01\x10\x42\x30\x1a\x8d\x00\x00\x1c\xc7\x21\xec\
\xaf\xe7\x4b\x00\x51\x14\x71\x3e\x9f\x01\x00\xba\xae\x63\x3c\x1e\
\x47\x07\xa0\x69\x1a\xa6\xd3\xa9\x2b\x27\x49\xd2\xcb\xfb\x7d\xbf\
\xdf\x61\xdb\xf6\xcf\x01\x04\x41\x80\x61\x18\x9e\xfc\x70\x38\x84\
\x65\x59\xbe\xe6\xad\x56\xcb\xd9\xb6\x6f\x03\x9c\x4e\x27\xdf\xa7\
\x54\x55\x55\x08\x82\xe0\xc9\x9b\xa6\x89\x76\xbb\x8d\xc7\xe3\x01\
\x51\x14\x21\xcb\xf2\xf7\x00\x08\x21\xe0\x79\xfe\x69\xe3\x62\xb1\
\x80\xa2\x28\x4e\x6c\xdb\x36\xda\xed\x36\x2e\x97\x8b\x93\x63\x59\
\xd6\x15\x07\x06\x90\x65\x19\xc7\xe3\xf1\x69\xe3\x1f\x03\x42\x08\
\x08\x21\xe8\xf5\x7a\x9e\x1e\xcb\xb2\xd0\xeb\xf5\x7c\xb7\xeb\x4b\
\x00\xd3\x34\x03\x9f\xf4\xcb\xe5\x82\xf9\x7c\x0e\x9e\xe7\xb1\xd9\
\x6c\x7c\x6b\x58\x96\xf5\x5d\xc3\xf3\x12\xce\x66\xb3\xb7\xee\xfa\
\x64\x32\x79\x59\x23\xcb\x32\xb2\xd9\x2c\x4a\xa5\x92\xe7\x37\xd7\
\x04\x54\x55\xc5\x72\xb9\x0c\x6c\xfe\x8e\x38\x8e\x73\xde\x13\x5f\
\x00\x8e\xe3\x02\xdf\xdf\x77\x65\x59\x16\xba\xdd\xae\xe7\x3c\xb8\
\x00\x82\x1c\xbc\x9f\xe8\x76\xbb\x61\x30\x18\xf8\x03\x44\xa1\xdd\
\x6e\xf7\x59\x80\x7f\xf5\x1f\x20\x46\xd3\xf4\xc7\xcc\x69\x9a\xc6\
\x2f\x6b\xaf\x16\xcf\x00\x32\x85\x29\x00\x00\x00\x00\x49\x45\x4e\
\x44\xae\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x0f\
\x04\xd3\xe1\x87\
\x00\x69\
\x00\x6d\x00\x61\x00\x67\x00\x65\x00\x65\x00\x64\x00\x69\x00\x74\x00\x6f\x00\x72\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x6a\xe4\xf0\xa2\x20\
"

qt_version = [int(v) for v in qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()