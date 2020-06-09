# -*- coding: utf-8 -*-
import os
import sys, random
from PySide2.QtCore import Slot, Qt, QRectF, QItemSelectionModel

from PySide2.QtGui import QBrush, QStandardItemModel, QStandardItem

from PySide2.QtWidgets import QApplication, QMainWindow, QColorDialog, \
    QInputDialog, QLabel, QMessageBox, QFileDialog, QActionGroup, QUndoStack, QGraphicsItem, QGraphicsView, QFontDialog, \
    QHeaderView, QAbstractItemView

from BezierEdge import BezierEdge
from BezierNode import BezierNode
from BezierText import BezierText
from Graph import Graph
from GraphicsScene import GraphicsScene
from GraphicsView import GraphicsView
from PointItem import ItemType
from ShowMatrixWidget import ShowMatrixWidget
from UndoCommand import AddCommand, MoveCommand
from ui_MainWindow import Ui_MainWindow
from ThicknessDialog import ThicknessDialog
from OperatorFile import OperatorData


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面

        self.setWindowTitle("离散数学可视化认知系统")

        self.ui.nodeDetails.setEnabled(False)
        self.ui.edgeDetails.setEnabled(False)
        self.tableWidget = self.ui.tabWidget

        self.tableWidget.setVisible(False)
        self.tableWidget.clear()
        self.tableWidget.setTabsClosable(True)
        self.tableWidget.setDocumentMode(True)

        self.setCentralWidget(self.tableWidget)
        self.setAutoFillBackground(True)

        self.__buildStatusBar()  # 构造状态栏
        # self.__iniGraphicsSystem()  # 初始化 graphics View系统
        self.__buildUndoCommand()  # 初始化撤销重做系统
        self.__initModeMenu()
        self.__initToolMenu()

        # self.__updateNodeView()
        # self.__updateEdgeView()

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

    def __iniGraphicsSystem(self):  ##初始化 Graphics View系统

        self.scene = GraphicsScene(self)  # 创建QGraphicsScene
        self.scene.setSceneRect(QRectF(-300, -200, 600, 200))
        self.view = GraphicsView(self, self.scene)  # 创建图形视图组件
        self.view.setCursor(Qt.CrossCursor)  # 设置鼠标
        self.view.setMouseTracking(True)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)

        self.setCentralWidget(self.view)

        self.view.mouseMove.connect(self.do_mouseMove)  # 鼠标移动
        self.view.mouseClicked.connect(self.do_mouseClicked)  # 左键按下
        self.scene.itemMoveSignal.connect(self.do_shapeMoved)
        self.scene.itemLock.connect(self.do_nodeLock)

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

        self.scene.addItem(item)
        self.scene.clearSelection()
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
        self.ui.actionRedigraph_s_Degrees.setEnabled(not self.ui.actionDigraph_Mode.isChecked())

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
        edgeModel = QStandardItemModel(5, edgeColCount, self)
        edgeSelectionModel = QItemSelectionModel(edgeModel)
        edgeModel.clear()
        edgeHeaderList = ['ID', '始点', '终点', '坐标', '权重']
        edgeModel.setHorizontalHeaderLabels(edgeHeaderList)

        self.ui.edgeDetails.setModel(edgeModel)
        self.ui.edgeDetails.setSelectionModel(edgeSelectionModel)
        self.ui.edgeDetails.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.edgeDetails.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.edgeDetails.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.edgeDetails.setAlternatingRowColors(True)
        edgeModel.setRowCount(len(edges))
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
                edgeModel.setItem(i, j, item)

    # def __updateNodeView(self):
    #     nodes = self.singleItems(BezierNode)
    #     if len(nodes):
    #         self.ui.nodeDetails.setEnabled(True)
    #     else:
    #         return
    #     nodeColCount = 4
    #     nodeModel = QStandardItemModel(5, nodeColCount, self)
    #     nodeModel.clear()
    #     nodeSelectionModel = QItemSelectionModel(nodeModel)
    #     nodeHeaderList = ['ID', '边数', '坐标', '权重']
    #     if self.ui.actionDigraph_Mode.isChecked():
    #         nodeHeaderList.append('出度')
    #         nodeHeaderList.append('入度')
    #         nodeColCount += 2
    #     else:
    #         nodeHeaderList.append("度")
    #         nodeColCount += 1
    #     nodeModel.setHorizontalHeaderLabels(nodeHeaderList)
    #     nodeModel.setRowCount(len(nodes))
    #     # nodeSelectionModel.currentChanged.connect(self.do_curChanged)
    #     self.ui.nodeDetails.setModel(nodeModel)
    #     self.ui.nodeDetails.setSelectionModel(nodeSelectionModel)
    #     self.ui.nodeDetails.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    #     self.ui.nodeDetails.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #     self.ui.nodeDetails.setAlternatingRowColors(True)
    #     nodes.reverse()
    #     for i in range(len(nodes)):
    #         node: BezierNode = nodes[i]
    #         strList = [f"V{node.data(self.__NodeId)}", str(len(node.bezierEdges)),
    #                    f"x:{node.pos().x()},y:{node.pos().y()}", str(node.data(self.__NodeId))]
    #         if self.ui.actionDigraph_Mode.isChecked():
    #             strList.append(f'{node.digraphDegrees(self.ui.actionDigraph_Mode.isChecked())[1]}')
    #             strList.append(f'{node.digraphDegrees(self.ui.actionDigraph_Mode.isChecked())[0]}')
    #         else:
    #             strList.append(f'{node.digraphDegrees(self.ui.actionDigraph_Mode.isChecked())}')
    #         for j in range(nodeColCount):
    #             item = QStandardItem(strList[j])
    #             nodeModel.setItem(i, j, item)
    #
    # def __updateDataDetail(self, name: str):
    #     self.connectGraph()
    #     data = None
    #     HorizontalHeaderList = []
    #     VerticalHeaderList = []
    #     dataDetailView = None
    #     if name == "邻接矩阵":
    #         data = self.__graph.adjacentMatrix()
    #         for node in self.__graph:
    #             HorizontalHeaderList.append(f'V{node.id()}')
    #         VerticalHeaderList = HorizontalHeaderList
    #         dataDetailView = self.ui.adjacentMatrixDetails
    #     elif name == "可达矩阵":
    #         temp = self.__graph.reachableMatrix()
    #         data = temp[0]
    #         step = temp[1]
    #         for node in self.__graph:
    #             HorizontalHeaderList.append(f'V{node.id()}')
    #         VerticalHeaderList = HorizontalHeaderList
    #         dataDetailView = self.ui.reachableMatrixDetails
    #         self.ui.incidenceLabel.setText(f"可达矩阵，步数{step}")
    #     elif name == "关联矩阵":
    #         for node in self.__graph:
    #             VerticalHeaderList.append(f'V{node.id()}')
    #         for edge in self.__graph.edges():
    #             HorizontalHeaderList.append(f'e{edge}')
    #         data = self.__graph.incidenceMatrix()
    #         dataDetailView = self.ui.incidenceMatrixDetails
    #
    #     dataDetailView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #
    #     HorizontalHeaderList.reverse()
    #     colCount = data.shape[1]
    #     rowCount = data.shape[0]
    #     data = data.tolist()
    #
    #     dataModel = QStandardItemModel(rowCount, colCount, self)
    #     dataSelectionModel = QItemSelectionModel(dataModel)
    #     dataModel.clear()
    #     dataModel.setHorizontalHeaderLabels(HorizontalHeaderList)
    #     dataModel.setVerticalHeaderLabels(VerticalHeaderList)
    #     dataDetailView.setModel(dataModel)
    #     dataDetailView.setSelectionModel(dataSelectionModel)
    #     dataDetailView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    #     dataDetailView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #     dataDetailView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #     dataDetailView.setAlternatingRowColors(True)
    #
    #     for i in range(rowCount):
    #         strList = []
    #         for x in data[i]:
    #             strList.append(f"{x}")
    #         for j in range(colCount):
    #             item = QStandardItem(strList[j])
    #             dataModel.setItem(i, j, item)
    #
    #     dataModel.setRowCount(rowCount)

    # def singleItems(self, className) -> list:
    #     items = []
    #     for item in self.scene.uniqueItems():
    #         if type(item) is className:
    #             items.append(item)
    #     return items

    # def connectGraph(self):
    #     self.__graph.setMode(self.ui.actionDigraph_Mode.isChecked())
    #     items = self.scene.uniqueItems()
    #     nodeList = []
    #     edgeList = []
    #     if not len(items):
    #         return
    #     for item in items:
    #         if type(item) is BezierNode:
    #             nodeList.append(item)
    #         elif type(item) is BezierEdge:
    #             edgeList.append(item)
    #     for node in nodeList:
    #         self.__graph.addVertex(node.data(self.__NodeId))
    #
    #     badEdgeList = []
    #     for i in range(len(edgeList)):
    #         for edge in edgeList:
    #             edge: BezierEdge
    #             if edge.data(self.__EdgeId) == i:
    #                 if edge.sourceNode and edge.destNode:
    #                     self.__graph.addEdge(edge.sourceNode.data(self.__NodeId), edge.destNode.data(self.__NodeId),
    #                                          edge.weight())
    #                 else:
    #                     badEdgeList.append(edge)
    #
    #     if len(badEdgeList) != 0:
    #         string = ""
    #         for x in range(len(badEdgeList)):
    #             demo = "、"
    #             if x == len(badEdgeList) - 1:
    #                 demo = ""
    #             string = f'{string}e{badEdgeList[x].data(self.__EdgeId)}{demo}'
    #         QMessageBox.warning(self, "连接故障！", "警告，" + string + "的连接不完整")
    #         return False
    #     return True
    #
    # def disconnectGraph(self):
    #     self.__graph.clearAllData()

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
    @Slot()
    def on_actionNew_triggered(self):
        scene = GraphicsScene(self)  # 创建QGraphicsScene
        scene.setSceneRect(QRectF(-300, -200, 600, 200))
        view = GraphicsView(self, scene)  # 创建图形视图组件
        view.setCursor(Qt.CrossCursor)  # 设置鼠标
        view.setMouseTracking(True)
        view.setDragMode(QGraphicsView.RubberBandDrag)

        view.setAttribute(Qt.WA_DeleteOnClose)

        view.mouseMove.connect(self.do_mouseMove)  # 鼠标移动
        # view.mouseClicked.connect(self.do_mouseClicked)  # 左键按下
        # scene.itemMoveSignal.connect(self.do_shapeMoved)
        # scene.itemLock.connect(self.do_nodeLock)

        title = f'Board{self.tableWidget.count()}'
        curIndex = self.tableWidget.addTab(view, title)
        self.tableWidget.setCurrentIndex(curIndex)
        self.tableWidget.setVisible(True)



    @Slot()
    def on_actionArc_triggered(self):  # 添加曲线
        item = BezierEdge()
        item.setGraphMode(self.ui.actionDigraph_Mode.isChecked())
        self.__setItemProperties(item, "边")
        self.do_addItem(item)
        self.__updateEdgeView()
        self.__updateNodeView()

    @Slot()
    def on_actionCircle_triggered(self):  # 添加原点
        item = BezierNode()
        # item.nodesLockOn.connect(self.do_nodeLock)
        self.__setItemProperties(item, "顶点")
        self.do_addItem(item)
        self.__updateNodeView()
        self.__updateEdgeView()

    @Slot()
    def on_actionRectangle_triggered(self):  # 添加矩形
        # for item in self.scene.items():
        #     if type(item) is BezierNode:
        #         print(item.data(2))
        #     elif type(item) is BezierEdge:
        #         print(item.data(3))
        # self.do_connectGraph()
        # print(self.scene.selectedItems())

        # for item in self.singleItems(BezierNode):
        #     print(item.data(2), item.bezierEdges)

        print(self.tableWidget.currentWidget())

        pass

    @Slot()
    def on_actionAdd_Annotation_triggered(self):
        strText, OK = QInputDialog.getText(self, "输入", "请输入文字")
        if not OK:
            return
        item = BezierText(strText)
        self.__setItemProperties(item, "注释")
        self.do_addItem(item)

    @Slot()
    def on_actionRedigraph_s_Degrees_triggered(self):  # 无向图的度
        if len(self.scene.selectedItems()):
            items = self.scene.selectedItems()
        elif len(self.scene.uniqueItems()):
            items = self.scene.uniqueItems()
        else:
            QMessageBox.warning(self, "警告", "图中没有元素")
            return
        copyItem = []
        for item in items:
            if str(type(item)).find("BezierNode") >= 0:
                copyItem.append(item)

        if len(copyItem) == 0:
            QMessageBox.warning(self, "警告", "图中没有结点")
            return

        if self.connectGraph():
            degrees = self.__graph.degrees()
            self.__graph.clearAllData()

    @Slot()
    def on_actionOut_degree_triggered(self):  # 有向图的出度
        pass

    @Slot()
    def on_actionIn_degree_triggered(self):  ## 有向图的入度
        pass

    @Slot()
    def on_actionAdjacent_Matrix_Digraph_triggered(self):
        if self.connectGraph():
            MatrixTable = ShowMatrixWidget(self, self.__graph, "邻接矩阵")
            MatrixTable.setWindowTitle('邻接矩阵')
            MatrixTable.setWindowFlag(Qt.Window, True)
            MatrixTable.setWindowOpacity(0.9)
            MatrixTable.show()

    @Slot()
    def on_actionReachable_Matrix_triggered(self):
        if self.connectGraph():
            MatrixTable = ShowMatrixWidget(self, self.__graph, "可达矩阵")
            MatrixTable.setWindowTitle('可达矩阵')
            MatrixTable.setWindowFlag(Qt.Window, True)
            MatrixTable.setWindowOpacity(0.9)
            MatrixTable.show()

    @Slot()
    def on_actionIncidence_Matrix_Undigraph_triggered(self):
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
            MatrixTable.setWindowTitle('关联矩阵')
            MatrixTable.setWindowFlag(Qt.Window, True)
            MatrixTable.setWindowOpacity(0.9)
            MatrixTable.show()

    # @Slot()
    # def on_actionUndo_triggered(self):  # 撤销
    #     self.command.undo()
    #
    # @Slot()
    # def on_actionRedo_triggered(self):  # 重做
    #     self.command.redo()

    # @Slot()
    # def on_actionPen_Color_triggered(self):  # 画笔颜色
    #     iniColor = self.view.getPenColor()
    #     color = QColorDialog.getColor(iniColor, self, "选择颜色")
    #     if color.isValid():
    #         self.view.setPenColor(color)

    @Slot()
    def on_actionPen_Thickness_triggered(self):  # 画笔粗细
        iniThickness = self.view.getPenThickness()
        intPenStyle = self.view.getPenStyle()
        thicknessDialog = ThicknessDialog(None, "画笔粗细与样式", iniThickness, intPenStyle)
        ret = thicknessDialog.exec_()
        thickness = thicknessDialog.getThickness()
        penStyle = thicknessDialog.getPenStyle()
        self.view.setPenStyle(penStyle)
        self.view.setPenThickness(thickness)

    @Slot()
    def on_actionBackground_Color_triggered(self):

        iniColor = self.view.getBackgroundColor()
        color = QColorDialog.getColor(iniColor, self, "选择颜色")
        if color.isValid():
            self.view.setBackgroundBrush(color)

    # @Slot(bool)
    # def on_actionProperty_And_History_triggered(self, checked):
    #     self.ui.dockWidget.setVisible(checked)

    @Slot()
    def on_actionSave_Image_triggered(self):
        savePath, fileType = QFileDialog.getSaveFileName(self, '保存图片', '.\\', '*bmp;;*.png')
        # if savePath[0] == "":
        #     print("Save cancel")
        #     return
        filename = os.path.basename(savePath)
        if filename != "":
            self.view.saveImage(savePath, fileType)

    @Slot()
    def on_actionDelete_triggered(self):
        self.do_deleteItem()

    @Slot(bool)
    def on_actionDigraph_Mode_triggered(self, checked: bool):
        self.__graph.setMode(checked)
        items = self.scene.uniqueItems()
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

                    self.scene.removeItem(item)  # 删除绘图项
        self.ui.actionRedigraph_s_Degrees.setEnabled(self.ui.actionRedigraph_Mode.isChecked())
        self.ui.menuDigraph_s_Degrees.setEnabled(self.ui.actionDigraph_Mode.isChecked())

    @Slot(bool)
    def on_actionRedigraph_Mode_triggered(self, checked: bool):
        self.__graph.setMode(checked)
        items = self.scene.uniqueItems()
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

                    self.scene.removeItem(item)  # 删除绘图项

        self.ui.actionRedigraph_s_Degrees.setEnabled(self.ui.actionRedigraph_Mode.isChecked())
        self.ui.menuDigraph_s_Degrees.setEnabled(self.ui.actionDigraph_Mode.isChecked())

    def on_tabWidget_currentChanged(self, index):  # tabWidget当前页面变化
        hasTabs = self.tabWidget.count() > 0  # 再无页面时
        self.tabWidget.setVisible(hasTabs)

    def on_tabWidget_tabCloseRequested(self, index):  # 分页关闭时关闭窗体
        if index < 0:
            return
        aForm = self.tabWidget.widget(index)
        aForm.close()

    #  =============自定义槽函数===============================
    def do_nodeLock(self, item):
        self.__updateNodeView()
        self.__updateEdgeView()

    def do_mouseMove(self, point):  ##鼠标移动
        ##鼠标移动事件，point是 GraphicsView的坐标,物理坐标
        self.__labViewCord.setText("View 坐标：%d,%d" % (point.x(), point.y()))
        pt = self.tableWidget.currentWidget().mapToScene(point)  # 转换到Scene坐标
        self.__labSceneCord.setText("Scene 坐标：%.0f,%.0f" % (pt.x(), pt.y()))

    def do_mouseClicked(self, point):  ##鼠标单击
        pt = self.view.mapToScene(point)  # 转换到Scene坐标
        item = self.scene.itemAt(pt, self.view.transform())  # 获取光标下的图形项
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
        pt = self.view.mapToScene(point)  # 转换到Scene坐标,QPointF
        item = self.scene.itemAt(pt, self.view.transform())  # 获取光标下的绘图项
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
                self.operatorData.save_Graph(filename, self.view.getContentAsGraph())

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
        add = AddCommand(self.scene, item)
        self.undoStack.push(add)

    def do_shapeMoved(self, item, pos):
        move = MoveCommand(item, pos)
        self.undoStack.push(move)

    def do_deleteItem(self):
        items = self.scene.selectedItems()
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

            self.scene.removeItem(item)  # 删除绘图项

    def do_curChanged(self, current, previous):
        if current is not None:
            text = f"当前单元格{current.row()},{current.column()}"
            item = self.nodeModel.itemFromIndex(current)


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = MainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
