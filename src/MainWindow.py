# -*- coding: utf-8 -*-
import sys, random
from PyQt5.QtCore import pyqtSlot, Qt, QPointF

from PyQt5.QtGui import QBrush, QPolygonF, QPen, QFont, QTransform

from PyQt5.QtWidgets import (QApplication, QMainWindow, QColorDialog,
                             QFontDialog, QInputDialog, QLabel, QGraphicsScene,
                             QGraphicsView, QGraphicsItem, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsPolygonItem,
                             QGraphicsLineItem, QGraphicsItemGroup, QGraphicsTextItem)

from DrawBoard import DrawBoardView
from ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象

        self.ui.setupUi(self)  # 构造UI界面

        self.__buildStatusBar()
        self.__initGraphicsSystem()

        self.__ItemId = 1  # 绘图项自定义数据的key
        self.__ItemDesc = 2  # 绘图项自定义数据的key

        self.__seqNum = 0  # 每个图形项设置一个序号
        self.__backZ = 0  # 后置序号
        self.__frontZ = 0  # 前置序号

        self.setWindowTitle("离散数学可视化认知系统")

    #  ==============自定义功能函数========================
    def __buildStatusBar(self):  # 构造状态栏
        self.__labelViewCord = QLabel("坐标：")
        self.__labelViewCord.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.__labelViewCord)

        self.__labelItemInfo = QLabel('图形信息：')
        self.ui.statusbar.addPermanentWidget(self.__labelItemInfo)

        self.__softwareDetailLabel = QLabel("CopyRight @ LiXiaolong 2020")
        self.ui.statusbar.addPermanentWidget(self.__softwareDetailLabel)

    def __initGraphicsSystem(self):  # 初始化 Graphics View系统
        self.view = DrawBoardView(self)  # 创建图形视图组件
        self.setCentralWidget(self.view)

        self.scene = QGraphicsScene(-300, -200, 600, 200)
        self.view.setScene(self.scene)

        self.view.setCursor(Qt.CrossCursor)  # 设置鼠标
        self.view.setMouseTracking(True)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)

        # 4个信号与槽函数的关联
        self.view.mouseMove.connect(self.do_mouseMove)
        """
        self.view.mouseClicked.connect()
        self.view.mouseDoubleClick.connect()
        self.view.keyPress.connect()
        """

    def __setItemProperties(self, item, desc):  # item是具体类型的QGraphicsItem
        item.setFlag(QGraphicsItem.ItemIsFocusable)
        item.setFlag(QGraphicsItem.ItemIsMovable)
        item.setFlag(QGraphicsItem.ItemIsSelectable)

        self.__frontZ = self.__frontZ + 1
        item.setZValue(self.__frontZ)  # 叠放次序
        item.setPos(-150 + random.randint(1, 200), -200 + random.randint(1, 200))

        self.__seqNum = 1 + self.__seqNum
        item.setData(self.__ItemId, self.__seqNum)  # 图件编号
        item.setData(self.__ItemDesc, desc)  # 图件描述

        self.scene.addItem(item)
        self.scene.clearSelection()
        item.setSelected(True)

    def __setBrushColor(self, item):  # 设置填充颜色
        color = item.brush().color()
        color = QColorDialog.getColor(color, self, "选择填充颜色")
        if color.isValid():
            item.setBrush(QBrush(color))

    # ==============event处理函数==========================

    #  ==========由connectSlotsByName()自动连接的槽函数============
    @pyqtSlot()
    def on_actionArc_triggered(self):
        item = QGraphicsEllipseItem(-50, -30, 60, 60)
        item.setBrush(QBrush(Qt.blue))  # 设置填充颜色
        self.__setItemProperties(item, "椭圆")


    #  =============自定义槽函数===============================
    def do_mouseMove(self, point):  # 鼠标移动
        # 鼠标移动时间，point是GraphicsView的坐标，物理坐标
        pt = self.view.mapToScene(point)  # 转移到Scene坐标
        self.__labelViewCord.setText("坐标：%d,%d" % (pt.x(), pt.y()))

    def do_mouseClicked(self, point):  # 鼠标单击
        pt = self.view.mapToScene(point)
        item = self.scene.itemAt(pt, self.view.transform())
        if item is None:
            return
        pm = item.mapFromScene(pt)  # 转换为绘图项的局部坐标
        self.__labelViewCord.setText("坐标：%.0f,%.0f" % (pm.x(), pm.y()))
        self.__labelItemInfo.setText(str(item.data(self.__ItemDesc)) + ",ItemId=" + str(item.data(self.__ItemId)))


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = MainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
