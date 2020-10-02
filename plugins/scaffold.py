#############################################################################
# Copyright (C) 2020 Olaf Japp
#
# self file is part of FlatSiteBuilder.
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

from widgets.interfaces import GeneratorInterface


class ScaffoldGenerator(GeneratorInterface):
    def __init__(self):
        self.class_name = "ScaffoldGenerator"
        self.display_name = "Scaffold"
        self.version = "1.0"
        self.normal_image = "scaffold_normal.png"
        self.hover_image = "scaffold_hover.png"
        self.pressed_image = "scaffold_pressed.png"

    def clicked(self):
        pass