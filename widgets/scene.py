#############################################################################
# Copyright (C) 2023 CrowdWare
#
# self file is part of AnimationMaker.
#
#  AnimationMaker is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  AnimationMaker is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AnimationMaker.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from PySide6.QtCore import Property
from PySide6.QtQuick import QQuickItem
from PySide6.QtQml import QQmlProperty


class Scene(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._fps = 24
        self._width = 1200
        self._height = 720
        self._filename = ""
        self._isChanged = False

    @Property(int)
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps):
        self._fps = fps

    @Property(int)
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @Property(int)
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    def setFilename(self, name):
        self._filename = name

    def filename(self):
        return self._filename

    def isChanged(self):
        return self._isChanged
    
    def setPlayheadPosition(self, pos):
        # simulate animation
        for item in self.childItems():
            x = QQmlProperty(item, "x")
            val = x.read()
            x.write(val + 2)