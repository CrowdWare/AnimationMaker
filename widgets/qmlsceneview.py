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
from widgets.qmleditor import QmlEditor
from widgets.ruler import Ruler
from widgets.enums import RulerType
from widgets.animationscene import AnimationScene
from PySide6.QtWidgets import QWidget, QGridLayout, QScrollArea
from PySide6.QtCore import QUrl, QRectF, QPoint
from PySide6.QtGui import QPalette
from PySide6.QtQuickWidgets import QQuickWidget

class QmlSceneView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.scene = None
        grid = QGridLayout()
        self.horizontalRuler = Ruler(RulerType.Horizontal)
        self.verticalRuler = Ruler(RulerType.Vertical)

        self.corner = QWidget()
        self.corner.setBackgroundRole(QPalette.Window)
        self.corner.setFixedSize(20, 20)
        grid.addWidget(self.corner, 0, 0)
        grid.addWidget(self.horizontalRuler, 0, 1)
        grid.addWidget(self.verticalRuler, 1, 0)
        self.view = QmlEditor(self)
        self.view.setMinimumSize(1200, 720)
        self.view.setResizeMode(QQuickWidget.ResizeMode.SizeViewToRootObject)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.view)
        grid.addWidget(self.scroll, 1, 1)
        self.setLayout(grid)
        self.showRulers(0)

    def grabImage(self):
        return self.view.grabFramebuffer()

    def load(self, filename):
        self.view.setSource(QUrl.fromLocalFile(filename))
        self.scene = self.view.rootObject()
        return self.scene

    def showRulers(self, mode):
        #self.setViewportMargins(mode * 20, mode * 20, 0, 0)
        self.corner.setVisible(mode)
        self.horizontalRuler.setVisible(mode)
        self.verticalRuler.setVisible(mode)

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        p1 = self.mapToScene(QPoint(0, 0))
        p2 = self.mapToScene(QPoint(self.viewport().width(), self.viewport().height()))

        if self.verticalScrollBar():
            p2.setX(p2.x() + self.verticalScrollBar().width())
        if self.horizontalScrollBar():
            p2.setY(p2.y() + self.horizontalScrollBar().height())
        r = QRectF(p1, p2)

        self.horizontalRuler.setScaledRect(r)
        self.verticalRuler.setScaledRect(r)


    def mouseMoveEvent(self, event):
        #pt = self.mapToScene(event.pos())
        #self.horizontalRuler.setCursorPos(pt.toPoint())
        #self.verticalRuler.setCursorPos(pt.toPoint())
        super().mouseMoveEvent(event)
  