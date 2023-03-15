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
from widgets.functions import timeString
from PySide6.QtWidgets import QScrollBar, QTreeWidget, QGridLayout, QLabel, QToolButton, QMessageBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsScene
from PySide6.QtCore import Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon, QImage, QColor, QPainter
import resources

#define SCROLL_OFFSET 20
#define VALUE_OFFSET 5

class PlayHead(QWidget):
    valueChanged = Signal(int)
    def __init__(self):
        QWidget.__init__(self)
        self.image = QImage(":/images/playhead.png")
        self.pressed = False
        self.value = 0
        self.horizontalScrollPos = 0
        self.setMinimumHeight(35)

    def paintEvent(self, pe):
        gray = QColor(64, 66, 68)
        width = self.size().width()
        height = self.size().height()
        offset = self.horizontalScrollPos * 20

        painter = QPainter(self)
        font = painter.font()
        font.setPixelSize(10)
        painter.setFont(font)
        painter.setPen(Qt.white)
        fm = painter.fontMetrics()
        for i in range(0 - offset,  width, 20):
            painter.drawLine(i, 12, i, 13)
        for i in range(0 - offset, width, 100):
            painter.drawLine(i, 12, i, 20)
            if i > 0:
                posString = timeString((i + offset) * 5, False)
                width = fm.horizontalAdvance(posString)
                painter.drawText(i - width / 2, 0, width, fm.height(), 0, posString)

        painter.setPen(QColor(41, 41, 41))
        painter.fillRect(0, 22, width, height, gray)
        painter.drawRect(0, 22, width - 1, height - 1)
        painter.drawImage(self.value / 5 - 4 - offset, 17, self.image)

    def setValue(self, value):
        self.value = value
        self.update() 
        self.valueChanged.emit(value)