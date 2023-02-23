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
from PySide6.QtWidgets import QGridLayout, QMessageBox, QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsView
from PySide6.QtCore import Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
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
        #gridLayout.setMargin(0)

        #self.horizontalRuler = Ruler(Ruler.Horizontal)
        #self.verticalRuler = Ruler(Ruler.Vertical)

        self.corner = QWidget()
        self.corner.setBackgroundRole(QPalette.Window)
        self.corner.setFixedSize(20, 20)
        gridLayout.addWidget(self.corner, 0, 0)
        #gridLayout.addWidget(self.horizontalRuler, 0, 1)
        #gridLayout.addWidget(self.verticalRuler, 1, 0)
        gridLayout.addWidget(self.viewport(), 1, 1)

        self.setLayout(gridLayout)