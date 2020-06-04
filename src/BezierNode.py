from math import sqrt
from random import random, randint
from typing import Optional

import typing
from PySide2.QtWidgets import QStyleOptionGraphicsItem, QWidget, QStyle, QGraphicsSceneMouseEvent, QGraphicsItem, \
    QGraphicsSceneContextMenuEvent, QMenu, QAction, QWidgetAction
from PySide2.QtCore import QPointF, QRectF, Qt, qAbs, QPoint
from PySide2.QtGui import QPainterPath, QPainter, QKeyEvent, QColor, QPen, QRadialGradient, QCursor

from BezierGraphicsItem import BezierGraphicsItem


class BezierNode(BezierGraphicsItem):
    __bezierEdgeList = []
    __newPos = QPointF()

    def __init__(self, center=QPointF(0, 0)):
        super(BezierNode, self).__init__(center)

        self.textCp = BezierTextItem(self, self._m_textPos, PointType.Text, ItemType.PointType)

    ##  ==============自定义功能函数========================

    def addBezierEdge(self, bezierEdge, itemType):
        if {bezierEdge: itemType} not in self.__bezierEdgeList:
            self.__bezierEdgeList.append({bezierEdge: itemType})

    @property
    def bezierEdges(self):
        return self.__bezierEdgeList

    @property
    def textPos(self):
        self._m_textPos = QPointF(self._m_centerPos.x() -7, self._m_centerPos.y()-30)
        return self._m_textPos

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
            if str(type(item)).find("BezierPointItem") >= 0:
                return item
            elif str(type(item)).find("BezierEdge") >= 0:
                return item
        return None

    def setBezierEdges(self, item):
        if type(item) is BezierPointItem:
            edge = item.parentItem()
            self.addBezierEdge(edge, item.itemType())
            if item.itemType() == ItemType.SourceType:
                edge.setSourceNode(self)
            if item.itemType() == ItemType.DestType:
                edge.setDestNode(self)
        elif type(item) is BezierEdge:
            if not item.sourceNode:
                if self.contains(self.mapFromItem(item, item.specialControlPoints()[0])):
                    self.addBezierEdge(item, ItemType.SourceType)
                    item.setSourceNode(self)
            if not item.destNode:
                if self.contains(self.mapFromItem(item, item.specialControlPoints()[1])):
                    self.addBezierEdge(item, ItemType.DestType)
                    item.setDestNode(self)

    # def calculateForces(self):
    #     if not self.scene() and self.scene().mouseGrabberItem() == self:
    #         self.__newPos = self.pos()
    #         return
    #
    #     xvel, yvel = 0, 0
    #     items = self.scene().items()
    #     for item in items:
    #         node = item
    #         if not node:
    #             continue
    #         vec = self.mapToItem(node, 0, 0)
    #         dx, dy = vec.x(), vec.y()
    #         l = 2.0 * (dx * dx + dy * dy)
    #         if l > 0:
    #             xvel = xvel + dx * 150 / l
    #             yvel = yvel + dy * 150 / l
    #
    #     weight = (len(self.__edgeList) + 1) * 10
    #     for edge in self.__edgeList:
    #         vec = QPointF()
    #         if edge.getSourceNode() == self:
    #             vec = self.mapToItem(edge.getDestNode(), 0, 0)
    #         else:
    #             vec = self.mapToItem(edge.getSourceNode(), 0, 0)
    #
    #         xvel = xvel - vec.x() / weight
    #         yvel = yvel - vec.y() / weight
    #
    #     if qAbs(xvel) < 0.1 and qAbs(yvel) < 0.1:
    #         xvel = 0
    #         yvel = 0
    #
    #     sceneRect = self.scene().sceneRect()
    #     self.__newPos = self.pos() + QPointF(xvel, yvel)
    #     self.__newPos.setX(min(max(self.newPos.x(), sceneRect.left() + 10), sceneRect.right() - 10))
    #     self.__newPos.setY(min(max(self.newPos.y(), sceneRect.top() + 10), sceneRect.bottom() - 10))
    #
    # def advancePosition(self):
    #     if self.__newPos == self.pos():
    #         return False
    #
    #     self.setPos(self.__newPos)
    #     return True

    #
    # def getEdge(self):
    #     return self._m_edge
    #
    # def setEdge(self, p: QPointF, itemType):
    #     self._m_edge = p

    # def updateRadius(self):
    #     ret = QRectF(self._m_center.x() - 18, self._m_center.y() - 18,
    #                  18 * 2, 18 * 2)
    #     if ret.contains(self._m_edge):
    #         if 10 < self._m_radius:
    #             self._m_radius = sqrt(
    #                 pow(self._m_center.x() - self._m_edge.x(), 2) + pow(self._m_center.y() - self._m_edge.y(), 2))
    #         else:
    #             self._m_radius = 10.606601717798213

    ##  ==============event处理函数==========================

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...):
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)

        # path = QPainterPath()

        gradient = QRadialGradient(self._m_centerPos.x(), self._m_centerPos.y(), 10)

        if option.state and QStyle.State_Sunken:
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

        if self.isSelected():
            painter.setPen(QPen(Qt.black, 1, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
            rect = self.boundingRect()
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(rect)

    def boundingRect(self) -> QRectF:
        adjust = 2

        return QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

        # return QRectF(self._m_center.x() - self._m_radius, self._m_center.y() - self._m_radius,
        #               self._m_radius * 2, self._m_radius * 2)

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
                elif itemType == ItemType.DestType:
                    edge.setDestNode(None)
                    newPos: QPointF = edge.specialControlPoints()[1]
                    newPos.setX(newPos.x() + intRandom)
                    edge.setSpecialControlPoint(newPos, itemType)


from BezierEdge import BezierEdge
from PointItem import BezierPointItem, BezierTextItem, PointType, ItemType
