# -*- coding: utf-8 -*-
import os
import sys, random
from PyQt5.QtCore import pyqtSlot, Qt, QPointF, QPoint

from PyQt5.QtGui import QBrush, QPolygonF, QPen, QFont, QTransform, QPainterPath, QColor, QPixmap, QPalette

from PyQt5.QtWidgets import (QApplication, QMainWindow, QColorDialog,
                             QFontDialog, QInputDialog, QLabel, QMessageBox, QMenu, QFileDialog,
                             QActionGroup, QScrollArea)
from ui_MainWindow import Ui_MainWindow
from PainterBoard import PainterBoard
from ThicknessDialog import ThicknessDialog


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象

        self.ui.setupUi(self)  # 构造UI界面

        self.__buildStatusBar()
        self.__initDrawBoardSystem()
        self.__initModeMenu()
        self.__initFileMenu()

        self.__graphicsToolId = 0
        self.__backgroundColor = QColor(Qt.white)
        self.setWindowTitle("离散数学可视化认知系统")

    #  ==============自定义功能函数========================
    def __buildStatusBar(self):  # 构造状态栏
        self.__labelViewCord = QLabel("坐标：")
        self.__labelViewCord.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.__labelViewCord)

        self.__labelItemInfo = QLabel('图形信息')
        self.ui.statusbar.addPermanentWidget(self.__labelItemInfo)

        self.__softwareDetailLabel = QLabel("CopyRight @ LiXiaolong 2020")
        self.ui.statusbar.addPermanentWidget(self.__softwareDetailLabel)

    def __initDrawBoardSystem(self):  # 初始化 DrawBoard系统
        self.view = PainterBoard(self)  # 创建图形视图组件

        self.view.setPalette(QPalette(Qt.white))
        self.view.setAutoFillBackground(True)

        self.setCentralWidget(self.view)

        self.view.setCursor(Qt.CrossCursor)  # 设置鼠标
        self.view.setMouseTracking(True)

        # 4个信号与槽函数的关联
        self.view.mouseMove.connect(self.do_mouseMove)
        # self.view.mouseClicked.connect(self.do_mouseClicked)

        # self.view.mouseDoubleClick.connect(self.do_mouseDoubleClick)
        # self.view.keyPress.connect(self.do_keyPress)

    def __initFileMenu(self):

        # 信号与槽的关联
        #  self.ui.actionNew.triggered.connect()
        self.ui.actionOpen.triggered.connect(self.do_open_file)
        self.ui.actionSave.triggered.connect(self.do_save_file)
        self.ui.actionQuit.triggered.connect(self.close)

    def __initEditMenu(self):
        pass

    def __initModeMenu(self):
        self.modeMenuGroup = QActionGroup(self)
        self.modeMenuGroup.addAction(self.ui.actionDigraph_Mode)
        self.modeMenuGroup.addAction(self.ui.actionTree_Mode)
        self.modeMenuGroup.addAction(self.ui.actionRedigraph_Mode)
        self.ui.actionDigraph_Mode.setChecked(True)

    def __setBrushColor(self, item):  # 设置填充颜色
        color = item.brush().color()
        color = QColorDialog.getColor(color, self, "选择填充颜色")
        if color.isValid():
            item.setBrush(QBrush(color))

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

    def contextMenuEvent(self, event):  # 右键菜单功能
        rightMouseMenu = QMenu(self)

        rightMouseMenu.addAction(self.ui.actionNew)
        rightMouseMenu.addAction(self.ui.actionOpen)

        self.action = rightMouseMenu.exec_(self.mapToGlobal(event.pos()))

    #  ==========由connectSlotsByName()自动连接的槽函数============
    @pyqtSlot()
    def on_actionArc_triggered(self):  # 添加弧
        self.view.setDrawGraphStyle(0)

    @pyqtSlot()
    def on_actionStraight_Line_triggered(self):  # 添加直线
        self.view.setDrawGraphStyle(1)

    @pyqtSlot()
    def on_actionCircle_triggered(self):  # 添加原点
        self.view.setDrawGraphStyle(2)

    @pyqtSlot()
    def on_actionRectangle_triggered(self):  # 添加矩形
        self.view.setDrawGraphStyle(3)

    @pyqtSlot()
    def on_actionUndo_triggered(self):  # 撤销
        pass

    def on_actionRedo_triggered(self):  # 重做
        pass

    @pyqtSlot()
    def on_actionPen_Color_triggered(self):  # 画笔颜色
        iniColor = self.view.getPenColor()
        color = QColorDialog.getColor(iniColor, self, "选择颜色")
        if color.isValid():
            self.view.setPenColor(color)

    @pyqtSlot()
    def on_actionPen_Thickness_triggered(self):  # 画笔粗细
        thicknessDialog = ThicknessDialog(None, "画笔粗细与样式")
        ret = thicknessDialog.exec_()
        thickness = thicknessDialog.getThickness()
        penStyle = thicknessDialog.getPenStyle()
        self.view.setPenStyle(penStyle)
        self.view.setPenThickness(thickness)

    @pyqtSlot()
    def on_actionBackground_Color_triggered(self):
        iniColor = self.view.getBackgroundColor()
        color = QColorDialog.getColor(iniColor, self, "选择颜色")
        if color.isValid():
            self.view.setBackgroundColor(color)

    @pyqtSlot()
    def on_actionClues_Color_triggered(self):
        iniColor = self.view.getRt_PenColor()
        color = QColorDialog.getColor(iniColor, self, "选择颜色")
        if color.isValid():
            self.view.setRT_PenColor(color)

    @pyqtSlot()
    def on_actionClues_Thickness_triggered(self):
        thicknessDialog = ThicknessDialog(None, "提示画笔粗细与样式")
        ret = thicknessDialog.exec_()
        thickness = thicknessDialog.getThickness()
        penStyle = thicknessDialog.getPenStyle()
        self.view.setRT_PenStyle(penStyle)
        self.view.setRt_PenThickness(thickness)

    #  =============自定义槽函数===============================

    def do_save_file(self):  # 保存文件
        savePath, fileType = QFileDialog.getSaveFileName(self, '保存文件', '.\\', '*.graph;;*.json;;*.csv')

        filename = os.path.basename(savePath)

        if fileType == '*.json':
            pass
            # self.operatorData.save_Json(filename, nodes)
        elif fileType == '*.csv':
            pass
            # self.operatorData.save_Csv(filename, ['point(1)', 'point(2)'], nodes)
        elif fileType == '*.graph':
            self.operatorData.save_Graph(filename, self.painterBoard.GetContentAsGraph())

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

    def do_mouseMove(self, point):  # 鼠标移动
        # 鼠标移动时间
        self.__endPoint = point
        self.__labelViewCord.setText("坐标：%d,%d" % (point.x(), point.y()))

    def do_mouseRelease(self, point):
        self.__labelViewCord.setText("坐标：%.0f,%.0f" % (point.x(), point.y()))

    def do_mouseClicked(self, point):  # 鼠标单击
        pass

    # def do_mouseDoubleClick(self, point):  # 鼠标双击

    # def do_keyPress(self, event):  # 键盘输入


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = MainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
