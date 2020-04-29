from PyQt5.QtWidgets import QWidget, QApplication

from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QLine

from PyQt5.QtGui import QMouseEvent, QKeyEvent, QColor, QPainter, QPen, QPalette, QPixmap

from Graph import Graph


class DrawBoardWidget(QWidget):
    mouseMove = pyqtSignal(QPoint)  # 鼠标移动

    mouseClicked = pyqtSignal(QPoint)  # 鼠标单击

    mouseDoubleClick = pyqtSignal(QPoint)  # 鼠标双击

    mouseReleased = pyqtSignal(QPoint)  # 鼠标释放

    keyPress = pyqtSignal(QKeyEvent)  # 按键按下

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initData()

    ##  =================自定义功能函数=================================
    def __initData(self):
        self.__whiteBoard = QPixmap(self.width(), self.height())
        self.__whiteBoard.fill(Qt.white)

        self.__IsEmpty = True  # 默认为空画板
        self.EraseMode = False  # 默认禁用橡皮擦模式
        self.__IsHasDirection = False  # 有向无向图标志 默认为无向图

        self.__thickness = 3  # 画笔粗细
        self.__RT_thickness = 5  # 实时画笔粗细
        self.__penColor = QColor('black')  # 画笔颜色
        self.__RT_penColor = QColor('blue')  # 提示画笔颜色
        self.__colorList = QColor.colorNames()  # 所有可用颜色列表

        self.begin_point = QPoint()  # 鼠标起始位置
        self.end_point = QPoint()  # 鼠标终结位置

        self.graph = Graph()

        self.pressLocation = QPoint()  # 鼠标点击点坐标
        self.releaseLocation = QPoint()  # 鼠标释放点坐标
        self.RT_MouseLocation = QPoint()  # 鼠标实时位置

    ##========== event 处理函数============
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        if self.begin_point and self.end_point:  # 如果起始点终结点都存在则进行绘图
            line = QLine(self.begin_point, self.end_point)  # 绘制的线
            painter.drawLine(line)  # 实时绘制线
        painter.end()

    def mouseMoveEvent(self, event):  ##鼠标移动
        point = event.pos()
        self.mouseMove.emit(point)  # 发射信号
        super().mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton:
            self.end_point = event.pos()
            self.update()  # 3

    def mousePressEvent(self, event):  ##鼠标单击
        if event.button() == Qt.LeftButton:
            point = event.pos()
            self.pressLocation = event.pos()  # 鼠标点击原点
            self.mouseClicked.emit(point)

            if self.graph.getTotalVertex():
                self.begin_point = self.lockLineToPoint(event.pos())
            if not self.graph.IsContainsPoint(self.begin_point):
                self.graph.addVertex(self.graph.getTotalVertex(), self.begin_point)
                painter = QPainter(self.__whiteBoard)
                painter.setPen(QPen(self.__penColor, self.__thickness))
                painter.setBrush(Qt.darkYellow)
                painter.drawEllipse(self.begin_point, 10, 10)
            self.end_point = self.begin_point
            self.update()  # 3

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = event.pos()
            self.mouseReleased.emit(point)  # 发射信号

            painter = QPainter(self.__whiteboard)

            #self.end_point = self.lockLineToPoint(event.pos())
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):  ##鼠标双击
        if event.button() == Qt.LeftButton:
            point = event.pos()
            self.mouseDoubleClick.emit(point)  # 发射信号
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):  ##按键按下
        self.keyPress.emit(event)  # 发射信号
        super().keyPressEvent(event)

    #  =============自定义槽函数===============================
    def lockLineToPoint(self, event):  # 锁定坐标函数
        if self.graph.getTotalVertex():
            for k, vertices in self.graph.vertDict.items():
                x, y = vertices.getCoordinates()
                value = QPoint(x, y)
                distance = event - value
                if distance.manhattanLength() <= 60:  # 当所在位置于附近点小于等于50个单位时，自动将坐标调整到最近的点
                    return value
        return event

    def Clear(self):  # 清空画板
        self.__whiteboard.fill(Qt.white)
        self.graph.ClearAllDetails()
        self.update()
        self.__IsEmpty = True

    def ChangePenColor(self, color='black'):  # 改变画笔颜色
        self.__thickness = QColor(color)

    def ChangePenThickness(self, thickness=3, RT_thickness=5):  # 改变画笔粗细
        self.__thickness, self.__RT_thickness = thickness, RT_thickness

    def IsEmpty(self):  # 判断桌面是否为空
        return self.__IsEmpty

    def GetContentAsGraph(self):
        return self.graph.getStandardData()
