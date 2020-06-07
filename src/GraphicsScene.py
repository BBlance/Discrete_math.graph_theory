import typing
from PySide2.QtCore import Signal, QPointF, Qt
from PySide2.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from BezierEdge import BezierEdge
from BezierNode import BezierNode
from BezierText import BezierText


class GraphicsScene(QGraphicsScene):
    edgeMoveSignal = Signal(BezierEdge, QPointF)
    nodeMoveSignal = Signal(BezierNode, QPointF)
    textMoveSignal = Signal(BezierText, QPointF)

    def __init__(self):
        super(GraphicsScene, self).__init__()

        self.m_Item = None
        self.m_oldPos = QPointF()

    def items(self, order: Qt.SortOrder = ...) -> typing.List:
        items = QGraphicsScene.items(self, order=Qt.SortOrder.DescendingOrder)
        itemList = []
        for item in items:
            className = str(type(item))
            if not className.find("PointItem") >= 0:
                itemList.append(item)
        return itemList

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        mousePos = QPointF(event.buttonDownScenePos(Qt.LeftButton).x(), event.buttonDownScenePos(Qt.LeftButton).y())

        itemList = list(self.items(mousePos))

        if len(itemList) > 0:
            self.m_Item = itemList[0]

        if self.m_Item is not None and event.button() == Qt.LeftButton:
            self.m_oldPos = self.m_Item.pos()

        super(GraphicsScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self.m_Item is not None and event.button() == Qt.LeftButton:
            if self.m_oldPos != self.m_Item.pos():
                self.edgeMoveSignal.emit(self.m_Item, self.m_oldPos)

            self.m_Item = None

        super(GraphicsScene, self).mouseReleaseEvent(event)
