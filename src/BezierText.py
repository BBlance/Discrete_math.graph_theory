from PySide2.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsTextItem, QGraphicsItem
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QFocusEvent
from BezierGraphicsItem import GraphicsType


class BezierText(QGraphicsTextItem):
    def __init__(self, string):
        super().__init__()
        self._m_graphicsType = GraphicsType.TextType
        self.setPlainText(string)

        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

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

    ##  ==============自定义功能函数========================

    ##  ==============event处理函数==========================

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
        if event.button() == Qt.LeftButton:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)

    ##  ==========由connectSlotsByName()自动连接的槽函数============

    ##  =============自定义槽函数===============================


from PointItem import BezierPointItem, PointType, ItemType, BezierTextItem
