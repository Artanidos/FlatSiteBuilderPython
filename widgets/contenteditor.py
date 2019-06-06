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
from pathlib import Path
from widgets.hyperlink import HyperLink
from widgets.flatbutton import FlatButton
from widgets.animateableeditor import AnimateableEditor
from widgets.section import Section
from widgets.generator import Generator
from widgets.pageeditor import PageEditor
from widgets.roweditor import RowEditor
from widgets.columneditor import ColumnEditor
from widgets.elementeditor import ElementEditor, Mode
from widgets.content import ContentType
from widgets.plugins import Plugins
from widgets.commands import ChangeContentCommand, RenameContentCommand
from widgets.sectionpropertyeditor import SectionPropertyEditor
from PyQt5.QtWidgets import QUndoStack, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, QDate, QPoint, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, pyqtSignal
import resources

class ContentEditor(AnimateableEditor):
    contentChanged = pyqtSignal(object)
    preview = pyqtSignal(object)

    def __init__(self, win, site, content):
        AnimateableEditor.__init__(self)

        self.win = win
        self.site = site
        self.content = content
        self.is_new = False
        self.editor = None
        self.undoStack = QUndoStack()
        self.changed = False
        self.setAutoFillBackground(True)

        self.previewLink = HyperLink("")
        self.vbox = QVBoxLayout()
        self.layout = QGridLayout()
        self.titleLabel = QLabel()

        fnt = self.titleLabel.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        self.titleLabel.setFont(fnt)
        self.script = QPushButton("Page Script")
        self.title = QLineEdit()
        self.source = QLineEdit()
        self.source.setPlaceholderText("*.xml")
        self.excerpt = QLineEdit()
        self.date = QLineEdit()
        self.labelPermalink = QLabel("Permalink")
        self.labelTitle = QLabel("Title")
        self.labelAuthor = QLabel("Author")
        self.labelKeyword = QLabel("Keywords")
        self.labelLayout = QLabel("Layout")
        self.labelMenu = QLabel("Menu")
        self.author = QLineEdit()
        self.keywords = QLineEdit()
        self.menus = QComboBox()
        self.layouts = QComboBox()
        self.layouts.setMaximumWidth(100)

        for menu in self.site.menus.menus:
            self.menus.addItem(menu.name)

        for root, dirs, files in os.walk(os.path.join(self.site.source_path, "layouts")):
            for file in files:
                self.layouts.addItem(Path(file).stem)
        
        for root, dirs, files in os.walk(os.path.join(Generator.themesPath(), self.site.theme, "layouts")):
            for file in files:
                self.layouts.addItem(Path(file).stem)

        self.close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        self.close.setToolTip("Close Content Editor")
        self.undo = FlatButton(":/images/undo_normal.png", ":/images/undo_hover.png", "", ":/images/undo_disabled.png")
        self.redo = FlatButton(":/images/redo_normal.png", ":/images/redo_hover.png", "", ":/images/redo_disabled.png")
        self.undo.setToolTip("Undo")
        self.redo.setToolTip("Redo")
        self.undo.setEnabled(False)
        self.redo.setEnabled(False)
        hbox = QHBoxLayout()
        hbox.addWidget(self.undo)
        hbox.addWidget(self.redo)
        hbox.addWidget(self.close)

        self.scroll = QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.installEventFilter(self)
        self.layout.addWidget(self.titleLabel, 0, 0)
        self.layout.addWidget(self.previewLink, 0, 1)
        self.layout.addLayout(hbox, 0, 3)
        self.layout.addWidget(self.labelTitle, 1, 0)
        self.layout.addWidget(self.title, 2, 0)
        self.layout.addWidget(self.labelPermalink, 1, 1)
        self.layout.addWidget(self.source, 2, 1)
        self.layout.addWidget(self.labelAuthor, 3, 0)
        self.layout.addWidget(self.author, 4, 0)
        self.layout.addWidget(self.labelKeyword, 3, 1)
        self.layout.addWidget(self.keywords, 4, 1)
        self.layout.addWidget(self.labelMenu, 3, 2)
        self.layout.addWidget(self.menus, 4, 2)
        self.layout.addWidget(self.labelLayout, 3, 3)
        self.layout.addWidget(self.layouts, 4, 3)
        self.layout.addWidget(self.scroll, 7, 0, 1, 4)
        self.layout.addWidget(self.script, 8, 0, 1, 4)
        self.vbox.addLayout(self.layout)
        self.setLayout(self.vbox)

        if self.content.content_type == ContentType.POST:
            self.previewLink.setText("view post")
            self.excerptLabel = QLabel("Excerpt")
            self.layout.addWidget(self.excerptLabel, 5, 0)
            self.layout.addWidget(self.excerpt, 6, 0, 1, 2)
            self.datelabel = QLabel("Date")
            self.layout.addWidget(self.datelabel, 5, 2)
            self.layout.addWidget(self.date, 6, 2, 1, 2)
            self.filename = self.site.source_path + "/posts/" + content.source
        else:
            self.previewLink.setText("view page")
            self.filename = self.site.source_path + "/pages/" + content.source

        self.load()

        self.close.clicked.connect(self.closeEditor)
        self.title.editingFinished.connect(self.titleFinished)
        self.title.textChanged.connect(self.titleChanged)
        self.source.editingFinished.connect(self.sourceChanged)
        self.excerpt.editingFinished.connect(self.excerptChanged)
        self.date.editingFinished.connect(self.dateChanged)
        self.author.editingFinished.connect(self.authorChanged)
        self.keywords.editingFinished.connect(self.keywordsChanged)
        self.menus.currentTextChanged.connect(self.menuChanged)
        self.layouts.currentTextChanged.connect(self.layoutChanged)
        self.undoStack.canUndoChanged.connect(self.canUndoChanged)
        self.undoStack.canRedoChanged.connect(self.canRedoChanged)
        self.undoStack.undoTextChanged.connect(self.undoTextChanged)
        self.undoStack.redoTextChanged.connect(self.redoTextChanged)
        self.undo.clicked.connect(self.undoAction)
        self.redo.clicked.connect(self.redoAction)
        self.previewLink.clicked.connect(self.previewPage)

        #connect(self.script, SIGNAL(clicked()), self, SLOT(script()))

    def previewPage(self):
        self.preview.emit(self.content)

    def rowEdit(self, re):
        from widgets.rowpropertyeditor import RowPropertyEditor

        self.row_editor = re
        self.editor = RowPropertyEditor()
        self.editor.setRow(re.row)
        self.editor.close.connect(self.rowEditorClose)
        self.animate(re)

    def rowEditorClose(self):
        if self.editor and self.editor.changed:
            self.row_editor.load(self.editor.row)
            self.editChanged("Update Row")
        self.editorClosed()

    def canUndoChanged(self, can):
        self.undo.setEnabled(can)

    def canRedoChanged(self, can):
        self.redo.setEnabled(can)

    def undoTextChanged(self, text):
        self.undo.setToolTip("Undo " + text)

    def redoTextChanged(self, text):
        self.redo.setToolTip("Redo " + text)

    def undoAction(self):
        self.undoStack.undo()

    def redoAction(self):
        self.undoStack.redo()

    def menuChanged(self, menu):
        if menu != self.content.menu:
            self.content.menu = menu
            self.contentChanged.emit(self.content)
            self.editChanged("Menu Changed")

    def layoutChanged(self, layout):
        if layout != self.content.layout:
            self.content.layout = layout
            self.contentChanged.emit(self.content)
            self.editChanged("Layout Changed")

    def keywordsChanged(self):
        if self.keywords.text() != self.content.keywords:
            self.content.keywords = self.keywords.text()
            self.contentChanged.emit(self.content)
            self.editChanged("Keywords Changed")

    def authorChanged(self):
        if self.author.text() != self.content.author:
            self.content.author = self.author.text()
            self.contentChanged.emit(self.content)
            self.editChanged("Author Changed")

    def excerptChanged(self):
        if self.excerpt.text() != self.content.excerpt:
            self.content.excerpt = self.excerpt.text()
            self.contentChanged.emit(self.content)
            self.editChanged("Excerpt Changed")

    def dateChanged(self):
        if self.date.text() != self.content.date.toString("dd.MM.yyyy"):
            self.content.date = QDate.fromString(self.date.text(), "dd.MM.yyyy")
            self.contentChanged.emit(self.content)
            self.editChanged("Date Changed")

    def sourceChanged(self):
        if self.source.text() != self.content.source:
            oldname = self.filename
            self.content.source = self.source.text()
            if self.content.content_type == ContentType.PAGE:
                self.filename = self.site.source_path + "/pages/" + self.content.source
            else:
                self.filename = self.site.source_path + "/posts/" + self.content.source

            self.contentChanged.emit(self.content)

            renameCommand = RenameContentCommand(self, oldname, self.filename, "content file renamed")
            self.undoStack.push(renameCommand)

    def titleChanged(self, title):
        if self.is_new:
            source = title.lower().replace(" ", "_") + ".xml"
            self.source.setText(source)

    def titleFinished(self):
        if self.title.text() != self.content.title:
            if self.is_new:
                self.sourceChanged()
            self.content.title = self.title.text()
            self.contentChanged.emit(self.content)
            self.editChanged("Titel Changed")

    def sectionEdit(self, se):
        self.section_editor = se

        self.editor = SectionPropertyEditor()
        self.editor.setSection(se.section)
        self.editor.close.connect(self.sectionEditorClose)
        self.animate(se)

    def sectionEditorClose(self):
        if self.editor.changed:
            self.section_editor.setSection(self.editor.section)
            self.editChanged("Update Section")
        self.editorClosed()
    
    def load(self):
        from widgets.sectioneditor import SectionEditor
        self.content = self.site.loadContent(self.content.source, self.content.content_type)
        self.is_new = not self.content.title
        self.title.setText(self.content.title)
        self.source.setText(self.content.source)
        self.author.setText(self.content.author)
        self.keywords.setText(self.content.keywords)
        self.menus.setCurrentText(self.content.menu)
        self.layouts.setCurrentText(self.content.layout)
        if self.content.content_type == ContentType.POST:
            self.excerpt.setText(self.content.excerpt)
            self.date.setText(self.content.date.toString("dd.MM.yyyy"))

        pe = PageEditor()
        self.scroll.setWidget(pe)
        for item in self.content.items:
            if isinstance(item, Section):
                se = SectionEditor(item.fullwidth)
                se.load(item)
                pe.addSection(se)
            # todo other types

    def siteLoaded(self, site):
        self.site = site
        if self.content.contentType == ContentType.PAGE:
            for c in self.site.pages:
                if c.source == self.content.source:
                    self.title.setText(c.title)
        else:
            for c in self.site.posts:
                if c.source == self.content.source:
                    self.excerpt.setText(c.excerpt)
                    self.title.setText(c.title)

    def closeEditor(self):
        if self.editor:
            self.editor.closeEditor()
        self.closes.emit()

    def elementEdit(self, ee):
        self.element_editor = ee
        plugin_name = ""
        if ee.type:
            plugin_name = Plugins.getElementPluginByTagname(ee.type)
        if plugin_name:
            self.editor = Plugins.element_plugins[plugin_name]
        else:
            self.editor = Plugins.element_plugins["TextEditor"]
        self.editor.site = self.site
        self.editor.setContent(ee.getContent())
        self.editor.close.connect(self.editorClose)
        self.animate(ee)

    def animate(self, widget):
        self.sourcewidget = widget
        pos = widget.mapTo(self.scroll, QPoint(0,0))

        self.editor.setParent(self.scroll)
        self.editor.move(pos)
        self.editor.resize(widget.size())
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
        self.animw.setStartValue(widget.size().width())
        self.animw.setEndValue(self.scroll.size().width())
        self.animw.setTargetObject(self.editor)
        self.animw.setPropertyName("width".encode("utf-8"))
        self.animationgroup.addAnimation(self.animw)
        self.animh = QPropertyAnimation()
        self.animh.setDuration(300)
        self.animh.setStartValue(widget.size().height())
        self.animh.setEndValue(self.scroll.size().height())
        self.animh.setTargetObject(self.editor)
        self.animh.setPropertyName("height".encode("utf-8"))
        self.animationgroup.addAnimation(self.animh)
        self.animationgroup.finished.connect(self.animationFineshedZoomIn)
        self.animationgroup.start()
    
    def animationFineshedZoomIn(self):
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.title.setEnabled(False)
        self.author.setEnabled(False)
        self.keywords.setEnabled(False)
        self.menus.setEnabled(False)
        self.layouts.setEnabled(False)
        self.labelAuthor.setEnabled(False)
        self.labelKeyword.setEnabled(False)
        self.labelMenu.setEnabled(False)
        self.labelLayout.setEnabled(False)
        self.labelTitle.setEnabled(False)
        self.labelPermalink.setEnabled(False)
        self.previewLink.hide()
        self.undo.hide()
        self.redo.hide()
        self.close.hide()
        self.source.setEnabled(False)
        if self.content.content_type == ContentType.POST:
            self.excerpt.setEnabled(False)
            self.excerptLabel.setEnabled(False)
        self.animationgroup.finished.disconnect(self.animationFineshedZoomIn)
        
    def editorClose(self):
        if self.editor.changed:
            self.element_editor.setContent(self.editor.getContent())
            self.editChanged("Update Element")
        self.editorClosed()

    def editorClosed(self):
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        pos = self.sourcewidget.mapTo(self.scroll, QPoint(0,0))
        # correct end values in case of resizing the window
        self.animx.setStartValue(pos.x())
        self.animy.setStartValue(pos.y())
        self.animw.setStartValue(self.sourcewidget.size().width())
        self.animh.setStartValue(self.sourcewidget.size().height())
        self.animationgroup.setDirection(QAbstractAnimation.Backward)
        self.animationgroup.finished.connect(self.animationFineshedZoomOut)
        self.animationgroup.start()

    def animationFineshedZoomOut(self):
        from widgets.rowpropertyeditor import RowPropertyEditor
        from widgets.sectionpropertyeditor import SectionPropertyEditor

        self.title.setEnabled(True)
        self.source.setEnabled(True)
        self.author.setEnabled(True)
        self.keywords.setEnabled(True)
        self.menus.setEnabled(True)
        self.layouts.setEnabled(True)
        self.labelAuthor.setEnabled(True)
        self.labelKeyword.setEnabled(True)
        self.labelMenu.setEnabled(True)
        self.labelLayout.setEnabled(True)
        self.labelTitle.setEnabled(True)
        self.labelPermalink.setEnabled(True)
        self.previewLink.show()
        self.undo.show()
        self.redo.show()
        self.close.show()
        if self.content.content_type == ContentType.POST:
            self.excerpt.setEnabled(True)
            self.excerptLabel.setEnabled(True)
        del self.animationgroup
        self.editor.hide()
        # parent has to be set to NULL, otherwise the plugin will be dropped by parent
        self.editor.setParent(None)
        # only delete Row- and SectionPropertyEditor the other editors are plugins
        if isinstance(self.editor, RowPropertyEditor):
            del self.editor
        elif isinstance(self.editor, SectionPropertyEditor):
            self.editor.close.disconnect(self.sectionEditorClose)
            del self.editor
        self.editor = None

    def editChanged(self, text):
        changeCommand = ChangeContentCommand(self.win, self, text)
        self.undoStack.push(changeCommand)

    def save(self):
        with open(self.filename, "w") as f:
            f.write("import FlatSiteBuilder 2.0\n")
            
            taglist = []
            self.content.collectPluginNames(taglist)

            for tag in taglist:
                plugin_name = Plugins.getElementPluginByTagname(tag)
                plugin = Plugins.element_plugins[plugin_name]
                plugin.writeImportString(f)
            f.write("\n")
            self.content.save(f)

    def contentRenamed(self, name):
        self.filename = name
        base = os.path.basename(name)
        self.source.setText(base)
        self.content.source = base
