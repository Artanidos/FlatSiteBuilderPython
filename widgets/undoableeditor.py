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

from widgets.flatbutton import FlatButton
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QGridLayout, QUndoStack, QUndoCommand
from PySide2.QtCore import QFileInfo, QDir, QFile


class UndoableEditor(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.filename = ""
        self.undoStack = QUndoStack()
        self.undo = FlatButton("./images/undo_normal.png", "./images/undo_hover.png", "", "./images/undo_disabled.png")
        self.redo = FlatButton("./images/redo_normal.png", "./images/redo_hover.png", "", "./images/redo_disabled.png")
        self.undo.setToolTip("Undo")
        self.redo.setToolTip("Redo")
        self.undo.setEnabled(False)
        self.redo.setEnabled(False)
        hbox = QHBoxLayout()
        hbox.addStretch(0)
        hbox.addWidget(self.undo)
        hbox.addWidget(self.redo)

        self.titleLabel = QLabel()
        fnt = self.titleLabel.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        self.titleLabel.setFont(fnt)
        self.layout = QGridLayout()
        self.layout.addWidget(self.titleLabel, 0, 0)
        self.layout.addLayout(hbox, 0, 2)
        self.setLayout(self.layout)

        #connect(self.redo, SIGNAL(clicked()), self, SLOT(redo()))
        #connect(self.undo, SIGNAL(clicked()), self, SLOT(undo()))
        #connect(self.undoStack, SIGNAL(canUndoChanged(bool)), self, SLOT(canUndoChanged(bool)))
        #connect(self.undoStack, SIGNAL(canRedoChanged(bool)), self, SLOT(canRedoChanged(bool)))
        #connect(self.undoStack, SIGNAL(undoTextChanged(QString)), self, SLOT(undoTextChanged(QString)))
        #connect(self.undoStack, SIGNAL(redoTextChanged(QString)), self, SLOT(redoTextChanged(QString)))

    def contentChanged(self, text):
        changeCommand = ChangeFileCommand(self, self.filename, text)
        self.undoStack.push(changeCommand)


class ChangeFileCommand(QUndoCommand):
    fileVersionNumber = 0

    def __init__(self, editor, filename, text):
        QUndoCommand.__init__(self)
        ChangeFileCommand.fileVersionNumber += 1
        self.editor = editor
        self.filename = filename
        self.setText(text)

        info = QFileInfo(filename)
        dir = info.dir().dirName()
        file = info.fileName()
        self.undoFilename = QDir.tempPath() + "/FlatSiteBuilder/" + dir + "/" + file + "." + str(ChangeFileCommand.fileVersionNumber) + ".undo"
        self.redoFilename = QDir.tempPath() + "/FlatSiteBuilder/" + dir + "/" + file + "." + str(ChangeFileCommand.fileVersionNumber) + ".redo"

    def undo(self):
        dest = QFile(self.filename)
        if dest.exists():
            dest.remove()
        QFile.copy(self.undoFilename, self.filename)
        self.editor.load()

    def redo(self):
        redo = QFile(self.redoFilename)
        if redo.exists():
            dest = QFile(self.filename)
            if dest.exists():
                dest.remove()
            QFile.copy(self.redoFilename, self.filename)
            self.editor.load()
        else:
            QFile.copy(self.filename, self.undoFilename)
            self.editor.save()
            QFile.copy(self.filename, self.redoFilename)
