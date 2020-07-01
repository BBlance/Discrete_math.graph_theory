from PySide2.QtCore import Signal, QPointF, Qt, QRectF
from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent
from BezierGraphicsItem import BezierGraphicsItem
from time import time


class GraphicsScene(QGraphicsScene):
    itemMoveSignal = Signal(BezierGraphicsItem, QPointF)
    isHasItem = Signal(int)
    itemLock = Signal(BezierGraphicsItem)
    itemNode = Signal(list)

    def __init__(self):
        super(GraphicsScene, self).__init__()

        self.m_Item = None
        self.m_oldPos = QPointF()
        self.nodeList = []
        self.another = False
        self.setSceneRect(QRectF(-300, -200, 600, 200))

    def singleItems(self, className, order=0) -> list:
        items = []
        if order == 0:
            for item in self.items():
                if type(item) is className:
                    items.append(item)
        elif order == 1:
            for item in self.selectedItems():
                if type(item) is className:
                    items.append(item)
        return items

    def uniqueIdList(self, className):
        items = []
        for item in self.items():
            if type(item) is className:
                items.append(item.data(0))
        return items

    #  获取需要的结点和边
    def uniqueItems(self):
        items = QGraphicsScene.items(self, order=Qt.SortOrder.DescendingOrder)
        itemList = []
        for item in items:
            className = str(type(item))
            if not className.find("PointItem") >= 0:
                itemList.append(item)
        return itemList

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if not self.focusItem():
            self.nodeList.clear()
        if event.buttons() and Qt.LeftButton:
            mousePos = QPointF(event.buttonDownScenePos(Qt.LeftButton).x(), event.buttonDownScenePos(Qt.LeftButton).y())
            itemList = list(self.items(mousePos))
            if len(itemList) > 0:
                self.m_Item = itemList[0]
                self.itemLock.emit(self.m_Item)
        if len(self.nodeList) > 0:
            self.itemNode.emit(self.nodeList)
        if not self.another:
            if len(self.nodeList) > 1:
                self.nodeList = self.nodeList[1:]
        self.isHasItem.emit(len(self.items()))

        if len(self.nodeList) > 2:
            self.nodeList.clear()

        super(GraphicsScene, self).mouseMoveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        mousePos = QPointF(event.buttonDownScenePos(Qt.LeftButton).x(), event.buttonDownScenePos(Qt.LeftButton).y())

        itemList = list(self.items(mousePos))
        super(GraphicsScene, self).mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            if len(self.nodeList) <= 2:
                if self.focusItem():
                    self.nodeList.append((self.focusItem(), time()))

        if not self.focusItem():
            self.nodeList.clear()

        if len(itemList) > 0:
            self.m_Item = itemList[0]
            self.itemLock.emit(self.m_Item)
        if self.m_Item is not None and event.button() == Qt.LeftButton:
            self.m_oldPos = self.m_Item.pos()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self.m_Item is not None and event.button() == Qt.LeftButton:
            self.itemLock.emit(self.m_Item)
            if self.m_oldPos != self.m_Item.pos():
                self.itemMoveSignal.emit(self.m_Item, self.m_oldPos)
            self.m_Item = None
        super(GraphicsScene, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Control:
            self.another = True
