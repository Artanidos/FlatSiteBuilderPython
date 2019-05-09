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
from widgets.flatbutton import FlatButton
from widgets.expander import Expander
from widgets.generator import Generator
from widgets.site import Site
from widgets.hyperlink import HyperLink
from widgets.dashboard import Dashboard
from widgets.contentlist import ContentList
from widgets.menulist import MenuList
from widgets.menueditor import MenuEditor
from widgets.content import ContentType
from widgets.webview import WebView
from widgets.webpage import WebPage
from widgets.plugins import Plugins
from widgets.sitewizard import SiteWizard
from widgets.contenteditor import ContentEditor
from widgets.themechooser import ThemeChooser
from widgets.sitesettingseditor import SiteSettingsEditor
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QUndoStack, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QPoint, QAbstractAnimation, QPropertyAnimation
from PyQt5.QtQml import QQmlEngine, QQmlComponent


class MainWindow(QMainWindow):
    siteLoaded = pyqtSignal(object)

    def __init__(self, install_directory):
        QMainWindow.__init__(self)
        #self.engine = QQmlEngine()
        self.site = None
        self.editor = ""
        self.install_directory = install_directory
        self.content_after_animation = ""
        self.default_path = ""
        self.method_after_animation = ""

        Generator.install_directory = install_directory

        self.initUndoRedo()
        self.initGui()
        self.readSettings()
        self.install()
        self.loadPlugins()

        if self.default_path:
            self.loadProject(self.default_path + "/Site.qml")

            # if site has never been generated (after install)
            # generate the site
            site = QDir(Generator.sitesPath() + "/" + self.site.title)
            if site.exists():
                gen = Generator()
                gen.generateSite(self, self.site)

        self.dashboard.setExpanded(True)
        self.showDashboard()
        self.statusBar().showMessage("Ready")

    def loadProject(self, filename):
        self.reloadProject(filename)

        # create temp dir for undo redo
        tempPath = self.site.source_path[self.site.source_path.rfind("/") + 1:]
        temp = QDir(QDir.tempPath() + "/FlatSiteBuilder")
        temp.mkdir(tempPath)
        temp.cd(tempPath)
        temp.mkdir("pages")
        temp.mkdir("posts")

    def initUndoRedo(self):
        self.undoStack = QUndoStack()
        temp = QDir(QDir.tempPath() + "/FlatSiteBuilder")
        if temp.exists():
            temp.removeRecursively()
        temp.setPath(QDir.tempPath())
        temp.mkdir("FlatSiteBuilder")

    def initGui(self):
        self.installEventFilter(self)
        self.dashboard = Expander("Dashboard", "./images/dashboard_normal.png", "./images/dashboard_hover.png", "./images/dashboard_selected.png")
        self.content = Expander("Content", "./images/pages_normal.png", "./images/pages_hover.png", "./images/pages_selected.png")
        self.appearance = Expander("Appearance", "./images/appearance_normal.png", "./images/appearance_hover.png", "./images/appearance_selected.png")
        self.settings = Expander("Settings", "./images/settings_normal.png", "./images/settings_hover.png", "./images/settings_selected.png")

        self.setWindowTitle(QCoreApplication.applicationName() + " " + QCoreApplication.applicationVersion())
        vbox = QVBoxLayout()
        vbox.addWidget(self.dashboard)
        vbox.addWidget(self.content)
        vbox.addWidget(self.appearance)
        vbox.addWidget(self.settings)
        vbox.addStretch()

        content_box = QVBoxLayout()
        pages_button = HyperLink("Pages")
        posts_button = HyperLink("Posts")
        content_box.addWidget(pages_button)
        content_box.addWidget(posts_button)
        self.content.addLayout(content_box)

        app_box = QVBoxLayout()
        themes_button = HyperLink("Themes")
        menus_button = HyperLink("Menus")
        self.theme_settings_button = HyperLink("Theme Settings")
        self.theme_settings_button.setVisible(False)
        app_box.addWidget(menus_button)
        app_box.addWidget(themes_button)
        app_box.addWidget(self.theme_settings_button)

        self.appearance.addLayout(app_box)

        scroll_content = QWidget()
        scroll_content.setLayout(vbox)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setMaximumWidth(200)
        scroll.setMinimumWidth(200)

        self.navigationdock = QDockWidget("Navigation", self)
        self.navigationdock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.navigationdock.setWidget(scroll)
        self.navigationdock.setObjectName("Navigation")

        self.addDockWidget(Qt.LeftDockWidgetArea, self.navigationdock)

        self.showDock = FlatButton("./images/edit_normal.png", "./images/edit_hover.png")
        self.showDock.setToolTip("Show Navigation")
        self.statusBar().addPermanentWidget(self.showDock)

        self.dashboard.expanded.connect(self.dashboardExpanded)
        self.dashboard.clicked.connect(self.showDashboard)
        self.content.expanded.connect(self.contentExpanded)
        self.content.clicked.connect(self.showPages)
        self.appearance.expanded.connect(self.appearanceExpanded)
        self.appearance.clicked.connect(self.showMenus)
        self.settings.expanded.connect(self.settingsExpanded)
        self.settings.clicked.connect(self.showSettings)
        menus_button.clicked.connect(self.showMenus)
        pages_button.clicked.connect(self.showPages)
        posts_button.clicked.connect(self.showPosts)
        themes_button.clicked.connect(self.showThemes)
        self.theme_settings_button.clicked.connect(self.showThemesSettings)
        self.showDock.clicked.connect(self.showMenu)
        self.navigationdock.visibilityChanged.connect(self.dockVisibilityChanged)

    def install(self):
        pass

    def loadPlugins(self):
        pass

    def showDashboard(self):
        if self.editor:
            self.method_after_animation = "showDashboard"
            self.editor.closeEditor()
            return

        db = Dashboard(self.site, self.default_path)
        db.loadSite.connect(self.loadProject)
        db.previewSite.connect(self.previewSite)
        db.publishSite.connect(self.publishSite)
        db.createSite.connect(self.createSite)
        db.buildSite.connect(self.buildSite)
        self.siteLoaded.connect(db.siteLoaded)
        self.setCentralWidget(db)

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def writeSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        if self.site:
            settings.setValue("lastSite", self.site.source_path)

    def readSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        geometry = settings.value("geometry", QByteArray())
        if geometry.isEmpty():
            availableGeometry = QApplication.desktop().availableGeometry(self)
            print(availableGeometry)
            self.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
            self.move(int((availableGeometry.width() - self.width() / 2)), int((availableGeometry.height() - self.height()) / 2))
        else:
            self.restoreGeometry(geometry)
            self.restoreState(settings.value("state"))
        self.default_path = settings.value("lastSite")

    def reloadProject(self, filename):
        engine = QQmlEngine()
        component = QQmlComponent(engine)
        component.loadUrl(QUrl(filename))
        self.site = component.create()
        if self.site is not None:
            self.site.setFilename(filename)
            self.site.setWindow(self)
        else:
            for error in component.errors():
                print(error.toString())

        self.site.loadMenus()
        self.site.loadPages()
        self.site.loadPosts()

        self.theme_settings_button.setVisible(False)
        Plugins.setActualThemeEditorPlugin("")
        for key in Plugins.themePluginNames():
            tei = Plugins.getThemePlugin(key)
            if tei:
                if tei.themeName() == self.site.theme():
                    Plugins.setActualThemeEditorPlugin(tei.className())
                    self.themeSettingsButton.setVisible(True)
                    break

        if not self.site.publisher:
            if len(Plugins.publishPluginNames()) > 0:
                self.site.setPublisher(Plugins.publishPluginNames[0])

        Plugins.setActualPublishPlugin(self.site.publisher)
        self.siteLoaded.emit(self.site)

    def dashboardExpanded(self, value):
        if value:
            self.content.setExpanded(False)
            self.appearance.setExpanded(False)
            self.settings.setExpanded(False)

    def contentExpanded(self, value):
        if value:
            self.dashboard.setExpanded(False)
            self.appearance.setExpanded(False)
            self.settings.setExpanded(False)

    def appearanceExpanded(self, value):
        if value:
            self.dashboard.setExpanded(False)
            self.content.setExpanded(False)
            self.settings.setExpanded(False)

    def settingsExpanded(self, value):
        if value:
            self.dashboard.setExpanded(False)
            self.content.setExpanded(False)
            self.appearance.setExpanded(False)

    def showMenus(self):
        if self.editor:
            self.method_after_animation = "showMenus"
            self.editor.closeEditor()
            return

        edit = MenuList(self, self.site)
        edit.editContent.connect(self.editMenu)
        self.setCentralWidget(edit)

    def showPages(self):
        if self.editor:
            self.method_after_animation = "showPages"
            self.editor.closeEditor()
            return

        list = ContentList(self.site, ContentType.PAGE)
        list.editContent.connect(self.editContent)
        self.setCentralWidget(list)

    def showPosts(self):
        if self.editor:
            self.method_after_animation = "showPosts"
            self.editor.closeEditor()
            return

        list = ContentList(self.site, ContentType.POST)
        list.editContent.connect(self.editContent)
        self.setCentralWidget(list)

    def showThemes(self):
        if self.editor:
            self.method_after_animation = "showThemes"
            self.editor.closeEditor()
            return

        tc = ThemeChooser(self, self.site)
        self.setCentralWidget(tc)

    def showThemesSettings(self):
        tei = Plugins.getThemePlugin(Plugins.actualThemeEditorPlugin())
        if tei:
            if self.editor:
                self.method_after_animation = "showThemesSettings"
                self.editor.closeEditor()
                return

            path = self.site.sourcePath()
            tei.setWindow(self)
            tei.setSourcePath(path)
            self.setCentralWidget(tei)
        else:
            self.statusBar().showMessage("Unable to load plugin " + Plugins.actualThemeEditorPlugin())

    def showSettings(self):
        if self.editor:
            self.method_after_animation = "showSettings"
            self.editor.closeEditor()
            return

        sse = SiteSettingsEditor(self, self.site)
        self.setCentralWidget(sse)

    def showMenu(self):
        self.navigationdock.setVisible(True)

    def dockVisibilityChanged(self, visible):
        self.showDock.setVisible(not visible)

    def previewSite(self, content):
        if self.editor and content:
            self.contentAfterAnimation = content
            self.editor.closeEditor()
            return

        dir = self.install_directory + "/sites"
        path = QDir(dir + "/" + self.site.title())
        if not content:
            if self.site.pages().count() > 0:
                content = self.site.pages()[0]
                for c in self.site.pages():
                    if c.url() == "index.html":
                        content = c
                        break
            elif self.site.posts().count() > 0:
                content = self.site.posts()[0]

        if content:
            file = content.url()

            QWebEngineSettings.defaultSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

            self.webView = WebView()
            webPage = WebPage(QWebEngineProfile.defaultProfile(), self.webView)
            self.webView.setPage(webPage)
            self.webView.loadFinished.connect(self.webViewLoadFinished)
            self.webView.setUrl(QUrl("file:///" + path.absoluteFilePath(file)))
            self.setCursor(Qt.WaitCursor)
        else:
            self.statusBar().showMessage("Site has no pages or posts to preview.")

    def publishSite(self):
        pluginName = Plugins.actualPublishPlugin()
        pi = Plugins.getPublishPlugin(pluginName)
        if pi:
            self.setCentralWidget(pi)
            pi.setSitePath(self.site.deployPath())

    def createSite(self):
        wiz = SiteWizard(self.install_directory, parent=self)
        wiz.loadSite.connect(self.loadProject)
        wiz.buildSite.connect(self.buildSite)
        wiz.show()

    def buildSite(self):
        self.site.loadMenus()
        if len(self.site.pages) == 0 and len(self.site.posts) == 0:
            self.statusBar().showMessage("Site has no pages or posts to build.")
        else:
            gen = Generator()
            gen.generateSite(self, self.site)
            self.statusBar().showMessage(self.site.title + " has been generated")

    def editMenu(self, item):
        menu = item.data(Qt.UserRole)
        me = MenuEditor(self, menu, self.site)
        self.editor = me
        list = self.centralWidget()
        if list:
            list.registerMenuEditor(me)
            list.editedItemChanged.connect(self.editedItemChanged)

        self.editor.closes.connect(self.editorClosed)
        self.editor.contentChanged.connect(self.menuChanged)
        self.animate(item)

    def editContent(self, item):
        content = item.data(Qt.UserRole)
        self.editor = ContentEditor(self, self.site, content)
        self.siteLoaded.connect(self.editor.siteLoaded)
        self.editor.closes.connect(self.editorClosed)
        self.animate(item)

    def animate(self, item):
        panel = self.centralWidget()
        self.list = item.tableWidget()
        self.row = item.row()

        # create a cell widget to get the right position in the table
        self.cellWidget = QWidget()
        self.list.setCellWidget(self.row, 1, self.cellWidget)
        pos = self.cellWidget.mapTo(panel, QPoint(0, 0))

        self.editor.setParent(panel)
        self.editor.move(pos)
        self.editor.resize(self.cellWidget.size())
        self.editor.show()

        self.animation = QPropertyAnimation(self.editor, "geometry".encode("utf-8"))
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(pos.x(), pos.y(), self.cellWidget.size().width(), self.cellWidget.size().height()))
        self.animation.setEndValue(QRect(0, 0, panel.size().width(), panel.size().height()))
        self.animation.start()

    def eventFilter(self, watched, event):
        if watched == self and event.type() == QEvent.Resize and self.editor:
            w = self.centralWidget()
            if w:
                self.editor.resize(w.size())
        return False

    def editorClosed(self):
        pos = self.cellWidget.mapTo(self.centralWidget(), QPoint(0, 0))
        # correct end values in case of resizing the window
        self.animation.setStartValue(QRect(pos.x(), pos.y(), self.cellWidget.size().width(), self.cellWidget.size().height()))
        self.animation.finished.connect(self.animationFineshedZoomOut)
        self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.start()

    def animationFineshedZoomOut(self):
        self.list.removeCellWidget(self.row, 1)
        del self.animation

        # in the case self.editor was a MenuEditor, we have to unregister it in the MenuList
        # should be refactored some day :-)
        list = self.centralWidget()
        if list is MenuEditor:
            list.unregisterMenuEditor()

        del self.editor
        self.editor = None

        if self.method_after_animation == "showDashboard":
            self.showDashboard()
            self.method_after_animation = ""
        elif self.method_after_animation == "showSettings":
            self.showSettings()
        elif self.method_after_animation == "showThemesSettings":
            self.showThemesSettings()
        elif self.method_after_animation == "showThemes":
            self.showThemes()
        elif self.method_after_animation == "showMenus":
            self.showMenus()
        elif self.method_after_animation == "showPages":
            self.showPages()
        elif self.method_after_animation == "showPosts":
            self.showPosts()

        if self.content_after_animation:
            self.previewSite(self.content_after_animation)
            self.content_after_animation = None

    def contentChanged(self, content):
        self.list.item(self.row, 1).setText(content.title())
        self.list.item(self.row, 2).setText(content.source())
        self.list.item(self.row, 3).setText(content.layout())
        self.list.item(self.row, 4).setText(content.author())
        self.list.item(self.row, 5).setText(content.date().toString("dd.MM.yyyy"))

    def menuChanged(self, menu):
        self.list.item(self.row, 1).setText(menu.name())

    def editedItemChanged(self, item):
        # self will happen, if the MenuList.reloadMenu() has been called by the undo.command
        self.list = item.tableWidget()
        self.row = item.row()
        self.cellWidget = QWidget()
        self.list.setCellWidget(self.row, 1, self.cellWidget)
