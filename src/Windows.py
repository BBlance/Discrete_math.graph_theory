# -*- coding: utf-8 -*-
import os
import sys
from random import randint
from PySide2.QtCore import Slot, Qt, QRectF, QItemSelectionModel, QModelIndex, QDataStream, QIODevice, QDir, QFile, \
    QPointF, QLineF, QCoreApplication

from PySide2.QtGui import QBrush, QStandardItemModel, QStandardItem, QMouseEvent

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
from OperatorFile import OperatorFile
from webbrowser import open


class MainWindow(QMainWindow):
    _tr = QCoreApplication.translate

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.__scene = None  # 创建QGraphicsScene
        self.__view = None  # 创建图形视图组件
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面
        self.dir = QDir()
        self.operatorFile = OperatorFile(self)

        self.ui.menubar.raise_()

        self.__curFileName = ''
        self.__translator = None
        title = self.tr("基于Python的图的绘制及相关概念的可视化展示")
        self.setWindowTitle(title)

        self.ui.nodeDetails.setEnabled(False)
        self.ui.edgeDetails.setEnabled(False)
        self.ui.actionSave.setEnabled(False)

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
        self.__labViewCord = QLabel(self._tr("MainWindow", "视图坐标："))
        self.__labViewCord.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.__labViewCord)

        self.__labSceneCord = QLabel(self._tr("MainWindow", "场景坐标："))
        self.__labSceneCord.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.__labSceneCord)

        self.__labItemCord = QLabel(self._tr("MainWindow", "图元坐标："))
        self.__labItemCord.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.__labItemCord)

        self.__labItemInfo = QLabel(self._tr("MainWindow", "图元信息: "))
        self.ui.statusbar.addPermanentWidget(self.__labItemInfo)
        self.__labModeInfo = QLabel(self._tr("MainWindow", "有向图模式"))
        self.ui.statusbar.addPermanentWidget(self.__labModeInfo)

    def iniGraphicsSystem(self, name=None):  ##初始化 Graphics View系统

        scene = GraphicsScene(self)  # 创建QGraphicsScene
        view = GraphicsView(self, scene)  # 创建图形视图组件
        scene.setSceneRect(QRectF(-300, -200, 600, 200))
        view.setCursor(Qt.CrossCursor)  # 设置鼠标
        view.setMouseTracking(True)
        view.setDragMode(QGraphicsView.RubberBandDrag)

        view.mouseMove.connect(self.do_mouseMove)  # 鼠标移动
        view.mouseClicked.connect(self.do_mouseClicked)  # 左键按下
        scene.itemMoveSignal.connect(self.do_shapeMoved)
        scene.itemLock.connect(self.do_nodeLock)
        scene.isHasItem.connect(self.do_checkIsHasItems)
        if name:
            title = name
        else:
            text = self.tr('画板')
            title = f'{text}{self.ui.tabWidget.count()}'
        curIndex = self.ui.tabWidget.addTab(view, title)
        self.ui.tabWidget.setCurrentIndex(curIndex)
        self.ui.tabWidget.setVisible(True)
        self.ui.tabWidget.update()

        ##  4个信号与槽函数的关联

        # self.view.mouseDoubleClick.connect(self.do_mouseDoubleClick)  # 鼠标双击
        # self.view.keyPress.connect(self.do_keyPress)  # 左键按下

    def __buildUndoCommand(self):
        self.undoStack = QUndoStack()
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
        item.setPos(-150 + randint(1, 200), -200 + randint(1, 200))

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
        color = QColorDialog.getColor(color, self, self._tr("MainWindow", "选择填充颜色"))
        if color.isValid():
            item.setBrush(QBrush(color))

    def __initFileMenu(self):
        self.ui.actionOpen.triggered.connect(self.do_open_file)
        self.ui.actionSave.triggered.connect(self.do_save_file)
        self.ui.actionQuit.triggered.connect(self.close)

    def __initModeMenu(self):
        modeMenuGroup = QActionGroup(self)
        modeMenuGroup.addAction(self.ui.actionDigraph_Mode)
        modeMenuGroup.addAction(self.ui.actionRedigraph_Mode)

    def __updateEdgeView(self):
        edges = self.singleItems(BezierEdge)
        if len(edges):
            self.ui.edgeDetails.setEnabled(True)
        else:
            return
        edgeColCount = 5

        self.edgeModel.clear()
        edgeHeaderList = [self._tr("MainWindow", 'ID'), self._tr("MainWindow", '始点'), self._tr("MainWindow", '终点'),
                          self._tr("MainWindow", '坐标'), self._tr("MainWindow", '权重')]
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
        nodeHeaderList = [self._tr("MainWindow", 'ID'), self._tr("MainWindow", '边数'), self._tr("MainWindow", '坐标'),
                          self._tr("MainWindow", '权重')]
        if self.ui.actionDigraph_Mode.isChecked():
            nodeHeaderList.append(self._tr("MainWindow", '出度'))
            nodeHeaderList.append(self._tr("MainWindow", '入度'))
            nodeColCount += 2
        else:
            nodeHeaderList.append(self._tr("MainWindow", "度"))
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
                strList.append(f'{node.degrees(self.ui.actionDigraph_Mode.isChecked())[1]}')
                strList.append(f'{node.degrees(self.ui.actionDigraph_Mode.isChecked())[0]}')
            else:
                strList.append(f'{node.degrees(self.ui.actionDigraph_Mode.isChecked())}')
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
            self.disconnectGraph()
            string = ""
            for x in range(len(badEdgeList)):
                demo = "、"
                if x == len(badEdgeList) - 1:
                    demo = ""
                string = f'{string}e{badEdgeList[x].data(self.__EdgeId)}{demo}'
            QMessageBox.warning(self, self._tr("MainWindow", "连接故障！"),
                                self._tr("MainWindow", "警告，") + string + self._tr("MainWindow", "的连接不完整"))
            return False

        return True

    def disconnectGraph(self):
        self.__graph.clearAllData()

    def viewAndScene(self):
        if self.ui.tabWidget.count():
            self.__view: GraphicsView = self.ui.tabWidget.currentWidget()
            self.__scene = self.__view.scene()

    def standardGraphData(self):
        mode = int(self.ui.actionDigraph_Mode.isChecked())
        nodes = self.__scene.singleItems(BezierNode)
        edges = self.__scene.singleItems(BezierEdge)
        texts = self.__scene.singleItems(BezierText)
        nodeDataList = []
        edgeDataList = []
        textDataList = []
        for node in nodes:
            node: BezierNode
            data = [node.data(self.__NodeId), node.weight(), node.pos().x(), node.pos().y()]
            nodeDataList.append(data)

        for edge in edges:
            edge: BezierEdge
            data = [edge.data(self.__EdgeId)]
            if edge.sourceNode:
                data.append(edge.sourceNode.data(self.__NodeId))
            else:
                data.append(-1)
            if edge.destNode:
                data.append(edge.destNode.data(self.__NodeId))
            else:
                data.append(-1)

            data = data + [edge.weight(), edge.beginCp.point().x(), edge.beginCp.point().y(),
                           edge.edge1Cp.point().x(), edge.edge1Cp.point().y(), edge.edge2Cp.point().x(),
                           edge.edge2Cp.point().y(), edge.endCp.point().x(), edge.endCp.point().y(),
                           edge.scenePos().x(), edge.scenePos().y()]
            edgeDataList.append(data)

        for text in texts:
            text: BezierText
            data = [text.data(self.__TextId), text.toPlainText(), text.scenePos().x(),
                    text.scenePos().y()]
            textDataList.append(data)

        nodeDataList.reverse()
        edgeDataList.reverse()
        textDataList.reverse()

        return [mode, nodeDataList, edgeDataList, textDataList]

    def reverseStandardData(self, excelData):
        graphName = excelData[0]
        mode = excelData[1]
        nodes = []
        edges = []
        texts = []
        self.ui.actionDigraph_Mode.setChecked(bool(mode))

        for nodeDetail in excelData[2]:
            node = BezierNode()
            node.textCp.setPlainText(f"V{nodeDetail[0]}")
            node.setData(self.__NodeId, nodeDetail[0])
            nodeText = self._tr("MainWindow", "顶点")
            node.setData(self.__ItemDesc, nodeText)
            if len(nodeDetail) < 3:
                for i in range(2):
                    intRandom = randint(-400, 400)
                    nodeDetail.append(intRandom)

            node.setPos(QPointF(nodeDetail[2], nodeDetail[3]))
            node.weightCp.setPlainText(str(nodeDetail[1]))

            nodes.append(node)

        for edgeDetail in excelData[3]:
            edge = BezierEdge()
            edge.setData(self.__EdgeId, edgeDetail[0])
            edge.setData(self.__ItemDesc, "边")
            edge.textCp.setPlainText(f"e{edgeDetail[0]}")
            edge.weightCp.setPlainText(str(edgeDetail[3]))

            if len(edgeDetail) <= 4:
                for i in range(10):
                    intRandom = randint(-400, 400)
                    edgeDetail.append(intRandom)

            edge.setPos(QPointF(edgeDetail[12], edgeDetail[13]))

            if edgeDetail[1] >= 0:
                for node in nodes:
                    node: BezierNode
                    if node.data(self.__NodeId) == edgeDetail[1]:
                        edge.setSourceNode(node)
                        node.addBezierEdge(edge, ItemType.SourceType)
                        line = QLineF(edge.mapFromScene(node.pos()), edge.edge1Cp.point())
                        length = line.length()
                        edgeOffset = QPointF(line.dx() * 10 / length, line.dy() * 10 / length)
                        source = edge.mapFromScene(node.pos()) + edgeOffset
                        edge.setSpecialControlPoint(source, ItemType.SourceType)
                        edge.beginCp.setVisible(False)
            else:
                edge.setSpecialControlPoint(QPointF(edgeDetail[4], edgeDetail[5]), ItemType.SourceType)

            if edgeDetail[2] >= 0:
                for node in nodes:
                    node: BezierNode
                    if node.data(self.__NodeId) == edgeDetail[2]:
                        edge.setDestNode(node)
                        node.addBezierEdge(edge, ItemType.DestType)
                        line = QLineF(edge.mapFromScene(node.pos()), edge.edge2Cp.point())
                        length = line.length()
                        edgeOffset = QPointF(line.dx() * 10 / length, line.dy() * 10 / length)
                        if mode:
                            dest = edge.mapFromScene(node.pos()) + edgeOffset * 2.3
                        else:
                            dest = edge.mapFromScene(node.pos()) + edgeOffset
                        edge.setSpecialControlPoint(dest, ItemType.DestType)
                        edge.endCp.setVisible(False)
            else:
                edge.setSpecialControlPoint(QPointF(edgeDetail[10], edgeDetail[11]), ItemType.DestType)

            edge.setEdgeControlPoint(QPointF(edgeDetail[6], edgeDetail[7]), ItemType.SourceType)
            edge.setEdgeControlPoint(QPointF(edgeDetail[8], edgeDetail[9]), ItemType.DestType)
            edge.centerCp.setPoint(edge.updateCenterPos())

            edges.append(edge)

        if len(excelData) <= 4:
            return [graphName, nodes + edges]

        for textDetail in excelData[4]:
            text = BezierText(str(textDetail[1]))
            text.setData(self.__TextId, textDetail[0])
            text.setData(self.__ItemDesc, "文本")
            text.setPos(textDetail[2], textDetail[3])
            texts.append(text)

        return [graphName, nodes + edges + texts]

    def setTranslator(self, translator, language):
        self.__translator = translator
        if language == 'EN':
            self.ui.actionSetEnglish.setChecked(True)
        else:
            self.ui.actionSetChinese.setChecked(True)

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
        item = BezierEdge()
        item.setGraphMode(self.ui.actionDigraph_Mode.isChecked())
        self.__setItemProperties(item, self._tr("MainWindow", "边"))
        self.do_addItem(item)
        self.__updateEdgeView()
        self.__updateNodeView()

    @Slot()  # 添加顶点
    def on_actionCircle_triggered(self):  # 添加原点
        self.viewAndScene()
        item = BezierNode()
        self.__setItemProperties(item, self._tr("MainWindow", "顶点"))
        self.do_addItem(item)
        self.__updateNodeView()
        self.__updateEdgeView()

    @Slot()  # 添加注释
    def on_actionAdd_Annotation_triggered(self):
        self.viewAndScene()
        strText, OK = QInputDialog.getText(self, self._tr("MainWindow", "输入"), self._tr("MainWindow", "请输入文字"))
        if not OK:
            return
        item = BezierText(strText)
        self.__setItemProperties(item, self._tr("MainWindow", "注释"))
        self.do_addItem(item)

    @Slot(bool)  # 显示和隐藏结点权重
    def on_actionShowNodesWeight_toggled(self, check: bool):
        nodes = self.__scene.singleItems(BezierNode)
        for node in nodes:
            node: BezierNode
            node.weightCp.setVisible(check)

        # if check:
        #     self.ui.actionShowNodesWeight.setText("隐藏顶点权重")
        # else:
        #     self.ui.actionShowNodesWeight.setText("显示顶点权重")

    @Slot(bool)  # 显示和隐藏边权重
    def on_actionShowEdgesWeight_toggled(self, check: bool):
        edges = self.__scene.singleItems(BezierEdge)
        for edge in edges:
            edge: BezierEdge
            edge.weightCp.setVisible(check)
        # if check:
        #     self.ui.actionShowEdgesWeight.setText("隐藏边权重")
        # else:
        #     self.ui.actionShowEdgesWeight.setText("显示边权重")

    @Slot(bool)  # 显示和隐藏边的控制点
    def on_actionHideControlPoint_toggled(self, check: bool):
        edges = self.__scene.singleItems(BezierEdge)
        for edge in edges:
            edge: BezierEdge
            for point in edge.pointList:
                point.setVisible(check)
            if edge.sourceNode:
                edge.beginCp.setVisible(False)
            if edge.destNode:
                edge.endCp.setVisible(False)

    @Slot()  # 简单通路
    def on_actionEasy_Pathway_triggered(self):
        self.viewAndScene()
        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "对不起，你没有选择起始节点"))
            return
        elif len(items) != 2:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "选择的起始点数目不符合要求"))
            return

        if self.connectGraph():
            PathWay = ShowDataWidget(self, items, self.__graph, name=self._tr("MainWindow", "简单通路"))
            PathWay.pathSignal.connect(self.do_ShowSelectPath)
            if PathWay.easyPath():
                PathWay.updateToolWidget()
                PathWay.show()

        self.disconnectGraph()

    @Slot()  # 简单回路
    def on_actionEasy_Loop_triggered(self):
        self.viewAndScene()
        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "对不起，你没有选择起点"))
            return

        if self.connectGraph():
            LoopWay = ShowDataWidget(self, items, self.__graph, name=self._tr("MainWindow", "简单回路"))
            LoopWay.pathSignal.connect(self.do_ShowSelectPath)
            if LoopWay.easyLoop():
                LoopWay.updateToolWidget(mode=1)
                LoopWay.show()
        self.disconnectGraph()

    @Slot()  # 初级通路
    def on_actionPrimary_Pathway_triggered(self):
        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "对不起，你没有选择起始节点"))
            return
        elif len(items) != 2:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "选择的起始点数目不符合要求"))
            return

        if self.connectGraph():
            PathWay = ShowDataWidget(self, items, self.__graph, name="初级通路")
            PathWay.pathSignal.connect(self.do_ShowSelectPath)
            if PathWay.primaryPath():
                PathWay.updateToolWidget(path=1)
                PathWay.show()

        self.disconnectGraph()

    @Slot()  # 初级回路
    def on_actionPrimary_Loop_triggered(self):
        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "对不起，你没有选择起点"))
            return

        if self.connectGraph():
            LoopWay = ShowDataWidget(self, items, self.__graph, name=self._tr("MainWindow", "初级回路"))
            LoopWay.pathSignal.connect(self.do_ShowSelectPath)
            if LoopWay.primaryLoop():
                LoopWay.updateToolWidget(mode=1, path=1)
                LoopWay.show()

        self.disconnectGraph()

    @Slot()  # 邻接矩阵 边数
    def on_action_EdgeNum_triggered(self):
        self.viewAndScene()
        items = self.__scene.singleItems(BezierNode)
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "图中没有结点"))
            return
        if self.connectGraph():
            MatrixTable = ShowMatrixWidget(self, self.__graph, self._tr("MainWindow", "邻接矩阵"), 0)
            MatrixTable.show()

    @Slot()  # 邻接矩阵 权重
    def on_actionWeight_triggered(self):
        self.viewAndScene()
        items = self.__scene.singleItems(BezierNode)
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "图中没有结点"))
            return
        if self.connectGraph():
            if not self.__graph.multipleOrSimple():
                MatrixTable = ShowMatrixWidget(self, self.__graph, self._tr("MainWindow", "邻接矩阵"), 1)
                MatrixTable.show()
            else:
                QMessageBox.information(self, "Sorry", "这个图不是简单图")
                self.disconnectGraph()

    @Slot()  # 可达矩阵
    def on_actionReachable_Matrix_triggered(self):
        self.viewAndScene()
        items = self.__scene.singleItems(BezierNode)
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "图中没有结点"))
            return
        if self.connectGraph():
            MatrixTable = ShowMatrixWidget(self, self.__graph, self._tr("MainWindow", "可达矩阵"))
            MatrixTable.show()

    @Slot()  # 关联矩阵
    def on_actionIncidence_Matrix_Undigraph_triggered(self):
        self.viewAndScene()
        items = self.__scene.singleItems(BezierNode)
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "图中没有结点"))
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
                text = self._tr("MainWindow", '有向图的关联矩阵需要有向图无环,而')
                text1 = self._tr("MainWindow", '存在环！')
                QMessageBox.warning(self, self._tr("MainWindow", "致命错误"), f"{text}{badNodes}{text1}")
                return
        if self.connectGraph():
            MatrixTable = ShowMatrixWidget(self, self.__graph, self._tr("MainWindow", "关联矩阵"))
            MatrixTable.show()

    @Slot()  # 图的连通性
    def on_actionConnectivity_triggered(self):
        name = ''
        if self.connectGraph():
            num = self.__graph.connectivity()
            if num is False:
                name = self._tr("MainWindow", '此图为非连通图')
            elif num == 2:
                name = self._tr("MainWindow", "此图为单向连通图")
            elif num == 3:
                name = self._tr("MainWindow", "此图为强连通图")
            elif num == 1:
                name = self._tr("MainWindow", '此图为连通图')

            QMessageBox.information(self, self._tr("MainWindow", "图的连通性"), name)

            self.disconnectGraph()

    @Slot()  # 完全图判定
    def on_actionCompleteGraph_triggered(self):
        if self.connectGraph():
            edge = self.__graph.completeGraph()
            if edge:
                name = self._tr("MainWindow", "此图为完全图")
            else:
                name = self._tr("MainWindow", '此图不是完全图')

            QMessageBox.information(self, self._tr("MainWindow", "完全图判定"), name)

            self.disconnectGraph()

    @Slot()  # 简单图多重图判定
    def on_actionMultipleOrSimple_triggered(self):
        if self.connectGraph():
            edges = self.__graph.multipleOrSimple()
            if not edges:
                QMessageBox.information(self, self._tr("MainWindow", "简单图与多重图的判定"), self._tr("MainWindow", "此图为简单图"))

            else:
                parallelSides = ShowDataWidget(self, edges, self.__graph, self._tr("MainWindow", "简单图与多重图的判定"))
                parallelSides.multipleOrSimple()
                parallelSides.show()

    @Slot()  # 最短路径
    def on_actionShortestPath_triggered(self):

        items = self.__scene.nodeList
        if len(items) == 0:
            QMessageBox.warning(self, self._tr("MainWindow", "警告"), self._tr("MainWindow", "对不起，你没有选择结点"))
            return
        if self.connectGraph():
            ShortestPath = ShowDataWidget(self, items, self.__graph, name=self._tr("MainWindow", "最短路径"))
            ShortestPath.pathSignal.connect(self.do_ShowSelectPath)
            if ShortestPath.shortestPath():
                ShortestPath.updateToolWidget(mode=1, path=2)
                ShortestPath.show()

    @Slot()  # 撤销
    def on_actionUndo_triggered(self):  # 撤销
        self.undoStack.undo()
        self.__updateEdgeView()
        self.__updateNodeView()

    @Slot()  # 重做
    def on_actionRedo_triggered(self):  # 重做
        self.undoStack.redo()
        self.__updateEdgeView()
        self.__updateNodeView()

    @Slot()  # 帮助
    def on_actionHelp_Document_triggered(self):
        open("https://github.com/BBlance/Discrete_math.graph_theory")

    # @Slot()
    # def on_actionPen_Color_triggered(self):  # 画笔颜色
    #     iniColor = self.view.getPenColor()
    #     color = QColorDialog.getColor(iniColor, self, "选择颜色")
    #     if color.isValid():
    #         self.view.setPenColor(color)

    # @Slot()
    # def on_actionPen_Thickness_triggered(self):  # 画笔粗细
    #     self.viewAndScene()
    #     iniThickness = self.__view.getPenThickness()
    #     intPenStyle = self.__view.getPenStyle()
    #     thicknessDialog = ThicknessDialog(None, self._tr("MainWindow", "画笔粗细与样式"), iniThickness, intPenStyle)
    #     ret = thicknessDialog.exec_()
    #     thickness = thicknessDialog.getThickness()
    #     penStyle = thicknessDialog.getPenStyle()
    #     self.__view.setPenStyle(penStyle)
    #     self.__view.setPenThickness(thickness)

    @Slot()
    def on_actionBackground_Color_triggered(self):
        self.viewAndScene()
        # iniColor = self.__view.getBackgroundColor()
        # color = QColorDialog.getColor(iniColor, self, "选择颜色")
        # if color.isValid():
        #     self.__view.setBackgroundBrush(color)
        for item in self.standardGraphData():
            print(item)

    # @Slot(bool)
    # def on_actionProperty_And_History_triggered(self, checked):
    #     self.ui.dockWidget.setVisible(checked)

    @Slot()  # 保存文件
    def on_actionSave_triggered(self):
        tableName = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        filename = self.operatorFile.saveGraphData(self.standardGraphData(), tableName)
        if filename:
            index = self.ui.tabWidget.currentIndex()
            self.ui.tabWidget.setTabText(index, filename.baseName())

    @Slot()  # 读取文件
    def on_actionOpen_triggered(self):
        graph = self.operatorFile.openGraphData()
        if graph:
            graph = self.reverseStandardData(graph)
            self.iniGraphicsSystem(graph[0])
            for item in graph[1]:
                self.__scene.addItem(item)
            self.__updateNodeView()
            self.__updateEdgeView()
            self.__scene.update()

    @Slot()  # 另存为
    def on_actionSave_As_triggered(self):
        filename = self.operatorFile.saveExcelAs(self.standardGraphData())
        if filename:
            index = self.ui.tabWidget.currentIndex()
            self.ui.tabWidget.setTabText(index, filename.baseName())

    @Slot()  # 导出数据
    def on_actionOutputData_triggered(self):
        data = self.standardGraphData()
        data = data[:3]
        dataCpoy = [data[0], [], []]
        for node in data[1]:
            node = node[:2]
            dataCpoy[1].append(node)

        for edge in data[2]:
            edge = edge[:4]
            dataCpoy[2].append(edge)

        if self.operatorFile.outputData(dataCpoy):
            title = self.tr("恭喜")
            strInfo = self.tr("数据导出成功")
            QMessageBox.information(self, title, strInfo)

    @Slot()  # 导入数据
    def on_actionImportData_triggered(self):
        data = self.operatorFile.inputData()
        if data:
            graph = self.reverseStandardData(data)
            self.iniGraphicsSystem(graph[0])
            for item in graph[1]:
                self.__scene.addItem(item)
            self.__updateNodeView()
            self.__updateEdgeView()
            self.__scene.update()

    @Slot()
    def on_actionSave_Image_triggered(self):
        self.viewAndScene()
        savePath, fileType = QFileDialog.getSaveFileName(self, self._tr("MainWindow", '保存图片'), '.\\', '*bmp;;*.png')
        filename = os.path.basename(savePath)
        if filename != "":
            self.__view.saveImage(savePath, fileType)

    @Slot()
    def on_actionDelete_triggered(self):
        self.viewAndScene()
        self.do_deleteItem()

    @Slot(bool)
    def on_actionDigraph_Mode_toggled(self, checked: bool):
        self.__labModeInfo.setText(self._tr("MainWindow", "有向图模式"))
        self.__graph.setMode(checked)
        items = self.__scene.uniqueItems()
        if len(items) != 0:
            dlgTitle = self._tr("MainWindow", "警告！！")
            strInfo = self._tr("MainWindow", "更换模式会清楚画板所有元素！是否要更换模式")
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
        self.__labModeInfo.setText(self._tr("MainWindow", "无向图模式"))
        self.__graph.setMode(checked)
        items = self.__scene.uniqueItems()
        if len(items) != 0:
            dlgTitle = self._tr("MainWindow", "警告！！")
            strInfo = self._tr("MainWindow", "更换模式会清楚画板所有元素！是否要更换模式")
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
        if self.__view and self.__scene:
            self.__updateEdgeView()
            self.__updateNodeView()

        hasTabs = self.ui.tabWidget.count() > 0  # 再无页面时

        self.ui.tabWidget.setVisible(hasTabs)
        self.ui.dockWidget.setVisible(hasTabs)
        self.ui.actionProperty_And_History.setChecked(hasTabs)

    @Slot(int)
    def on_tabWidget_tabCloseRequested(self, index):  # 分页关闭时关闭窗体

        self.__view: GraphicsView = self.ui.tabWidget.widget(index)
        self.__scene = self.__view.scene()
        if index < 0:
            return
        self.__view = None
        self.__scene = None
        aForm = self.ui.tabWidget.widget(index)
        aForm.close()
        self.ui.tabWidget.tabBar().removeTab(index)

    #  =============自定义槽函数===============================
    def do_nodeLock(self, item):
        self.__updateNodeView()
        self.__updateEdgeView()

    def do_mouseMove(self, point):  ##鼠标移动
        ##鼠标移动事件，point是 GraphicsView的坐标,物理坐标
        view = self._tr("MainWindow", '视图坐标：')
        scene = self._tr("MainWindow", '场景坐标：')
        self.__labViewCord.setText("%s%d,%d" % (view, point.x(), point.y()))
        pt = self.ui.tabWidget.currentWidget().mapToScene(point)  # 转换到Scene坐标
        self.__labSceneCord.setText("%s%.0f,%.0f" % (scene, pt.x(), pt.y()))

    def do_mouseClicked(self, point):  ##鼠标单击
        pt = self.__view.mapToScene(point)  # 转换到Scene坐标
        item = self.__scene.itemAt(pt, self.__view.transform())  # 获取光标下的图形项
        if item is None:
            return
        pm = item.mapFromScene(pt)  # 转换为绘图项的局部坐标
        itemInfo = self._tr("MainWindow", "Item 坐标：")
        self.__labItemCord.setText("%s%.0f,%.0f" % (itemInfo, pm.x(), pm.y()))
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

    def do_checkIsHasItems(self, num):
        if num:
            self.ui.actionSave.setEnabled(True)
        else:
            self.ui.actionSave.setEnabled(False)


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = MainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
