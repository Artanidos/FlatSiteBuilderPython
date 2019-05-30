
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
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FlatSiteBuilder.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtCore import QDir, pyqtSlot
from PyQt5.QtGui import QPixmap


class InstallDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Init FlatSiteBuilder")
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        pathBox = QHBoxLayout()
        layout = QGridLayout()
        icon = QLabel()
        icon.setPixmap(QPixmap(":/images/icon_128.png"))
        self.path = QLineEdit()
        self.install_directory = QDir.homePath() + "/FlatSiteBuilder"
        self.path.setText(self.install_directory)
        choose = QPushButton("...")
        install = QPushButton("Install")
        install.setDefault(True)
        cancel = QPushButton("Cancel")
        pathBox.addWidget(self.path)
        pathBox.addWidget(choose)
        hbox.addStretch()
        hbox.addWidget(cancel)
        hbox.addWidget(install)
        vbox.addWidget(QLabel("FlatSiteBuilder is about to be set the working directory onto your computer."))
        vbox.addWidget(QLabel("Please choose a directory where the files should be stored."))
        vbox.addLayout(pathBox)
        vbox.addStretch()
        layout.addWidget(icon, 0, 0)
        layout.addLayout(vbox, 0, 1)
        layout.addLayout(hbox, 1, 0, 1, 2)
        self.setLayout(layout)

        install.clicked.connect(self.installClicked)
        cancel.clicked.connect(self.cancelClicked)
        choose.clicked.connect(self.chooseClicked)

    @pyqtSlot()
    def installClicked(self):
        install_dir = QDir(self.path.text())
        if install_dir.exists() and install_dir:
            rc = QMessageBox.question(self, "Warning", "The folder already exists and is not empty. Do you really want to use this directory for FlatSiteBuilder?")
            if rc != QMessageBox.Yes:
                return

        self.install_directory = self.path.text()
        self.close()

    @pyqtSlot()
    def cancelClicked(self):
        self.install_directory = ""
        self.close()

    @pyqtSlot()
    def chooseClicked(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setWindowTitle("Init FlatSiteBuilder to ...")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setDirectory(self.path.text())
        if dialog.exec_():
            fileName = dialog.selectedFiles()[0]

        if not fileName:
            return
        self.install_directory = fileName
        self.path.setText(self.install_directory)
