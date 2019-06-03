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
from widgets.text import Text
from widgets.generator import Generator
from widgets.pageeditor import PageEditor
from widgets.sectioneditor import SectionEditor
from widgets.roweditor import RowEditor
from widgets.columneditor import ColumnEditor
from widgets.texteditor import TextEditor
from widgets.elementeditor import ElementEditor, Mode
from widgets.content import ContentType
from widgets.commands import ChangeContentCommand
from PyQt5.QtWidgets import QUndoStack, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, QPoint, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation


class ContentEditor(AnimateableEditor):

    def __init__(self, win, site, content):
        AnimateableEditor.__init__(self)
        self.win = win
        self.site = site
        self.content = content
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

        self.close = FlatButton("./images/close_normal.png", "./images/close_hover.png")
        self.close.setToolTip("Close Content Editor")
        self.undo = FlatButton("./images/undo_normal.png", "./images/undo_hover.png", "", "./images/undo_disabled.png")
        self.redo = FlatButton("./images/redo_normal.png", "./images/redo_hover.png", "", "./images/redo_disabled.png")
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
            self.layout.addWidget(self.datelabel, 5, 2, 0)
            self.layout.addWidget(self.date, 6, 2, 1, 2)
            self.filename = self.site.source_path + "/posts/" + content.source
        else:
            self.previewLink.setText("view page")
            self.filename = self.site.source_path + "/pages/" + content.source

        self.load()

        self.close.clicked.connect(self.closeEditor)

        #connect(self.undo, SIGNAL(clicked()), self, SLOT(undo()))
        #connect(self.redo, SIGNAL(clicked()), self, SLOT(redo()))
        #connect(self.title, SIGNAL(editingFinished()), self, SLOT(titleChanged()))
        #connect(self.title, SIGNAL(textChanged(QString)), self, SLOT(titleChanged(QString)))
        #connect(self.source, SIGNAL(editingFinished()), self, SLOT(sourceChanged()))
        #connect(self.excerpt, SIGNAL(editingFinished()), self, SLOT(excerptChanged()))
        #connect(self.date, SIGNAL(editingFinished()), self, SLOT(dateChanged()))
        #connect(self.author, SIGNAL(editingFinished()), self, SLOT(authorChanged()))
        #connect(self.keywords, SIGNAL(editingFinished()), self, SLOT(keywordsChanged()))
        #connect(self.menus, SIGNAL(currentIndexChanged(QString)), self, SLOT(menuChanged(QString)))
        #connect(self.layouts, SIGNAL(currentIndexChanged(QString)), self, SLOT(layoutChanged(QString)))
        #connect(self.previewLink, SIGNAL(clicked()), self, SLOT(preview()))
        #connect(self.undoStack, SIGNAL(canUndoChanged(bool)), self, SLOT(canUndoChanged(bool)))
        #connect(self.undoStack, SIGNAL(canRedoChanged(bool)), self, SLOT(canRedoChanged(bool)))
        #connect(self.undoStack, SIGNAL(undoTextChanged(QString)), self, SLOT(undoTextChanged(QString)))
        #connect(self.undoStack, SIGNAL(redoTextChanged(QString)), self, SLOT(redoTextChanged(QString)))
        #connect(self.script, SIGNAL(clicked()), self, SLOT(script()))

    def load(self):
        pe = PageEditor()
        self.scroll.setWidget(pe)
        for item in self.content.items:
            if isinstance(item, Section):
                se = SectionEditor(item.fullwidth)
                se.load(item)
                #se.setCssClass(stream.attributes().value("cssclass").toString())
                #se.setStyle(stream.attributes().value("style").toString())
                #se.setAttributes(stream.attributes().value("attributes").toString())
                #se.setId(stream.attributes().value("id").toString())
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
        #if Plugins.hasElementPlugin(ee.type()))
        #    self.editor = dynamic_cast<AnimateableEditor*>(Plugins.getElementPlugin(ee.type()))
        #else
        #    self.editor = dynamic_cast<AnimateableEditor*>(Plugins.getElementPlugin("TextEditor"))
        #    qDebug() << "Plugin for type " + ee.type() + " not loaded."
        self.editor = TextEditor()
        self.editor.setSite(self.site)
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
        self.animationgroup.finished.disconnect(self.animationFineshedZoomIn)
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
        self.editor.close.disconnect(self.editorClose)
        # only delete Row- and SectionPropertyEditor the other editor are plugins
        if isinstance(self.editor, RowPropertyEditor) or isinstance(self.editor, SectionPropertyEditor) or isinstance(self.editor, TextEditor):
            del self.editor
        self.editor = None

    def editChanged(self, text):
        changeCommand = ChangeContentCommand(self.win, self, text)
        self.undoStack.push(changeCommand)

    def save(self):
        with open(self.filename, "w") as f:
            f.write("import FlatSiteBuilder 2.0\n\n")
            self.content.save(f)
