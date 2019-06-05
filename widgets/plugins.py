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


class Plugins:
    actual_theme_editor_plugin = None
    actual_publish_plugin = None
    theme_plugins = {}
    publish_plugins = {}
    element_plugins = {}
    used_plugins = []

    def __init__(self):
        pass

    @staticmethod
    def setActualThemeEditorPlugin(tep):
        Plugins.actual_theme_editor_plugin = tep

    @staticmethod
    def themePluginNames():
        return Plugins.theme_plugins.keys()

    @staticmethod
    def publishPluginNames():
        return Plugins.publish_plugins.keys()

    @staticmethod
    def elementPluginNames():
        return Plugins.element_plugins.keys()

    @staticmethod
    def setActualPublishPlugin(ap):
        Plugins.actual_publish_plugin = ap

    @staticmethod
    def addElementPlugin(name, plugin):
        Plugins.element_plugins[name] = plugin

    @staticmethod
    def addThemePlugin(name, plugin):
        Plugins.theme_plugins[name] = plugin

    @staticmethod
    def addPublishPlugin(name, plugin):
        Plugins.publish_plugins[name] = plugin

    @staticmethod
    def getElementPluginByTagname(tag):
        for name in Plugins.element_plugins.keys():
            plugin = Plugins.element_plugins[name]
            if plugin.tag_name == tag:
                return name
        return ""
