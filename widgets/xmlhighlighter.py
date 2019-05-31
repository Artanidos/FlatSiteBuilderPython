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

from widgets.hyperlink import HyperLink
from widgets.flatbutton import FlatButton
from widgets.animateableeditor import AnimateableEditor
from widgets.section import Section
from widgets.text import Text
from widgets.pageeditor import PageEditor
from widgets.sectioneditor import SectionEditor
from widgets.roweditor import RowEditor
from widgets.columneditor import ColumnEditor
from widgets.elementeditor import ElementEditor, Mode
from widgets.content import ContentType
from PyQt5.QtWidgets import QUndoStack, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QUrl, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from enum import Enum


ENTITY = 0
TAG = 1
CODE = 2
COMMENT = 3
LAST_CONSTRUCT = COMMENT


NORMAL_STATE = -1
IN_COMMENT = 0
IN_TAG = 1
IN_VAR = 2
IN_LOOP = 3


class XmlHighlighter(QSyntaxHighlighter):

    def __init__(self, parent = None):
        super(XmlHighlighter, self).__init__(parent)

        self.formats = [0] * (LAST_CONSTRUCT + 1)
        entityFormat = QTextCharFormat()
        entityFormat.setForeground(QColor(0, 128, 0))
        entityFormat.setFontWeight(QFont.Normal)
        self.setFormatFor(ENTITY, entityFormat)

        tagFormat = QTextCharFormat()
        tagFormat.setForeground(QColor("#f0e68c"))
        tagFormat.setFontWeight(QFont.Normal)
        self.setFormatFor(TAG, tagFormat)

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#87ceeb"))
        commentFormat.setFontItalic(True)
        self.setFormatFor(COMMENT, commentFormat)

        codeFormat = QTextCharFormat()
        codeFormat.setForeground(QColor("#ff9e00"))
        self.setFormatFor(CODE, codeFormat)

    def setFormatFor(self, construct, format):
        self.formats[construct] = format
        self.rehighlight()

    def formatFor(self, construct):
        return self.formats[construct]

    def highlightBlock(self, text):
        state = self.previousBlockState()
        length = len(text)
        start = 0
        pos = 0

        while pos < length:
            if state == IN_VAR:
                start = pos
                while pos < length:
                    if text[pos:pos + 2] == "":
                        pos += 2
                        state = NORMAL_STATE
                        break
                    else:
                        pos = pos + 1
                self.setFormat(start, pos - start, self.formats[CODE])

            elif state == IN_LOOP:
                start = pos
                while pos < length:
                    if text[pos: pos + 2] == "%":
                        pos += 2
                        state = NORMAL_STATE
                        break
                    else:
                        pos = pos + 1
                self.setFormat(start, pos - start, self.formats[CODE])

            elif state == IN_COMMENT:
                start = pos
                while pos < length:
                    if text[pos: pos + 3] == "-->":
                        pos += 3
                        state = NORMAL_STATE
                        break
                    else:
                        pos = pos + 1
                self.setFormat(start, pos - start, self.formats[COMMENT])

            elif state == IN_TAG:
                quote = 0
                start = pos
                while pos < length:
                    ch = text[pos]
                    if quote == 0:
                        if ch == "\"" or ch == '"':
                            quote = ch
                        elif ch == '>':
                            pos = pos + 1
                            state = NORMAL_STATE
                            break
                    elif ch == quote:
                        quote = 0
                    pos = pos + 1
                self.setFormat(start, pos - start, self.formats[TAG])

            else:
                while pos < length:
                    ch = text[pos]
                    if ch == '<':
                        if text[pos: pos + 4] == "<!--":
                            state = IN_COMMENT
                        else:
                            state = IN_TAG
                        break
                        
                    elif ch == '&':
                        start = pos
                        while pos < length and text[pos] != '':
                            pos = pos + 1
                                
                        self.setFormat(start, pos - start, self.formats[ENTITY])
                    elif ch == "":
                        if text[pos: pos + 2] == "":
                            state = IN_VAR
                            break
                        elif text[pos: pos + 2] == "%":
                            state = IN_LOOP
                            break
                        pos = pos + 1
                        break
                    else:
                        pos = pos +1

        self.setCurrentBlockState(state)
        
