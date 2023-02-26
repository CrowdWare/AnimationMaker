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
from enum import Enum
from widgets.animationitem import AnimationItem
from PySide6.QtWidgets import QStyle, QMessageBox, QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsScene
from PySide6.QtCore import Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon, QPen
import resources

class Ellipse(AnimationItem):
    def __init__(self, scene):
        AnimationItem.__init__(self, scene)
        self.setRect(0, 0, 0, 0)
        self.typeName = "Ellipse"
        #self.type = Ellipse.Type

    def paint(self, paint, option, widget):
        paint.setPen(self.pen)
        paint.setBrush(self.brush)
        paint.drawEllipse(self.rect)

        if option.state & QStyle.State_Selected:
            self.drawHighlightSelected(paint, option)