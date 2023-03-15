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

from widgets.enums import RulerType
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QPoint
from PySide6.QtGui import QFont, QPen, QPainter

class Ruler(QWidget):
    def __init__(self, rulerType):
        QWidget.__init__(self)
        self.rulerType = rulerType
        self.origin = 0.
        self.rulerUnit = 1.
        self.rulerZoom = 1.
        self.mouseTracking = True
        self.drawText = False
        self.scaledRect = QRectF()
        self.setMouseTracking(True)
        txtFont = QFont("Arial", 7, 20)
        self.setFont(txtFont)
        self.cursorPos = QPoint()

    def setScaledRect(self, rect):
        self.scaledRect = rect
        self.update()

    def setCursorPos(self, cursorPos):
        self.cursorPos = cursorPos
        self.cursorPos.setX(self.cursorPos.x() - self.scaledRect.left())
        self.cursorPos.setY(self.cursorPos.y() - self.scaledRect.top())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.TextAntialiasing)
        pen = QPen(Qt.gray, 1)
        painter.setPen(pen)
        rulerRect = self.rect()
        self.drawMeter(painter, rulerRect, 4)

        painter.setOpacity(0.4)
        self.drawMousePosTick(painter)
        painter.setOpacity(1.0)

        starPt = rulerRect.bottomLeft() if self.rulerType == RulerType.Horizontal else rulerRect.topRight()
        endPt = rulerRect.bottomRight()
        if self.rulerType == RulerType.Horizontal:
            endPt.setX(rulerRect.bottomRight().x())
        else:
            endPt.setY(rulerRect.bottomRight().y())
        painter.setPen(QPen(Qt.gray, 2))
        painter.drawLine(starPt, endPt)

    def mouseMoveEvent(self, event):
        self.cursorPos = event.pos()
        self.update()
        super().mouseMoveEvent(event)

    def drawMeter(self, painter, rulerRect, div):
        widgetWidth = rulerRect.width() if self.rulerType == RulerType.Horizontal else rulerRect.height()
        scaledLength = self.scaledRect.width() if self.rulerType == RulerType.Horizontal else self.scaledRect.height()
        minScaledVal = self.scaledRect.left() if self.rulerType == RulerType.Horizontal else self.scaledRect.top()
        
        if scaledLength == 0:
            a = widgetWidth
        else:
            a = widgetWidth / scaledLength
        b = -(a * minScaledVal)

        unit = 0.0001
        unitSize = a * unit

        while unitSize < div * 7:
            unit *= 10
            unitSize = a * unit

        for i in [1, 2, 4]:
            if i == div:
                self.drawText = True
            else:
                self.drawText = False

            tickFact = i / div

            self.drawFromOrigin(painter, rulerRect, b, 0, widgetWidth, unit * tickFact, unitSize * tickFact, tickFact)
            self.drawFromOrigin(painter, rulerRect, b, widgetWidth, widgetWidth, unit * tickFact, unitSize * tickFact, tickFact)

    def drawFromOrigin(self, painter, rulerRect, origin, until, widgetWidth, unit, unitSize, tickFact):
        sens = origin < until
        isHorz = self.rulerType == RulerType.Horizontal
        nbreUnit = 0
        currentTickPos = origin

        x1, x2, y1, y2 = 0, 0, 0, 0

        while sens and currentTickPos <= until or not sens and currentTickPos >= until:
            if currentTickPos >= 0 and currentTickPos <= widgetWidth:
                x1 = currentTickPos if isHorz else rulerRect.right()
                y1 = rulerRect.bottom() if isHorz else currentTickPos
                x2 = currentTickPos if isHorz else rulerRect.right() - rulerRect.right()*tickFact
                y2 = rulerRect.bottom() - rulerRect.bottom()*tickFact if isHorz else currentTickPos

                painter.drawLine(x1, y1, x2, y2)

                if self.drawText:
                    xt = currentTickPos + 2 if isHorz else rulerRect.left() + 2
                    yt = rulerRect.top() + 11 if isHorz else currentTickPos - 5
                    painter.drawText(xt, yt, str(unit*nbreUnit))

            nbreUnit += 1
            currentTickPos = currentTickPos + unitSize if sens else currentTickPos - unitSize

    def drawMousePosTick(self, painter):
        if self.mouseTracking:
            starPt = self.cursorPos
            endPt = QPoint()
            if self.rulerType == RulerType.Horizontal:
                starPt.setY(self.rect().top())
                endPt.setX(starPt.x())
                endPt.setY(self.rect().bottom())
            else:
                starPt.setX(self.rect().left())
                endPt.setX(self.rect().right())
                endPt.setY(starPt.y())
            painter.drawLine(starPt, endPt)

