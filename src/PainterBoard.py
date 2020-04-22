import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.Graph import Graph


class Demo(QMainWindow):

    def __init__(self):
        super(Demo, self).__init__()

        self.__InitData(QApplication.desktop())
        self.__InitView()

    def __InitData(self, desktop=QApplication.desktop()):
        # 获取屏幕尺寸，设置绘图界面大小
        self.screenRect = desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.__size = QSize(self.width / 2, self.height / 2.03)

        # 新建画板，尺寸为__size
        self.__whiteboard = QPixmap(self.__size)
        self.__whiteboard.fill(Qt.white)

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

        self.nodes = {}  # 图的结点
        self.edges = {}  # 图的边

        self.pressLocation = QPoint()  # 鼠标点击点坐标
        self.releaseLocation = QPoint()  # 鼠标释放点坐标
        self.RT_MouseLocation = QPoint()  # 鼠标实时位置

        self.node_Num = len(self.nodes)  # 结点个数
        self.edges_Num = len(self.edges)  # 边的条数

        self.brush = QBrush()  # 填充颜色

    def __InitView(self):
        self.setFixedSize(self.__size)  # 将窗口尺寸锁死

    def paintEvent(self, event):  # 2
        painter = QPainter(self)  # 定义画笔
        painter.begin(self)
        painter.drawPixmap(0, 0, self.__whiteboard)  # 绘制绘图板
        painter.setPen(QPen(Qt.blue, 5))  # 设置绘图笔的颜色
        if self.begin_point and self.end_point:  # 如果起始点终结点都存在则进行绘图
            line = QLine(self.begin_point, self.end_point)  # 绘制的线
            painter.drawLine(line)  # 实时绘制线
        painter.end()

    def mousePressEvent(self, event):  # 鼠标点击检测函数
        self.setMouseTracking(True)  # 鼠标跟踪默认触发
        if event.button() == Qt.LeftButton:

            self.begin_point = event.pos()  # 鼠标点击起始点

            self.pressLocation = event.pos()  # 鼠标点击原点

            if self.graph.getTotalVertex():
                self.begin_point = self.lockLineToPoint(event.pos())
            if not self.graph.IsContainsPoint(self.begin_point):
                self.graph.addVertex(self.graph.getTotalVertex(), self.begin_point)
                painter = QPainter(self.__whiteboard)
                painter.setPen(QPen(self.__penColor, self.__thickness))
                painter.setBrush(Qt.darkYellow)
                painter.drawEllipse(self.begin_point, 10, 10)
            self.end_point = self.begin_point
            self.update()  # 3

    def mouseMoveEvent(self, event):  # 鼠标移动事件
        self.setMouseTracking(True)
        self.RT_MouseLocation = event.pos()
        if event.buttons() == Qt.LeftButton:
            self.end_point = event.pos()
            self.update()  # 3

    def mouseReleaseEvent(self, event):  # 鼠标释放事件
        self.setMouseTracking(True)
        if event.button() == Qt.LeftButton:
            self.releaseLocation = event.pos()

            painter = QPainter(self.__whiteboard)

            self.end_point = self.lockLineToPoint(event.pos())

            line = QLine(self.begin_point, self.end_point)
            painter.setPen(QPen(self.__penColor, self.__thickness))

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

                painter.setBrush(Qt.darkYellow)
                painter.drawLine(line)
                painter.drawEllipse(self.begin_point, 10, 10)
                painter.setPen(QPen(Qt.black, 3))
                painter.drawEllipse(self.end_point, 10, 10)

            self.begin_point = self.end_point = QPoint()  # 初始化绘图点
            self.update()
            self.__IsEmpty = False

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

    def GetContentAsQImage(self):  # 存储图片
        image = self.__whiteboard.toImage()
        return image


    def GetMouseLocation(self):  # 获取实时坐标
        return self.RT_MouseLocation

    def GetContentAsGraph(self):
        return self.graph.getStandardData()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph = Demo()
    graph.show()
    sys.exit(app.exec_())
