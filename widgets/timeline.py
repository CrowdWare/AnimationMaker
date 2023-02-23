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
from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsScene
from PySide6.QtCore import Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon
import resources


class Timeline(QWidget):
    def __init__(self, scene):
        QWidget.__init__(self)
        self.scene = scene

    def setPlayheadPosition(self, pos):
        pass