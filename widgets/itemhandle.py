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
from widgets.playhead import PlayHead
import widgets.functions
from widgets.enums import MouseState
from PySide6.QtWidgets import QScrollBar, QTreeWidget, QGridLayout, QLabel, QToolButton, QMessageBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsScene, QGraphicsItem
from PySide6.QtCore import Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QRectF, QPointF, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon, QBrush, QColor
import resources


class ItemHandle(QGraphicsItem):
    def __init__(self, parent, corner: int, scaling: int):
        QGraphicsItem.__init__(parent)
        self.mouseDownX = 0
        self.mouseDownY = 0
        self.color = Qt.black
        self.pen = Qt.white
        self.corner = corner
        self.mouseButtonState = MouseState.kMouseReleased
        self.pen.setWidth(1)
        if scaling == 0:
            self.width = 18.0
            self.height = 18.0
        elif scaling == 1:
            self.width = 9.0
            self.height = 9.0
        elif scaling == 2:
            self.width = 4.5
            self.height = 4.5
        elif scaling == 3 or scaling == 4:
            self.width = 2.25
            self.height = 2.25

        self.setAcceptHoverEvents(True)
        self.setZValue(100)

        if corner in [0, 2]:
            self.setCursor(Qt.SizeFDiagCursor)
        elif corner in [1, 3]:
            self.setCursor(Qt.SizeBDiagCursor)
        elif corner in [4, 6]:
            self.setCursor(Qt.SizeVerCursor)
        elif corner in [5, 7]:
            self.setCursor(Qt.SizeHorCursor)

    def width(self):
        return self.width

    def setMouseState(self, s):
        self.mouseButtonState = s

    def getMouseState(self):
        return self.mouseButtonState

    def getCorner(self):
        return self.corner

    def mouseMoveEvent(self, event):
        event.setAccepted(False)

    def mousePressEvent(self, event):
        event.setAccepted(False)

    def mouseReleaseEvent(self, event ):
        event.setAccepted(True)

    def mousePressEvent(self, event ):
        event.setAccepted(False)

    def mouseMoveEvent(self, event ):
        event.setAccepted(False)

    def hoverLeaveEvent(self, event):
        self.color = Qt.black
        self.update(0, 0, self.width, self.height)

    def hoverEnterEvent(self, event):
        self.color = QColor(255, 127, 42)
        self.update(0, 0, self.width, self.height)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, item, widget):
        self.pen.setCapStyle(Qt.SquareCap)
        self.pen.setStyle(Qt.SolidLine)
        painter.setPen(self.pen)
        topLeft = QPointF(0, 0)
        bottomRight = QPointF(self.width, self.height)
        rect = QRectF(topLeft, bottomRight)
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.color)
        painter.drawRect(rect)
        painter.fillRect(rect,brush)
