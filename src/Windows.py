# -*- coding: utf-8 -*-
import os
import sys, random
from PySide2.QtCore import Slot, Qt, QRectF, QItemSelectionModel, QModelIndex

from PySide2.QtGui import QBrush, QStandardItemModel, QStandardItem

from PySide2.QtWidgets import QApplication, QMainWindow, QColorDialog, \
    QInputDialog, QLabel, QMessageBox, QFileDialog, QActionGroup, QUndoStack, QGraphicsItem, QGraphicsView, \
    QHeaderView, QFontDialog

from BezierEdge import BezierEdge
from BezierNode import BezierNode
from BezierText import BezierText
from Graph import Graph
from GraphicsScene import GraphicsScene
from GraphicsView import GraphicsView
from PointItem import ItemType
from ShowDataWidget import ShowDataWidget
from ShowMatrixWidget import ShowMatrixWidget
from UndoCommand import AddCommand, MoveCommand
from ui_MainWindow import Ui_MainWindow
from ThicknessDialog import ThicknessDialog
from OperatorFile import OperatorData


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.__scene = GraphicsScene(self)  # 创建QGraphicsScene
        self.__view = GraphicsView(self, self.__scene)  # 创建图形视图组件
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面

        self.setWindowTitle("离散数学可视化认知系统")

        self.ui.nodeDetails.setEnabled(False)
        self.ui.edgeDetails.setEnabled(False)

        self.edgeModel = QStandardItemModel(5, 5, self)
        self.edgeSelectionModel = QItemSelectionModel(self.edgeModel)
        self.edgeModel.dataChanged.connect(self.do_updateEdgeWeight)

        self.nodeModel = QStandardItemModel(5, 4, self)
        self.nodeSelectionModel = QItemSelectionModel(self.nodeModel)
        self.nodeModel.dataChanged.connect(self.do_updateNodeWeight)

        self.ui.tabWidget.setVisible(False)
        self.ui.tabWidget.clear()
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.setDocumentMode(True)
        self.setCentralWidget(self.ui.tabWidget)
        self.setAutoFillBackground(True)

        self.__buildStatusBar()  # 构造状态栏
        self.__buildUndoCommand()  # 初始化撤销重做系统
        self.__initModeMenu()
        self.__initToolMenu()
        self.__lastColumnFlag = Qt.NoItemFlags

        self.iniGraphicsSystem()

        self.__ItemId = 0  # 绘图项自定义数据的key
        self.__ItemDesc = 1  # 绘图项自定义数据的key

        self.__NodeId = 2
        self.__EdgeId = 3
        self.__TextId = 4

        self.__seqNum = 0  # 每个图形项设置一个序号
        self.__nodeNum = 0  # 结点的序号
        self.__edgeNum = 0  # 边的序号
        self.__textNum = 0
        self.__backZ = 0  # 后置序号
        self.__frontZ = 0  # 前置序号

        self.lastColumnFlags = (Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

        self.__graph = Graph()

    ##  ==============自定义功能函数============

    def nodeNum(self):
        return self.__nodeNum

    def edgeNum(self):
        return self.__edgeNum

    def scene(self):
        self.viewAndScene()
        return self.__scene

    def view(self):
        self.viewAndScene()
        return self.__view

    def graph(self):
        return self.__graph

    def __buildStatusBar(self):  ##构造状态栏
        self.__labViewCord = QLabel("View 坐标：")
        self.__labViewCord.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.__labViewCord)

        self.__labSceneCord = QLabel("Scene 坐标：")
        self.__labSceneCord.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.__labSceneCord)

        self.__labItemCord = QLabel("Item 坐标：")
        self.__labItemCord.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.__labItemCord)

        self.__labItemInfo = QLabel("ItemInfo: ")
        self.ui.statusbar.addPermanentWidget(self.__labItemInfo)
        self.__labModeInfo = QLabel("有向图模式")
        self.ui.statusbar.addPermanentWidget(self.__labModeInfo)

    def iniGraphicsSystem(self):  ##初始化 Graphics View系统

        self.__scene = GraphicsScene(self)  # 创建QGraphicsScene
        self.__view = GraphicsView(self, self.__scene)  # 创建图形视图组件
        self.__scene.setSceneRect(QRectF(-300, -200, 600, 200))
        self.__view.setCursor(Qt.CrossCursor)  # 设置鼠标
        self.__view.setMouseTracking(True)
        self.__view.setDragMode(QGraphicsView.RubberBandDrag)

        self.__view.mouseMove.connect(self.do_mouseMove)  # 鼠标移动
        self.__view.mouseClicked.connect(self.do_mouseClicked)  # 左键按下
        self.__scene.itemMoveSignal.connect(self.do_shapeMoved)
        self.__scene.itemLock.connect(self.do_nodeLock)

        title = f'Board_{self.ui.tabWidget.count()}'
        curIndex = self.ui.tabWidget.addTab(self.__view, title)
        self.ui.tabWidget.setCurrentIndex(curIndex)
        self.ui.tabWidget.setVisible(True)
        self.ui.tabWidget.update()

        ##  4个信号与槽函数的关联

        # self.view.mouseDoubleClick.connect(self.do_mouseDoubleClick)  # 鼠标双击
        # self.view.keyPress.connect(self.do_keyPress)  # 左键按下

    def __buildUndoCommand(self):
        self.undoStack = QUndoStack()
        self.ui.actionUndo = self.undoStack.createUndoAction(self, "撤销")
        self.ui.actionRedo = self.undoStack.createRedoAction(self, "重做")

        self.addAction(self.ui.actionUndo)
        self.addAction(self.ui.actionRedo)

        self.ui.undoView.setStack(self.undoStack)

    def __setItemProperties(self, item, desc):  ##item是具体类型的QGraphicsItem

        self.__nodeNum = len(self.singleItems(BezierNode))
        self.__edgeNum = len(self.singleItems(BezierEdge))
        self.__textNum = len(self.singleItems(BezierText))
        item.setFlag(QGraphicsItem.ItemIsFocusable)
        item.setFlag(QGraphicsItem.ItemIsMovable)
        item.setFlag(QGraphicsItem.ItemIsSelectable)
        item.setPos(-150 + random.randint(1, 200), -200 + random.randint(1, 200))

        if type(item) is BezierNode:
            item.setData(self.__NodeId, self.__nodeNum)
            item.textCp.setPlainText("V" + str(self.__nodeNum))
            self.__nodeNum = 1 + self.__nodeNum
        elif type(item) is BezierEdge:
            item.setData(self.__EdgeId, self.__edgeNum)
            item.textCp.setPlainText("e" + str(self.__edgeNum))
            self.__edgeNum = 1 + self.__edgeNum
        elif type(item) is BezierText:
            item.setData(self.__TextId, self.__textNum)
            self.__textNum = 1 + self.__textNum

        self.__seqNum = 1 + self.__seqNum
        item.setData(self.__ItemId, self.__seqNum)  # 图件编号
        item.setData(self.__ItemDesc, desc)  # 图件描述

        self.__scene.addItem(item)
        self.__scene.clearSelection()
        item.setSelected(True)

    def __setBrushColor(self, item):  ##设置填充颜色
        color = item.brush().__color()
        color = QColorDialog.getColor(color, self, "选择填充颜色")
        if color.isValid():
            item.setBrush(QBrush(color))

    def __initFileMenu(self):
        self.ui.actionOpen.triggered.connect(self.do_open_file)
        self.ui.actionSave.triggered.connect(self.do_save_file)
        self.ui.actionQuit.triggered.connect(self.close)

    def __initEditMenu(self):
        self.ui.actionProperty_And_History.setChecked(True)
        self.ui.actionUndo = self.undoStack.createRedoAction(self, "redo")
        self.ui.actionRedo = self.undoStack.createRedoAction(self, "Redo")
        self.addAction(self.ui.actionRedo)
        self.addAction(self.ui.actionUndo)

    def __initModeMenu(self):
        modeMenuGroup = QActionGroup(self)
        modeMenuGroup.addAction(self.ui.actionDigraph_Mode)
        modeMenuGroup.addAction(self.ui.actionRedigraph_Mode)
        # self.ui.actionRedigraph_s_Degrees.setEnabled(not self.ui.actionDigraph_Mode.isChecked())

    def __initToolMenu(self):
        pass
        # modeMenuGroup = QActionGroup(self)
        # modeMenuGroup.addAction(self.ui.actionRedigraph_s_Degrees)
        # modeMenuGroup.addAction(self.ui.menuDigraph_s_Degrees)
        # self.ui.menuDigraph_s_Degrees.setEnabled(self.ui.actionRedigraph_Mode.isChecked())

    def __updateEdgeView(self):
        edges = self.singleItems(BezierEdge)
        if len(edges):
            self.ui.edgeDetails.setEnabled(True)
        else:
            return
        edgeColCount = 5

        self.edgeModel.clear()
        edgeHeaderList = ['ID', '始点', '终点', '坐标', '权重']
        self.edgeModel.setHorizontalHeaderLabels(edgeHeaderList)
        self.edgeSelectionModel.currentChanged.connect(self.do_curEdgeChanged)

        self.ui.edgeDetails.setModel(self.edgeModel)
        self.ui.edgeDetails.setSelectionModel(self.edgeSelectionModel)
        self.ui.edgeDetails.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.edgeDetails.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.edgeDetails.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.edgeDetails.setAlternatingRowColors(True)
        self.edgeModel.setRowCount(len(edges))
        edges.reverse()
        for i in range(len(edges)):
            edge: BezierEdge = edges[i]
            sourceNode = f'V{edge.sourceNode.data(self.__NodeId)}' if edge.sourceNode else None
            destNode = f'V{edge.destNode.data(self.__NodeId)}' if edge.destNode else None

            strList = [f"e{edge.data(self.__EdgeId)}", sourceNode,
                       destNode, f"x:{edge.pos().x()},y:{edge.pos().y()}",
                       f"{edge.weight()}"]

            for j in range(edgeColCount):
                item = QStandardItem(strList[j])
                if j != edgeColCount - 1:
                    item.setFlags(self.__lastColumnFlag)
                self.edgeModel.setItem(i, j, item)

    def __updateNodeView(self):
        nodes = self.singleItems(BezierNode)
        if len(nodes):
            self.ui.nodeDetails.setEnabled(True)
        else:
            return
        nodeColCount = 4
        self.nodeModel.clear()
        nodeHeaderList = ['ID', '边数', '坐标', '权重']
        if self.ui.actionDigraph_Mode.isChecked():
            nodeHeaderList.append('出度')
            nodeHeaderList.append('入度')
            nodeColCount += 2
        else:
            nodeHeaderList.append("度")
            nodeColCount += 1
        self.nodeModel.setHorizontalHeaderLabels(nodeHeaderList)
        self.nodeModel.setRowCount(len(nodes))
        self.nodeSelectionModel.currentChanged.connect(self.do_curNodeChanged)
        self.ui.nodeDetails.setModel(self.nodeModel)
        self.ui.nodeDetails.setSelectionModel(self.nodeSelectionModel)
        self.ui.nodeDetails.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.nodeDetails.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.nodeDetails.setAlternatingRowColors(True)
        nodes.reverse()
        for i in range(len(nodes)):
            node: BezierNode = nodes[i]
            strList = [f"V{node.data(self.__NodeId)}", str(len(node.bezierEdges)),
                       f"x:{node.pos().x()},y:{node.pos().y()}", str(node.weight())]
            if self.ui.actionDigraph_Mode.isChecked():
                strList.append(f'{node.digraphDegrees(self.ui.actionDigraph_Mode.isChecked())[1]}')
                strList.append(f'{node.digraphDegrees(self.ui.actionDigraph_Mode.isChecked())[0]}')
            else:
                strList.append(f'{node.digraphDegrees(self.ui.actionDigraph_Mode.isChecked())}')
            for j in range(nodeColCount):
                item = QStandardItem(strList[j])
                if j != 3:
                    item.setFlags(self.__lastColumnFlag)
                self.nodeModel.setItem(i, j, item)

    def singleItems(self, className) -> list:
        self.viewAndScene()
        return self.__scene.singleItems(className)

    def connectGraph(self):
        self.__graph.setMode(self.ui.actionDigraph_Mode.isChecked())
        items = self.__scene.uniqueItems()
        nodeList = []
        edgeList = []
        if not len(items):
            return
        for item in items:
            if type(item) is BezierNode:
                nodeList.append(item)
            elif type(item) is BezierEdge:
                edgeList.append(item)
        for node in nodeList:
            self.__graph.addVertex(node.data(self.__NodeId))

        badEdgeList = []
        for i in range(len(edgeList)):
            for edge in edgeList:
                edge: BezierEdge
                if edge.data(self.__EdgeId) == i:
                    if edge.sourceNode and edge.destNode:
                        self.__graph.addEdge(edge.sourceNode.data(self.__NodeId), edge.destNode.data(self.__NodeId),
                                             edge.weight())
                    else:
                        badEdgeList.append(edge)

        if len(badEdgeList) != 0:
            string = ""
            for x in range(len(badEdgeList)):
                demo = "、"
                if x == len(badEdgeList) - 1:
                    demo = ""
                string = f'{string}e{badEdgeList[x].data(self.__EdgeId)}{demo}'
            QMessageBox.warning(self, "连接故障！", "警告，" + string + "的连接不完整")
            return False

        return True

    def disconnectGraph(self):
        self.__graph.clearAllData()

    def viewAndScene(self):
        if self.ui.tabWidget.count():
            self.__view: GraphicsView = self.ui.tabWidget.currentWidget()
            self.__scene = self.__view.scene()

    # ==============event处理函数==========================

    # def closeEvent(self, event):  # 退出函数
    #
    #     msgBox = QMessageBox()
    #     msgBox.setWindowTitle('关闭')
    #     msgBox.setText("是否保存")
    #     msgBox.setIcon(QMessageBox.Question)
    #     btn_Do_notSave = msgBox.addButton('不保存', QMessageBox.AcceptRole)
    #     btn_cancel = msgBox.addButton('取消', QMessageBox.RejectRole)
    #     btn_save = msgBox.addButton('保存', QMessageBox.AcceptRole)
    #     msgBox.setDefaultButton(btn_save)
    #     msgBox.exec_()
    #
    #     if msgBox.clickedButton() == btn_Do_notSave:
    #         event.accept()
    #     elif msgBox.clickedButton() == btn_cancel:
    #         event.ignore()
    #     elif msgBox.clickedButton() == btn_save:
    #         self.do_save_file()
    #         event.accept()

    # def contextMenuEvent(self, event):  # 右键菜单功能
    #     rightMouseMenu = QMenu(self)
    #
    #     rightMouseMenu.addAction(self.ui.actionNew)
    #     rightMouseMenu.addAction(self.ui.actionOpen)
    #
    #     self.action = rightMouseMenu.exec_(self.mapToGlobal(event.pos()))

    #  ==========由connectSlotsByName()自动连接的槽函数============
    @Slot()  # 新建画板
    def on_actionNew_triggered(self):
        self.iniGraphicsSystem()

    @Slot()  # 添加边
    def on_actionArc_triggered(self):  # 添加曲线
        # self.viewAndScene()
        item = BezierEdge()
        item.setGraphMode(self.ui.actionDigraph_Mode.isChecked())
        self.__setItemProperties(item, "边")
        self.do_addItem(item)
        self.__updateEdgeView()
        self.__updateNodeView()

    @Slot()  # 添加顶点
    def on_actionCircle_triggered(self):  # 添加原点
        self.viewAndScene()
        item = BezierNode()
        self.__setItemProperties(item, "顶点")
        self.do_addItem(item)
        self.__updateNodeView()
        self.__updateEdgeView()

    @Slot()  # 添加矩形框
    def on_actionRectangle_triggered(self):  # 添加矩形

        for item in self.singleItems(BezierNode):
            print(item.data(2), item.bezierEdges)
        pass

    @Slot()  # 添加注释
    def on_actionAdd_Annotation_triggered(self):
        self.viewAndScene()
        strText, OK = QInputDialog.getText(self, "输入", "请输入文字")
        if not OK:
            return
        item = BezierText(strText)
        self.__setItemProperties(item, "注释")
        self.do_addItem(item)

    @Slot(bool)  # 显示和隐藏结点权重
    def on_actionShowNodesWeight_toggled(self, check: bool):
        nodes = self.__scene.singleItems(BezierNode)
        for node in nodes:
            node: BezierNode
            node.weightCp.setVisible(check)

        if check:
            self.ui.actionShowNodesWeight.setText("隐藏顶点权重")
        else:
            self.ui.actionShowNodesWeight.setText("显示顶点权重")

    @Slot(bool)  # 显示和隐藏边权重
    def on_actionShowEdgesWeight_toggled(self, check: bool):
        edges = self.__scene.singleItems(BezierEdge)
        for edge in edges:
            edge: BezierNode
            edge.weightCp.setVisible(check)
        if check:
            self.ui.actionShowEdgesWeight.setText("隐藏边权重")
        else:
            self.ui.actionShowEdgesWeight.setText("显示边权重")

    @Slot()  # 简单通路
    def on_actionEasy_Pathway_triggered(self):
        self.viewAndScene()
        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "对不起，你没有选择起始节点")
            return
        elif len(items) != 2:
            QMessageBox.warning(self, "警告", "选择的起始点数目不符合要求")
            return

        if self.connectGraph():
            PathWay = ShowDataWidget(self, items, self.__graph, name="简单通路")
            PathWay.pathSignal.connect(self.do_ShowSelectPath)
            if PathWay.easyPath():
                PathWay.updateToolWidget()
                PathWay.show()

    @Slot()  # 简单回路
    def on_actionEasy_Loop_triggered(self):
        self.viewAndScene()
        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "对不起，你没有选择起始节点")
            return

        if self.connectGraph():
            LoopWay = ShowDataWidget(self, items, self.__graph, name="简单回路")
            LoopWay.pathSignal.connect(self.do_ShowSelectPath)
            if LoopWay.easyLoop():
                LoopWay.updateToolWidget(mode=1)
                LoopWay.show()

    @Slot()  # 初级通路
    def on_actionPrimary_Pathway_triggered(self):
        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "对不起，你没有选择起始节点")
            return
        elif len(items) != 2:
            QMessageBox.warning(self, "警告", "选择的起始点数目不符合要求")
            return

        if self.connectGraph():
            PathWay = ShowDataWidget(self, items, self.__graph, name="简单通路")
            PathWay.pathSignal.connect(self.do_ShowSelectPath)
            if PathWay.primaryPath():
                PathWay.updateToolWidget(path=1)
                PathWay.show()

    @Slot()  # 初级回路
    def on_actionPrimary_Loop_triggered(self):
        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "对不起，你没有选择起始节点")
            return

        if self.connectGraph():
            LoopWay = ShowDataWidget(self, items, self.__graph, name="简单回路")
            LoopWay.pathSignal.connect(self.do_ShowSelectPath)
            if LoopWay.primaryLoop():
                LoopWay.updateToolWidget(mode=1, path=1)
                LoopWay.show()

    @Slot()  # 邻接矩阵 边数
    def on_action_EdgeNum_triggered(self):
        self.viewAndScene()
        items = self.__scene.singleItems(BezierNode)
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "图中没有结点")
            return
        if self.connectGraph():
            MatrixTable = ShowMatrixWidget(self, self.__graph, "邻接矩阵", 0)
            MatrixTable.show()

    @Slot()  # 邻接矩阵 权重
    def on_actionWeight_triggered(self):
        self.viewAndScene()
        items = self.__scene.singleItems(BezierNode)
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "图中没有结点")
            return
        if self.connectGraph():
            if not self.__graph.multipleOrSimple():
                MatrixTable = ShowMatrixWidget(self, self.__graph, "邻接矩阵", 1)
                MatrixTable.show()
            else:
                QMessageBox.information(self, "Sorry", "这个图不是简单图")
                self.disconnectGraph()

    @Slot()  # 可达矩阵
    def on_actionReachable_Matrix_triggered(self):
        self.viewAndScene()
        items = self.__scene.singleItems(BezierNode)
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "图中没有结点")
            return
        if self.connectGraph():
            MatrixTable = ShowMatrixWidget(self, self.__graph, "可达矩阵")
            MatrixTable.show()

    @Slot()  # 关联矩阵
    def on_actionIncidence_Matrix_Undigraph_triggered(self):
        self.viewAndScene()
        items = self.__scene.singleItems(BezierNode)
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "图中没有结点")
            return
        if self.ui.actionDigraph_Mode.isChecked():
            items = self.singleItems(BezierEdge)
            badNodeList = []
            badNodes = ''
            for x in range(len(items)):
                if items[x].sourceNode is not None and items[x].destNode is not None:
                    if items[x].sourceNode == items[x].destNode:
                        badNodeList.append(items[x])
                        demo = "、"
                        if x == len(items) - 1:
                            demo = ""
                        badNodes = f"{badNodes}V{items[x].sourceNode.data(self.__NodeId)}{demo}"
            if len(badNodeList):
                QMessageBox.warning(self, "致命错误", f"有向图的关联矩阵需要有向图无环,而{badNodes}存在环！")
                return
        if self.connectGraph():
            MatrixTable = ShowMatrixWidget(self, self.__graph, "关联矩阵")
            MatrixTable.show()

    @Slot()  # 图的连通性
    def on_actionConnectivity_triggered(self):
        print(True)
        name = ''
        if self.connectGraph():
            num = self.__graph.connectivity()
            if num is False:
                name = '此图为非连通图'
            elif num == 2:
                name = "此图为单向连通图"
            elif num == 3:
                name = "此图为强连通图"
            elif num == 1:
                name = '此图为连通图'

            QMessageBox.information(self, "图的连通性", name)

            self.disconnectGraph()

    @Slot()  # 完全图判定
    def on_actionCompleteGraph_triggered(self):
        if self.connectGraph():
            edge = self.__graph.completeGraph()
            if edge:
                name = "此图为完全图"
            else:
                name = '此图不是完全图'

            QMessageBox.information(self, "完全图判定", name)

            self.disconnectGraph()

    @Slot()  # 简单图多重图判定
    def on_actionMultipleOrSimple_triggered(self):
        print(True)
        if self.connectGraph():
            edges = self.__graph.multipleOrSimple()
            if not edges:
                QMessageBox.information(self, "简单图与多重图的判定", "此图为简单图")

            else:
                parallelSides = ShowDataWidget(self, edges, self.__graph, "简单图与多重图的判定")
                parallelSides.multipleOrSimple()
                parallelSides.show()

    @Slot()
    def on_actionShortestPath_triggered(self):

        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, "警告", "对不起，你没有选择结点")
            return
        if self.connectGraph():
            ShortestPath = ShowDataWidget(self, items, self.__graph, name="最短路径")
            ShortestPath.pathSignal.connect(self.do_ShowSelectPath)
            if ShortestPath.shortestPath():
                ShortestPath.updateToolWidget(mode=1, path=2)
                ShortestPath.show()

    @Slot()
    def on_actionUndo_triggered(self):  # 撤销
        self.undoStack.undo()
        self.__updateEdgeView()
        self.__updateNodeView()

    @Slot()
    def on_actionRedo_triggered(self):  # 重做
        self.undoStack.redo()
        self.__updateEdgeView()
        self.__updateNodeView()

    # @Slot()
    # def on_actionPen_Color_triggered(self):  # 画笔颜色
    #     iniColor = self.view.getPenColor()
    #     color = QColorDialog.getColor(iniColor, self, "选择颜色")
    #     if color.isValid():
    #         self.view.setPenColor(color)

    @Slot()
    def on_actionPen_Thickness_triggered(self):  # 画笔粗细
        self.viewAndScene()
        iniThickness = self.__view.getPenThickness()
        intPenStyle = self.__view.getPenStyle()
        thicknessDialog = ThicknessDialog(None, "画笔粗细与样式", iniThickness, intPenStyle)
        ret = thicknessDialog.exec_()
        thickness = thicknessDialog.getThickness()
        penStyle = thicknessDialog.getPenStyle()
        self.__view.setPenStyle(penStyle)
        self.__view.setPenThickness(thickness)

    @Slot()
    def on_actionBackground_Color_triggered(self):
        self.viewAndScene()
        iniColor = self.__view.getBackgroundColor()
        color = QColorDialog.getColor(iniColor, self, "选择颜色")
        if color.isValid():
            self.__view.setBackgroundBrush(color)

    # @Slot(bool)
    # def on_actionProperty_And_History_triggered(self, checked):
    #     self.ui.dockWidget.setVisible(checked)

    @Slot()
    def on_actionSave_Image_triggered(self):
        self.viewAndScene()
        savePath, fileType = QFileDialog.getSaveFileName(self, '保存图片', '.\\', '*bmp;;*.png')
        # if savePath[0] == "":
        #     print("Save cancel")
        #     return
        filename = os.path.basename(savePath)
        if filename != "":
            self.__view.saveImage(savePath, fileType)

    @Slot()
    def on_actionDelete_triggered(self):
        self.viewAndScene()
        self.do_deleteItem()

    @Slot(bool)
    def on_actionDigraph_Mode_toggled(self, checked: bool):
        self.__labModeInfo.setText("有向图模式")
        self.__graph.setMode(checked)
        items = self.__scene.uniqueItems()
        if len(items) != 0:
            dlgTitle = "警告！！"
            strInfo = "更换模式会清楚画板所有元素！是否要更换模式"
            result = QMessageBox.question(self, dlgTitle, strInfo, QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.NoButton)
            if result == QMessageBox.Yes:
                self.__edgeNum = 0
                self.__nodeNum = 0
                self.__seqNum = 0
                cnt = len(items)
                for i in range(cnt):
                    item = items[i]
                    if str(type(item)).find("BezierNode") >= 0:
                        item: BezierNode
                        for edge in item.bezierEdges:
                            for node, itemType in edge.items():
                                if itemType == ItemType.SourceType:
                                    node.setSourceNode(None)
                                elif itemType == ItemType.DestType:
                                    node.setDestNode(None)
                    elif str(type(item)).find("BezierEdge") >= 0:
                        item: BezierEdge
                        sourceNode: BezierNode = item.sourceNode
                        destNode: BezierNode = item.destNode
                        if sourceNode:
                            sourceNodeList = sourceNode.bezierEdges
                            for sourceEdge in sourceNodeList:
                                for edge in sourceEdge.keys():
                                    if item is edge:
                                        sourceNodeList.remove(sourceEdge)
                        if destNode:
                            destNodeList = destNode.bezierEdges
                            for destEdge in destNodeList:
                                for edge in destEdge.keys():
                                    if item is edge:
                                        destNodeList.remove(destEdge)

                    self.__scene.removeItem(item)  # 删除绘图项
        # self.ui.actionRedigraph_s_Degrees.setEnabled(self.ui.actionRedigraph_Mode.isChecked())

    @Slot(bool)
    def on_actionRedigraph_Mode_toggled(self, checked: bool):
        self.__labModeInfo.setText("无向图模式")
        self.__graph.setMode(checked)
        items = self.__scene.uniqueItems()
        if len(items) != 0:
            dlgTitle = "警告！！"
            strInfo = "更换模式会清楚画板所有元素！是否要更换模式"
            result = QMessageBox.question(self, dlgTitle, strInfo, QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.NoButton)
            if result == QMessageBox.Yes:
                self.__edgeNum = 0
                self.__nodeNum = 0
                self.__seqNum = 0
                cnt = len(items)
                for i in range(cnt):
                    item = items[i]
                    if str(type(item)).find("BezierNode") >= 0:
                        item: BezierNode
                        for edge in item.bezierEdges:
                            for node, itemType in edge.items():
                                if itemType == ItemType.SourceType:
                                    node.setSourceNode(None)
                                elif itemType == ItemType.DestType:
                                    node.setDestNode(None)
                    elif str(type(item)).find("BezierEdge") >= 0:
                        item: BezierEdge
                        sourceNode: BezierNode = item.sourceNode
                        destNode: BezierNode = item.destNode
                        if sourceNode:
                            sourceNodeList = sourceNode.bezierEdges
                            for sourceEdge in sourceNodeList:
                                for edge in sourceEdge.keys():
                                    if item is edge:
                                        sourceNodeList.remove(sourceEdge)
                        if destNode:
                            destNodeList = destNode.bezierEdges
                            for destEdge in destNodeList:
                                for edge in destEdge.keys():
                                    if item is edge:
                                        destNodeList.remove(destEdge)

                    self.__scene.removeItem(item)  # 删除绘图项

    @Slot(int)
    def on_tabWidget_currentChanged(self, index):  # ui.tabWidget当前页面变化
        self.viewAndScene()
        self.__updateEdgeView()
        self.__updateNodeView()
        hasTabs = self.ui.tabWidget.count() > 0  # 再无页面时
        self.ui.tabWidget.setVisible(hasTabs)

    @Slot(int)
    def on_tabWidget_tabCloseRequested(self, index):  # 分页关闭时关闭窗体
        if index < 0:
            return
        aForm = self.ui.tabWidget.widget(index)
        aForm.close()
        self.ui.tabWidget.tabBar().removeTab(index)

    #  =============自定义槽函数===============================
    def do_nodeLock(self, item):
        self.__updateNodeView()
        self.__updateEdgeView()

    def do_mouseMove(self, point):  ##鼠标移动
        ##鼠标移动事件，point是 GraphicsView的坐标,物理坐标
        self.__labViewCord.setText("View 坐标：%d,%d" % (point.x(), point.y()))
        pt = self.ui.tabWidget.currentWidget().mapToScene(point)  # 转换到Scene坐标
        self.__labSceneCord.setText("Scene 坐标：%.0f,%.0f" % (pt.x(), pt.y()))

    def do_mouseClicked(self, point):  ##鼠标单击
        pt = self.__view.mapToScene(point)  # 转换到Scene坐标
        item = self.__scene.itemAt(pt, self.__view.transform())  # 获取光标下的图形项
        if item is None:
            return
        pm = item.mapFromScene(pt)  # 转换为绘图项的局部坐标
        self.__labItemCord.setText("Item 坐标：%.0f,%.0f" % (pm.x(), pm.y()))
        data = f"{item.data(self.__ItemDesc)}, ItemId={item.data(self.__ItemId)}"
        if type(item) is BezierEdge:
            data = f"{data},EdgeId=e{item.data(self.__EdgeId)}"
        elif type(item) is BezierNode:
            data = f"{data}, NodeId=V{item.data(self.__NodeId)}"
        self.__labItemInfo.setText(data)

    def do_mouseDoubleClick(self, point):  ##鼠标双击
        pt = self.__view.mapToScene(point)  # 转换到Scene坐标,QPointF
        item = self.__scene.itemAt(pt, self.__view.transform())  # 获取光标下的绘图项
        if item is None:
            return

        className = str(type(item))  # 将类名称转换为字符串
        ##      print(className)

        if className.find("QGraphicsRectItem") >= 0:  # 矩形框
            self.__setBrushColor(item)
        elif className.find("QGraphicsEllipseItem") >= 0:  # 椭圆和圆都是 QGraphicsEllipseItem
            self.__setBrushColor(item)
        elif className.find("QGraphicsPolygonItem") >= 0:  # 梯形和三角形
            self.__setBrushColor(item)
        elif className.find("QGraphicsLineItem") >= 0:  # 直线，设置线条颜色
            pen = item.pen()
            color = item.pen().__color()
            color = QColorDialog.getColor(color, self, "选择线条颜色")
            if color.isValid():
                pen.setColor(color)
                item.setPen(pen)
        elif className.find("QGraphicsTextItem") >= 0:  # 文字，设置字体
            font = item.font()
            font, OK = QFontDialog.getFont(font)
            if OK:
                item.setFont(font)

    def do_save_file(self):  # 保存文件
        savePath, fileType = QFileDialog.getSaveFileName(self, '保存文件', '.\\', '*.graph;;*.json;;*.csv')

        filename = os.path.basename(savePath)

        if filename != "":
            if fileType == '*.json':
                pass
                # self.operatorData.save_Json(filename, nodes)
            elif fileType == '*.csv':
                pass
                # self.operatorData.save_Csv(filename, ['point(1)', 'point(2)'], nodes)
            elif fileType == '*.graph':
                self.operatorData.save_Graph(filename, self.__view.getContentAsGraph())

    def do_open_file(self):  # 打开文件
        dict_file = {}
        openPath, fileType = QFileDialog.getOpenFileName(self, '打开文件', '.\\', '*.graph;;*.json;;*.csv')

        if fileType == '*.json':
            dict_file = self.operatorData.open_Json(openPath)
        elif fileType == '*.csv':
            dict_file = self.operatorData.open_Csv(openPath)
        elif fileType == '*.graph':
            dict_file = self.operatorData.open_Graph(openPath)

        return dict_file

    def do_addItem(self, item):
        add = AddCommand(self, self.__scene, item)
        self.undoStack.push(add)

    def do_shapeMoved(self, item, pos):
        move = MoveCommand(item, pos)
        self.undoStack.push(move)

    def do_deleteItem(self):
        items = self.__scene.selectedItems()
        cnt = len(items)
        for i in range(cnt):
            item = items[i]
            if str(type(item)).find("BezierNode") >= 0:
                item: BezierNode
                for edge in item.bezierEdges:
                    for node, itemType in edge.items():
                        if itemType == ItemType.SourceType:
                            node.setSourceNode(None)
                        elif itemType == ItemType.DestType:
                            node.setDestNode(None)
                self.__nodeNum -= 1
            elif str(type(item)).find("BezierEdge") >= 0:
                item: BezierEdge
                sourceNode: BezierNode = item.sourceNode
                destNode: BezierNode = item.destNode
                if sourceNode:
                    sourceNodeList = sourceNode.bezierEdges
                    for sourceEdge in sourceNodeList:
                        for edge in sourceEdge.keys():
                            if item is edge:
                                sourceNodeList.remove(sourceEdge)
                if destNode:
                    destNodeList = destNode.bezierEdges
                    for destEdge in destNodeList:
                        for edge in destEdge.keys():
                            if item is edge:
                                destNodeList.remove(destEdge)
                self.__edgeNum -= 1

            self.__scene.removeItem(item)  # 删除绘图项

    def do_curEdgeChanged(self, current, previous):
        if current is not None:
            text = f"当前单元格{current.row()},{current.column()}"
            item = self.edgeModel.itemFromIndex(current)

    def do_curNodeChanged(self, current, previous):
        if current is not None:
            text = f"当前单元格{current.row()},{current.column()}"
            item = self.nodeModel.itemFromIndex(current)

    def do_updateEdgeWeight(self, topLeft, bottomRight):
        if topLeft.column() == 4:
            edges = self.__scene.singleItems(BezierEdge)
            for edge in edges:
                edge: BezierEdge
                if edge.textCp.toPlainText() == self.edgeModel.index(topLeft.row(), 0, QModelIndex()).data():
                    edge.weightCp.setPlainText(topLeft.data())
                    self.__scene.update()

    def do_updateNodeWeight(self, topLeft, bottomRight):
        if topLeft.column() == 3:
            nodes = self.__scene.singleItems(BezierNode)
            for node in nodes:
                node: BezierNode
                if node.textCp.toPlainText() == self.nodeModel.index(topLeft.row(), 0, QModelIndex()).data():
                    node.weightCp.setPlainText(topLeft.data())
                    self.__scene.update()

    def do_ShowSelectPath(self, pathList: list):
        self.__scene.clearSelection()
        items = self.__scene.uniqueItems()
        for item in items:
            if item.textCp.toPlainText() in pathList:
                item.setSelected(True)


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = MainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
