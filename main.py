#############################################################################
# Copyright (C) 2023 CrowdWare
#
# This file is part of AnimationMaker.
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
import sys
import os
from widgets.mainwindow import MainWindow
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QPalette, QColor, QIcon, QFont
import main_rc


if __name__ == "__main__":
    QCoreApplication.setApplicationName("AnimationMaker")
    QCoreApplication.setApplicationVersion("2.0.0")
    QCoreApplication.setOrganizationName("CrowdWare")

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    
    font = QFont("Sans Serif", 10)
    app.setFont(font)

    p = app.palette()
    p.setColor(QPalette.Window, QColor(53, 53, 53))
    p.setColor(QPalette.WindowText, Qt.white)
    p.setColor(QPalette.Base, QColor(64, 66, 68))
    p.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    p.setColor(QPalette.ToolTipBase, Qt.white)
    p.setColor(QPalette.ToolTipText, Qt.black)
    p.setColor(QPalette.Text, Qt.white)
    p.setColor(QPalette.Button, QColor(53, 53, 53))
    p.setColor(QPalette.ButtonText, Qt.white)
    p.setColor(QPalette.BrightText, Qt.red)
    p.setColor(QPalette.Highlight, QColor("#45bbe6"))
    p.setColor(QPalette.HighlightedText, Qt.black)
    p.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    p.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    p.setColor(QPalette.Link, QColor("#bbb"))
    app.setPalette(p)
    app.setWindowIcon(QIcon(":/images/logo.svg"))        
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
