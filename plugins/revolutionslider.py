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
import shutil
import os
from widgets.interfaces import ElementEditorInterface
from widgets.item import Item
from widgets.flatbutton import FlatButton
from widgets.tablecellbuttons import TableCellButtons
from widgets.animateableeditor import AnimateableEditor
from widgets.imageselector import ImageSelector
from plugins.texteditor import XmlHighlighter
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtCore import Qt, pyqtProperty, QObject, Q_CLASSINFO, QDir, QFileInfo, QFile, QPoint, QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation
from PyQt5.QtQml import QQmlListProperty
from PyQt5.QtGui import QImage, QFont, QFontMetrics
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QGridLayout, QWidget, QTextEdit, QTableWidgetItem, QLabel, QPushButton, QTableWidget, QAbstractItemView, QHeaderView

import plugins.revolution_rc

class RevolutionSliderEditor(ElementEditorInterface):
    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.class_name = "RevolutionSliderEditor"
        self.display_name = "RevolutionSlider"
        self.tag_name = "RevolutionSlider"
        self.version = "1.0"
        self.icon = QImage(":/revolution.png")
        self.changed = False
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
                self.content.removeSlides()
                self.content.adminlabel = self.adminlabel.text()
                #self.content.text = html.escape(self.html.toPlainText())
                for i in range(self.list.rowCount()):
                    item = self.list.item(i, 1)
                    slide = item.data(Qt.UserRole)
                    self.content.addSlide(slide)
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
        return RevolutionSlider()

    def setContent(self, content):
        self.content = content
        if content:
            #self.adminlabel.setText(content.adminlabel)
            self.changed = False

        self.list.setRowCount(0)

        for slide in content._items:
            self.addListItem(slide)
        self.changed = False

    def getContent(self):
        return self.content

    def addSlide(self):
        slide = Slide()
        self.addListItem(slide)
        self.contentChanged()
        self.tableDoubleClicked(self.list.rowCount() - 1)

    def addListItem(self, slide):
        rows = self.list.rowCount()
        self.list.setRowCount(rows + 1)
        tcb = TableCellButtons()
        tcb.setItem(slide)
        tcb.deleteItem.connect(self.deleteSlide)
        tcb.editItem.connect(self.editSlide)
        self.list.setCellWidget(rows, 0, tcb)
        self.list.setRowHeight(rows, tcb.sizeHint().height())
        titleItem = QTableWidgetItem(slide.title)
        titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
        titleItem.setData(Qt.UserRole, slide)
        self.list.setItem(rows, 1, titleItem)

    def tableDoubleClicked(self, row):
        item = self.list.item(row, 1)
        slide = item.data(Qt.UserRole)

        self.editor = SlideEditor()
        self.editor.setSite(self.site)
        self.editor.setSlide(slide)
        self.editor.closes.connect(self.editorClosed)
        self.animate(item)

    def animate(self, item):
        self.row = item.row()

        # create a cell widget to get the right position in the table
        self.sourcewidget = QWidget()
        self.list.setCellWidget(self.row, 1, self.sourcewidget)
        pos = self.sourcewidget.mapTo(self, QPoint(0,0))

        self.editor.setParent(self)
        self.editor.move(pos)
        self.editor.resize(self.sourcewidget.size())
        self.editor.show()

        self.animationgroup = QParallelAnimationGroup()
        self.animx = QPropertyAnimation()
        self.animx.setDuration(300)
        self.animx.setStartValue(pos.x())
        self.animx.setEndValue(0)
        self.animx.setTargetObject(self.editor)
        self.animx.setPropertyName("x".encode("utf-8"))
        self.animationgroup.addAnimation(self.animx)
        self.animy = QPropertyAnimation()
        self.animy.setDuration(300)
        self.animy.setStartValue(pos.y())
        self.animy.setEndValue(0)
        self.animy.setTargetObject(self.editor)
        self.animy.setPropertyName("y".encode("utf-8"))
        self.animationgroup.addAnimation(self.animy)
        self.animw = QPropertyAnimation()
        self.animw.setDuration(300)
        self.animw.setStartValue(self.sourcewidget.size().width())
        self.animw.setEndValue(self.size().width())
        self.animw.setTargetObject(self.editor)
        self.animw.setPropertyName("width".encode("utf-8"))
        self.animationgroup.addAnimation(self.animw)
        self.animh = QPropertyAnimation()
        self.animh.setDuration(300)
        self.animh.setStartValue(self.sourcewidget.size().height())
        self.animh.setEndValue(self.size().height())
        self.animh.setTargetObject(self.editor)
        self.animh.setPropertyName("height".encode("utf-8"))
        self.animationgroup.addAnimation(self.animh)
        self.animationgroup.finished.connect(self.animationFineshedZoomIn)
        self.animationgroup.start()

    def animationFineshedZoomIn(self):
        pass

    def editorClosed(self):
        pos = self.sourcewidget.mapTo(self, QPoint(0,0))
        # correct end values in case of resizing the window
        self.animx.setStartValue(pos.x())
        self.animy.setStartValue(pos.y())
        self.animw.setStartValue(self.sourcewidget.size().width())
        self.animh.setStartValue(self.sourcewidget.size().height())
        self.animationgroup.setDirection(QAbstractAnimation.Backward)
        #self.animationgroup.finished()), this, SLOT(animationFineshedZoomIn()))
        #connect(m_animationgroup, SIGNAL(finished()), this, SLOT(animationFineshedZoomOut()))
        self.animationgroup.start()

        item = self.list.item(self.row, 1)
        item.setData(Qt.UserRole, self.editor.slide)
        item.setText(self.editor.slide.title)
        if self.editor.changed:
            self.contentChanged()

    def animationFineshedZoomOut(self):
        #delete m_animationgroup
        #delete m_editor
        #self.editor = None
        pass

    def deleteSlide(self, slide):
        for row in range(self.list.rowCount()):
            item = self.list.item(row, 1)
            m = item.data(Qt.UserRole)
            if m == slide:
                self.list.removeRow(row)
                self.contentChanged()
                break

    def editSlide(self, slide):
        for row in range(self.list.rowCount()):
            item = self.list.item(row, 1)
            m = item.data(Qt.UserRole)
            if m == slide:
                self.list.selectRow(row)
                self.tableDoubleClicked(row)
                break


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

    @pyqtProperty('QString')
    def title(self):
        if self.adminlabel:
            return self._adminlabel
        else:
            return "New Slide"

    def getHtml(self):
        return ""
    
    def save(self, f, indent):
        f.write("\n")
        f.write(" " * indent + self.tag_name + " {\n")
        self.writeAttribute(f, indent + 4, "id", self._id)
        self.writeAttribute(f, indent + 4, "src", self._src)
        self.writeAttribute(f, indent + 4, "text", self._text)
        self.writeAttribute(f, indent + 4, "adminlabel", self._adminlabel)
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

    def addSlide(self, slide):
        self._items.append(slide)

    def removeSlides(self):
        self._items.clear()

class SlideEditor(AnimateableEditor):

    def __init__(self):
        super().__init__()
        self.changed = False
        self.setAutoFillBackground(True)
        grid = QGridLayout()

        seek = QPushButton("...")
        seek.setMaximumWidth(50)
        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)
        titleLabel = QLabel("Slide")
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)
        self.source = QLineEdit()
        self.image = ImageSelector()
        self.image.setImage(QImage(":/images/image_placeholder.png"))

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip("Close Editor")

        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(13)
        self.innerHtml = QTextEdit()
        self.innerHtml.setMaximumHeight(120)
        self.innerHtml.setFont(font)
        self.innerHtml.setAcceptRichText(False)
        self.innerHtml.setLineWrapMode(QTextEdit.NoWrap)
        metrics = QFontMetrics(font)
        self.innerHtml.setTabStopWidth(4 * metrics.width(' '))
        XmlHighlighter(self.innerHtml.document())

        grid.addWidget(titleLabel, 0, 0)
        grid.addWidget(close, 0, 2, 1, 1, Qt.AlignRight)
        grid.addWidget(QLabel("Path"), 1, 0)
        grid.addWidget(self.source, 2, 0, 1, 2)
        grid.addWidget(seek, 2, 2)
        grid.addWidget(self.image, 3, 0, 1, 2)
        grid.setRowStretch(3, 1)
        grid.addWidget(QLabel("Inner HTML"), 4, 0)
        grid.addWidget(self.innerHtml, 5, 0, 1, 3)
        grid.addWidget(QLabel("Admin Label"), 6, 0)
        grid.addWidget(self.adminlabel, 7, 0)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        self.image.clicked.connect(self.seek)
        seek.clicked.connect(self.seek)
        self.source.textChanged.connect(self.contentChanged)
        self.adminlabel.textChanged.connect(self.contentChanged)
        self.innerHtml.textChanged.connect(self.contentChanged)

    def setSite(self, site):
        self.site = site

    def setSlide(self, slide):
        self.slide = slide
        self.source.setText(slide.src)
        if slide.src:
            self.image.setImage(QImage(slide.src))
        else:
            self.image.setImage(QImage(":/images/image_placeholder.png"))
        self.innerHtml.setPlainText(html.unescape(slide._text))
        self.adminlabel.setText(slide._adminlabel)
        self.changed = False

    def closeEditor(self):
        if self.changed:
            self.slide.src = self.source.text()
            self.slide._text = html.escape(self.innerHtml.toPlainText())
            self.slide._adminlabel = self.adminlabel.text()
        self.closes.emit()

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
        if not fileName:
            return

        # copy file to assets dir
        info = QFileInfo(fileName)
        name = info.fileName().replace(" ", "_")
        path = os.path.join(self.site.source_path, "assets", "images",  name)
        self.source.setText(path)
        try:
            shutil.copy2(fileName, path)
        except shutil.SameFileError:
            pass # just ignore
        # also copy file to deploy dir for previews
        dpath = os.path.join(self.site.source_path, "docs", "assets", "images", name)
        shutil.copy2(fileName, dpath)

        self.image.setImage(QImage(path))
        self.contentChanged()
