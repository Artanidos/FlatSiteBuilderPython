#!/usr/bin/env python3

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

import sys
from widgets.installdialog import InstallDialog
from widgets.mainwindow import MainWindow
from PySide2.QtWidgets import QApplication, QStyleFactory
from PySide2.QtCore import Qt, QCoreApplication, QSettings
from PySide2.QtGui import QPalette, QColor, QIcon, QFont


if __name__ == "__main__":
    QCoreApplication.setApplicationName("FlatSiteBuilder")
    QCoreApplication.setApplicationVersion("2.0.0 (Python)")
    QCoreApplication.setOrganizationName("Artanidos")

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setStyleSheet("QPushButton:hover { color: #45bbe6 }")

    font = QFont("Sans Serif", 10)
    app.setFont(font)

    p = app.palette()
    p.setColor(QPalette.Window, QColor(53,53,53))
    p.setColor(QPalette.WindowText, Qt.white)
    p.setColor(QPalette.Base, QColor(64, 66, 68))
    p.setColor(QPalette.AlternateBase, QColor(53,53,53))
    p.setColor(QPalette.ToolTipBase, Qt.white)
    p.setColor(QPalette.ToolTipText, Qt.black)
    p.setColor(QPalette.Text, Qt.white)
    p.setColor(QPalette.Button, QColor(53,53,53))
    p.setColor(QPalette.ButtonText, Qt.white)
    p.setColor(QPalette.BrightText, Qt.red)
    p.setColor(QPalette.Highlight, QColor("#45bbe6"))
    p.setColor(QPalette.HighlightedText, Qt.black)
    p.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    p.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    p.setColor(QPalette.Link, QColor("#bbb"))
    app.setPalette(p)
    app.setWindowIcon(QIcon("images/logo.svg"))

    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
    install_directory = settings.value("installDirectory")
    if not install_directory:
        dlg = InstallDialog()
        dlg.exec()
        install_directory = dlg.install_directory
        if not install_directory:
            sys.exit(-1)
        settings.setValue("installDirectory", install_directory)
        del dlg

    win = MainWindow(install_directory)
    win.show()

    sys.exit(app.exec_())