from enum import Enum, unique
from typing import Optional

from PySide2.QtCore import QPointF, Qt, QRectF, qrand
from PySide2.QtGui import QColor, QPainter, QBrush, QFocusEvent
from PySide2.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QWidget, QStyleOptionGraphicsItem, \
    QGraphicsSceneMouseEvent, QGraphicsTextItem


@unique
class PointType(Enum):
    Center = 0
    Edge = 1
    Special = 2
    Text = 3


@unique
class ItemType(Enum):
    SourceType = 1
    DestType = 2
    NoneType = 3
    PointType = 4
    PathType = 5


class BezierPointItem(QAbstractGraphicsShapeItem):

    def __init__(self, parent: QAbstractGraphicsShapeItem, p: QPointF, pointType: PointType,
                 itemType=ItemType.NoneType, ):

        self.__m_point = p
        self.__m_type = pointType
        self.__m_item_type = itemType

        super().__init__(parent)

        self.setPos(self.__m_point)

        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsFocusable )

        if pointType == PointType.Center:
            self.setCursor(Qt.OpenHandCursor)
        elif pointType == PointType.Edge:
            self.setCursor(Qt.PointingHandCursor)
        elif pointType == PointType.Special:
            self.setCursor(Qt.PointingHandCursor)

    def point(self):
        return self.__m_point

    def setPoint(self, p: QPointF):
        self.__m_point = p

    def pointType(self):
        return self.__m_type

    def itemType(self):
        return self.__m_item_type

    def boundingRect(self) -> QRectF:
        if self.__m_type != PointType.Text:
            return QRectF(-4, -4, 8, 8)
        else:
            return QRectF(-16, -8, 32, 16)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...):
        painter.setPen(self.pen())
        painter.setBrush(self.brush())

        self.setPos(self.__m_point)

        if self.__m_type == PointType.Center:
            painter.drawEllipse(-4, -4, 8, 8)
        elif self.__m_type == PointType.Edge:
            painter.drawRect(-4, -4, 8, 8)
        elif self.__m_type == PointType.Special:
            painter.drawRect(-4, -4, 8, 8)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.buttons() and Qt.LeftButton:
            item = self.parentItem()
            dx = event.scenePos().x() - event.lastScenePos().x()
            dy = event.scenePos().y() - event.lastScenePos().y()
            if item.sourceNode or item.destNode:
                item.adjust()

            item.centerCp.setPoint(item.updateCenterPos())
            item.textCp.setPos(item.textPos)
            item.weightCp.setPos(item.weightPos)
            self.scene().update()
            if self.__m_type == PointType.Center:
                item.moveBy(dx, dy)
                self.scene().update()
            elif self.__m_type == PointType.Edge:
                self.__m_point = self.mapToParent(event.pos())
                #self.setPos(self.__m_point)
                item.setEdgeControlPoint(self.__m_point, self.__m_item_type)
                self.scene().update()
            elif self.__m_type == PointType.Special:
                self.__m_point = self.mapToParent(event.pos())
                #self.setPos(self.__m_point)
                item.setSpecialControlPoint(self.__m_point, self.__m_item_type)
                if self.collidingItem(item):
                    if self.itemType() == ItemType.DestType:
                        item.setDestNode(self.collidingItem(item))
                    if self.itemType() == ItemType.SourceType:
                        item.setSourceNode(self.collidingItem(item))
                    self.collidingItem(item).addBezierEdge(item, self.itemType())

                self.scene().update()
            elif self.__m_type == PointType.Text:
                self.__m_point = self.mapToParent(event.pos())
                self.setPos(self.__m_point)
                self.scene().update()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):

        item = self.parentItem()
        if event.button() and Qt.LeftButton:
            item.focusInEvent(event)
            self.scene().update()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        item = self.parentItem()
        if event.button() and Qt.LeftButton:
            item.focusOutEvent(event)
            self.scene().update()

    def setTextVisible(self, visible: bool):
        if self.__m_type == PointType.Text:
            self.setVisible(visible)

    def collidingItem(self, item):
        for x in self.collidingItems():
            if str(type(x)).find("BezierNode") >= 0:
                return x
        return None


class BezierTextItem(QGraphicsTextItem):
    def __init__(self, parent: QAbstractGraphicsShapeItem, p: QPointF, pointType: PointType,
                 itemType=ItemType.NoneType):
        super().__init__(parent)

        self.__m_point = p
        self.__m_type = pointType
        self.__m_item_type = itemType
        self.setPos(self.__m_point)

        self._m_noSelectedFont = self.font()
        self._m_noSelectedFont.setPointSize(10)
        self._m_noSelectedFont.setBold(False)

        self._m_isSelectedFont = self.font()
        self._m_isSelectedFont.setPointSize(10)
        self._m_isSelectedFont.setBold(True)

        self._m_pen_noSelectedColor = QColor(Qt.gray)
        self._m_pen_isSelectedColor = QColor(Qt.blue)

        self.setFont(self._m_noSelectedFont)
        self.setDefaultTextColor(self._m_pen_isSelectedColor)
        self.setCursor(Qt.PointingHandCursor)

    def pointType(self):
        return self.__m_type

    def point(self):
        return self.__m_point

    def setPoint(self, p: QPointF):
        self.__m_point = p

    def focusInEvent(self, event: QFocusEvent):
        self.setDefaultTextColor(self._m_pen_isSelectedColor)
        self.setFont(self._m_isSelectedFont)
        self.setCursor(Qt.IBeamCursor)

    def focusOutEvent(self, event: QFocusEvent):
        self.setDefaultTextColor(self._m_pen_noSelectedColor)
        self.setFont(self._m_noSelectedFont)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        self.setCursor(Qt.PointingHandCursor)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):

        if event.buttons() and Qt.LeftButton:
            self.__m_point = self.mapToParent(event.pos())
            self.setPos(self.__m_point)
            self.scene().update()

        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
        super().mouseDoubleClickEvent(event)


class BezierPointItemList(list):
    def __init__(self):
        super(BezierPointItemList, self).__init__()

    def setRandColor(self):
        self.setColor(QColor(qrand() % 256, qrand() % 256, qrand() % 256))

    def setColor(self, color: QColor):
        for temp in self:
            temp.setBrush(QBrush(color))

    def setVisible(self, visible: bool):
        for temp in self:
            temp.setVisible(visible)

    def setParentItem(self, parent):
        for temp in self:
            if temp.pointType() != PointType.Center:
                temp.setParentItem(parent)
