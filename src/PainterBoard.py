import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.Graph import Graph
import math


class PainterBoard(QWidget):
    mouseMove = pyqtSignal(QPoint)  # 鼠标移动

    mouseClicked = pyqtSignal(QPoint)  # 鼠标单击

    mouseReleased = pyqtSignal(QPoint)  # 鼠标释放

    mouseDoubleClick = pyqtSignal(QPoint)  # 鼠标双击

    keyPress = pyqtSignal(QKeyEvent)  # 按键按下

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__InitData()

    ##  =================自定义功能函数=================================

    def __InitData(self):

        self.__size = QSize(2435, 1276)

        # 新建画板，尺寸为__size

        self.__whiteboard = QPixmap(self.__size)

        self.__IsEmpty = True  # 默认为空画板
        self.__EraseMode = False  # 默认禁用橡皮擦模式
        self.__IsHasDirection = False  # 有向无向图标志 默认为无向图
        self.__graphToolId = 0  # 绘图工具ID

        self.__thickness = 3  # 画笔粗细
        self.__RT_thickness = 5  # 实时画笔粗细
        self.__penColor = QColor('black')  # 画笔颜色
        self.__RT_penColor = QColor('blue')  # 提示画笔颜色
        self.__colorList = QColor.colorNames()  # 所有可用颜色列表
        self.__backgroundColor = QColor('white')
        self.__penStyle = Qt.SolidLine
        self.__RT_penStyle = Qt.SolidLine
        self.__pen = QPen(self.__penColor, self.__thickness, self.__penStyle)
        self.__RT_pen = QPen(self.__RT_pen, self.__RT_thickness, self.__RT_penStyle)
        self.__painter = QPainter()

        self.__whiteboard.fill(self.__backgroundColor)

        self.begin_point = QPoint()  # 鼠标起始位置
        self.end_point = QPoint()  # 鼠标终结位置
        self.__rect = QRect()

        self.graph = Graph()

        self.pressLocation = QPoint()  # 鼠标点击点坐标
        self.releaseLocation = QPoint()  # 鼠标释放点坐标
        self.RT_MouseLocation = QPoint()  # 鼠标实时位置

        self.brush = QBrush()  # 填充颜色

    def lockLineToPoint(self, event):  # 锁定坐标函数
        if self.graph.getTotalVertex():
            for k, vertices in self.graph.vertDict.items():
                x, y = vertices.getCoordinates()
                value = QPoint(x, y)
                distance = event - value
                if distance.manhattanLength() <= 60:  # 当所在位置于附近点小于等于50个单位时，自动将坐标调整到最近的点
                    return value
        return event

    def lockArcBegin_EndPoint(self):

        p = QPoint()

        if self.begin_point.x() == self.end_point.x():
            p.setX(self.begin_point.x() + 40)
            p.setY(self.begin_point.y())
        elif self.begin_point.y() == self.end_point.y():
            p.setX(self.begin_point.x())
            p.setY(self.begin_point.y() + 40)
        else:
            tan = (self.begin_point.x() - self.end_point.x()) / (self.end_point.y() - self.begin_point.y())
            atan = math.atan(tan)
            cos = math.cos(atan)
            sin = math.sin(atan)
            p.setX(self.begin_point.x() + cos * 40)
            p.setY(self.begin_point.y() + sin * 40)

        print(p)

        x = self.begin_point.x() - self.end_point.x()
        y = self.begin_point.y() - self.end_point.y()
        width = math.sqrt(math.pow(x, 2) + math.pow(y, 2))

        self.__rect.setX(p.x())
        self.__rect.setY(p.y())
        self.__rect.setSize(QSize(width, 40))

    def setDrawGraphStyle(self, toolId=0):
        self.__graphToolId = toolId

    def chooseDrawGraph(self):

        pass

    ##========== event 处理函数============

    def paintEvent(self, event):  # 2
        self.__painter = QPainter(self)  # 定义画笔
        self.__painter.begin(self)
        self.__painter.drawPixmap(0, 0, self.__whiteboard)  # 绘制绘图板
        self.__painter.setPen(self.__RT_pen)  # 设置绘图笔的颜色

        if self.begin_point and self.end_point:  # 如果起始点终结点都存在则进行绘图
            line = QLine(self.begin_point, self.end_point)  # 绘制的线
            self.__painter.drawLine(line)  # 实时绘制线
        self.__painter.end()

    def mousePressEvent(self, event):  # 鼠标点击检测函数
        self.setMouseTracking(True)  # 鼠标跟踪默认触发
        if event.button() == Qt.LeftButton:

            self.begin_point = event.pos()  # 鼠标点击起始点

            self.pressLocation = event.pos()  # 鼠标点击原点

            if self.graph.getTotalVertex():
                self.begin_point = self.lockLineToPoint(event.pos())
            if not self.graph.IsContainsPoint(self.begin_point):
                self.graph.addVertex(self.graph.getTotalVertex(), self.begin_point)
                self.__painter = QPainter(self.__whiteboard)
                self.__painter.setPen(self.__pen)
                self.__painter.setBrush(Qt.darkYellow)
                self.__painter.drawEllipse(self.begin_point, 10, 10)
            self.end_point = self.begin_point
            self.update()  # 3

    def mouseMoveEvent(self, event):  # 鼠标移动事件
        self.setMouseTracking(True)
        point = event.pos()
        self.mouseMove.emit(point)  # 发射信号
        super().mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton:
            self.end_point = event.pos()
            self.update()  # 3

    def mouseReleaseEvent(self, event):  # 鼠标释放事件
        self.setMouseTracking(True)
        if event.button() == Qt.LeftButton:
            self.releaseLocation = event.pos()

            self.__painter = QPainter(self.__whiteboard)

            self.end_point = self.lockLineToPoint(event.pos())

            line = QLine(self.begin_point, self.end_point)
            self.__painter.setPen(self.__pen)

            self.distence = self.begin_point - self.end_point

            if self.distence.manhattanLength() > 60:

                if not self.graph.IsContainsPoint(self.end_point):
                    self.graph.addVertex(self.graph.getTotalVertex(), self.end_point)

                fromVert = self.graph.get_VertexKey(self.begin_point)
                toVert = self.graph.get_VertexKey(self.end_point)

                if not self.graph.IsEmptyEdge():
                    self.graph.addEdge(fromVert, toVert)
                else:
                    if not self.graph.IsContainsEdge(line):
                        lines = QLine(line.p2(), line.p1())
                        if not self.graph.IsContainsEdge(lines):
                            self.graph.addEdge(fromVert, toVert)

                self.__painter.setBrush(Qt.darkYellow)
                self.__painter.drawLine(line)
                self.__painter.drawEllipse(self.begin_point, 10, 10)
                self.__painter.setPen(self.__pen)
                self.__painter.drawEllipse(self.end_point, 10, 10)

            self.begin_point = self.end_point = QPoint()  # 初始化绘图点
            self.update()
            self.__IsEmpty = False

    #  =============自定义槽函数===============================

    def Clear(self, color=QColor(Qt.white)):  # 清空画板
        self.__whiteboard.fill(color)
        self.graph.ClearAllDetails()
        self.update()
        self.__IsEmpty = True

    def getPenColor(self):
        return self.__penColor

    def getPenThickness(self):
        return self.__thickness

    def getRt_PenColor(self):
        return self.__RT_penColor

    def getRt_PenThickness(self):
        return self.__RT_thickness

    def getBackgroundColor(self):
        return self.__backgroundColor

    def getPenStyle(self):
        return self.__penStyle

    def setPenStyle(self, style=Qt.DashLine):  # 改变画笔样式
        self.__pen.setStyle(style)

    def setPenColor(self, color='black'):  # 改变画笔颜色
        self.__pen.setColor(QColor(color))

    def setRT_PenColor(self, color="blue"):  # 改变提示画笔颜色
        self.__RT_pen.setColor(QColor(color))

    def setPenThickness(self, thickness=3):  # 改变画笔粗细
        self.__pen.setWidth(thickness),

    def setRT_PenCThickness(self, RT_thickness=5):
        self.__RT_pen.setWidth(RT_thickness)

    def setBackgroundColor(self, color='white'):
        self.__whiteboard.fill(QColor(color))

    def isEmpty(self):  # 判断桌面是否为空
        return self.__IsEmpty

    def getContentAsQImage(self):  # 存储图片
        image = self.__whiteboard.toImage()
        return image

    def getContentAsGraph(self):
        return self.graph.getStandardData()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph = PainterBoard()
    graph.show()
    sys.exit(app.exec_())
