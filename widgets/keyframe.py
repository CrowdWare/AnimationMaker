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


class Keyframe(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._time = 0
        self._value = 0
        self._easing = 0
        self.next = None

    @Property(int)
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    @Property(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @Property(int)
    def easing(self):
        return self._easing

    @easing.setter
    def easing(self, easing):
        self._easing = easing
