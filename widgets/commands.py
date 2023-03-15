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
from widgets.enums import EditMode
from widgets.rectangle import Rectangle
from widgets.ellipse import Ellipse
from PySide6.QtWidgets import QScrollBar, QTreeWidget, QGridLayout, QLabel, QToolButton, QMessageBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsScene, QGraphicsItem
from PySide6.QtCore import Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QUndoCommand, QScreen, QAction, QKeySequence, QActionGroup, QIcon, QImage, QColor, QPainter, QPen, QBrush
import resources


class AddItemCommand(QUndoCommand):
    def __init__(self, x, y, mode, fileName, scene):
        QUndoCommand.__init__(self)
        self.scene = scene
        self.item = None

        if mode == EditMode.ModeSelect:
            # ignore
            return
        elif mode == EditMode.ModeRectangle:
            self.item = Rectangle(self.scene)
            self.item.setId("Rectangle")
            self.item.setPen(QPen(Qt.black))
            self.item.setBrush(QBrush(Qt.blue))
            self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.item.setPos(x, y)
            self.item.setWidth(50)
            self.item.setHeight(50)
            self.setText("Add Rectangle")
        elif mode == EditMode.ModeEllipse:
            self.item = Ellipse(self.scene)
            self.item.setId("Ellipse")
            self.item.setPen(QPen(Qt.black))
            self.item.setBrush(QBrush(Qt.blue))
            self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.item.setPos(x, y)
            self.item.setWidth(50)
            self.item.setHeight(50)
            self.setText("Add Ellipse")

    #         case AnimationScene.EditMode.ModeText:
    #         {
    #             self.item = new Text("Lorem ipsum dolor", self.scene)
    #             self.item.setId("Text")
    #             self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
    #             self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
    #             self.item.setPos(x, y)
    #             setText(QObject.tr("Add Text"))
    #             break
    #         }
    #         case AnimationScene.EditMode.ModeBitmap:
    #         {
    #             self.item = new Bitmap(fileName, self.scene)
    #             self.item.setId("Bitmap")
    #             self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
    #             self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
    #             self.item.setPos(x, y)
    #             setText(QObject.tr("Add Bitmap"))
    #             break
    #         }
    #         case AnimationScene.EditMode.ModeSvg:
    #         {
    #             self.item = new Vectorgraphic(fileName, self.scene)
    #             self.item.setId("Vectorgraphic")
    #             self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
    #             self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
    #             self.item.setPos(x, y)
    #             setText(QObject.tr("Add Vectorgraphic"))
    #             break
    #         }
    #         case AnimationScene.EditMode.ModePlugin:
    #         {
    #             ItemInterface *item = Plugins.getItemPlugin(self.scene.actPluginName())
    #             self.item = item.getInstance(self.scene)
    #             self.item.setId(item.displayName())
    #             self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
    #             self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
    #             self.item.setPos(x, y)
    #             self.item.setPlayheadPosition(self.scene.playheadPosition())
    #             setText("Add " + item.displayName())
    #             break
    #         }
    #     }
    # }


    def undo(self):
        self.scene.clearSelection()
        self.scene.removeItem(self.item)
        self.item.setDeleted(True)
        #emit self.scene.itemRemoved(self.item)

    def redo(self):
        self.scene.clearSelection()
        self.scene.addItem(self.item)
        #emit self.scene.itemAdded(self.item)


class MoveItemCommand(QUndoCommand):
    def __init__(self, x, y, oldx, oldy, scene, item):
        QUndoCommand.__init__(self)
        self.x = x
        self.y = y
        self.oldx = oldx
        self.oldy = oldy
        self.time = scene.playheadPosition
        self.autokeyframes = scene.autokeyframes
        self.autotransition = scene.autotransition
        self.item = item
        self.keyframeLeft = None
        self.keyframeTop = None
        self.setText("Move " + item.typeName)

    def undo(self):
        self.item.setPos(self.oldx, self.oldy)
        #self.item.adjustKeyframes("left", self.oldx, self.time, self.autokeyframes, self.autotransition, self.keyframeLeft, True)
        #self.item.adjustKeyframes("top", self.oldy, self.time, self.autokeyframes, self.autotransition, self.keyframeTop, True)

    def redo(self):
        self.item.setPos(self.x, self.y)
        print("move")
        #self.item.adjustKeyframes("left", self.x, self.time, self.autokeyframes, self.autotransition, self.keyframeLeft, False)
        #self.item.adjustKeyframes("top", self.y, self.time, self.autokeyframes, self.autotransition, self.keyframeTop, False)
