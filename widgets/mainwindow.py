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
import inspect
import pathlib
import sys
import shutil
from importlib import import_module
from widgets.flatbutton import FlatButton
from widgets.expander import Expander
from widgets.generator import Generator
from widgets.hyperlink import HyperLink
from widgets.dashboard import Dashboard
from widgets.contentlist import ContentList
from widgets.menulist import MenuList
from widgets.menueditor import MenuEditor
from widgets.content import ContentType
from widgets.plugins import Plugins
from widgets.sitewizard import SiteWizard
from widgets.contenteditor import ContentEditor
from widgets.themechooser import ThemeChooser
from widgets.interfaces import ElementEditorInterface, ThemeEditorInterface, PublisherInterface
from widgets.sitesettingseditor import SiteSettingsEditor
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QUndoStack, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QPoint, QAbstractAnimation, QPropertyAnimation
from PyQt5.QtQml import QQmlEngine, QQmlComponent
from PyQt5.QtWebEngineWidgets import QWebEngineView
import resources

class MainWindow(QMainWindow):
    siteLoaded = pyqtSignal(object)

    def __init__(self):
        QMainWindow.__init__(self)
        self.site = None
        self.editor = ""
        self.install_directory = os.getcwd()

        # switch to install path in dev machine
        if "SourceCode" in self.install_directory:
            self.install_directory = "/home/art/FlatSiteBuilder"
        self.content_after_animation = ""
        self.default_path = ""
        self.method_after_animation = ""

        Generator.install_directory = self.install_directory

        self.initUndoRedo()
        self.initGui()
        self.readSettings()
        self.loadPlugins()

        if self.default_path:
            if self.loadProject(self.default_path + "/Site.qml"):
                gen = Generator()
                gen.generateSite(self, self.site)

        self.dashboard.setExpanded(True)
        self.showDashboard()
        self.statusBar().showMessage("Ready")

    def actualThemeChanged(self, themename):
        self.theme_settings_button.setVisible(False)
        for name in Plugins.themePluginNames():
            tei = Plugins.getThemePlugin(name)
            if tei:
                if tei.theme_name == themename:
                    self.theme_settings_button.setVisible(True)
                    break

    def loadProject(self, filename):
        self.default_path = filename[0:-9] # - /Site.qml
        if self.reloadProject(filename):
            # create temp dir for undo redo
            tempPath = self.site.source_path[self.site.source_path.rfind("/") + 1:]
            temp = QDir(QDir.tempPath() + "/FlatSiteBuilder")
            temp.mkdir(tempPath)
            temp.cd(tempPath)
            temp.mkdir("pages")
            temp.mkdir("posts")
            return True
        else:
            return False

    def initUndoRedo(self):
        self.undoStack = QUndoStack()
        temp = QDir(QDir.tempPath() + "/FlatSiteBuilder")
        if temp.exists():
            temp.removeRecursively()
        temp.setPath(QDir.tempPath())
        temp.mkdir("FlatSiteBuilder")

    def initGui(self):
        self.installEventFilter(self)
        self.dashboard = Expander("Dashboard", ":/images/dashboard_normal.png", ":/images/dashboard_hover.png", ":/images/dashboard_selected.png")
        self.content = Expander("Content", ":/images/pages_normal.png", ":/images/pages_hover.png", ":/images/pages_selected.png")
        self.appearance = Expander("Appearance", ":/images/appearance_normal.png", ":/images/appearance_hover.png", ":/images/appearance_selected.png")
        self.settings = Expander("Settings", ":/images/settings_normal.png", ":/images/settings_hover.png", ":/images/settings_selected.png")

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

        self.showDock = FlatButton(":/images/edit_normal.png", ":/images/edit_hover.png")
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

    def setCentralWidget(self, widget):
        # do not delete plugin editors
        old_widget = self.takeCentralWidget()
        if not isinstance(old_widget, PublisherInterface) and not isinstance(old_widget, ThemeEditorInterface):
            del old_widget
        super().setCentralWidget(widget)
        widget.show()

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
            self.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
            self.move(int(((availableGeometry.width() - self.width()) / 2)), int((availableGeometry.height() - self.height()) / 2))
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
            return False

        self.site.loadMenus()
        self.site.loadPages()
        self.site.loadPosts()

        self.theme_settings_button.setVisible(False)
        Plugins.setActualThemeEditorPlugin("")
        for key in Plugins.themePluginNames():
            tei = Plugins.getThemePlugin(key)
            if tei:
                if tei.theme_name == self.site.theme:
                    Plugins.setActualThemeEditorPlugin(tei.class_name)
                    self.theme_settings_button.setVisible(True)
                    break

        #if not self.site.publisher:
        #    if len(Plugins.publishPluginNames()) > 0:
        #        self.site.publisher = Plugins.publishPluginNames[0]

        Plugins.setActualPublishPlugin(self.site.publisher)
        self.siteLoaded.emit(self.site)
        return True

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

            path = self.site.source_path
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

    def previewSite(self, content = None):
        if self.editor and content:
            self.content_after_animation = content
            self.editor.closeEditor()
            return

        dir = os.path.join(self.default_path, "docs")
        if not content:
            if len(self.site.pages) > 0:
                content = self.site.pages[0]
                for c in self.site.pages:
                    if c.url == "index.html":
                        content = c
                        break
            elif len(self.site.posts) > 0:
                content = self.site.posts()[0]

        if content:
            file = content.url
            self.webView = QWebEngineView()
            self.webView.loadFinished.connect(self.webViewLoadFinished)
            url = pathlib.Path(os.path.join(dir, file)).as_uri()
            self.webView.setUrl(QUrl(url))
            self.setCursor(Qt.WaitCursor)
        else:
            self.statusBar().showMessage("Site has no pages or posts to preview.")

    def webViewLoadFinished(self, success):
        if success:
            self.setCentralWidget(self.webView)
            self.webView.loadFinished.disconnect(self.webViewLoadFinished)
        else:
            QMessageBox.warning(self, "FlatSiteBuilder", "Unable to open webpage.")
        self.setCursor(Qt.ArrowCursor)

    def publishSite(self):
        pluginName = Plugins.actualPublishPlugin()
        pi = Plugins.getPublishPlugin(pluginName)
        if pi:
            self.setCentralWidget(pi)
            pi.setSitePath(self.site.source_path)

    def createSite(self):
        wiz = SiteWizard(self.install_directory, parent = self)
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
        self.editor.preview.connect(self.previewSite)
        self.animate(item)

    def animate(self, item):
        panel = self.centralWidget()
        self.list = item.tableWidget()
        self.row = item.row()

        # create a cell widget to get the right position in the table
        self.cellWidget = QWidget()
        self.cellWidget.setMaximumHeight(0)
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
        # this will happen, if the MenuList.reloadMenu() has been called by the undo.command
        self.list = item.tableWidget()
        self.row = item.row()
        self.cellWidget = QWidget()
        self.list.setCellWidget(self.row, 1, self.cellWidget)

    def loadPlugins(self):
        # check if we are running in a frozen environment (pyinstaller --onefile)
        if getattr(sys, "frozen", False):
            bundle_dir = sys._MEIPASS
            # if we are running in a onefile environment, then copy all plugin to /tmp/...
            if bundle_dir != os.getcwd():
                os.mkdir(os.path.join(bundle_dir, "plugins"))
                for root, dirs, files in os.walk(os.path.join(os.getcwd(), "plugins")):
                    for file in files:
                        shutil.copy(os.path.join(root, file), os.path.join(bundle_dir, "plugins"))
                        print("copy", file)
                    break # do not copy __pycache__
        else:
            bundle_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))
        
        plugins_dir = os.path.join(bundle_dir, "plugins")
        for root, dirs, files in os.walk(plugins_dir):
            for file in files:
                modulename, ext = os.path.splitext(file)
                if ext == ".py":
                    module = import_module("plugins." + modulename)
                    for name, klass in inspect.getmembers(module, inspect.isclass):
                        if klass.__module__ == "plugins." + modulename:
                            instance = klass()
                            if isinstance(instance, ElementEditorInterface):
                                Plugins.addElementPlugin(name, instance)
                                instance.registerContenType()
                            elif isinstance(instance, ThemeEditorInterface):
                                Plugins.addThemePlugin(name, instance)
                            elif isinstance(instance, PublisherInterface):
                                Plugins.addPublishPlugin(name, instance)
            break # not to list __pycache__
