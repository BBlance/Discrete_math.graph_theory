from enum import Enum
from math import sqrt
from typing import Optional

from PySide2.QtWidgets import QStyleOptionGraphicsItem, QWidget, QGraphicsSceneMouseEvent, \
    QGraphicsTextItem
from PySide2.QtCore import QPointF, QRectF, Qt, QLineF
from PySide2.QtGui import QPainterPath, QPainter, QKeyEvent, QColor, QPolygonF, QPen, QFocusEvent
from BezierGraphicsItem import BezierGraphicsItem, GraphicsType


class BezierPath(BezierGraphicsItem):
    def __init__(self, mouseClicked: QPointF, mouseReleased: QPointF):

        self._beginPos = mouseClicked
        self._endPos = mouseReleased
        self._edge1 = -(mouseClicked - mouseReleased) / 4
        self._edge2 = -(mouseClicked - mouseReleased) / 4 * 3
        self._m_graphicsType = GraphicsType.PathType

        super(BezierPath, self).__init__(self.updateCenter(self.getEdge() + self.getSpecial()))

        self.center = BezierPointItem(self, self._m_center, PointType.Center, ItemType.NoneType)
        self.edge1 = BezierPointItem(self, self._edge1, PointType.Edge, ItemType.OneType)
        self.edge2 = BezierPointItem(self, self._edge2, PointType.Edge, ItemType.TwoType)
        self.beginPos = BezierPointItem(self, self._beginPos, PointType.Special, ItemType.OneType)
        self.endPos = BezierPointItem(self, self._endPos, PointType.Special, ItemType.TwoType)
        self.text = BezierTextItem(self, self._m_text, PointType.Text, ItemType.PathType)

        self._m_pointList.append(self.center)
        self._m_pointList.append(self.beginPos)
        self._m_pointList.append(self.edge1)
        self._m_pointList.append(self.edge2)
        self._m_pointList.append(self.endPos)
        self._m_pointList.append(self.text)

        self._m_pointList.setRandColor()
        self._m_pointList.setParentItem(self)

        self._startAngle = float(0)
        self._endAngle = float(0)
        self._sweepLength = float(0)
        self._startPoint = QPointF()

        self._isDigraph = True
        self.path = QPainterPath()

    def getSpecial(self):
        return self._beginPos, self._endPos

    def setSpecial(self, p: QPointF, itemType):
        if itemType == ItemType.OneType:
            self._beginPos = p
        elif itemType == ItemType.TwoType:
            self._endPos = p

    def getEdge(self):
        return self._edge1, self._edge2

    def setEdge(self, p: QPointF, itemType):
        if itemType == ItemType.OneType:
            self._edge1 = p
        elif itemType == ItemType.TwoType:
            self._edge2 = p

    @classmethod
    def updateCenter(cls, specialTuple: tuple):
        x = 0
        y = 0
        for temp in specialTuple:
            x = x + temp.x()
            y = y + temp.y()
        x = x / len(specialTuple)
        y = y / len(specialTuple)

        return QPointF(x, y)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...):
        painter.setPen(self.pen())
        brush = self.brush()
        painter.setBrush(brush)
        path = QPainterPath()
        self._edge1 = (self.getEdge())[0]
        self._edge2 = (self.getEdge())[1]
        self._beginPos = (self.getSpecial())[0]
        self._endPos = (self.getSpecial())[1]

        self._m_center = self.updateCenter(self.getEdge() + self.getSpecial())
        self._m_text = QPointF(self._m_center.x(), self._m_center.y() - 15)

        vector = self._beginPos - self._endPos
        vector = sqrt(pow(vector.x(), 2) + pow(vector.y(), 2))
        if vector <= 25:

            ret = QRectF(self._m_center.x() - self.getRadius(), self._m_center.y() - self.getRadius(),
                         self.getRadius() * 2, self.getRadius() * 2)
            self.calc_angle()
            path.moveTo(self._startPoint)

            path.arcTo(ret, self._startAngle, self._sweepLength)
            self.edge1.setVisible(False)
            if self._isDigraph:
                line = QLineF(self._endPos, self._m_center)
                if self.startLine.angle() > self.endLine.angle():
                    line.setPoints(self._m_center, self._endPos)
                    line.translate(line.dx(), line.dy())

                v = line.normalVector()
                v.setLength(7)
                n = v.normalVector()
                n.setLength(n.length() * 0.5)
                n2 = n.normalVector().normalVector()
                p1 = v.p2()
                p2 = n.p2()
                p3 = n2.p2()
                points = QPolygonF([p1, p2, p3, p1])
                path.addPolygon(points)
        else:
            path.moveTo(self._beginPos)
            path.cubicTo(self._edge1, self._edge2, self._endPos)
            self.edge1.setVisible(True)
            if self._isDigraph:
                line = QLineF(self._edge2, self._endPos)
                v = line.unitVector()
                v.setLength(7)
                v.translate(QPointF(line.dx(), line.dy()))
                n = v.normalVector()
                n.setLength(n.length() * 0.5)
                n2 = n.normalVector().normalVector()
                p1 = v.p2()
                p2 = n.p2()
                p3 = n2.p2()
                points = QPolygonF([p1, p2, p3, p1])
                path.addPolygon(points)

        painter.drawPath(path)
        self.path = path

        if self.isSelected():
            painter.setPen(QPen(Qt.black, 1, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
            rect = self.boundingRect()
            painter.drawRect(rect)

    def shape(self) -> QPainterPath:
        return self.path

    def boundingRect(self) -> QRectF:
        self.getMaxLength()

        return QRectF(self._m_center.x() - self._m_radius, self._m_center.y() - self._m_radius,
                      self._m_radius * 2, self._m_radius * 2)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_H:
            for temp in self._m_pointList:
                if temp.getPointType() != PointType.Text:
                    if temp.isVisible():
                        temp.setVisible(False)
                    else:
                        temp.setVisible(True)

    def getRadius(self):
        vec = []
        for temp in self.getSpecial():
            dis = sqrt(pow(self._m_center.x() - temp.x(), 2) + pow(self._m_center.y() - temp.y(), 2))
            vec.append(dis)

        ret = float(0)
        for temp in vec:
            if temp > ret:
                ret = temp

        return ret

    def calc_angle(self):
        self.startLine = QLineF(self._m_center, self._beginPos)
        self.endLine = QLineF(self._m_center, self._endPos)

        self._startAngle = self.startLine.angle()
        self._endAngle = self.endLine.angle()

        if self._startAngle < self._endAngle:
            temp = self._startAngle
            self._startAngle = self._endAngle
            self._endAngle = temp
            self._startPoint = self._endPos
        else:
            self._startPoint = self._beginPos
        self._sweepLength = 360 - (self._startAngle - self._endAngle)
        if self._sweepLength < 90:
            self._sweepLength = 360 - self._sweepLength
            temp = self._startAngle
            self._startAngle = self._endAngle
            self._endAngle = temp
            self._startPoint = self._endPos


class BezierPoint(BezierGraphicsItem):
    def __init__(self, center=QPointF(20, 20), width=15, height=15):
        super(BezierPoint, self).__init__(center)
        self._m_graphicsType = GraphicsType.PointType
        self._m_edge = QPointF(center.x() + width / 2, center.y() + height / 2)
        self.edge = BezierPointItem(self, self._m_edge, PointType.Edge, ItemType.NoneType)
        self.center = BezierPointItem(self, self._m_center, PointType.Center, ItemType.NoneType)
        self.text = BezierTextItem(self, self._m_text, PointType.Text, ItemType.PointType)
        self.edge.setParentItem(self)
        self._m_pointList.append(self.center)
        self._m_pointList.append(self.edge)
        self._m_pointList.append(self.text)
        self._m_pointList.setRandColor()
        self.path = QPainterPath()
        self._m_radius = sqrt(
            pow(self._m_center.x() - self._m_edge.x(), 2) + pow(self._m_center.y() - self._m_edge.y(), 2))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...):
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        path = QPainterPath()

        self._m_edge = self.getEdge()
        self.updateRadius()
        self._m_text = QPointF(self._m_center.x(), self._m_center.y() - 15)

        ret = QRectF(self._m_center.x() - self._m_radius, self._m_center.y() - self._m_radius,
                     self._m_radius * 2, self._m_radius * 2)

        path.addEllipse(ret)
        painter.drawPath(path)
        self.path = path

        if self.isSelected():
            painter.setPen(QPen(Qt.black, 1, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
            rect = self.boundingRect()
            painter.drawRect(rect)

    def boundingRect(self) -> QRectF:
        return QRectF(self._m_center.x() - self._m_radius, self._m_center.y() - self._m_radius,
                      self._m_radius * 2, self._m_radius * 2)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_H:
            for temp in self._m_pointList:
                if temp.getPointType() != PointType.Text:
                    if temp.isVisible():
                        temp.setVisible(False)
                    else:
                        temp.setVisible(True)

    def getEdge(self):
        return self._m_edge

    def setEdge(self, p: QPointF, itemType):
        self._m_edge = p

    def updateRadius(self):
        ret = QRectF(self._m_center.x() - 18, self._m_center.y() - 18,
                     18 * 2, 18 * 2)
        if ret.contains(self._m_edge):
            if 10 < self._m_radius:
                self._m_radius = sqrt(
                    pow(self._m_center.x() - self._m_edge.x(), 2) + pow(self._m_center.y() - self._m_edge.y(), 2))
            else:
                self._m_radius = 10.606601717798213


class BezierText(QGraphicsTextItem):
    def __init__(self, string):
        super().__init__()
        self._m_graphicsType = GraphicsType.TextType
        self.setPlainText(string)

        self._m_noSelectedFont = self.font()
        self._m_noSelectedFont.setPointSize(20)
        self._m_noSelectedFont.setBold(False)

        self._m_isSelectedFont = self.font()
        self._m_isSelectedFont.setPointSize(20)
        self._m_isSelectedFont.setBold(True)

        self._m_pen_noSelectedColor = QColor(Qt.gray)
        self._m_pen_isSelectedColor = QColor(Qt.blue)

        self.setFont(self._m_noSelectedFont)
        self.setDefaultTextColor(self._m_pen_isSelectedColor)

    def focusInEvent(self, event: QFocusEvent):
        self.setDefaultTextColor(self._m_pen_isSelectedColor)
        self.setFont(self._m_isSelectedFont)

    def focusOutEvent(self, event: QFocusEvent):
        self.setDefaultTextColor(self._m_pen_noSelectedColor)
        self.setFont(self._m_noSelectedFont)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        print(event.button())
        if event.button() == Qt.LeftButton:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)


from PointItem import BezierPointItem, PointType, ItemType, BezierTextItem
