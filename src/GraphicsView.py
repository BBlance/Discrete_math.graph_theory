import sys

from PySide2.QtWidgets import QGraphicsView
from PySide2.QtCore import Signal, QPoint, Qt
from PySide2.QtGui import QMouseEvent, QPainter, QColor


class GraphicsView(QGraphicsView):
    mouseMove = Signal(QPoint)
    mouseClicked = Signal(QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._backgroundColor = Qt.white
        self.setRenderHints(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setBackgroundBrush(QColor(self._backgroundColor))

    def mouseMoveEvent(self, event: QMouseEvent):
        point = event.pos()
        self.mouseMove.emit(point)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            point = event.pos()
            self.mouseClicked.emit(point)
        super().mousePressEvent(event)
