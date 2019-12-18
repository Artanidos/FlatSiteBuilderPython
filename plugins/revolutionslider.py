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
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtCore import pyqtProperty, QObject, Q_CLASSINFO, QDir, QFile
from PyQt5.QtQml import QQmlListProperty
from PyQt5.QtGui import QImage
import plugins.revolution_rc

class RevolutionSliderEditor(ElementEditorInterface):
    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.class_name = "RevolutionSliderEditor"
        self.display_name = "RevolutionSlider"
        self.tag_name = "RevolutionSlider"
        self.version = "1.0"
        self.icon = QImage(":/revolution.png")

    def closeEditor(self):
        if self.changed:
            if self.content:
                self.content.adminlabel = self.adminlabel.text()
                self.content.text = html.escape(self.html.toPlainText())
        self.close.emit()

    def registerContenType(self):
        qmlRegisterType(RevolutionSlider, 'RevolutionSlider', 1, 0, 'RevolutionSlider')
        qmlRegisterType(Slide, 'RevolutionSlider', 1, 0, 'Slide')
    
    def writeImportString(self, f):
        f.write("import RevolutionSlider 1.0\n")

    def pluginStyles(self):
        return "<link href=\"assets/plugins/revolution-slider/css/settings.css\" rel=\"stylesheet\" type=\"text/css\"/>\n"

    def pluginScripts(self):
        script = "<script type=\"text/javascript\" src=\"assets/plugins/revolution-slider/js/jquery.themepunch.plugins.min.js\"></script>\n"
        script += "<script type=\"text/javascript\" src=\"assets/plugins/revolution-slider/js/jquery.themepunch.revolution.min.js\"></script>\n"
        script += "<script type=\"text/javascript\" src=\"assets/js/slider_revolution.js\"></script>\n"
        return script

    def installAssets(self, assets_path):
        assets = QDir(assets_path)
        assets.mkdir("plugins")
        assets.cd("plugins")   
        assets.mkdir("revolution-slider")
        assets.cd("revolution-slider")
        assets.mkdir("css")
        assets.mkdir("js")
        assets.mkdir("assets")
        QFile.copy(":/css", assets_path + "/plugins/revolution-slider/css")
        QFile.copy(":/js", assets_path + "/js")
        QFile.copy(":/js/plugins", assets_path + "/plugins/revolution-slider/js")
        QFile.copy(":/assets", assets_path + "/plugins/revolution-slider/assets")

    def getDefaultContent(self):
        return Slide()


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

class RevolutionSlider(Item):
    Q_CLASSINFO('DefaultProperty', 'items')

    def __init__(self, parent = None):
        super().__init__(parent)
        self.tag_name = "RevolutionSlider"
        self._fullscreen = False
        self._fullwidth = False
        self._data_transition = "slideleft"
        self._data_masterspeed = "700"
        self._items = []

    @pyqtProperty(QQmlListProperty)
    def items(self):
        return QQmlListProperty(Item, self, self._items)

    @pyqtProperty('QString')
    def dataTransition(self):
        return self._data_transition

    @dataTransition.setter
    def dataTransition(self, data_transition):
        self._data_transition = data_transition

    @pyqtProperty('QString')
    def dataMasterspeed(self):
        return self._data_masterspeed
        
    @dataMasterspeed.setter
    def dataMasterspeed(self, data_masterspeed):
        self._data_masterspeed = data_masterspeed

    @pyqtProperty('bool')
    def fullscreen(self):
        return self._fullscreen
    
    @fullscreen.setter
    def fullscreen(self, fullscreen):
        self._fullscreen = fullscreen

    @pyqtProperty('bool')
    def fullwidth(self):
        return self._fullwidth
    
    @fullwidth.setter
    def fullwidth(self, fullwidth):
        self._fullwidth = fullwidth

    def getHtml(self):
        sliderContainerClass = ""
        sliderClass = ""

        if self.fullscreen:
            sliderContainerClass = "fullscreenbanner-container"
            sliderClass = "fullscreenbanner"

        if self.fullwidth:
            sliderContainerClass = "fullwidthbanner-container"
            sliderClass = "fullwidthbanner"
        
        htm = "<div class=\"" + sliderContainerClass + "\">\n"
        htm += "<div class=\"" + sliderClass + "\">\n"
        htm += "<ul>\n"
        for slide in self._items:
            url = slide.src[slide.src.index("assets/images/"):]
            htm += "<li data-transition=\"" + self._data_transition + "\" data-masterspeed=\"" + self._data_masterspeed + "\""
            htm += ">\n"
            htm += "<img src=\"" + url + "\" alt=\"\" data-bgfit=\"cover\" data-bgposition=\"center center\" data-bgrepeat=\"no-repeat\">\n"
            htm += html.unescape(slide._text) + "\n"
            htm += "</li>\n"        
        htm += "</ul>\n"
        htm += "<div class=\"tp-bannertimer\"></div>\n"
        htm += "</div>\n"
        htm += "</div>\n"
        return htm

    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + "RevolutionSlider {\n")
        self.writeAttribute(f, indent + 4, "id", self._id)
        self.writeAttribute(f, indent + 4, "text", self._text)
        self.writeAttribute(f, indent + 4, "adminlabel", self._adminlabel)
        self.writeAttribute(f, indent + 4, "fullwidth", self._fullwidth)
        self.writeAttribute(f, indent + 4, "fullscreen", self._fullscreen)
        for slide in self._items:
            slide.save(f, indent + 4)
        f.write(" " * indent + "}\n")