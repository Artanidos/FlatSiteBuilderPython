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

from django.template import Context, Engine
from django.utils.safestring import mark_safe
from widgets.content import ContentType
from widgets.plugins import Plugins
import os
import shutil
import sys
import html
from jinja2 import Template


class Generator:
    install_directory = ""

    def __init__(self):
        self.content = ""

    @staticmethod
    def themesPath():
        return os.path.join(Generator.install_directory, "themes")

    def generateSite(self, win, site, content_to_build = None):
        self.site = site
        site_dir = os.path.join(site.source_path, "docs")
        if not content_to_build:
            # clear directory
            for r, dirs, files in os.walk(site_dir):
                if not ".git" in r:
                    for f in files:
                        os.remove(os.path.join(site_dir, f))

                    for d in dirs:
                        shutil.rmtree(os.path.join(site_dir, d))

        pages = []
        posts = []
        menus = {}

        for content in site.pages:
            cm = {}
            cm["author"] = content.author
            cm["date"] = content.date
            cm["layout"] = content.layout
            cm["menu"] = content.menu
            cm["source"] = content.source
            cm["title"] = content.title
            cm["url"] = content.url
            if content.logo:
                cm["logo"] = content.logo
            else:
                cm["logo"] = site.logo
            cm["keywords"] = content.keywords
            cm["script"] = content.script

            for att, value in content.attributes.items():
                cm[att] = value

            pages.append(cm)

        for content in site.posts:
            cm = {}
            cm["author"] = content.author
            cm["date"] = content.date
            cm["excerpt"] = content.excerpt
            cm["layout"] = content.layout
            cm["menu"] = content.menu
            cm["source"] = content.source
            cm["title"] = content.title
            cm["url"] = content.url
            if content.logo:
                cm["logo"] = content.logo
            else:
                cm["logo"] = site.logo
            cm["keywords"] = content.keywords
            cm["script"] = content.script

            for att, value in content.attributes.items():
                cm[att] = value

            posts.append(cm)

        for menu in site.menus.menus:
            items = []
            for item in menu.items:
                menuitem = {}
                menuitem["title"] = item.title
                menuitem["url"] = item.url
                menuitem["icon"] = item.icon
                menuitem["attributes"] = mark_safe(item.attributes)

                subitems = []
                for subitem in item.items:
                    submenuitem = {}
                    submenuitem["title"] = subitem.title
                    submenuitem["url"] = subitem.url
                    submenuitem["icon"] = subitem.icon
                    submenuitem["attributes"] = mark_safe(subitem.attributes)
                    subitems.append(submenuitem)

                menuitem["items"] = subitems
                menuitem["hasItems"] = len(subitems) > 0
                items.append(menuitem)

            menus[menu.name] = items

        #qStableSort(posts.begin(), posts.end(), postLaterThan)

        sitevars = {}
        sitevars["title"] = site.title
        sitevars["description"] = site.description
        sitevars["theme"] = site.theme
        sitevars["copyright"] = site.copyright
        sitevars["source"] = site.source_path
        sitevars["keywords"] = site.keywords
        sitevars["author"] = site.author
        if site.logo:
            sitevars["logo"] = site.logo
        else:
            sitevars["logo"] = "logo.png"
        sitevars["pages"] = pages
        sitevars["posts"] = posts

        for att, value in site.attributes.items():
            sitevars[att] = value
        act = Plugins.actualThemeEditorPlugin()
        if act:
            tei = Plugins.getThemePlugin(Plugins.actualThemeEditorPlugin())
            if tei:
                tei.setWindow(win)
                tei.setSourcePath(site.source_path)
                themevars = tei.themeVars()
        else:
            themevars = {}

        context = Context()
        context["site"] = sitevars
        context["theme"] = themevars

        copy_assets = False
        if not os.path.exists(site_dir):
            os.mkdir(site_dir)
            copy_assets = True

        if not content_to_build or copy_assets:
            self.copytree(os.path.join(Generator.install_directory, "themes", site.theme, "assets"), os.path.join(site.source_path, "docs", "assets"))
            self.copytree(os.path.join(site.source_path, "assets"), os.path.join(site.source_path, "docs", "assets"))
            self.copytree(os.path.join(site.source_path, "content"), os.path.join(site.source_path, "docs"))

            for page in site.pages:
                self.generateContent(page, context, menus, site)
            for post in site.posts:
                self.generateContent(post, context, menus, site)
        else:
            self.generateContent(content_to_build, context, menus, site)

    def generateContent(self, content, context, menus, site):
        dirs = [
            os.path.join(self.site.source_path, "includes"),
            os.path.join(self.site.source_path, "layouts"),
            os.path.join(Generator.install_directory, "themes", self.site.theme, "layouts"),
            os.path.join(Generator.install_directory, "themes", self.site.theme, "includes")
        ]
        eng = Engine(dirs = dirs, debug=True)
        cm = {}

        if content.content_type == ContentType.POST:
            cm["excerpt"] = content.excerpt
        cm["author"] = content.author
        cm["date"] = content.date.toString("dd.MM.yyyy")
        cm["layout"] = content.layout
        cm["menu"] = content.menu
        cm["source"] = content.source
        cm["title"] = content.title
        cm["url"] = content.url
        if content.logo:
            cm["logo"] = content.logo
        else:
            cm["logo"] = site.logo
        cm["keywords"] = content.keywords
        cm["script"] = html.unescape(content.script)
        cm["menuitems"] = menus[content.menu]

        used_tag_list = []
        self.content = ""
        for item in content.items:
            self.content += item.getHtml()
            item.collectTagNames(used_tag_list)

        pluginvars = {}
        pluginvars["styles"] = ""
        pluginvars["scripts"] = ""
        for name in Plugins.elementPluginNames():
            plugin = Plugins.element_plugins[name]
            if plugin.tag_name in used_tag_list:
                
                plugin = Plugins.element_plugins[name]
                pluginvars["styles"] = pluginvars["styles"] + plugin.pluginStyles()
                pluginvars["scripts"] = pluginvars["scripts"] + plugin.pluginScripts()
                plugin.installAssets(os.path.join(site.source_path, "docs", "assets"))
        
        pluginvars["styles"] = mark_safe(pluginvars["styles"])
        pluginvars["scripts"] = mark_safe(pluginvars["scripts"])
        context["plugin"] = pluginvars

        layout = content.layout
        if not layout:
            layout = "default"

        context["page"] = cm

        ctx = {}
        ctx["page"] = content
        ctx["site"] = self.site
        tmp = Template(self.content)
        try:
            xhtml = tmp.render(ctx)
        except:
            type, value, traceback = sys.exc_info()
            msg = "Render content failed"
            print(msg, type, value, traceback)
            #todo: debug info from rendering
            return

        context["content"] = mark_safe(xhtml)

        outputfile = os.path.join(site.source_path, "docs", content.url)

        try:
            with open(outputfile, 'w') as f:
                f.write(eng.render_to_string(layout + ".html", context=context))
        except:
            type, value, traceback = sys.exc_info()
            msg = "Generate content failed: Unable to create file " + outputfile
            print(msg, type, value, traceback)

    def copytree(self, src, dst):
        names = os.listdir(src)
        if not os.path.exists(dst):
            os.makedirs(dst)
        for name in names:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            if os.path.isdir(srcname):
                self.copytree(srcname, dstname)
            else:
                shutil.copy2(srcname, dstname)
