from enum import unique, Enum
from PySide2.QtCore import QPointF, Qt, QCoreApplication
from PySide2.QtGui import QPen, QColor, QFocusEvent
from PySide2.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem


@unique
class GraphicsType(Enum):
    PathType = 0
    PointType = 1
    TextType = 2
    NoneType = 3


class BezierGraphicsItem(QAbstractGraphicsShapeItem):
    _tr = QCoreApplication.translate

    def __init__(self, center: QPointF):
        super(BezierGraphicsItem, self).__init__()
        self.setCursor(Qt.ArrowCursor)
        self.setZValue(-1)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self._m_radius = float(0)
        self._m_centerPos = center
        self._m_textPos = QPointF(center.x() - 7, center.y() - 30)
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

    @property
    def center(self):
        return self._m_centerPos

    def setCenter(self, p: QPointF):
        self._m_centerPos = p

    @property
    def textPos(self):
        self._m_textPos = QPointF(self._m_centerPos.x() - 7, self._m_centerPos.y() - 30)
        return self._m_textPos


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


from PointItem import BezierPointItemList
