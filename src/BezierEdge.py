from random import randint
from typing import Optional
from PySide2.QtWidgets import QStyleOptionGraphicsItem, QWidget, QGraphicsSceneMouseEvent, QMessageBox, \
    QGraphicsSceneContextMenuEvent, QMenu, QAction

from PySide2.QtCore import QPointF, QRectF, Qt, QLineF
from PySide2.QtGui import QPainterPath, QPainter, QKeyEvent, QPolygonF, QPen, \
    QPainterPathStroker, QCursor

from BezierGraphicsItem import BezierGraphicsItem


class BezierEdge(BezierGraphicsItem):
    __source = None
    __dest = None
    __sourcePoint = QPointF(-50, -50)
    __destPoint = QPointF(50, 50)
    __arrowSize = 10
    _edge1 = __sourcePoint + (__destPoint - __sourcePoint) / 4
    _edge2 = __sourcePoint + (__destPoint - __sourcePoint) / 4 * 3
    __path = QPainterPath()
    _isDigraph = True
    _m_weightPos = QPointF(0, 0)

    def __init__(self, sourceNode=None, destNode=None):

        super(BezierEdge, self).__init__(QPointF(0, 0))

        self.centerCp = BezierPointItem(self, self._m_centerPos, PointType.Center, ItemType.NoneType)
        self.edge1Cp = BezierPointItem(self, self._edge1, PointType.Edge, ItemType.SourceType)
        self.edge2Cp = BezierPointItem(self, self._edge2, PointType.Edge, ItemType.DestType)
        self.beginCp = BezierPointItem(self, self.__sourcePoint, PointType.Special, ItemType.SourceType)
        self.endCp = BezierPointItem(self, self.__destPoint, PointType.Special, ItemType.DestType)
        self.textCp = BezierTextItem(self, self._m_textPos, PointType.Text, ItemType.PathType)
        self.weightCp = BezierTextItem(self, self.weightPos, PointType.Text, ItemType.PathType)
        self.weightCp.setPlainText("0")

        self.weightCp.setVisible(False)

        if sourceNode:
            self.__source: BezierNode = sourceNode
            self.__source.textCp.setText("source")
            self.__source.addBezierEdge(self, self.beginCp.itemType())
            self.__source.setPos(self.specialControlPoints()[0])

        if destNode:
            self.__dest: BezierNode = destNode
            self.__dest.textCp.setText("dest")
            self.__dest.addBezierEdge(self, self.endCp.itemType())
            self.__dest.setPos(self.specialControlPoints()[1])

        self._m_pointList.append(self.centerCp)
        self._m_pointList.append(self.beginCp)
        self._m_pointList.append(self.edge1Cp)
        self._m_pointList.append(self.edge2Cp)
        self._m_pointList.append(self.endCp)

        self._m_pointList.setRandColor()
        self._m_pointList.setParentItem(self)

        # self._startAngle = float(0)
        # self._endAngle = float(0)
        # self._sweepLength = float(0)
        # self._startPoint = QPointF()

    ##  ==============自定义功能函数========================
    @property
    def sourceNode(self):
        return self.__source

    @property
    def destNode(self):
        return self.__dest

    @property
    def weightPos(self):
        self._m_weightPos = QPointF(self._m_centerPos.x() - 10, self._m_centerPos.y() + 5)
        return self._m_weightPos

    def setSourceNode(self, source):
        self.__source = source

    def setDestNode(self, dest):
        self.__dest = dest

    def adjust(self):
        if self.__source:
            self.beginCp.setVisible(False)
            line1 = QLineF(self.mapFromItem(self.__source, 0, 0), self._edge1)
            length1 = line1.length()
            if length1 > 20.0:
                edgeOffset = QPointF(line1.dx() * 10 / length1, line1.dy() * 10 / length1)
                self.__sourcePoint = line1.p1() + edgeOffset
            else:
                self.__sourcePoint = line1.p1()
        else:
            self.beginCp.setVisible(True)
            self.beginCp.setPoint(self.__sourcePoint)
        if self.__dest:
            self.endCp.setVisible(False)
            line2 = QLineF(self.mapFromItem(self.__dest, 0, 0), self._edge2)
            length2 = line2.length()
            if length2 > 20.0:
                edgeOffset = QPointF(line2.dx() * 10 / length2, line2.dy() * 10 / length2)
                if self._isDigraph:
                    self.__destPoint = line2.p1() + edgeOffset * 2.3
                else:
                    self.__destPoint = line2.p1() + edgeOffset
            else:
                self.__destPoint = line2.p1()
        else:
            self.endCp.setVisible(True)
            self.endCp.setPoint(self.__destPoint)

        self.prepareGeometryChange()

    def specialControlPoints(self):
        return self.__sourcePoint, self.__destPoint

    def setSpecialControlPoint(self, p: QPointF, itemType):
        if itemType == ItemType.SourceType:
            self.__sourcePoint = p
        elif itemType == ItemType.DestType:
            self.__destPoint = p

    def edgeControlPoints(self):
        return self._edge1, self._edge2

    def setEdgeControlPoint(self, p: QPointF, itemType):
        if itemType == ItemType.SourceType:
            self._edge1 = p
        elif itemType == ItemType.DestType:
            self._edge2 = p

    def updateCenterPos(self):
        specialTuple = self.edgeControlPoints() + self.specialControlPoints()
        x = 0
        y = 0
        for temp in specialTuple:
            x = x + temp.x()
            y = y + temp.y()

        x = x / len(specialTuple)
        y = y / len(specialTuple)

        self._m_centerPos = QPointF(x, y)
        return self._m_centerPos

    def isDigraph(self):
        return self._isDigraph

    def setGraphMode(self, mode):
        self._isDigraph = mode

    def weight(self):
        weight = self.weightCp.toPlainText()
        if weight.isdigit():
            return int(weight)
        elif self.is_Float():
            return int(float(weight))

        title = "权重设置错误"
        strInfo = "您的权重有误，请更正为数字！"
        QMessageBox.warning(None, title, strInfo)

    def is_Float(self):
        weight = self.weightCp.toPlainText()
        try:
            float(weight)
            return True
        except ValueError:
            pass
        return False

    def drawArrow(self):
        line = QLineF(self._edge2, self.__destPoint)
        v = line.unitVector()
        v.setLength(12)
        v.translate(QPointF(line.dx(), line.dy()))
        n = v.normalVector()
        n.setLength(n.length() * 0.5)
        n2 = n.normalVector().normalVector()
        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()
        return QPolygonF([p1, p2, p3, p1])

    # def calc_angle(self):
    #     self.startLine = QLineF(self._m_center, self._sourcePoint)
    #     self.endLine = QLineF(self._m_center, self._destPoint)
    #
    #     self._startAngle = self.startLine.angle()
    #     self._endAngle = self.endLine.angle()
    #
    #     if self._startAngle < self._endAngle:
    #         temp = self._startAngle
    #         self._startAngle = self._endAngle
    #         self._endAngle = temp
    #         self._startPoint = self._destPoint
    #     else:
    #         self._startPoint = self._sourcePoint
    #     self._sweepLength = 360 - (self._startAngle - self._endAngle)
    #     if self._sweepLength < 90:
    #         self._sweepLength = 360 - self._sweepLength
    #         temp = self._startAngle
    #         self._startAngle = self._endAngle
    #         self._endAngle = temp
    #         self._startPoint = self._destPoint

    ##  ==============event处理函数==========================
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...):
        painter.setPen(self.pen())
        brush = self.brush()
        painter.setBrush(brush)
        path = QPainterPath()
        path.moveTo(self.__sourcePoint)
        path.cubicTo(self._edge1, self._edge2, self.__destPoint)
        if self._isDigraph:
            painter.setBrush(Qt.gray)
            painter.drawPolygon(self.drawArrow())
            path.addPolygon(self.drawArrow())
        painter.setBrush(Qt.NoBrush)
        if self.isSelected():
            pen = painter.pen()
            pen.setColor(self.get_isSelectedPenColor())
        else:
            pen = painter.pen()
            pen.setColor(self.get_noSelectedPenColor())
        painter.setPen(pen)

        painter.drawPath(path)
        self.__path = path

        # if self.isSelected():
        #     painter.setPen(QPen(Qt.black, 1, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
        #     rect = self.boundingRect()
        #     painter.drawRect(rect)

    def shape(self) -> QPainterPath:
        stroker = QPainterPathStroker()
        stroker.setWidth(10)
        stroker.setJoinStyle(Qt.MiterJoin)
        stroker.setCapStyle(Qt.RoundCap)
        stroker.setDashPattern(Qt.DashLine)
        return stroker.createStroke(self.__path)

    def boundingRect(self) -> QRectF:
        return self.shape().boundingRect()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_H:
            for temp in self._m_pointList:
                if temp.pointType() != PointType.Text:
                    if temp.isVisible():
                        temp.setVisible(False)
                    else:
                        temp.setVisible(True)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.buttons() and Qt.LeftButton:
            if self.__dest or self.__source:
                self.adjust()
        super().mouseMoveEvent(event)

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):
        menu = QMenu()
        if self._isDigraph:
            changeDirection = QAction("更换方向")
            changeDirection.triggered.connect(self.do_changeDirection)
            menu.addAction(changeDirection)

        if self.__source:
            lockOnSourceAction = QAction("解除始点连接")
            lockOnSourceAction.triggered.connect(lambda: self.do_lockOnNodes(self.__source))
            menu.addAction(lockOnSourceAction)
        if self.__dest:
            lockOnDestAction = QAction("解除终点连接")
            lockOnDestAction.triggered.connect(lambda: self.do_lockOnNodes(self.__dest))
            menu.addAction(lockOnDestAction)

        menu.exec_(QCursor.pos())

    def do_lockOnNodes(self, node):

        node: BezierNode
        intRandom = randint(10, 80)

        if node is self.__source:
            self.__source = None
            newPos: QPointF = self.specialControlPoints()[0]
            newPos.setX(newPos.x() + intRandom)
            self.setSpecialControlPoint(newPos, ItemType.SourceType)
            node.removeBezierEdge(edge=self, itemType=ItemType.SourceType)
            self.beginCp.setPoint(newPos)
            self.beginCp.setVisible(True)
        else:
            self.__dest = None
            newPos: QPointF = self.specialControlPoints()[1]
            newPos.setX(newPos.x() + intRandom)
            self.setSpecialControlPoint(newPos, ItemType.DestType)
            node.removeBezierEdge(edge=self, itemType=ItemType.DestType)
            self.endCp.setPoint(newPos)
            self.endCp.setVisible(True)

    def do_changeDirection(self):
        node = self.__sourcePoint
        self.__sourcePoint = self.__destPoint
        self.__destPoint = node

        node = self._edge1
        self._edge1 = self._edge2
        self._edge2 = node

        if self.__source:
            self.__source: BezierNode
            edges = self.__source.bezierEdges
            self.__source.removeBezierEdge(self, ItemType.SourceType)
            self.__source.addBezierEdge(self, ItemType.DestType)

        if self.__dest:
            self.__dest: BezierNode
            edges = self.__dest.bezierEdges
            self.__dest.removeBezierEdge(self, ItemType.DestType)
            self.__dest.addBezierEdge(self, ItemType.SourceType)

        node = self.__source
        self.__source = self.__dest
        self.__dest = node


from BezierNode import BezierNode
from PointItem import BezierPointItem, PointType, ItemType, BezierTextItem
