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
#  along with FlatSiteBuilder.  If not, see <http.//www.gnu.org/licenses/>.
#
#############################################################################

import html
from widgets.interfaces import ElementEditorInterface
from widgets.item import Item
from widgets.flatbutton import FlatButton
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtCore import Qt, pyqtProperty, QObject, Q_CLASSINFO, QDir, QFile
from PyQt5.QtGui import QImage
from PyQt5.QtQml import QQmlListProperty
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QLabel, QPushButton, QTableWidget, QAbstractItemView, QHeaderView
import plugins.carousel_rc


class CarouselEditor(ElementEditorInterface):
    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.class_name = "CarouselEditor"
        self.display_name = "Carousel"
        self.tag_name = "Carousel"
        self.version = "1.0"
        self.icon = QImage(":/carousel.png")

        self.changed = False
        #self.editor = 0
        self.setAutoFillBackground(True)

        grid = QGridLayout()
        self.id = QLineEdit()
        self.id.setMaximumWidth(200)
        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)
        titleLabel = QLabel("Slider Module")
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip("Close Editor")

        addSlide = QPushButton("Add Slide")
        addSlide.setMaximumWidth(120)

        self.list = QTableWidget(0, 2, self)
        self.list.verticalHeader().hide()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch )
        self.list.setToolTip("Double click to edit item")
        labels = ["", "Name"]
        self.list.setHorizontalHeaderLabels(labels)

        grid.addWidget(titleLabel, 0, 0)
        grid.addWidget(close, 0, 2, 1, 1, Qt.AlignRight)
        grid.addWidget(addSlide, 1, 0)
        grid.addWidget(self.list, 2, 0, 1, 3)
        grid.addWidget(QLabel("Id"), 4, 0)
        grid.addWidget(self.id, 5, 0)
        grid.addWidget(QLabel("Admin Label"), 6, 0)
        grid.addWidget(self.adminlabel, 7, 0)

        self.setLayout(grid)

        addSlide.clicked.connect(self.addSlide)
        self.adminlabel.textChanged.connect(self.contentChanged)
        self.id.textChanged.connect(self.contentChanged)
        close.clicked.connect(self.closeEditor)
        self.list.cellDoubleClicked.connect(self.tableDoubleClicked)

        self.installEventFilter(self)

    def closeEditor(self):
        if self.changed:
            if self.content:
                self.content.id = self.id.text()
                self.content.adminlabel = self.adminlabel.text()
        self.close.emit()

    def setContent(self, content):
        self.content = content
        if content:
            self.id.setText(content.id)
            self.adminlabel.setText(content.adminlabel)
            self.changed = False

    def getContent(self):
        return self.content

    def registerContenType(self):
        qmlRegisterType(Carousel, 'Carousel', 1, 0, 'Carousel')
        qmlRegisterType(Slide, 'Carousel', 1, 0, 'Slide')

    def writeImportString(self, f):
        f.write("import Carousel 1.0\n")

    def getDefaultContent(self):
        return Carousel()

    def addSlide(self):
        pass

    def tableDoubleClicked(self):
        pass 


class Slide(Item):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tag_name = "Slide"
        self._src = ""

    @pyqtProperty('QString')
    def src(self):
        return self._src
    
    @src.setter
    def src(self, src):
        self._src = src

    def getHtml(self):
        return ""
    
    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Slide {\n")
        self.writeAttribute(f, indent + 4, "id", self._id)
        self.writeAttribute(f, indent + 4, "src", self._src)
        self.writeAttribute(f, indent + 4, "text", self._text)
        f.write(" " * indent + "}\n")

class Carousel(Item):
    Q_CLASSINFO('DefaultProperty', 'items')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tag_name = "Carousel"
        self._src = ""
        self._id = ""
        self._items = []
    
    @pyqtProperty(QQmlListProperty)
    def items(self):
        return QQmlListProperty(Item, self, self._items)

    @pyqtProperty('QString')
    def src(self):
        return self._src

    @src.setter
    def src(self, src):
        self._src = src

    @pyqtProperty('QString')
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "Carousel {\n")
        self.writeAttribute(f, indent + 4, "id", self._id)
        self.writeAttribute(f, indent + 4, "src", self._src)
        self.writeAttribute(f, indent + 4, "text", self._text)
        self.writeAttribute(f, indent + 4, "adminlabel", self._adminlabel)
        f.write(" " * indent + "}\n")

    def getHtml(self):
        #QHash<QString,QString> attributes
        #QStringList urls
        #QStringList inner
        id = "main-carousel"

        #foreach(QXmlStreamAttribute att, xml.attributes())
        #{
        #    QString attName = att.name().toString()
        #    QString value = att.value().toString()
        #    if(attName == "adminlabel")
        #         // ignore
        #    else if(attName == "id")
        #    {
        #        if(!value.isEmpty())
        #            id = value
        #    }
        #    else
        #        attributes.insert(attName, value)
        #}

        html = "<div id=\"" + id + "\" class=\"carousel slide\" data-ride=\"carousel\">\n"
        html += "<ol class=\"carousel-indicators\">\n"

        #while(xml.readNext())
        #{
        #    if(xml.isStartElement() && xml.name() == "Slide")
        #    {
        #        QString source = xml.attributes().value("src").toString()
        #        QString url = source.mid(source.indexOf("assets/images/"))
        #        urls.append(url)

        #        inner.append(xml.readElementText())
        #    }
        #    else if(xml.isEndElement() && xml.name() == "Slider")
        #        break
        #}

        #int pos = 0
        #foreach(QString url, urls)
        #{
        #    html += "<li data-target=\"#" + id + "\" data-slide-to=\"" + QString.number(pos) + "\"" + (pos == 0 ? " class=\"active\"" : "") + "></li>\n"
        #    pos++
        #}
        html += "</ol>\n"
        html += "<div class=\"carousel-inner\">\n"

        #pos = 0
        #foreach(QString url, urls)
        #{
        #    html += "<div class=\"item"
        #    if(pos == 0)
        #        html += " active"
        #    html += "\" "
        #    foreach(QString attName, attributes.keys())
        #    {
        #        html += " " + attName + "=\"" + attributes.value(attName) + "\""
        #    }
        #    html += ">\n"
        #    html += "<img src=\"" + url + "\" style=\"width:100%\">\n"
        #    html += inner.at(pos) + "\n"
        #    html += "</div>\n"
        #    pos++
        #}
        html += "</div>\n"
        html += "<a class=\"left carousel-control\" href=\"#" + id + "\" data-slide=\"prev\">\n"
        html += "<span class=\"glyphicon glyphicon-chevron-left\"></span>\n"
        html += "<span class=\"sr-only\">Previous</span>\n"
        html += "</a>\n"
        html += "<a class=\"right carousel-control\" href=\"#" + id + "\" data-slide=\"next\">\n"
        html += "<span class=\"glyphicon glyphicon-chevron-right\"></span>\n"
        html += "<span class=\"sr-only\">Next</span>\n"
        html += "</a>\n"
        html += "</div>\n"
        return html