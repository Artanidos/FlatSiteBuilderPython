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

from PyQt5.QtWidgets import QWidget, QTextBrowser, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import QFile
from widgets.interfaces import PublisherInterface

html = \
"<html>" \
"<head>" \
"</head>" \
"<body style=\"margin:10; background-color: #353535; color: #ffffff;\">" \
"<section class=\"container\">" \
"<div class=\"row\">" \
"<div class=\"col-md-12\">" \
"<h1>No Publisher</h1>" \
"<p>This plugin is only here to demonstrate the possibility of a publisher plugin.</p>" \
"<p>But you can publish your website manually using git with the following commands.</p>" \
"<p>&nbsp;</p>" \
"<p>Your content is stored at ~/FlatSiteBuilder/MyProject</p>" \
"<p>Please exchange <strong>MyProject</strong> with the project title and <strong>mycompany</strong> and <strong>myproject</strong> with the appropriate values.</p>" \
"<p>We assume that you already have a github repository for your project. If not you should create a repo prior to push content.</p>" \
"<h3>Publish site source</h3>" \
"<p style=\"font-family: Courier;\">" \
"    <ul>" \
"	    <li>cd ~/FlatSiteBuilder</li>" \
"		<li>cd sources</li>" \
"		<li>cd myproject</li>" \
"		<li>git init</li>" \
"		<li>git add .</li>" \
"		<li>git commit -m \"first commit\"</li>" \
"		<li>git remote add origin https://github.com/mycompany/myproject.git</li>" \
"		<li>git push -u origin master</li>" \
"	</ul>" \
"</p>" \
"<h3>Publish site content</h3>" \
"<p style=\"font-family: Courier;\">" \
"    <ul>" \
"	    <li>cd ~/FlatSiteBuilder</li>" \
"		<li>cd sources</li>" \
"		<li>cd MyProject</li>" \
"		<li>git init</li>" \
"		<li>git checkout --orphan gh-pages</li>" \
"		<li>git add .</li>" \
"		<li>git commit -m \"first commit\"</li>" \
"		<li>git remote add origin https://github.com/mycompany/myproject.git</li>" \
"		<li>git push origin gh-pages</li>" \
"	<ul>" \
"</p>" \
"" \
"<h3>Clone a website</h3>" \
"<p>If you already have published your website and want to download it from github use the following.</p>" \
"<p style=\"font-family: Courier;\">" \
"    <ul>" \
"	    <li>cd ~/FlatSiteBuilder</li>" \
"		<li>cd sources</li>" \
"		<li>git clone -b gh-pages https://github.com/mycompany/myproject.git MyProject</li>" \
"	<ul>" \
"</p>" \
"</div>" \
"</div>" \
"</section>" \
"</body>" \
"</html>"

class NoPublisher(PublisherInterface):
    def __init__(self):
        QWidget.__init__(self)
        self.display_name = "NoPublisher"
        self.browser = QTextBrowser()
        self.browser.setHtml(html)
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def setSitePath(self, path):
        pass