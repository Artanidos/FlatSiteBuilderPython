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

import os
import shutil

from PyQt5.Qt import QDir, QUndoCommand
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QScrollArea, QTextEdit,
                             QUndoStack, QVBoxLayout)

from widgets.animateableeditor import AnimateableEditor
from widgets.columneditor import ColumnEditor
from widgets.content import ContentType
from widgets.elementeditor import ElementEditor, Mode
from widgets.flatbutton import FlatButton
from widgets.generator import Generator
from widgets.hyperlink import HyperLink
from widgets.pageeditor import PageEditor
from widgets.roweditor import RowEditor
from widgets.section import Section
from widgets.sectioneditor import SectionEditor
from widgets.text import Text


class ChangeContentCommand(QUndoCommand):
    file_version_number = 0

    def __init__(self, win, ce, text, parent = None):
        super().__init__(parent)
        self.win = win
        self.content_editor = ce
        ChangeContentCommand.file_version_number = ChangeContentCommand.file_version_number + 1
        self.setText(text)

        sitedir = self.content_editor.site.source_path[self.content_editor.site.source_path.rfind("/") + 1:]
        if self.content_editor.content.content_type == ContentType.PAGE:
            subdir = "/pages/"
        else: 
            subdir = "/posts/"
        self.temp_filename = QDir.tempPath() + "/FlatSiteBuilder/" + sitedir + subdir + self.content_editor.content.source + "." + str(ChangeContentCommand.file_version_number) + ".undo"
        self.redo_filename = QDir.tempPath() + "/FlatSiteBuilder/" + sitedir + subdir + self.content_editor.content.source + "." + str(ChangeContentCommand.file_version_number) + ".redo"

    def undo(self):

        if os.path.exists(self.content_editor.filename):
            os.remove(self.content_editor.filename)
        shutil.copy(self.temp_filename, self.content_editor.filename)
        self.content_editor.load()

        gen = Generator()
        gen.generateSite(self.win, self.content_editor.site, self.content_editor.content)

    def redo(self):
        if os.path.exists(self.redo_filename):
            if os.path.exists(self.content_editor.filename):
                os.remove(self.content_editor.filename)
            shutil.copy(self.redo_filename, self.content_editor.filename)
            self.content_editor.load()
        else:
            shutil.copy(self.content_editor.filename, self.temp_filename)
            self.content_editor.save()
            shutil.copy(self.content_editor.filename, self.redo_filename)
        
        gen = Generator()
        gen.generateSite(self.win, self.content_editor.site, self.content_editor.content)


class RenameContentCommand(QUndoCommand):

    def __init__(self, ce, oldname, newname, text, parent = None):
        super().__init__(parent)
        self.content_editor = ce
        self.oldname = oldname
        self.newname = newname
        self.setText(text)

    def undo(self):
        shutil.copy(self.newname, self.oldname)
        os.remove(self.newname)
        self.contentEditor.contentRenamed(self.oldname)

    def redo(self):
        if os.path.exists(self.newname):
            path = os.path.dirname(self.newname)
            basename, extension = os.path.splitext(self.newname)
            start = basename.find("(")
            end = basename.find(")")
            number = 0
            
            if start > 0 and end > start:
                number = int(basename[start + 1:end])
                base = basename[:start]
            else:
                base = basename
            while True:
                number = number + 1
                self.newname = os.path.join(path, base + "(" + str(number) + ")." + extension)
                if not os.path.exists(self.newname):
                    break
            
        shutil.copy(self.oldname, self.newname)
        os.remove(self.oldname)
        self.content_editor.contentRenamed(self.newname)
