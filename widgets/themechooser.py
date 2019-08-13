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
from widgets.undoableeditor import UndoableEditor
from widgets.generator import Generator
from widgets.flatbutton import FlatButton
from widgets.plugins import Plugins
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QRectF, QUrl
from PyQt5.QtGui import QPixmap, QPainter, QImage, QColor, QFont, QPen, QTextOption, QDesktopServices


class ThemeChooser(UndoableEditor):
    def __init__(self, win, site):
        UndoableEditor.__init__(self)

        self.win = win
        self.site = site
        self.themename = site.theme
        self.titleLabel.setText("Theme Chooser")
        self.themes = []
        self.filename = os.path.join(site.source_path, site.filename)
        self.themeLayout = QGridLayout()
        scrollContent = QWidget()
        scrollContent.setLayout(self.themeLayout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(scrollContent)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll, 1, 0, 1, 3)

        self.load()

    def save(self):
        self.site.theme = self.themename
        self.site.save()

        Plugins.setActualThemeEditorPlugin("")
        for key in Plugins.themePluginNames():
            tei = Plugins.getThemePlugin(key)
            if tei:
                if tei.theme_name == self.site.theme:
                    Plugins.setActualThemeEditorPlugin(tei.class_name)
                    #self.theme_settings_button.setVisible(True)
                    break


        self.win.actualThemeChanged(self.themename)
        self.win.statusBar().showMessage("Theme has been changed. The site should be rebuildet on the dashboard.")
        self.load()

    def load(self):
        #self.site.load()
        self.themename = self.site.theme
        self.themes.clear()

        for root, dirs, files in os.walk(Generator.themesPath()):
            for dir in dirs:
                theme = Theme()
                theme.name = dir
                pic_name = os.path.join(Generator.themesPath(), dir , "sample.png")
                if os.path.exists(pic_name):
                    theme.sample_pic = pic_name
                html_name = os.path.join(Generator.themesPath(), dir, "sample.html")
                if os.path.exists(html_name):
                    theme.sample_url = html_name
                theme.aktiv = self.site.theme == dir
                self.themes.append(theme)
            break
        
        # delete the previous theme widgets
        for row in range(self.themeLayout.rowCount()):
            for col in range(self.themeLayout.columnCount()):
                item = self.themeLayout.itemAtPosition(row, col)
                if item:
                    w = item.widget()
                    if w:
                        w.hide()
                        self.themeLayout.removeWidget(w)
                        del w

        # load the actual themes
        row = 0
        col = 1
        for theme in self.themes:
            tw = ThemeWidget(theme)
            if theme.aktiv:
                self.themeLayout.addWidget(tw, 0, 0)
            else:
                tw.themeChanged.connect(self.themechanged)
                self.themeLayout.addWidget(tw, row, col)
                col = col + 1
                if col > 1:
                    row = row + 1
                    col = 0
        
        vbox = QVBoxLayout()
        vbox.addStretch()
        self.themeLayout.addLayout(vbox, row + 1, 0)
        self.win.statusBar().showMessage("Themes have been loaded")

    def themechanged(self, themename):
        if self.themename != themename:
            self.themename = themename
            self.contentChanged("theme changed to " + themename)


class Theme:
    def __init__(self):
        self.name = ""
        self.sample_pic = ""
        self.sample_url = ""
        self.aktiv = False


class ThemeWidget(QWidget):
    themeChanged = pyqtSignal(str)

    def __init__(self, theme):
        QWidget.__init__(self)
        self.theme = theme
        self.themename = theme.name
        self.setMaximumWidth(400)
        picurl = ":/images/theme.png"
        self.url = theme.sample_url
        if theme.sample_pic:
            picurl = theme.sample_pic
        pic = FlatButton(picurl, picurl)
        map = QPixmap(400, 200)
        p = QPainter(map)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.drawImage(QRect(0,0, 400, 200), QImage(picurl))
        p.fillRect(0, 0, map.size().width(), map.size().height(), QColor(69,187,230, 125))
        if self.url:
            w = 100
            h = 30

            p.fillRect(QRect((400 - w) / 2, (200 - h) / 2, w, h), QColor(69, 187, 230, 255))
            p.drawRoundedRect(QRect((400 - w) / 2, (200 - h) / 2, w, h), 5, 5)
            font = QFont()
            font.setFamily("Arial")
            font.setBold(True)
            font.setPixelSize(20)
            p.setFont(font)
            p.setPen(QPen(Qt.black))
            p.drawText(QRectF(0, 0, 400, 200), "PREVIEW", QTextOption(Qt.AlignHCenter|Qt.AlignVCenter))

            pic.clicked.connect(self.clicked)
        else:
            pic.setCursor(Qt.ArrowCursor)
        del p

        pic.setHoverPixmap(map)
        pic.setMaximumSize(400, 200)
        pic.setScaledContents(True)
        if theme.aktiv:
            name = QLabel(theme.name.upper() + " (Aktiv)")
        else:
            name = QLabel(theme.name.upper())
        fnt = name.font()
        fnt.setPointSize(13)
        fnt.setBold(True)
        name.setFont(fnt)
        layout = QGridLayout()
        layout.addWidget(pic, 0, 0, 1, 2)
        layout.addWidget(name, 1, 0)
        if not theme.aktiv:
            activate = QPushButton("Activate")
            layout.addWidget(activate, 1, 1, 1, 1, Qt.AlignRight)
            activate.clicked.connect(self.activate)
        
        self.setLayout(layout)

    def clicked(self):
        QDesktopServices.openUrl(QUrl(self.url))

    def activate(self):
        self.themeChanged.emit(self.themename)
