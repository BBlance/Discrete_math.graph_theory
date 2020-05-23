from enum import Enum, unique
from typing import Optional

from PySide2.QtCore import QObject, QPointF, Qt, QRectF, qrand
from PySide2.QtGui import QColor, QPainter, QBrush, QFont, QFocusEvent
from PySide2.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QWidget, QStyleOptionGraphicsItem, \
    QGraphicsSceneMouseEvent, QLineEdit, QInputDialog, QGraphicsObject, QGraphicsTextItem


@unique
class PointType(Enum):
    Center = 0
    Edge = 1
    Special = 2
    Text = 3


@unique
class ItemType(Enum):
    OneType = 1
    TwoType = 2
    NoneType = 3
    PointType = 4
    PathType = 5


class BezierPointItem(QAbstractGraphicsShapeItem):

    def __init__(self, parent: QAbstractGraphicsShapeItem, p: QPointF, pointType: PointType,
                 itemType=ItemType.NoneType):

        self.__m_point = p
        self.__m_type = pointType
        self.__m_item_type = itemType

        super().__init__(parent)

        self.setPos(self.__m_point)

        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsFocusable |
                      QGraphicsItem.ItemIsSelectable)

        if pointType == PointType.Center:
            self.setCursor(Qt.OpenHandCursor)
        elif pointType == PointType.Edge:
            self.setCursor(Qt.PointingHandCursor)
        elif pointType == PointType.Special:
            self.setCursor(Qt.PointingHandCursor)

    def getPoint(self):
        return self.__m_point

    def setPoint(self, p: QPointF):
        self.__m_point = p

    def getPointType(self):
        return self.__m_type

    def getItemType(self):
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
        item = self.parentItem()
        item.focusOutEvent(event)

        if event.buttons() and Qt.LeftButton:

            dx = event.scenePos().x() - event.lastScenePos().x()
            dy = event.scenePos().y() - event.lastScenePos().y()

            item.center.setPoint(item._m_center)
            item.text.setPoint(item._m_text)
            self.scene().update()

            if self.__m_type == PointType.Center:
                item.focusInEvent(event)
                item.moveBy(dx, dy)
                self.scene().update()
            elif self.__m_type == PointType.Edge:
                self.__m_point = self.mapToParent(event.pos())
                self.setPos(self.__m_point)
                item.setEdge(self.__m_point, self.__m_item_type)
                item.focusInEvent(event)
                self.scene().update()
            elif self.__m_type == PointType.Special:
                self.__m_point = self.mapToParent(event.pos())
                self.setPos(self.__m_point)
                item.setSpecial(self.__m_point, self.__m_item_type)
                item.focusInEvent(event)
                self.scene().update()

            elif self.__m_type == PointType.Text:
                self.__m_point = self.mapToParent(event.pos())
                self.setPos(self.__m_point)
                self.scene().update()

    def setTextVisible(self, visible: bool):
        if self.__m_type == PointType.Text:
            self.setVisible(visible)


class BezierTextItem(QGraphicsTextItem):
    def __init__(self, parent: QAbstractGraphicsShapeItem, p: QPointF, pointType: PointType,
                 itemType=ItemType.NoneType):
        super().__init__(parent)
        self._m_text = "数据"
        self.__m_point = p
        self.__m_type = pointType
        self.__m_item_type = itemType

        self.setPos(self.__m_point)
        self.setPlainText(self._m_text)

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

    def getText(self):
        return self.__m_text

    def setText(self, text: str):
        self.__m_text = text

    def getPointType(self):
        return self.__m_type

    def getPoint(self):
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
        item = self.parentItem()

        if event.buttons() and Qt.LeftButton:
            item.text.setPoint(item._m_text)
            self.__m_point = self.mapToParent(event.pos())
            self.setPos(self.__m_point)
            self.scene().update()

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)


class BezierPointItemList(list):
    def __init__(self):
        super(BezierPointItemList, self).__init__()

    def setRandColor(self):
        self.setColor(QColor(qrand() % 256, qrand() % 256, qrand() % 256))

    def setColor(self, color: QColor):
        for temp in self:
            if temp.getPointType() != PointType.Text:
                temp.setBrush(QBrush(color))

    def setVisible(self, visible: bool):
        for temp in self:
            if temp.getPointType() != PointType.Text:
                temp.setVisible(visible)

    def setParentItem(self, parent):
        for temp in self:
            if temp.getPointType() != PointType.Center:
                temp.setParentItem(parent)
