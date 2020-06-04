# -*- coding: utf-8 -*-
import os
import sys, random
from PySide2.QtCore import Slot, Qt, QRectF

from PySide2.QtGui import QBrush

from PySide2.QtWidgets import QApplication, QMainWindow, QColorDialog, \
    QInputDialog, QLabel, QMessageBox, QFileDialog, QActionGroup, QUndoStack, QGraphicsItem, QGraphicsView, QFontDialog

from BezierEdge import BezierEdge
from BezierNode import BezierNode
from BezierText import BezierText
from GraphicsScene import GraphicsScene
from GraphicsView import GraphicsView
from PointItem import ItemType
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

        self.__buildStatusBar()  # 构造状态栏
        self.__iniGraphicsSystem()  # 初始化 graphics View系统
        self.__buildUndoCommand()  # 初始化撤销重做系统
        self.__initModeMenu()

        self.__ItemId = 1  # 绘图项自定义数据的key
        self.__ItemDesc = 2  # 绘图项自定义数据的key

        self.__seqNum = 0  # 每个图形项设置一个序号
        self.__nodeNum = 0  # 结点的序号
        self.__edgeNum = 0  # 边的序号
        self.__backZ = 0  # 后置序号
        self.__frontZ = 0  # 前置序号

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

        self.scene = GraphicsScene()  # 创建QGraphicsScene
        self.scene.setSceneRect(QRectF(-300, -200, 600, 200))
        self.scene.itemMoveSignal.connect(self.do_shapeMoved)

        self.view = GraphicsView(self, self.scene)  # 创建图形视图组件
        self.setCentralWidget(self.view)

        self.view.setCursor(Qt.CrossCursor)  # 设置鼠标
        self.view.setMouseTracking(True)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)

        ##  4个信号与槽函数的关联
        self.view.mouseMove.connect(self.do_mouseMove)  # 鼠标移动
        self.view.mouseClicked.connect(self.do_mouseClicked)  # 左键按下
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
        if type(item) is BezierNode:
            item: BezierNode
        elif type(item) is BezierEdge:
            item: BezierEdge
        else:
            item: BezierText
        item.setPos(-150 + random.randint(1, 200), -200 + random.randint(1, 200))

        if type(item) is BezierNode:
            self.__nodeNum = 1 + self.__nodeNum
            item.setData(self.__ItemId, self.__nodeNum)
            item.textCp.setPlainText(str(self.__nodeNum))
        elif type(item) is BezierEdge:
            self.__edgeNum = 1 + self.__edgeNum
            item.setData(self.__ItemId, self.__edgeNum)
        else:
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
        self.modeMenuGroup = QActionGroup(self)
        self.modeMenuGroup.addAction(self.ui.actionDigraph_Mode)
        self.modeMenuGroup.addAction(self.ui.actionRedigraph_Mode)
        self.ui.actionDigraph_Mode.setChecked(True)

    # ==============event处理函数==========================

    def closeEvent(self, event):  # 退出函数

        msgBox = QMessageBox()
        msgBox.setWindowTitle('关闭')
        msgBox.setText("是否保存")
        msgBox.setIcon(QMessageBox.Question)
        btn_Do_notSave = msgBox.addButton('不保存', QMessageBox.AcceptRole)
        btn_cancel = msgBox.addButton('取消', QMessageBox.RejectRole)
        btn_save = msgBox.addButton('保存', QMessageBox.AcceptRole)
        msgBox.setDefaultButton(btn_save)
        msgBox.exec_()

        if msgBox.clickedButton() == btn_Do_notSave:
            event.accept()
        elif msgBox.clickedButton() == btn_cancel:
            event.ignore()
        elif msgBox.clickedButton() == btn_save:
            self.do_save_file()
            event.accept()

    # def contextMenuEvent(self, event):  # 右键菜单功能
    #     rightMouseMenu = QMenu(self)
    #
    #     rightMouseMenu.addAction(self.ui.actionNew)
    #     rightMouseMenu.addAction(self.ui.actionOpen)
    #
    #     self.action = rightMouseMenu.exec_(self.mapToGlobal(event.pos()))

    #  ==========由connectSlotsByName()自动连接的槽函数============
    @Slot()
    def on_actionArc_triggered(self):  # 添加曲线
        item = BezierEdge()
        item.setGraphMode(self.ui.actionDigraph_Mode.isChecked())
        self.__setItemProperties(item, "曲线")

    @Slot()
    def on_actionCircle_triggered(self):  # 添加原点
        item = BezierNode()
        self.__setItemProperties(item, "结点")

    @Slot()
    def on_actionRectangle_triggered(self):  # 添加矩形
        print(self.scene.items())

    @Slot()
    def on_actionAdd_Annotation_triggered(self):
        strText, OK = QInputDialog.getText(self, "输入", "请输入文字")
        if not OK:
            return
        item = BezierText(strText)
        self.__setItemProperties(item, "文字")

    # @Slot()
    # def on_actionUndo_triggered(self):  # 撤销
    #
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

    @Slot(bool)
    def on_actionProperty_And_History_triggered(self, checked):
        self.ui.dockWidget.setVisible(checked)

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

    #  =============自定义槽函数===============================
    def do_mouseMove(self, point):  ##鼠标移动
        ##鼠标移动事件，point是 GraphicsView的坐标,物理坐标
        self.__labViewCord.setText("View 坐标：%d,%d" % (point.__x(), point.__y()))
        pt = self.view.mapToScene(point)  # 转换到Scene坐标
        self.__labSceneCord.setText("Scene 坐标：%.0f,%.0f" % (pt.x(), pt.y()))

    def do_mouseClicked(self, point):  ##鼠标单击
        pt = self.view.mapToScene(point)  # 转换到Scene坐标
        item = self.scene.itemAt(pt, self.view.transform())  # 获取光标下的图形项
        if item is None:
            return
        pm = item.mapFromScene(pt)  # 转换为绘图项的局部坐标
        self.__labItemCord.setText("Item 坐标：%.0f,%.0f" % (pm.x(), pm.y()))
        self.__labItemInfo.setText(str(item.data(self.__ItemDesc))
                                   + ", ItemId=" + str(item.data(self.__ItemId)))

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

    def do_addItem(self):
        add = AddCommand(self.scene)
        self.undoStack.push(add)

    def do_shapeMoved(self, item, pos):
        move = MoveCommand(item, pos)
        self.undoStack.push(move)


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = MainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
