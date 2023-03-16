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


class Keyframes(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._propertyname = ""
        self._type = ""

    @Property('QString')
    def propertyname(self):
        return self._propertyname

    @propertyname.setter
    def propertyname(self, propertyname):
        self._propertyname = propertyname

    @Property('QString')
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type