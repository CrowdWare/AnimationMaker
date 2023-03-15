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
from PySide6.QtGui import QColor
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQml import QQmlProperty


class QmlEditor(QQuickWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        item = self.rootObject()
        child = item.childAt(event.position().x(), event.position().y())
        # if child:
        #     color = QQmlProperty(child, "color")
        #     color.write(QColor("#00FFFF"))
            
        #     x = QQmlProperty(child, "x")
        #     x.write(20)
        #     y = QQmlProperty(child, "y")
        #     y.write(20)
        return super().mousePressEvent(event)