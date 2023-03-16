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
from widgets.keyframes import Keyframes
from PySide6.QtCore import Property, QEasingCurve
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
        self.setPlayheadPositionForItem(self, pos)

    def setPlayheadPositionForItem(self, item, pos):
        for item in item.childItems():
            for child in item.childItems():
                if isinstance(child, Keyframes):
                    first = child.childItems()[0]
                    found = None
                    keyframe = first
                    while keyframe and keyframe.next:
                        if (keyframe == first and pos < first.time) or keyframe.time <= pos:
                            found = keyframe
                            break
                        keyframe = keyframe.next
                    if found:
                        if child.type == "int":
                            if found.easing >= 0:
                                value = int(self.calculateValue(found, pos))
                            else:
                                value = found.value
                            prop = QQmlProperty(item, child.propertyname)
                            prop.write(value)
                        else:
                            print("type not supported yet", child.type)
                else:
                    self.setPlayheadPositionForItem(child, pos)

    def getProgressValue(self, keyframe, playheadPosition):
        easing = QEasingCurve(QEasingCurve.Type(keyframe.easing))
        progress = 1.0 / (keyframe.next.time - keyframe.time) * (playheadPosition - keyframe.time)
        return easing.valueForProgress(progress)
    
    def calculateValue(self, keyframe, playheadPosition):
        return keyframe.value + (keyframe.next.value - keyframe.value) / 1.0 * self.getProgressValue(keyframe, playheadPosition)
    
    def arrangeKeyframes(self):
        self.arrangeItemKeyframes(self)

    def arrangeItemKeyframes(self, item):
        for item in item.childItems():
            for child in item.childItems():
                if isinstance(child, Keyframes):
                    prev = child.childItems()[0]
                    for keyframe in child.childItems():
                        if keyframe != prev:
                            prev.next = keyframe
                            prev = keyframe
                else:
                    self.arrangeItemKeyframes(child)
    