import sys

from PySide2.QtWidgets import QGraphicsView, QGraphicsScene
from PySide2.QtCore import Signal, QPoint, Qt, QRectF
from PySide2.QtGui import QMouseEvent, QPainter, QColor, QLinearGradient, QKeyEvent

from BezierEdge import BezierEdge
from BezierNode import BezierNode


class GraphicsView(QGraphicsView):
    mouseMove = Signal(QPoint)
    mouseClicked = Signal(QPoint)

    def __init__(self, parent, scene: QGraphicsScene):
        super().__init__(parent)
        self.setRenderHints(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        gradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomRight())
        gradient.setColorAt(0, Qt.white)
        gradient.setColorAt(1, Qt.lightGray)

        self.setBackgroundBrush(gradient)
        self.setScene(scene)


    def zoomIn(self):  # 放大场景
        self.scaleView(1.2)

    def zoomOut(self):  # 缩小场景
        self.scaleView(1 / 1.2)

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if 0.07 > factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)

    def mouseMoveEvent(self, event: QMouseEvent):
        point = event.pos()
        self.mouseMove.emit(point)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            point = event.pos()
            self.mouseClicked.emit(point)
        super().mousePressEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Plus:
            self.zoomIn()
        elif event.key() == Qt.Key_Minus:
            self.zoomOut()
        super().keyPressEvent(event)


