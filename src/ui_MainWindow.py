# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1117, 736)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 1, 1))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(800, 600))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1117, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRecent_File = QtWidgets.QMenu(self.menuFile)
        self.menuRecent_File.setObjectName("menuRecent_File")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuFind_or_Replace = QtWidgets.QMenu(self.menuEdit)
        self.menuFind_or_Replace.setObjectName("menuFind_or_Replace")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuDraw_Tools = QtWidgets.QMenu(self.menuSettings)
        self.menuDraw_Tools.setObjectName("menuDraw_Tools")
        self.menuLine = QtWidgets.QMenu(self.menuDraw_Tools)
        self.menuLine.setObjectName("menuLine")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuNodes_Edges_Details = QtWidgets.QMenu(self.menuTools)
        self.menuNodes_Edges_Details.setObjectName("menuNodes_Edges_Details")
        self.menuNode_s_Degree = QtWidgets.QMenu(self.menuNodes_Edges_Details)
        self.menuNode_s_Degree.setObjectName("menuNode_s_Degree")
        self.menuDigraph_s_Degrees = QtWidgets.QMenu(self.menuNode_s_Degree)
        self.menuDigraph_s_Degrees.setObjectName("menuDigraph_s_Degrees")
        self.menuPathway_and_Loop = QtWidgets.QMenu(self.menuTools)
        self.menuPathway_and_Loop.setObjectName("menuPathway_and_Loop")
        self.menuPathway = QtWidgets.QMenu(self.menuPathway_and_Loop)
        self.menuPathway.setObjectName("menuPathway")
        self.menuLoop = QtWidgets.QMenu(self.menuPathway_and_Loop)
        self.menuLoop.setObjectName("menuLoop")
        self.menuGraph_Matrix = QtWidgets.QMenu(self.menuTools)
        self.menuGraph_Matrix.setObjectName("menuGraph_Matrix")
        self.menuSpecial_Graph = QtWidgets.QMenu(self.menuTools)
        self.menuSpecial_Graph.setObjectName("menuSpecial_Graph")
        self.menuEuler_Graph = QtWidgets.QMenu(self.menuSpecial_Graph)
        self.menuEuler_Graph.setObjectName("menuEuler_Graph")
        self.menuHamiltonian_Graph = QtWidgets.QMenu(self.menuSpecial_Graph)
        self.menuHamiltonian_Graph.setObjectName("menuHamiltonian_Graph")
        self.menuShortest_Path_and_Critical_Path = QtWidgets.QMenu(self.menuTools)
        self.menuShortest_Path_and_Critical_Path.setObjectName("menuShortest_Path_and_Critical_Path")
        self.menuMode = QtWidgets.QMenu(self.menubar)
        self.menuMode.setObjectName("menuMode")
        self.menuGraph_Mode = QtWidgets.QMenu(self.menuMode)
        self.menuGraph_Mode.setObjectName("menuGraph_Mode")
        self.menuWinodws = QtWidgets.QMenu(self.menubar)
        self.menuWinodws.setObjectName("menuWinodws")
        self.menuLanguage = QtWidgets.QMenu(self.menuWinodws)
        self.menuLanguage.setObjectName("menuLanguage")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.general_utility_toolBar = QtWidgets.QToolBar(MainWindow)
        self.general_utility_toolBar.setObjectName("general_utility_toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.general_utility_toolBar)
        self.graphical_toolBar = QtWidgets.QToolBar(MainWindow)
        self.graphical_toolBar.setObjectName("graphical_toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.graphical_toolBar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setMinimumSize(QtCore.QSize(270, 40))
        self.dockWidget.setMaximumSize(QtCore.QSize(280, 524287))
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setMinimumSize(QtCore.QSize(260, 0))
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.dockWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 271, 611))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.propertyTab = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.propertyTab.setMaximumSize(QtCore.QSize(269, 16777215))
        self.propertyTab.setTabPosition(QtWidgets.QTabWidget.South)
        self.propertyTab.setObjectName("propertyTab")
        self.HistoryTab = QtWidgets.QWidget()
        self.HistoryTab.setObjectName("HistoryTab")
        self.undoView = QtWidgets.QUndoView(self.HistoryTab)
        self.undoView.setGeometry(QtCore.QRect(0, 0, 265, 581))
        self.undoView.setMinimumSize(QtCore.QSize(265, 0))
        self.undoView.setMaximumSize(QtCore.QSize(265, 16777215))
        self.undoView.setObjectName("undoView")
        self.propertyTab.addTab(self.HistoryTab, "")
        self.DetailsTab = QtWidgets.QWidget()
        self.DetailsTab.setObjectName("DetailsTab")
        self.GraphDetails = QtWidgets.QListView(self.DetailsTab)
        self.GraphDetails.setGeometry(QtCore.QRect(0, 0, 265, 581))
        self.GraphDetails.setMinimumSize(QtCore.QSize(265, 0))
        self.GraphDetails.setMaximumSize(QtCore.QSize(265, 16777215))
        self.GraphDetails.setObjectName("GraphDetails")
        self.propertyTab.addTab(self.DetailsTab, "")
        self.verticalLayout.addWidget(self.propertyTab)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/128.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/images/132.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/images/SaveFile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionSave_All = QtWidgets.QAction(MainWindow)
        self.actionSave_All.setObjectName("actionSave_All")
        self.actionImport_Data = QtWidgets.QAction(MainWindow)
        self.actionImport_Data.setObjectName("actionImport_Data")
        self.actionOutput_Data = QtWidgets.QAction(MainWindow)
        self.actionOutput_Data.setObjectName("actionOutput_Data")
        self.actionSave_Image = QtWidgets.QAction(MainWindow)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionClose = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/images/108.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClose.setIcon(icon3)
        self.actionClose.setObjectName("actionClose")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/images/DELETE.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon4)
        self.actionQuit.setObjectName("actionQuit")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/images/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon5)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/images/redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRedo.setIcon(icon6)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setIcon(icon4)
        self.actionDelete.setObjectName("actionDelete")
        self.actionFind = QtWidgets.QAction(MainWindow)
        self.actionFind.setObjectName("actionFind")
        self.actionReplace = QtWidgets.QAction(MainWindow)
        self.actionReplace.setObjectName("actionReplace")
        self.actionNode_s_Name = QtWidgets.QAction(MainWindow)
        self.actionNode_s_Name.setObjectName("actionNode_s_Name")
        self.actionNode_s_Coordinates = QtWidgets.QAction(MainWindow)
        self.actionNode_s_Coordinates.setObjectName("actionNode_s_Coordinates")
        self.actionEdge_s_Weight = QtWidgets.QAction(MainWindow)
        self.actionEdge_s_Weight.setObjectName("actionEdge_s_Weight")
        self.actionRedigraph_s_Degrees = QtWidgets.QAction(MainWindow)
        self.actionRedigraph_s_Degrees.setObjectName("actionRedigraph_s_Degrees")
        self.actionOut_degree = QtWidgets.QAction(MainWindow)
        self.actionOut_degree.setObjectName("actionOut_degree")
        self.actionIn_degree = QtWidgets.QAction(MainWindow)
        self.actionIn_degree.setObjectName("actionIn_degree")
        self.actionEasy_Pathway = QtWidgets.QAction(MainWindow)
        self.actionEasy_Pathway.setObjectName("actionEasy_Pathway")
        self.actionComplicated_Pathway = QtWidgets.QAction(MainWindow)
        self.actionComplicated_Pathway.setObjectName("actionComplicated_Pathway")
        self.actionEasy_Loop = QtWidgets.QAction(MainWindow)
        self.actionEasy_Loop.setObjectName("actionEasy_Loop")
        self.actionComplicated_Loop = QtWidgets.QAction(MainWindow)
        self.actionComplicated_Loop.setObjectName("actionComplicated_Loop")
        self.actionIncidence_Matrix = QtWidgets.QAction(MainWindow)
        self.actionIncidence_Matrix.setObjectName("actionIncidence_Matrix")
        self.actionAdjacent_Matrix = QtWidgets.QAction(MainWindow)
        self.actionAdjacent_Matrix.setObjectName("actionAdjacent_Matrix")
        self.actionBigraph = QtWidgets.QAction(MainWindow)
        self.actionBigraph.setObjectName("actionBigraph")
        self.actionShortest_Path = QtWidgets.QAction(MainWindow)
        self.actionShortest_Path.setObjectName("actionShortest_Path")
        self.actionCritical_Path = QtWidgets.QAction(MainWindow)
        self.actionCritical_Path.setObjectName("actionCritical_Path")
        self.actionFind_Euler_Loop = QtWidgets.QAction(MainWindow)
        self.actionFind_Euler_Loop.setObjectName("actionFind_Euler_Loop")
        self.actionFind_Hamiltonian_Loop = QtWidgets.QAction(MainWindow)
        self.actionFind_Hamiltonian_Loop.setObjectName("actionFind_Hamiltonian_Loop")
        self.actionGraph_Coloring_Problem = QtWidgets.QAction(MainWindow)
        self.actionGraph_Coloring_Problem.setObjectName("actionGraph_Coloring_Problem")
        self.actionDigraph_Mode = QtWidgets.QAction(MainWindow)
        self.actionDigraph_Mode.setCheckable(True)
        self.actionDigraph_Mode.setObjectName("actionDigraph_Mode")
        self.actionRedigraph_Mode = QtWidgets.QAction(MainWindow)
        self.actionRedigraph_Mode.setCheckable(True)
        self.actionRedigraph_Mode.setObjectName("actionRedigraph_Mode")
        self.actionTree_Mode = QtWidgets.QAction(MainWindow)
        self.actionTree_Mode.setCheckable(True)
        self.actionTree_Mode.setObjectName("actionTree_Mode")
        self.actionMinimise = QtWidgets.QAction(MainWindow)
        self.actionMinimise.setObjectName("actionMinimise")
        self.actionMaximize = QtWidgets.QAction(MainWindow)
        self.actionMaximize.setObjectName("actionMaximize")
        self.actionMini_Mode = QtWidgets.QAction(MainWindow)
        self.actionMini_Mode.setObjectName("actionMini_Mode")
        self.actionHide_ToolBar = QtWidgets.QAction(MainWindow)
        self.actionHide_ToolBar.setCheckable(True)
        self.actionHide_ToolBar.setObjectName("actionHide_ToolBar")
        self.actionConnect_Author = QtWidgets.QAction(MainWindow)
        self.actionConnect_Author.setObjectName("actionConnect_Author")
        self.actionWelcome = QtWidgets.QAction(MainWindow)
        self.actionWelcome.setObjectName("actionWelcome")
        self.actionHelp_Document = QtWidgets.QAction(MainWindow)
        self.actionHelp_Document.setObjectName("actionHelp_Document")
        self.actionFlie_List = QtWidgets.QAction(MainWindow)
        self.actionFlie_List.setObjectName("actionFlie_List")
        self.actionPen_Thickness = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/images/penStyle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPen_Thickness.setIcon(icon7)
        self.actionPen_Thickness.setObjectName("actionPen_Thickness")
        self.actionPen_Color = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/images/penColor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPen_Color.setIcon(icon8)
        self.actionPen_Color.setObjectName("actionPen_Color")
        self.actionBackground_Color = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/images/backgroundColor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBackground_Color.setIcon(icon9)
        self.actionBackground_Color.setObjectName("actionBackground_Color")
        self.actionArc = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/images/ARC.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionArc.setIcon(icon10)
        self.actionArc.setObjectName("actionArc")
        self.actionStraight_Line = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/images/LINE.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStraight_Line.setIcon(icon11)
        self.actionStraight_Line.setObjectName("actionStraight_Line")
        self.actionCircle = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/images/ELLIPSE.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCircle.setIcon(icon12)
        self.actionCircle.setObjectName("actionCircle")
        self.actionRectangle = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/images/RECTANGL.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRectangle.setIcon(icon13)
        self.actionRectangle.setObjectName("actionRectangle")
        self.actionSetEnglish = QtWidgets.QAction(MainWindow)
        self.actionSetEnglish.setCheckable(True)
        self.actionSetEnglish.setObjectName("actionSetEnglish")
        self.actionSetChinese = QtWidgets.QAction(MainWindow)
        self.actionSetChinese.setCheckable(True)
        self.actionSetChinese.setObjectName("actionSetChinese")
        self.actionAdd_Annotation = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/images/800.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionAdd_Annotation.setIcon(icon14)
        self.actionAdd_Annotation.setObjectName("actionAdd_Annotation")
        self.actionClues_Color = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/images/rt_penColor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClues_Color.setIcon(icon15)
        self.actionClues_Color.setObjectName("actionClues_Color")
        self.actionClues_Thickness = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icons/images/rt_penStyle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClues_Thickness.setIcon(icon16)
        self.actionClues_Thickness.setObjectName("actionClues_Thickness")
        self.actionProperty_And_History = QtWidgets.QAction(MainWindow)
        self.actionProperty_And_History.setCheckable(True)
        self.actionProperty_And_History.setObjectName("actionProperty_And_History")
        self.menuRecent_File.addAction(self.actionFlie_List)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuRecent_File.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_Image)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionSave_All)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_Data)
        self.menuFile.addAction(self.actionOutput_Data)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuFind_or_Replace.addAction(self.actionFind)
        self.menuFind_or_Replace.addAction(self.actionReplace)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.menuFind_or_Replace.menuAction())
        self.menuLine.addAction(self.actionArc)
        self.menuLine.addAction(self.actionStraight_Line)
        self.menuDraw_Tools.addAction(self.menuLine.menuAction())
        self.menuDraw_Tools.addAction(self.actionCircle)
        self.menuDraw_Tools.addAction(self.actionRectangle)
        self.menuSettings.addAction(self.menuDraw_Tools.menuAction())
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionPen_Thickness)
        self.menuSettings.addAction(self.actionPen_Color)
        self.menuSettings.addAction(self.actionBackground_Color)
        self.menuSettings.addAction(self.actionClues_Color)
        self.menuSettings.addAction(self.actionClues_Thickness)
        self.menuSettings.addAction(self.actionProperty_And_History)
        self.menuDigraph_s_Degrees.addAction(self.actionOut_degree)
        self.menuDigraph_s_Degrees.addAction(self.actionIn_degree)
        self.menuNode_s_Degree.addAction(self.menuDigraph_s_Degrees.menuAction())
        self.menuNode_s_Degree.addAction(self.actionRedigraph_s_Degrees)
        self.menuNodes_Edges_Details.addAction(self.actionNode_s_Name)
        self.menuNodes_Edges_Details.addAction(self.actionNode_s_Coordinates)
        self.menuNodes_Edges_Details.addAction(self.actionEdge_s_Weight)
        self.menuNodes_Edges_Details.addAction(self.menuNode_s_Degree.menuAction())
        self.menuPathway.addAction(self.actionEasy_Pathway)
        self.menuPathway.addAction(self.actionComplicated_Pathway)
        self.menuLoop.addAction(self.actionEasy_Loop)
        self.menuLoop.addAction(self.actionComplicated_Loop)
        self.menuPathway_and_Loop.addAction(self.menuPathway.menuAction())
        self.menuPathway_and_Loop.addAction(self.menuLoop.menuAction())
        self.menuGraph_Matrix.addAction(self.actionIncidence_Matrix)
        self.menuGraph_Matrix.addAction(self.actionAdjacent_Matrix)
        self.menuEuler_Graph.addAction(self.actionFind_Euler_Loop)
        self.menuHamiltonian_Graph.addAction(self.actionFind_Hamiltonian_Loop)
        self.menuSpecial_Graph.addAction(self.actionBigraph)
        self.menuSpecial_Graph.addAction(self.menuEuler_Graph.menuAction())
        self.menuSpecial_Graph.addAction(self.menuHamiltonian_Graph.menuAction())
        self.menuShortest_Path_and_Critical_Path.addAction(self.actionShortest_Path)
        self.menuShortest_Path_and_Critical_Path.addAction(self.actionCritical_Path)
        self.menuTools.addAction(self.menuNodes_Edges_Details.menuAction())
        self.menuTools.addAction(self.menuPathway_and_Loop.menuAction())
        self.menuTools.addAction(self.menuGraph_Matrix.menuAction())
        self.menuTools.addAction(self.menuSpecial_Graph.menuAction())
        self.menuTools.addAction(self.menuShortest_Path_and_Critical_Path.menuAction())
        self.menuTools.addAction(self.actionGraph_Coloring_Problem)
        self.menuGraph_Mode.addAction(self.actionDigraph_Mode)
        self.menuGraph_Mode.addAction(self.actionRedigraph_Mode)
        self.menuMode.addAction(self.menuGraph_Mode.menuAction())
        self.menuMode.addAction(self.actionTree_Mode)
        self.menuLanguage.addAction(self.actionSetEnglish)
        self.menuLanguage.addAction(self.actionSetChinese)
        self.menuWinodws.addAction(self.actionMinimise)
        self.menuWinodws.addAction(self.actionMaximize)
        self.menuWinodws.addAction(self.actionMini_Mode)
        self.menuWinodws.addAction(self.actionHide_ToolBar)
        self.menuWinodws.addAction(self.menuLanguage.menuAction())
        self.menuHelp.addAction(self.actionConnect_Author)
        self.menuHelp.addAction(self.actionWelcome)
        self.menuHelp.addAction(self.actionHelp_Document)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuWinodws.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.general_utility_toolBar.addAction(self.actionNew)
        self.general_utility_toolBar.addAction(self.actionOpen)
        self.general_utility_toolBar.addAction(self.actionSave)
        self.general_utility_toolBar.addAction(self.actionUndo)
        self.general_utility_toolBar.addAction(self.actionRedo)
        self.general_utility_toolBar.addAction(self.actionDelete)
        self.general_utility_toolBar.addSeparator()
        self.general_utility_toolBar.addAction(self.actionPen_Color)
        self.general_utility_toolBar.addAction(self.actionPen_Thickness)
        self.general_utility_toolBar.addAction(self.actionBackground_Color)
        self.general_utility_toolBar.addAction(self.actionClues_Color)
        self.general_utility_toolBar.addAction(self.actionClues_Thickness)
        self.graphical_toolBar.addAction(self.actionArc)
        self.graphical_toolBar.addAction(self.actionStraight_Line)
        self.graphical_toolBar.addAction(self.actionCircle)
        self.graphical_toolBar.addAction(self.actionRectangle)
        self.graphical_toolBar.addAction(self.actionAdd_Annotation)

        self.retranslateUi(MainWindow)
        self.propertyTab.setCurrentIndex(0)
        self.actionHide_ToolBar.triggered.connect(self.general_utility_toolBar.hide)
        self.actionHide_ToolBar.triggered.connect(self.graphical_toolBar.hide)
        self.actionMinimise.triggered.connect(MainWindow.showMinimized)
        self.actionMaximize.triggered.connect(MainWindow.showMaximized)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuRecent_File.setTitle(_translate("MainWindow", "Recent File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuFind_or_Replace.setTitle(_translate("MainWindow", "Find or Replace"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuDraw_Tools.setTitle(_translate("MainWindow", "Draw Tools"))
        self.menuLine.setTitle(_translate("MainWindow", "Line"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuNodes_Edges_Details.setTitle(_translate("MainWindow", "Nodes and Edges Details"))
        self.menuNode_s_Degree.setTitle(_translate("MainWindow", "Node\'s Degree"))
        self.menuDigraph_s_Degrees.setTitle(_translate("MainWindow", "Digraph\'s Degrees"))
        self.menuPathway_and_Loop.setTitle(_translate("MainWindow", "Pathway and Loop"))
        self.menuPathway.setTitle(_translate("MainWindow", "Pathway"))
        self.menuLoop.setTitle(_translate("MainWindow", "Loop"))
        self.menuGraph_Matrix.setTitle(_translate("MainWindow", "Graph Matrix"))
        self.menuSpecial_Graph.setTitle(_translate("MainWindow", "Special Graph"))
        self.menuEuler_Graph.setTitle(_translate("MainWindow", "Euler Graph"))
        self.menuHamiltonian_Graph.setTitle(_translate("MainWindow", "Hamiltonian Graph"))
        self.menuShortest_Path_and_Critical_Path.setTitle(_translate("MainWindow", "Shortest Path and Critical Path"))
        self.menuMode.setTitle(_translate("MainWindow", "Mode"))
        self.menuGraph_Mode.setTitle(_translate("MainWindow", "Graph Mode"))
        self.menuWinodws.setTitle(_translate("MainWindow", "Winodws"))
        self.menuLanguage.setTitle(_translate("MainWindow", "Language"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.general_utility_toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.graphical_toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.propertyTab.setTabText(self.propertyTab.indexOf(self.HistoryTab), _translate("MainWindow", "History"))
        self.propertyTab.setTabText(self.propertyTab.indexOf(self.DetailsTab), _translate("MainWindow", "Graph Details"))
        self.actionNew.setText(_translate("MainWindow", "New File"))
        self.actionNew.setToolTip(_translate("MainWindow", "新建文件"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open File"))
        self.actionOpen.setToolTip(_translate("MainWindow", "打开文件"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "保存文件"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionSave_As.setToolTip(_translate("MainWindow", "另存为"))
        self.actionSave_All.setText(_translate("MainWindow", "Save All"))
        self.actionSave_All.setToolTip(_translate("MainWindow", "保存全部"))
        self.actionImport_Data.setText(_translate("MainWindow", "Import Data"))
        self.actionImport_Data.setToolTip(_translate("MainWindow", "导入数据"))
        self.actionImport_Data.setShortcut(_translate("MainWindow", "Ctrl+Shift+I"))
        self.actionOutput_Data.setText(_translate("MainWindow", "Output Data"))
        self.actionOutput_Data.setToolTip(_translate("MainWindow", "导出数据"))
        self.actionOutput_Data.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.actionSave_Image.setText(_translate("MainWindow", "Save Image"))
        self.actionSave_Image.setToolTip(_translate("MainWindow", "保存为图片"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setToolTip(_translate("MainWindow", "关闭文件"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setToolTip(_translate("MainWindow", "退出应用"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setToolTip(_translate("MainWindow", "撤销"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionRedo.setToolTip(_translate("MainWindow", "重做"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setToolTip(_translate("MainWindow", "剪贴"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setToolTip(_translate("MainWindow", "复制"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setToolTip(_translate("MainWindow", "粘贴"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setToolTip(_translate("MainWindow", "删除"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Del"))
        self.actionFind.setText(_translate("MainWindow", "Find"))
        self.actionFind.setToolTip(_translate("MainWindow", "查找"))
        self.actionFind.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actionReplace.setText(_translate("MainWindow", "Replace"))
        self.actionReplace.setToolTip(_translate("MainWindow", "替换"))
        self.actionReplace.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionNode_s_Name.setText(_translate("MainWindow", "Node\'s Name"))
        self.actionNode_s_Name.setToolTip(_translate("MainWindow", "结点名称"))
        self.actionNode_s_Coordinates.setText(_translate("MainWindow", "Node\'s Coordinates"))
        self.actionNode_s_Coordinates.setToolTip(_translate("MainWindow", "结点坐标"))
        self.actionEdge_s_Weight.setText(_translate("MainWindow", "Edge\'s Weight"))
        self.actionEdge_s_Weight.setToolTip(_translate("MainWindow", "边的权重"))
        self.actionRedigraph_s_Degrees.setText(_translate("MainWindow", "Redigraph\'s Degrees"))
        self.actionRedigraph_s_Degrees.setToolTip(_translate("MainWindow", "结点度"))
        self.actionOut_degree.setText(_translate("MainWindow", "Out-degree"))
        self.actionOut_degree.setToolTip(_translate("MainWindow", "出度"))
        self.actionIn_degree.setText(_translate("MainWindow", "In-degree"))
        self.actionIn_degree.setToolTip(_translate("MainWindow", "入度"))
        self.actionEasy_Pathway.setText(_translate("MainWindow", "Easy Pathway"))
        self.actionEasy_Pathway.setToolTip(_translate("MainWindow", "简单通路"))
        self.actionComplicated_Pathway.setText(_translate("MainWindow", "Complicated Pathway"))
        self.actionComplicated_Pathway.setToolTip(_translate("MainWindow", "复杂通路"))
        self.actionEasy_Loop.setText(_translate("MainWindow", "Easy Loop"))
        self.actionEasy_Loop.setToolTip(_translate("MainWindow", "简单回路"))
        self.actionComplicated_Loop.setText(_translate("MainWindow", "Complicated Loop"))
        self.actionComplicated_Loop.setToolTip(_translate("MainWindow", "复杂回路"))
        self.actionIncidence_Matrix.setText(_translate("MainWindow", "Incidence Matrix"))
        self.actionIncidence_Matrix.setToolTip(_translate("MainWindow", "关联矩阵"))
        self.actionAdjacent_Matrix.setText(_translate("MainWindow", "Adjacent Matrix"))
        self.actionAdjacent_Matrix.setToolTip(_translate("MainWindow", "邻接矩阵"))
        self.actionBigraph.setText(_translate("MainWindow", "Bigraph"))
        self.actionBigraph.setToolTip(_translate("MainWindow", "二部图"))
        self.actionShortest_Path.setText(_translate("MainWindow", "Shortest Path"))
        self.actionShortest_Path.setToolTip(_translate("MainWindow", "最短路径"))
        self.actionCritical_Path.setText(_translate("MainWindow", "Critical Path"))
        self.actionFind_Euler_Loop.setText(_translate("MainWindow", "Find Euler Loop"))
        self.actionFind_Euler_Loop.setToolTip(_translate("MainWindow", "寻找欧拉回路"))
        self.actionFind_Hamiltonian_Loop.setText(_translate("MainWindow", "Find Hamiltonian Loop"))
        self.actionFind_Hamiltonian_Loop.setToolTip(_translate("MainWindow", "寻找哈密顿回路"))
        self.actionGraph_Coloring_Problem.setText(_translate("MainWindow", "Graph Coloring Problem"))
        self.actionGraph_Coloring_Problem.setToolTip(_translate("MainWindow", "着色问题"))
        self.actionDigraph_Mode.setText(_translate("MainWindow", "Digraph Mode"))
        self.actionDigraph_Mode.setToolTip(_translate("MainWindow", "有向图模式"))
        self.actionDigraph_Mode.setShortcut(_translate("MainWindow", "F1"))
        self.actionRedigraph_Mode.setText(_translate("MainWindow", "Redigraph Mode"))
        self.actionRedigraph_Mode.setToolTip(_translate("MainWindow", "无向图模式"))
        self.actionRedigraph_Mode.setShortcut(_translate("MainWindow", "F2"))
        self.actionTree_Mode.setText(_translate("MainWindow", "Tree Mode"))
        self.actionTree_Mode.setToolTip(_translate("MainWindow", "树模式"))
        self.actionTree_Mode.setShortcut(_translate("MainWindow", "F3"))
        self.actionMinimise.setText(_translate("MainWindow", "Minimise"))
        self.actionMinimise.setToolTip(_translate("MainWindow", "窗口最小化"))
        self.actionMaximize.setText(_translate("MainWindow", "Maximize"))
        self.actionMaximize.setToolTip(_translate("MainWindow", "窗口最大化"))
        self.actionMini_Mode.setText(_translate("MainWindow", "Mini-Mode"))
        self.actionMini_Mode.setToolTip(_translate("MainWindow", "迷你模式"))
        self.actionHide_ToolBar.setText(_translate("MainWindow", "Hide ToolBar"))
        self.actionHide_ToolBar.setToolTip(_translate("MainWindow", "隐藏工具栏"))
        self.actionConnect_Author.setText(_translate("MainWindow", "Connect Author"))
        self.actionConnect_Author.setToolTip(_translate("MainWindow", "联系作者"))
        self.actionWelcome.setText(_translate("MainWindow", "Welcome"))
        self.actionWelcome.setToolTip(_translate("MainWindow", "欢迎"))
        self.actionHelp_Document.setText(_translate("MainWindow", "Help Document"))
        self.actionHelp_Document.setToolTip(_translate("MainWindow", "帮助文档"))
        self.actionFlie_List.setText(_translate("MainWindow", "Flie List"))
        self.actionFlie_List.setToolTip(_translate("MainWindow", "最近文件"))
        self.actionPen_Thickness.setText(_translate("MainWindow", "Pen Thickness"))
        self.actionPen_Thickness.setToolTip(_translate("MainWindow", "画笔粗细与样式"))
        self.actionPen_Color.setText(_translate("MainWindow", "Pen Color"))
        self.actionPen_Color.setToolTip(_translate("MainWindow", "画笔颜色"))
        self.actionBackground_Color.setText(_translate("MainWindow", "Background Color"))
        self.actionBackground_Color.setToolTip(_translate("MainWindow", "背景色"))
        self.actionArc.setText(_translate("MainWindow", "Arc"))
        self.actionArc.setToolTip(_translate("MainWindow", "弧线"))
        self.actionStraight_Line.setText(_translate("MainWindow", "Straight Line"))
        self.actionStraight_Line.setToolTip(_translate("MainWindow", "直线"))
        self.actionCircle.setText(_translate("MainWindow", "Circle"))
        self.actionCircle.setToolTip(_translate("MainWindow", "椭圆"))
        self.actionRectangle.setText(_translate("MainWindow", "Rectangle"))
        self.actionRectangle.setToolTip(_translate("MainWindow", "矩形"))
        self.actionSetEnglish.setText(_translate("MainWindow", "English"))
        self.actionSetChinese.setText(_translate("MainWindow", "Chinese"))
        self.actionAdd_Annotation.setText(_translate("MainWindow", "Add Annotation"))
        self.actionAdd_Annotation.setToolTip(_translate("MainWindow", "添加注释"))
        self.actionClues_Color.setText(_translate("MainWindow", "Clues Color"))
        self.actionClues_Color.setToolTip(_translate("MainWindow", "提示颜色"))
        self.actionClues_Thickness.setText(_translate("MainWindow", "Clues Thickness"))
        self.actionClues_Thickness.setToolTip(_translate("MainWindow", "提示粗细与样式"))
        self.actionProperty_And_History.setText(_translate("MainWindow", "Property And History"))
import res_rc
