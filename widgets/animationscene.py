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
from widgets.rectangle import Rectangle
from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsScene, QGraphicsItem
from PySide6.QtCore import Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon, QColor, QBrush, QPen
import resources


class ItemType(Enum):
    TypeItem = 0
    TypeRectangle = 1
    TypeEllipse = 2
    TypeText = 3
    TypeBitmap = 4
    TypeSvg = 5


class EditMode(Enum):
    ModeSelect = 0
    ModeRectangle = 1
    ModeEllipse = 2
    ModeText = 3
    ModeBitmap = 4
    ModeSvg = 5
    ModePlugin = 6


class AnimationScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.rect = None
        self.blackSelectionRect = None
        self.whiteSelectionRect = None
        self.autokeyframes = False
        self.autotransitions = False
        self.initialize()

    def registerUndoStack(self, undostack):
        self.undoStack = undostack

    def initialize(self):
        self.setSceneRect(0, 0, 1200, 720)
        self.editMode = EditMode.ModeSelect
        self.fps = 24
        self.copy = None
        self.playheadPosition = 0
        self.movingItem = None
        self.scaling = 1
        self.addBackgroundRect()

    def addBackgroundRect(self):
        self.rect = Rectangle(self, isSceneRect=True)
        self.rect.setId("Scene")
        self.rect.setPos(0,0)
        self.rect.setWidth(self.width())
        self.rect.setHeight(self.height())
        self.backgroundColor = QColor("#404244")
        self.rect.setBrush(QBrush(QColor(self.backgroundColor)))
        self.rect.setPen(QPen(QColor("#000000")))
        self.addItem(self.rect)

    def reset(self):
        self.clear()
        self.initialize()
        self.undoStack.clear()

    def setEditMode(self, mode):
        self.editMode = mode

    def setEditMode(self, pluginName):
        self.editMode = EditMode.ModePlugin
        self.actPluginName = pluginName

    def setFileVersion(self, version): 
        self.fileVersion = version

    def fps(self):
        return self.fps

    def setFps(self, value):
        self.fps = value

    def setWidth(self, value):
        self.setSceneRect(0, 0, value, height())
        self.rect.setRect(0,0,value, height()) 
        #emit sizeChanged(value, height())

    def setHeight(self, value):
        self.setSceneRect(0, 0, self.width(), value)
        self.rect.setRect(0, 0, self.width(), value)
        #emit sizeChanged(width(), value)

    def backgroundColor(self): 
        return self.backgroundColor

    def setBackgroundColor(self, value):
        self.backgroundColor = value
        self.rect.setBrush(QBrush(QColor(self.backgroundColor)))
        #emit backgroundColorChanged(value)

    def backgroundRect(self):
        return self.rect

    def playheadPosition(self):
        return self.playheadPosition

    def setCursor(self, cursor):
        self.rect.setCursor(cursor)
    
    def copyItem(self):
        if self.selectedItems().count() == 0:
            return

        self.copy = self.selectedItems().first()

    def pasteItem(self):
        if self.copy == None:
            return

        self.copy.setSelected(False)
        if self.copy.type() == Rectangle.Type:
            r = Rectangle(self)
            r.setPos(self.copy.pos().x() + 10, self.copy.pos().y() + 10)
            r.setWidth(self.copy.rect().width())
            r.setHeight(self.copy.rect().height())
            r.setId("Rectangle")
            r.setPen(self.copy.pen())
            r.setBrush(self.copy.brush())
            r.setFlag(QGraphicsItem.ItemIsMovable, True)
            r.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.copyKeyframes(r)
            self.addItem(r)
            #emit itemAdded(r)
            
        # elif self.copy.type() == Ellipse.Type:
        #     e = Ellipse(self)
        #     e.setPos(self.copy.pos().x() + 10, self.copy.pos().y() + 10)
        #     e.setWidth(self.copy.rect().width())
        #     e.setHeight(self.copy.rect().height())
        #     e.setId("Ellipse")
        #     e.setPen(self.copy.pen())
        #     e.setBrush(self.copy.brush())
        #     e.setFlag(QGraphicsItem::ItemIsMovable, true)
        #     e.setFlag(QGraphicsItem::ItemIsSelectable, true)
        #     self.copyKeyframes(e)
        #     self.addItem(e)
        #     #emit itemAdded(e)
            
            
        # elif self.copy.type() == Text.Type:
        #     cpy = dynamic_cast<Text*>(self.copy)
        #     t = Text(cpy.text(), this)
        #     t.setId("Text")
        #     t.setPos(self.copy.pos().x() + 10, self.copy.pos().y() + 10)
        #     t.setFlag(QGraphicsItem::ItemIsMovable, true)
        #     t.setFlag(QGraphicsItem::ItemIsSelectable, true)
        #     t.setTextColor(cpy.textColor())
        #     t.setFont(cpy.font())
        #     t.setScale(cpy.xscale(), cpy.yscale())
        #     self.copyKeyframes(t)
        #     self.addItem(t)
        #     #emit itemAdded(t)
           
        # elif self.copy.type() == Bitmap.Type:
        #     bm = dynamic_cast<Bitmap*>(self.copy)
        #     b = Bitmap(bm.getImage(), self)
        #     b.setId("Bitmap")
        #     b.setPos(self.copy.pos().x() + 10, self.copy.pos().y() + 10)
        #     b.setWidth(bm.rect().width())
        #     b.setHeight(bm.rect().height())
        #     b.setFlag(QGraphicsItem::ItemIsMovable, true)
        #     b.setFlag(QGraphicsItem::ItemIsSelectable, true)
        #     b.setScale(bm.xscale(), bm.yscale())
        #     self.copyKeyframes(b)
        #     self.addItem(b)
        #     #emit itemAdded(b)
            
        # elif self.copy.type() == Vectorgraphic.Type:
        #     vg = dynamic_cast<Vectorgraphic*>(self.copy)
        #     v = Vectorgraphic(vg.getData(), self)
        #     v.setId("Vectorgraphic")
        #     v.setPos(self.copy.pos().x() + 10, self.copy.pos().y() + 10)
        #     v.setFlag(QGraphicsItem::ItemIsMovable, true)
        #     v.setFlag(QGraphicsItem::ItemIsSelectable, true)
        #     v.setScale(vg.xscale(), vg.yscale())
        #     self.copyKeyframes(v)
        #     self.addItem(v)
        #     #emit itemAdded(v)
   

    def deleteItem(self, item):
        pass

    def autokeyframes(self):
        return self.autokeyframes

    def setAutokeyframes(self, value):
        self.autokeyframes = value

    def autotransition(self):
        return self.autotransitions

    def setAutotransition(self, value):
        self.autotransitions = value

    def undoStack(self):
        return self.undoStack

    def actPluginName(self):
        return self.actPluginName

    def exportXml(self, fileName, exportAll = True):
        pass

    def importXml(self, fileName):
        pass

    def scaling(self):
        return self.scaling

    def setScaling(self, scaling):
        self.scaling = scaling

    def addNewImage(self, filename, mode):
        pass

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() != Qt.LeftButton:
            return
        #if self.editMode == EditMode.ModeSelect:
        #     self.movingItem = None
        #     handle = None
        #     mousePos = QPointF(mouseEvent.buttonDownScenePos(Qt.LeftButton).x(), mouseEvent.buttonDownScenePos(Qt.LeftButton).y())
        #     itemList = self.items(mousePos)
        #     for item in itemList:
        #         if item is ItemHandle:
        #             break
        #         self.movingItem = item
        #         if self.movingItem and self.movingItem.isSceneRect():
        #             self.movingItem = None

        #         if self.movingItem:
        #             self.oldPos = self.movingItem.pos()
        #             break
                
        #     if not self.movingItem# and not handle:
        #         self.blackSelectionRect = self.addRect(0, 0, 1, 1, QPen(QColor("#000000")))
        #         self.blackSelectionRect.setPos(mousePos)
        #         self.whiteSelectionRect = self.addRect(1, 1, 1, 1, QPen(QColor("#ffffff")))
        #         self.whiteSelectionRect.setPos(mousePos)
        #    QGraphicsScene.mousePressEvent(mouseEvent)
            
        #else:
        #    addCommand = AddItemCommand(mouseEvent.scenePos().x(), mouseEvent.scenePos().y(), self.editMode, None, self)
        #    self.undoStack.push(addCommand)

    def mouseMoveEvent(self, mouseEvent):
        pass
        # if self.editMode == EditMode.ModeSelect and self.blackSelectionRect:
        #     self.blackSelectionRect.setRect(0, 0, mouseEvent.lastScenePos().x() - self.blackSelectionRect.pos().x(), mouseEvent.lastScenePos().y() - self.blackSelectionRect.pos().y())
        #     self.whiteSelectionRect.setRect(1, 1, mouseEvent.lastScenePos().x() - self.blackSelectionRect.pos().x(), mouseEvent.lastScenePos().y() - self.blackSelectionRect.pos().y())
        #QGraphicsScene.mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self,  mouseEvent):
        pass
        # if self.editMode == EditMode.ModeSelect and self.blackSelectionRect:
        #     itemList = self.items(self.blackSelectionRect.pos().x(), self.blackSelectionRect.pos().y(), self.blackSelectionRect.rect().width(), self.blackSelectionRect.rect().height(), Qt::IntersectsItemShape, Qt::AscendingOrder)
        #     for item in itemList:
        #         item.setSelected(True)
                
        #     self.removeItem(self.blackSelectionRect)
        #     self.removeItem(self.whiteSelectionRect)
        #     del self.blackSelectionRect
        #     del self.whiteSelectionRect

        # if self.movingItem and mouseEvent.button() == Qt.LeftButton:
        #     if self.oldPos != self.movingItem.pos():
        #         cmd = MoveItemCommand(self.movingItem.x(), self.movingItem.y(), self.oldPos.x(), self.oldPos.y(), self, self.movingItem)
        #         self.undoStack.push(cmd)
        #     self.movingItem = None
        #QGraphicsScene.mouseReleaseEvent(mouseEvent)

    def keyPressEvent(self, e):
        pass
        # if self.selectedItems().count() == 0:
        #     return

        # itemList = self.selectedItems()
        # for item in itemList:
        #     if item is AnimationItem:
        #         if not item.isSceneRect():
        #             if e.key()== Qt.Key_Left:
        #                 cmd = MoveItemCommand(item.x() - 1, item.y(), item.x(), item.y(), self, item)
        #                 self.undoStack.push(cmd)
        #             elif e.key() == Qt.Key_Right:
        #                 cmd = MoveItemCommand(item.x() + 1, item.y(), item.x(), item.y(), self, item)
        #                 self.undoStack.push(cmd)
        #             elif e.key() == Qt.Key_Up:
        #                 cmd = MoveItemCommand(item.x(), item.y() - 1, item.x(), item.y(), self, item)
        #                 self.undoStack.push(cmd)
        #             elif e.key() == Qt.Key_Down:
        #                 cmd = MoveItemCommand(item.x(), item.y() + 1, item.x(), item.y(), self, item)
        #                 self.undoStack.push(cmd)
