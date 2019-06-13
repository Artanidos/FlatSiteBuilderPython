
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
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FlatSiteBuilder.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import os
import datetime
from PyQt5.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QComboBox, QGridLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QDir
from PyQt5.QtGui import QPixmap
import resources
from widgets.site import Site
from widgets.menu import Menu
from widgets.menuitem import Menuitem
from widgets.content import Content
from widgets.section import Section
from widgets.row import Row
from widgets.column import Column

class SiteWizard(QWizard):
    loadSite = pyqtSignal(object)
    buildSite = pyqtSignal()

    def __init__(self, install_directory, parent = None):
        super(SiteWizard, self).__init__(parent)
        self.install_directory = install_directory
        self.addPage(IntroPage())
        self.addPage(SiteInfoPage(install_directory))
        self.addPage(ConclusionPage())
        self.setWindowTitle("Site Wizard")

    def accept(self):
        siteName = self.field("siteName")
        description = self.field("description")
        copyright = self.field("copyright")
        path = os.path.join(self.install_directory, "sources", siteName.lower())
        os.mkdir(path)
        os.mkdir(os.path.join(path, "pages"))
        os.mkdir(os.path.join(path, "posts"))
        os.mkdir(os.path.join(path, "content"))
        os.mkdir(os.path.join(path, "includes"))
        os.mkdir(os.path.join(path, "layouts"))
        os.mkdir(os.path.join(path, "assets"))
        os.mkdir(os.path.join(path, "assets", "css"))
        os.mkdir(os.path.join(path, "assets", "fonts"))
        os.mkdir(os.path.join(path, "assets", "js"))
        os.mkdir(os.path.join(path, "assets", "images"))

        site = Site()
        site.theme = self.field("theme")
        site.title = siteName
        if description:
            site.description = description
        if copyright:
            site.copyright = copyright
        site.source_path = path
        site.save()

        menu = Menu()
        menu.name = "default"
        item = Menuitem()
        item.title = "Index"
        item.url = "index.html"
        menu.addMenuItem(item)
        site.addMenu(menu)
        site.saveMenus()
        
        content = Content()
        content.title = "Index"
        content.menu = "default"
        content.author = "admin"
        content.layout = "default"
        content.date = datetime.datetime.now().strftime("%Y-%m-%d")
        section = Section()
        row = Row()
        column = Column()
        column.span = 12
        row.addColumn(column)
        section._items.append(row)
        content._items.append(section)
        content.save(os.path.join(path, "pages", "index.qml"))
        
        super().accept()

        self.loadSite.emit(path + "/Site.qml")
        self.buildSite.emit()


class IntroPage(QWizardPage):

    def __init__(self):
        QWizardPage.__init__(self)
        self.setTitle("Introduction")
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/wizard.png"))

        label = QLabel("This wizard will generate a skeleton website. "
                       "You simply need to specify the site name and set a "
                       "few options to produce the site.")
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class SiteInfoPage(QWizardPage):

    def __init__(self, install_directory):
        QWizardPage.__init__(self)
        self.install_directory = install_directory
        self.setTitle("Site Information")
        self.setSubTitle("Specify basic information about the site for which you "
                         "want to generate site files.")
        self.setPixmap(QWizard.LogoPixmap, QPixmap(":/images/icon64.png"))

        self.siteNameLabel = QLabel("&Site title:")
        self.siteNameLineEdit = QLineEdit()
        self.siteNameLabel.setBuddy(self.siteNameLineEdit)
        self.siteNameLineEdit.setPlaceholderText("Site title")

        self.descriptionLabel = QLabel("&Description:")
        self.descriptionLineEdit = QLineEdit()
        self.descriptionLabel.setBuddy(self.descriptionLineEdit)
        self.descriptionLineEdit.setPlaceholderText("Site description")

        self.copyrightLabel = QLabel("&Copyright")
        self.copyrightLineEdit = QLineEdit()
        self.copyrightLabel.setBuddy(self.copyrightLineEdit)
        self.copyrightLineEdit.setPlaceholderText("&copy 2019 Artanidos. All Rights Reserved.")

        self.themeLabel = QLabel("&Theme")
        self.theme = QComboBox()
        self.themeLabel.setBuddy(self.theme)

        themesDir = QDir(os.path.join(install_directory, "themes"))
        for theme in themesDir.entryList(QDir.NoDotAndDotDot | QDir.Dirs):
            self.theme.addItem(theme)

        self.registerField("siteName*", self.siteNameLineEdit)
        self.registerField("description", self.descriptionLineEdit)
        self.registerField("copyright", self.copyrightLineEdit)
        self.registerField("theme", self.theme, "currentText")

        self.warning = QLabel("")
        self.warning.setStyleSheet("QLabel  color : orange ")

        layout = QGridLayout()
        layout.addWidget(self.siteNameLabel, 0, 0)
        layout.addWidget(self.siteNameLineEdit, 0, 1)
        layout.addWidget(self.descriptionLabel, 1, 0)
        layout.addWidget(self.descriptionLineEdit, 1, 1)
        layout.addWidget(self.copyrightLabel, 2, 0)
        layout.addWidget(self.copyrightLineEdit, 2, 1)
        layout.addWidget(self.themeLabel, 3, 0)
        layout.addWidget(self.theme, 3, 1)
        layout.addWidget(self.warning, 4, 0, 1, 2)
        self.setLayout(layout)
        self.siteNameLineEdit.textChanged.connect(self.siteNameChanged)

    def siteNameChanged(self, name):
        if os.path.isdir(os.path.join(self.install_directory, "sources", name.lower())):
            self.warning.setText("WARNING<br/>A site with the name " + name.lower() + " already exists.<br/>If you continue self site will be overridden.")
        else:
            self.warning.setText("")


class ConclusionPage(QWizardPage):

    def __init__(self):
        QWizardPage.__init__(self)
        self.setTitle("Conclusion")
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/wizard.png"))

        self.label = QLabel("Click Finish to generate the site skeleton.")
        self.label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
