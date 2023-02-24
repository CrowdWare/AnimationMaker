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
from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsScene, QGraphicsItem
from PySide6.QtCore import QRectF, Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon, QColor, QPen
import resources


class AnimationItem(QWidget, QGraphicsItem):
    def __init__(self, scene, isSceneRect):
        QWidget.__init__(self)
        QGraphicsItem.__init__(self)
        self.scene = scene
        self.isSceneRect = isSceneRect
        self.deleted = False
        self.hasHandles = False
        self.xscale = 1
        self.yscale = 1
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.shearX = 0.0
        self.shearY = 0.0
        self.rotationX = 0
        self.rotationY = 0
        self.rotationZ = 0
        self.originX = 0
        self.originY = 0
        self.opacity = 100
        self.keyframes = {}
        self.rect = QRectF(0,0,0,0)

        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # QAction *delAct = QAction(tr("Delete"), self)
        # delAct.setShortcut(tr("Delete"))
        # connect(delAct, SIGNAL(triggered()), this, SLOT(deleteItem()))

        # QAction *bringToFrontAct = new QAction("Bring to front", this)
        # connect(bringToFrontAct, SIGNAL(triggered()), this, SLOT(bringToFrontAction()))

        # QAction *sendToBackAct = new QAction("Send to back", this)
        # connect(sendToBackAct, SIGNAL(triggered()), this, SLOT(sendToBackAction()))

        # QAction *raiseAct = new QAction("Raise", this)
        # connect(raiseAct, SIGNAL(triggered()), this, SLOT(raiseAction()))

        # QAction *lowerAct = new QAction("Lower", this)
        # connect(lowerAct, SIGNAL(triggered()), this, SLOT(lowerAction()))

        # contextMenuActions.append(delAct)
        # contextMenuActions.append(bringToFrontAct)
        # contextMenuActions.append(sendToBackAct)
        # contextMenuActions.append(raiseAct)
        # contextMenuActions.append(lowerAct)

        # self.contextMenu = new QMenu()
        # self.contextMenu.addAction(delAct)
        # self.contextMenu.addSeparator()
        # self.contextMenu.addAction(bringToFrontAct)
        # self.contextMenu.addAction(raiseAct)
        # self.contextMenu.addAction(lowerAct)
        # self.contextMenu.addAction(sendToBackAct)
        # self.contextMenu.addSeparator()

    def setScene(self, scene):
        self.scene = scene

    def setId(self, id):
        self.id = id
        #emit idChanged(this, value)

    def setPen(self, pen):
        self.pen = pen
        self.update()
        #emit penChanged(m_pen.color())

    def setWidth(self, value):
        self.prepareGeometryChange()
        self.rect.setWidth(value)
        self.scaleObjects()
        self.update()
        self.setHandlePositions()
        #emit sizeChanged(value, rect().height())

    def setHeight(self, value):
        self.prepareGeometryChange()
        self.rect.setHeight(value)
        self.scaleObjects()
        self.update()
        self.setHandlePositions()
        #emit sizeChanged(rect().width(), value)

    def scaleObjects(self):
        pass

    def setHandlePositions(self):
        if not self.hasHandles:
            return

        halfwidth = self.handles[0].width() / 2.0
        self.handles[0].setPos(-halfwidth, -halfwidth)
        self.handles[1].setPos(self.rect().width() - halfwidth, -halfwidth)
        self.handles[2].setPos(self.rect().width() - halfwidth, self.rect().height() - halfwidth)
        self.handles[3].setPos(-halfwidth, self.rect().height() - halfwidth)
        self.handles[4].setPos(self.rect().width() / 2 - halfwidth, -halfwidth)
        self.handles[5].setPos(self.rect().width() - halfwidth, self.rect().height() / 2 - halfwidth)
        self.handles[6].setPos(self.rect().width() /2 - halfwidth, self.rect().height() - halfwidth)
        self.handles[7].setPos(- halfwidth, self.rect().height() / 2 - halfwidth)

        self.scene.update(self.x() - halfwidth - 5, self.y() - halfwidth - 5, self.x() + self.rect().width() + halfwidth * 2 + 5, self.y() + self.rect().height() + halfwidth * 2 + 5)

    def setBrush(self, brush):
        self.brush = brush
        self.update()

    def boundingRect(self):
        return self.rect


    def drawHighlightSelected(self, painter, option):
        itemPenWidth = self.pen.widthF()
        pad = itemPenWidth / 2
        penWidth = 0
        fgcolor = option.palette.windowText().color()
        bgcolor = QColor(0 if fgcolor.red() > 127 else 255, 0 if fgcolor.green() > 127 else 255, 0 if fgcolor.blue() > 127 else 255)

        painter.setOpacity(1.0)
        painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.boundingRect().adjusted(pad, pad, -pad, -pad))

        painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.boundingRect().adjusted(pad, pad, -pad, -pad))
