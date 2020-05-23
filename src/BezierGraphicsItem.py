from enum import unique, Enum
from math import sqrt

from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QPen, QColor, QFocusEvent
from PySide2.QtWidgets import QAbstractGraphicsShapeItem

from PointItem import BezierPointItemList


@unique
class GraphicsType(Enum):
    PathType = 0
    PointType = 1
    TextType = 2
    NoneType = 3


class BezierGraphicsItem(QAbstractGraphicsShapeItem):
    def __init__(self, center: QPointF):
        super(BezierGraphicsItem, self).__init__()
        self._m_radius = float(0)
        self._m_center = center
        self._m_text = QPointF(center.x(), center.y() - 15)
        self._m_pointList = BezierPointItemList()

        self._m_pen_isSelected = QPen()
        self._m_pen_noSelected = QPen()

        self._m_noSelectedThickness = 2
        self._m_isSelectedThickness = 2

        self._m_pen_noSelectedColor = QColor(Qt.gray)
        self._m_pen_isSelectedColor = QColor(Qt.blue)

        self._m_pen_isSelected.setColor(self._m_pen_isSelectedColor)
        self._m_pen_noSelected.setColor(self._m_pen_noSelectedColor)

        self._m_pen_isSelected.setWidth(self._m_isSelectedThickness)
        self._m_pen_noSelected.setWidth(self._m_noSelectedThickness)
        self._m_graphicsType = GraphicsType.NoneType

        self.setPen(self._m_pen_noSelected)

    def getCenter(self):
        return self._m_center

    def setCenter(self, p: QPointF):
        self._m_center = p

    # def getTextPos(self):
    #     return self._m_text
    #
    # def setTextPos(self):
    #     self._m_text = QPointF(self._m_center.x(), self._m_center.y() + 10)

    def getMaxLength(self):
        vec = []
        for temp in self._m_pointList:
            dis = sqrt(pow(self._m_center.x() - temp.x(), 2) + pow(self._m_center.y() - temp.y(), 2))
            vec.append(dis)

        ret = float(0)
        for temp in vec:
            if temp > ret:
                ret = temp

        self._m_radius = ret

    def set_noSelectedPenColor(self, color="gray"):
        self._m_pen_noSelectedColor = QColor(color)

    def get_noSelectedPenColor(self):
        return self._m_pen_noSelectedColor

    def set_isSelectedPenColor(self, color="blue"):
        self._m_pen_isSelectedColor = QColor(color)

    def get_isSelectedPenColor(self):
        return self._m_pen_isSelectedColor

    def set_isSelectedThickness(self, thickness=2):
        self._m_isSelectedThickness = thickness

    def get_isSelectedThickness(self):
        return self._m_isSelectedThickness

    def set_noSelectedThickness(self, thickness=2):
        self._m_noSelectedThickness = thickness

    def get_noSelectedThickness(self):
        return self._m_noSelectedThickness

    def focusInEvent(self, event: QFocusEvent):
        self.setPen(self._m_pen_isSelected)

    def focusOutEvent(self, event: QFocusEvent):
        self.setPen(self._m_pen_noSelected)
