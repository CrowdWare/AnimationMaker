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
from PySide6.QtWidgets import QScrollBar, QTreeWidget, QGridLayout, QLabel, QToolButton, QMessageBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QApplication, QMenu, QToolBar, QGraphicsScene
from PySide6.QtCore import Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon
import resources


class Timeline(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.scene = None
        self.horizontalScrollPos = 0
        hbox = QHBoxLayout()
        revertButton = QToolButton()
        forwardButton = QToolButton()
        autokeyframeButton = QToolButton()
        autokeyframeButton.setCheckable(True)
        autokeyframeButton.setChecked(False)
        autokeyframeButton.setIcon(QIcon(":/images/autokeyframe.png"))
        autokeyframeButton.setToolTip("Auto keyframes")
        #connect(autokeyframeButton, SIGNAL(toggled(bool)), self, SLOT(autokeyframes(bool)))

        autotransitionButton = QToolButton()
        autotransitionButton.setCheckable(True)
        autotransitionButton.setChecked(False)
        autotransitionButton.setIcon(QIcon(":/images/autotransition.png"))
        autotransitionButton.setToolTip("Auto transitions")
        #connect(autotransitionButton, SIGNAL(toggled(bool)), self, SLOT(autotransitions(bool)))
        playButton = QToolButton()
        pauseButton = QToolButton()
        pauseButton.setVisible(False)
        self.time = QLabel()
        self.time.setText("0:00.0")

        playAct = QAction("Play", self)
        playAct.setIcon(QIcon(":/images/play.png"))
        playAct.setToolTip("Start the animation")
        #connect(playAct, SIGNAL(triggered()), self, SLOT(playAnimation()))

        pauseAct = QAction("Pause", self)
        pauseAct.setIcon(QIcon(":/images/pause.png"))
        pauseAct.setToolTip("Pause the animation")
        #connect(pauseAct, SIGNAL(triggered()), self, SLOT(pauseAnimation()))

        reverseAct = QAction("Reverse", self)
        reverseAct.setIcon(QIcon(":/images/reverse.png"))
        reverseAct.setToolTip("Reverse the animation")
        #connect(reverseAct, SIGNAL(triggered()), self, SLOT(revertAnimation()))

        forwardAct = QAction("Forward", self)
        forwardAct.setIcon(QIcon(":/images/forward.png"))
        forwardAct.setToolTip("Forward the animation")
        #connect(forwardAct, SIGNAL(triggered()), self, SLOT(forwardAnimation()))

        revertButton.setDefaultAction(reverseAct)
        playButton.setDefaultAction(playAct)
        pauseButton.setDefaultAction(pauseAct)
        forwardButton.setDefaultAction(forwardAct)

        hbox.addWidget(revertButton)
        hbox.addWidget(playButton)
        hbox.addWidget(pauseButton)
        hbox.addWidget(forwardButton)
        hbox.addStretch()
        hbox.addWidget(autokeyframeButton)
        hbox.addWidget(autotransitionButton)
        hbox.addSpacing(5)
        hbox.addWidget(self.time)
        layout = QGridLayout()
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.header().resizeSection(0, 205)
        self.tree.header().close()
        self.tree.setStyleSheet("QTreeWidget.item:has-children:!selected {background-color: #4c4e50} QTreeWidget.item:!selected { border-bottom: 1px solid #292929} QTreeView.branch:!selected {border-bottom: 1px solid #292929} QTreeWidget.branch:has-children:!selected {background-color: #4c4e50} QTreeWidget.branch:has-children:!has-siblings:closed, QTreeWidget.branch:closed:has-children:has-siblings {border-image: none image: url(:/images/branch-closed.png)} QTreeWidget.branch:open:has-children:!has-siblings, QTreeWidget.branch:open:has-children:has-siblings {border-image: noneimage: url(:/images/branch-open.png)}")
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)

        self.playhead = PlayHead()
        self.sb = QScrollBar(Qt.Horizontal)
        self.sb.setMaximum(50)
        layout.setColumnMinimumWidth(0, 200)
        layout.addItem(hbox, 0, 0)
        layout.addWidget(self.playhead, 0, 1)
        layout.addWidget(self.tree, 1, 0, 1, 2)
        layout.addWidget(self.sb, 2, 1)
        layout.setColumnStretch(0,0)
        layout.setColumnStretch(1,1)

        self.setLayout(layout)

        self.contextMenu = QMenu()
        self.delAct = QAction("Delete", self)

        #connect(self.tree, SIGNAL(customContextMenuRequested(const QPoint &)), self, SLOT(onCustomContextMenu(const QPoint &)))
        self.playhead.valueChanged.connect(self.playheadValueChanged)
        #connect(self.sb, SIGNAL(valueChanged(int)), self.playhead, SLOT(scrollValueChanged(int)))
        #connect(self.sb, SIGNAL(valueChanged(int)), self, SLOT(scrollValueChanged(int)))
        #connect(self.tree, SIGNAL(currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)), self, SLOT(treeCurrentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)))
        #connect(self.playhead, SIGNAL(valueChanged(int)), scene, SLOT(setPlayheadPosition(int)))
        #connect(self.scene, SIGNAL(keyframeAdded(AnimationItem*, QString, KeyFrame*)), self, SLOT(keyframeAdded(AnimationItem*, QString, KeyFrame*)))

    def setScene(self, scene):
        self.scene = scene

    def setPlayheadPosition(self, pos):
        self.playhead.setValue(pos)

    def reset(self):
        pass

    def playheadValueChanged(self, value):
        #self.time.setText(Timeline.timeString(value))
        #m_scene->clearSelection();
        self.scene.setPlayheadPosition(value)

        # for(int i=0; i < m_tree->topLevelItemCount(); i++)
        # {
        #     QTreeWidgetItem *treeItem = m_tree->topLevelItem(i);
        #     TransitionLine *line = dynamic_cast<TransitionLine*>(m_tree->itemWidget(treeItem, 1));
        #     line->setPlayheadPosition(val);

        #     for(int j = 0; j < treeItem->childCount(); j++)
        #     {
        #         QTreeWidgetItem *cTreeItem = treeItem->child(j);
        #         TransitionLine *line = dynamic_cast<TransitionLine*>(m_tree->itemWidget(cTreeItem, 1));
        #         line->setPlayheadPosition(val);
        #     }
        # }
