from random import randint
from typing import Optional

import typing
from PySide2.QtWidgets import QStyleOptionGraphicsItem, QWidget, QGraphicsSceneMouseEvent, QGraphicsItem, \
    QGraphicsSceneContextMenuEvent, QMenu, QAction
from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import QPainterPath, QPainter, QColor, QPen, QRadialGradient, QCursor

from BezierGraphicsItem import BezierGraphicsItem


class BezierNode(BezierGraphicsItem):
    __newPos = QPointF()
    _m_weightPos = QPointF(0, 0)

    def __init__(self, center=QPointF(0, 0)):
        super(BezierNode, self).__init__(center)
        self.textCp = BezierTextItem(self, self._m_textPos, PointType.Text, ItemType.PointType)
        self.weightCp = BezierTextItem(self, self.weightPos, PointType.Text, ItemType.PathType)
        self.weightCp.setPlainText("0")
        self.weightCp.setVisible(False)
        self.__bezierEdgeList = []

    ##  ==============自定义功能函数========================

    def addBezierEdge(self, bezierEdge, itemType):
        if {bezierEdge: itemType} not in self.__bezierEdgeList:
            self.__bezierEdgeList.append({bezierEdge: itemType})

    @property
    def bezierEdges(self):
        return self.__bezierEdgeList

    def removeBezierEdge(self, edge, itemType):
        self.__bezierEdgeList.remove({edge: itemType})

    @property
    def weightPos(self):
        self._m_weightPos = QPointF(self._m_centerPos.x() - 10, self._m_centerPos.y() + 5)
        return self._m_weightPos

    @property
    def textPos(self):
        self._m_textPos = QPointF(self._m_centerPos.x() - 7, self._m_centerPos.y() - 30)
        return self._m_textPos

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

    def digraphDegrees(self, mode: bool):  # 结点的度
        if mode:
            outDegree = 0
            inDegree = 0
            for edge in self.__bezierEdgeList:
                for itemType in edge.values():
                    if itemType == ItemType.DestType:
                        inDegree = 1 + inDegree
                    else:
                        outDegree = 1 + outDegree
            return inDegree, outDegree
        else:
            return len(self.__bezierEdgeList)

    def name(self):
        return self.data(1)

    def collidingItem(self):
        for item in self.collidingItems():
            if str(type(item)).find("BezierEdge") >= 0:
                return item
        return None

    def setBezierEdges(self, item):
        if not item.sourceNode:
            if self.contains(self.mapFromItem(item, item.specialControlPoints()[0])):
                self.__bezierEdgeList.append({item: ItemType.SourceType})
                item.setSourceNode(self)
        if not item.destNode:
            if self.contains(self.mapFromItem(item, item.specialControlPoints()[1])):
                self.__bezierEdgeList.append({item: ItemType.DestType})
                item.setDestNode(self)

    ##  ==============event处理函数==========================

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...):
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)

        gradient = QRadialGradient(self._m_centerPos.x(), self._m_centerPos.y(), 10)

        if self.isSelected():
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QColor(Qt.yellow).lighter(120))
            gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.yellow)
            gradient.setColorAt(1, Qt.darkYellow)

        painter.setBrush(gradient)
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

    def boundingRect(self) -> QRectF:
        adjust = 2
        return QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any) -> typing.Any:
        if change is QGraphicsItem.ItemPositionHasChanged:
            for bezierEdge in self.__bezierEdgeList:
                for edge in bezierEdge.keys():
                    edge.adjust()

        return QGraphicsItem.itemChange(self, change, value)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.buttons() and Qt.LeftButton:

            item = self.collidingItem()
            if item is not None:
                self.setBezierEdges(item)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self.update()
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.update()
        super().mousePressEvent(event)

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):
        menu = QMenu()
        if len(self.bezierEdges):
            lockOnNodeAction = QAction("解除组合")
            lockOnNodeAction.triggered.connect(self.do_lockOnNodes)
            menu.addAction(lockOnNodeAction)
            menu.exec_(QCursor.pos())

    ##  ==========由connectSlotsByName()自动连接的槽函数============

    ##  =============自定义槽函数===============================

    def do_lockOnNodes(self):
        for edges in self.bezierEdges:
            intRandom = randint(10, 80)
            for edge, itemType in edges.items():
                if itemType == ItemType.SourceType:
                    edge.setSourceNode(None)
                    newPos: QPointF = edge.specialControlPoints()[0]
                    newPos.setX(newPos.x() + intRandom)
                    edge.setSpecialControlPoint(newPos, itemType)
                    edge.beginCp.setPoint(newPos)
                    edge.beginCp.setVisible(True)
                elif itemType == ItemType.DestType:
                    edge.setDestNode(None)
                    newPos: QPointF = edge.specialControlPoints()[1]
                    newPos.setX(newPos.x() + intRandom)
                    edge.setSpecialControlPoint(newPos, itemType)
                    edge.endCp.setPoint(newPos)
                    edge.endCp.setVisible(True)

        self.scene().update()

        self.__bezierEdgeList.clear()


from PointItem import BezierTextItem, PointType, ItemType
