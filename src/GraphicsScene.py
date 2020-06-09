import typing
from PySide2.QtCore import Signal, QPointF, Qt
from PySide2.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from BezierEdge import BezierEdge
from BezierGraphicsItem import BezierGraphicsItem
from BezierNode import BezierNode


class GraphicsScene(QGraphicsScene):
    itemMoveSignal = Signal(BezierGraphicsItem, QPointF)
    itemLock = Signal(BezierGraphicsItem)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_Item = None
        self.m_oldPos = QPointF()

    def singleItems(self, className) -> list:
        items = []
        for item in self.scene.items():
            if type(item) is className:
                items.append(item)
        return items

    # def items(self, order: Qt.SortOrder = ...) -> typing.List:
    #     items = QGraphicsScene.items(self, order=Qt.SortOrder.DescendingOrder)
    #     itemList = []
    #     for item in items:
    #         className = str(type(item))
    #         if not className.find("PointItem") >= 0:
    #             itemList.append(item)
    #     return itemList

    def uniqueItems(self):
        items = QGraphicsScene.items(self, order=Qt.SortOrder.DescendingOrder)
        itemList = []
        for item in items:
            className = str(type(item))
            if not className.find("PointItem") >= 0:
                itemList.append(item)
        return itemList

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.buttons() and Qt.LeftButton:
            mousePos = QPointF(event.buttonDownScenePos(Qt.LeftButton).x(), event.buttonDownScenePos(Qt.LeftButton).y())
            itemList = list(self.items(mousePos))
            if len(itemList) > 0:
                self.m_Item = itemList[0]
                self.itemLock.emit(self.m_Item)
        super(GraphicsScene, self).mouseMoveEvent(event)

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
                self.itemMoveSignal.emit(self.m_Item, self.m_oldPos)
            self.m_Item = None
        super(GraphicsScene, self).mouseReleaseEvent(event)
