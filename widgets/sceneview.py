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
from widgets.ruler import Ruler
from widgets.enums import RulerType
from PySide6.QtWidgets import QGridLayout, QMessageBox, QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsView
from PySide6.QtCore import Signal, Qt, QUrl, QRectF, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon, QPalette
import resources


class SceneView(QGraphicsView):
    def __init__(self, scene):
        QGraphicsView.__init__(self, scene)
        self.scene = scene
        self.setMouseTracking(True)
        self.setViewportMargins(20, 20, 0, 0)
        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)

        self.horizontalRuler = Ruler(RulerType.Horizontal)
        self.verticalRuler = Ruler(RulerType.Vertical)

        self.corner = QWidget()
        self.corner.setBackgroundRole(QPalette.Window)
        self.corner.setFixedSize(20, 20)
        gridLayout.addWidget(self.corner, 0, 0)
        gridLayout.addWidget(self.horizontalRuler, 0, 1)
        gridLayout.addWidget(self.verticalRuler, 1, 0)
        gridLayout.addWidget(self.viewport(), 1, 1)

        self.setLayout(gridLayout)

    def showRulers(self, mode):
        self.setViewportMargins(mode * 20, mode * 20, 0, 0)
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
        pt = self.mapToScene(event.pos())
        self.horizontalRuler.setCursorPos(pt.toPoint())
        self.verticalRuler.setCursorPos(pt.toPoint())
        super().mouseMoveEvent(event)