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
from widgets.animationscene import AnimationScene
from widgets.timeline import Timeline
from widgets.itempropertyeditor import ItemPropertyEditor
from widgets.scenepropertyeditor import ScenePropertyEditor
from widgets.sceneview import SceneView
from widgets.transitioneditor import TransitionEditor
from PySide6.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QMainWindow, QTreeWidgetItem, QAbstractItemView, QWidget, QTreeWidget, QScrollArea, QSplitter, QComboBox, QDockWidget, QApplication, QMenu, QToolBar
from PySide6.QtCore import QFileInfo, Signal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QSize, QPoint, QAbstractAnimation, QPropertyAnimation
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtGui import QUndoStack, QScreen, QAction, QKeySequence, QActionGroup, QIcon, QPainter, QPixmap
import resources

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.undoStack = QUndoStack(self)
        self.fileMenuActions = []
        self.editMenuActions = []
        self.viewMenuActions = []
        self.loadedFile = QFileInfo()
        self.setDockNestingEnabled(True)
        self.loadPlugins()
        self.createStatusBar()
        self.createActions()
        self.createMenus()
        self.createGui()
        self.readSettings()

    def loadPlugins(self):
        pass

    def createStatusBar(self):
        if self.statusBar().currentMessage() == "":
            self.statusBar().showMessage("Ready")

    def createActions(self):
        openAct = QAction("&Open...", self)
        openAct.setShortcut(QKeySequence.Open)
        openAct.triggered.connect(self.open)
        self.fileMenuActions.append(openAct)

        newAct = QAction("&New", self)
        newAct.setShortcut(QKeySequence.New)
        # connect(Act, SIGNAL(triggered()), self, SLOT(file()))
        self.fileMenuActions.append(newAct)

        saveAct = QAction("&Save", self)
        saveAct.setEnabled(False)
        saveAct.setShortcut(QKeySequence.Save)
        saveAct.triggered.connect(self.save)
        # connect(self, SIGNAL(enableSave(bool)), saveAct, SLOT(setEnabled(bool)))
        self.fileMenuActions.append(saveAct)

        saveAsAct = QAction("Save &As...", self)
        saveAsAct.setShortcut(QKeySequence.SaveAs)
        saveAsAct.triggered.connect(self.saveAs)
        self.fileMenuActions.append(saveAsAct)

        saveItemAsAct = QAction("Save &Item as...", self)
        saveItemAsAct.setEnabled(False)
        # connect(saveItemAsAct, SIGNAL(triggered()), self, SLOT(saveItemAs()))
        # connect(self, SIGNAL(enableSaveItem(bool)), saveItemAsAct, SLOT(setEnabled(bool)))
        self.fileMenuActions.append(saveItemAsAct)

        self.exportMovieAct = QAction("Export Movie", self)
        self.exportMovieAct.triggered.connect(self.exportMovie)

        self.exitAct = QAction("E&xit", self)
        self.exitAct.setShortcuts(QKeySequence.Quit)
        self.exitAct.setStatusTip("Exit the application")
        # connect(exitAct, SIGNAL(triggered()), self, SLOT(close()))

        undoAct = self.undoStack.createUndoAction(self, "&Undo")
        undoAct.setShortcuts(QKeySequence.Undo)
        self.editMenuActions.append(undoAct)

        redoAct = self.undoStack.createRedoAction(self, "&Redo")
        redoAct.setShortcuts(QKeySequence.Redo)
        self.editMenuActions.append(redoAct)

        copyAct = QAction("&Copy", self)
        copyAct.setShortcuts(QKeySequence.Copy)
        #connect(copyAct, SIGNAL(triggered()), self, SLOT(copy()))
        self.editMenuActions.append(copyAct)

        pasteAct = QAction("&Paste", self)
        pasteAct.setShortcuts(QKeySequence.Paste)
        # connect(pasteAct, SIGNAL(triggered()), self, SLOT(paste()))
        self.editMenuActions.append(pasteAct)

        delAct = QAction("&Delete", self)
        delAct.setShortcut(QKeySequence.Delete)
        # connect(delAct, SIGNAL(triggered()), self, SLOT(del()))
        self.editMenuActions.append(delAct)

        showElementsAct = QAction("Elements", self)
        # connect(showElementsAct, SIGNAL(triggered()), self, SLOT(showElementsPanel()))
        self.viewMenuActions.append(showElementsAct)

        showPropertyPanelAct = QAction("Properties", self)
        # connect(showPropertyPanelAct, SIGNAL(triggered()), self, SLOT(showPropertyPanel()))
        self.viewMenuActions.append(showPropertyPanelAct)

        showToolPanelAct = QAction("Tools", self)
        # connect(showToolPanelAct, SIGNAL(triggered()), self, SLOT(showToolPanel()))
        self.viewMenuActions.append(showToolPanelAct)

        showRulerAct = QAction("Rulers", self)
        showRulerAct.setCheckable(True)
        showRulerAct.setChecked(True)
        # connect(showRulerAct, SIGNAL(triggered(bool)), self, SLOT(showRuler(bool)))
        self.viewMenuActions.append(showRulerAct)

        self.aboutAct = QAction("&About", self)
        self.aboutAct.triggered.connect(self.about)

        self.addAction(copyAct)
        self.addAction(pasteAct)
        self.addAction(self.exitAct)
        self.addAction(delAct)

    def createMenus(self):
        importMenu =  QMenu("Import")
        importMenu.setEnabled(False)

        fileMenu = self.menuBar().addMenu("&File")
        for action in self.fileMenuActions:
            fileMenu.addAction(action)
        
        fileMenu.addSeparator()
        exportMenu = fileMenu.addMenu("Export")
        exportMenu.addAction(self.exportMovieAct)
        # foreach(QString pluginName, Plugins.exportPluginNames())
        # {
        #     ExportInterface *ei = Plugins.getExportPlugin(pluginName)
        #     QAction *exportAct =  QAction(ei.displayName(), ei)
        #     connect(exportAct, SIGNAL(triggered()), this, SLOT(pluginExport()))
        #     exportMenu.addAction(exportAct)
        # }
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        editMenu = self.menuBar().addMenu("&Edit")
        for action in self.editMenuActions:
            editMenu.addAction(action)
            self.addAction(action)
        
        viewMenu = self.menuBar().addMenu("&View")
        for action in self.viewMenuActions:
             viewMenu.addAction(action)

        self.menuBar().addSeparator()

        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction(self.aboutAct)

    def createGui(self):
        toolpanel = QToolBar(self)
        toolpanel.setOrientation(Qt.Vertical)
        anActionGroup = QActionGroup(toolpanel)
        
        self.selectAct = QAction("Select", anActionGroup)
        self.selectAct.setIcon(QIcon(":/images/arrow.png"))
        self.selectAct.setCheckable(True)
        #self.selectAct.setChecked.connect(self.setChecked)

        self.rectangleAct = QAction("Rectangle", anActionGroup)
        self.rectangleAct.setIcon(QIcon(":/images/rectangle.png"))
        self.rectangleAct.setCheckable(True)

        self.ellipseAct = QAction("Ellipse", anActionGroup)
        self.ellipseAct.setIcon(QIcon(":/images/ellipse.png"))
        self.ellipseAct.setCheckable(True)

        self.textAct = QAction("Text", anActionGroup)
        self.textAct.setIcon(QIcon(":/images/text.png"))
        self.textAct.setCheckable(True)

        self.bitmapAct = QAction("Bitmap", anActionGroup)
        self.bitmapAct.setIcon(QIcon(":/images/camera.png"))
        self.bitmapAct.setCheckable(True)

        self.svgAct = QAction("Vectorgraphic", anActionGroup)
        self.svgAct.setIcon(QIcon(":/images/svg.png"))
        self.svgAct.setCheckable(True)

        # connect(self.selectAct, SIGNAL(triggered()), this, SLOT(setSelectMode()))
        # connect(self.rectangleAct, SIGNAL(triggered()), this, SLOT(setRectangleMode()))
        # connect(self.ellipseAct, SIGNAL(triggered()), this, SLOT(setEllipseMode()))
        # connect(self.textAct, SIGNAL(triggered()), this, SLOT(setTextMode()))
        # connect(self.bitmapAct, SIGNAL(triggered()), this, SLOT(loadNewBitmap()))
        # connect(self.svgAct, SIGNAL(triggered()), this, SLOT(loadNewSvg()))

        toolpanel.addAction(self.selectAct)
        toolpanel.addAction(self.rectangleAct)
        toolpanel.addAction(self.ellipseAct)
        toolpanel.addAction(self.textAct)
        toolpanel.addAction(self.bitmapAct)
        toolpanel.addAction(self.svgAct)

        # // load plugins here
        # foreach(QString pluginName, Plugins.itemPluginNames())
        # {
        #     ItemInterface *plugin = Plugins.getItemPlugin(pluginName)
        #     QAction *act = QAction(plugin.displayName(), anActionGroup)
        #     act.setData(QVariant(plugin.className()))
        #     act.setIcon(plugin.icon())
        #     act.setCheckable(True)
        #     connect(act, SIGNAL(triggered()), this, SLOT(setPluginMode()))
        #     toolpanel.addAction(act)
        # }
        # self.selectAct.toggle()

        self.tooldock = QDockWidget("Tools", self)
        self.tooldock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.tooldock.setWidget(toolpanel)
        self.tooldock.setObjectName("Tools")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.tooldock)

        self.scene = AnimationScene()
        self.scene.registerUndoStack(self.undoStack)

        self.timeline = Timeline(self.scene)
        self.timeline.setMinimumHeight(110)

        self.itemPropertyEditor = ItemPropertyEditor(self.timeline)
        self.scenePropertyEditor = ScenePropertyEditor()
        self.transitionEditor = TransitionEditor()
        self.transitionEditor.setUndoStack(self.undoStack)

        self.scenePropertyEditor.setScene(self.scene)

        self.propertiesdock = QDockWidget("Properties", self)
        self.propertiesdock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.propertiesdock.setWidget(self.scenePropertyEditor)
        self.propertiesdock.setObjectName("Properties")

        self.addDockWidget(Qt.RightDockWidgetArea, self.propertiesdock)

        self.view = SceneView(self.scene)
        self.view.setSceneRect(-100, -100, self.scene.width() + 200, self.scene.height() + 200)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        # connect(self.scene, SIGNAL(selectionChanged()), this, SLOT(sceneSelectionChanged()))
        # connect(self.scene, SIGNAL(itemAdded(QGraphicsItem*)), this, SLOT(sceneItemAdded(QGraphicsItem*)))
        # connect(self.scene, SIGNAL(sizeChanged(int,int)), this, SLOT(sceneSizeChanged(int, int)))
        # connect(self.scene, SIGNAL(itemRemoved(AnimationItem*)), this, SLOT(sceneItemRemoved(AnimationItem*)))
        # connect(self.scene, SIGNAL(animationResetted()), this, SLOT(reset()))

        w = QWidget()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        zoom = QComboBox()
        zoom.addItem("1:2")
        zoom.addItem("1:1")
        zoom.addItem("2:1")
        zoom.addItem("4:1")
        zoom.addItem("8:1")
        zoom.setCurrentIndex(1)
        # connect(zoom, SIGNAL(currentIndexChanged(int)), this, SLOT(changeZoom(int)))

        vbox.addWidget(self.view)
        vbox.addLayout(hbox)
        hbox.addWidget(zoom)
        hbox.addStretch()
        w.setLayout(vbox)

        self.elementTree = QTreeWidget()
        self.elementTree.header().close()
        self.elementTree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.root = QTreeWidgetItem()
        self.root.setText(0, "Scene")
        self.elementTree.setColumnCount(3)
        self.elementTree.setColumnWidth(1, 18)
        self.elementTree.setColumnWidth(2, 18)
        self.elementTree.header().moveSection(0,2)
        self.elementTree.addTopLevelItem(self.root)
        # connect(self.elementTree, SIGNAL(currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)), this, SLOT(elementTreeItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)))

        self.elementsdock = QDockWidget("Elements", self)
        self.elementsdock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.elementsdock.setWidget(self.elementTree)
        self.elementsdock.setObjectName("Elements")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.elementsdock)
        self.splitDockWidget(self.tooldock, self.elementsdock, Qt.Horizontal)

        # connect(self.timeline, SIGNAL(itemSelectionChanged(AnimationItem *)), this, SLOT(timelineSelectionChanged(AnimationItem*)))
        # connect(self.timeline, SIGNAL(transitionSelectionChanged(KeyFrame*)), this, SLOT(transitionSelectionChanged(KeyFrame*)))
        # connect(self.itemPropertyEditor, SIGNAL(addKeyFrame(AnimationItem*,QString,QVariant)), self.timeline, SLOT(addKeyFrame(AnimationItem*,QString,QVariant)))
        # connect(self.scenePropertyEditor, SIGNAL(addKeyFrame(AnimationItem*,QString,QVariant)), self.timeline, SLOT(addKeyFrame(AnimationItem*,QString,QVariant)))

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(w)
        self.splitter.addWidget(self.timeline)

        self.setCentralWidget(self.splitter)

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def writeSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
        settings.setValue("state", self.saveState())

    def readSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope,  QCoreApplication.organizationName(), QCoreApplication.applicationName())
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)
        self.restoreState(settings.value("state"))
        #self.showRulers = settings.value("rulers", "True").toBool()
        #if not showRulers:
        #    emit showRulerAct.toggled(False)

    def open(self):
        pass
    
    def exportMovie(self):
        print("Export")

    def about(self):
        msg = QMessageBox()
        msg.setWindowTitle("About AnimationMaker")
        msg.setText(
            "AnimationMaker\nVersion: " + QCoreApplication.applicationVersion() + "\n" +
            "(C) Copyright 2023 CrowdWare. All rights reserved.\n" +
            "\n" +
            "The program is provided AS IS with NO WARRANTY OF ANY KIND," +
            "INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE."
        )
        msg.setIconPixmap(QPixmap(":/images/logo.png"))
        msg.exec()


    def save(self):
        self.writeFile(self.loadedFile.filePath())
    

    def saveAs(self):
        self._saveAs()

    def _saveAs(self):
        fileName = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("AnimationMaker XML (*.amx)All Files (*)")
        dialog.setWindowTitle("Save Animation")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("amx")
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]
        del dialog
        if fileName == "":
            return False

        self.writeFile(fileName)
        self.loadedFile.setFile(fileName)
        #emit this.enableSave(true)
        self.setTitle()
        return True

    def saveItemAs(self):
        fileName = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("AnimationMaker XML (*.amx)All Files (*)")
        dialog.setWindowTitle("Save Animation")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("amx")
        if dialog.exec():
            fileName = dialog.selectedFiles().first()
        del dialog
        if fileName == "":
            return

        self.scene.exportXml(fileName, False)
        self.statusBar().showMessage("Item saved as " + fileName)

    def writeFile(self, fileName):
        self.scene.clearSelection()
        self.timeline.setPlayheadPosition(0)

        self.scene.exportXml(fileName)
        self.statusBar().showMessage("File saved as " + fileName)

        self.undoStack.clear()

    def setTitle(self):
        if self.loadedFile.completeBaseName() == "":
            self.setWindowTitle(QCoreApplication.applicationName())
        else:
            self.setWindowTitle(QCoreApplication.applicationName() + " - " + self.loadedFile.completeBaseName() + "." + self.loadedFile.suffix())
