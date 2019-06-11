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
import shutil
from widgets.interfaces import ThemeEditorInterface
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, qVersion, QFile, QDir, qRegisterResourceData, qUnregisterResourceData, pyqtProperty
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QLineEdit, QCheckBox, QPushButton, QLabel, QFileDialog, QListWidget, QListWidgetItem
from PyQt5.QtQml import qmlRegisterType
from widgets.imageselector import ImageSelector
from widgets.flatbutton import FlatButton
from widgets.item import Item


class DefaultThemeEditor(ThemeEditorInterface):
    def __init__(self):
        ThemeEditorInterface.__init__(self)
        self.class_name = "DefaultThemeEditor"
        self.display_name = "Default Theme Editor"
        self.theme_name = "default"
        self.version = "1.0"
        self.win = None
        self.isHidePoweredByEnabled = False

        self.hidePoweredBy = QCheckBox("Hide powered by FlatSiteBuilder in footer")
        self.titleLabel.setText("Default Theme Settings")
        vbox = QVBoxLayout()
        vbox.addStretch()

        self.layout.addWidget(self.hidePoweredBy, 1, 0, 1, 3)
        self.layout.addWidget(QLabel(""), 2, 0)
        self.layout.addWidget(QLabel("Looks a bit empty here, right?"), 3, 0, 1, 3)
        self.layout.addWidget(QLabel("This is just a sample theme editor."), 4, 0, 1, 3)
        self.layout.addWidget(QLabel("To give theme creators an overview of what is possible."), 5, 0, 1, 3)
        self.layout.addLayout(vbox, 6, 0) # for stretching only

        self.hidePoweredBy.stateChanged.connect(self.showPoweredChanged)

    def setWindow(self, win):
        self.win = win

    def showPoweredChanged(self):
        if self.isHidePoweredByEnabled != self.hidePoweredBy.isChecked():
            self.contentChanged("show powered by changed")

    def load(self):
        pass
        # set default values in case load failes
        #self.isHidePoweredByEnabled = False

        #QFile theme(m_filename);
        #if (!theme.open(QIODevice::ReadOnly))
        #{
        #    m_win->statusBar()->showMessage("Unable to open " + m_filename);
        #    return;
        #}
        #QXmlStreamReader xml(&theme);
        #if(xml.readNextStartElement())
        #{
        #    if(xml.name() == "Settings")
        #    {
        #        m_isHidePoweredByEnabled = xml.attributes().value("hidePoweredBy").toString() == "true";
        #        m_hidePoweredBy->setChecked(m_isHidePoweredByEnabled);
        #    }
        #}
        #theme.close();

    def save(self):
        pass
        #QFile file(m_filename);
        #if(!file.open(QFile::WriteOnly))
        #{
        #    m_win->statusBar()->showMessage("Unable to open file " + m_filename);
        #    return;
        #}
        #QXmlStreamWriter xml(&file);
        #xml.setAutoFormatting(true);
        #xml.writeStartDocument();
        #xml.writeStartElement("Settings");
        #xml.writeAttribute("hidePoweredBy", (m_hidePoweredBy->isChecked() ? "true" : "false"));
        #xml.writeEndElement();
        ##xml.writeEndDocument();
        #file.close();
        #
        #m_win->statusBar()->showMessage("Theme settings have been saved.");

    def themeVars(self):
        #load();
        vars = {}
        vars["hidePoweredBy"] = self.isHidePoweredByEnabled
        return vars

