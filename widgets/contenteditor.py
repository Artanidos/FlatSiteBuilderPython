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

from widgets.hyperlink import HyperLink
from widgets.flatbutton import FlatButton
from widgets.animateableeditor import AnimateableEditor
from widgets.content import ContentType
from PySide2.QtWidgets import QUndoStack, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PySide2.QtCore import Qt


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

        #foreach(Menu *menu, self.site.menus())
        #    self.menus.addItem(menu.name())
        #QDir layouts(self.site.sourcePath() + "/layouts")
        #foreach(QString file, layouts.entryList(QDir.Files))
        #    self.layouts.addItem(file.mid(0, file.indexOf(".html")))
        #QDir themelayouts(Generator.themesPath() + "/" + self.site.theme() + "/layouts")
        #foreach(QString file, themelayouts.entryList(QDir.Files))
        #    QString layout = file.mid(0, file.indexOf(".html"))
        #    if(self.layouts.findText(layout) < 0)
        #        self.layouts.addItem(layout)

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

        if self.content.contentType() == ContentType.POST:
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
        #connect(self.close, SIGNAL(clicked()), self, SLOT(closeEditor()))
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
        pass

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
