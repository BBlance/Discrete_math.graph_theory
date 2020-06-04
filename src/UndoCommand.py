from random import random

from PySide2.QtCore import QPointF
from PySide2.QtWidgets import QUndoCommand, QGraphicsScene

from BezierEdge import BezierEdge


class AddCommand(QUndoCommand):
    def __init__(self, scene: QGraphicsScene):
        super(AddCommand, self).__init__()

        self.scene = scene
        self.shape = BezierEdge(QPointF(0, 0), QPointF(100, 100))
        self.m_initPos = QPointF(random.randint(1, 10), random.randint(1, 10))
        self.setText("添加曲线")

    def undo(self):
        self.scene.removeItem(self.shape)
        self.scene.update()

    def redo(self):
        self.scene.addItem(self.shape)
        self.shape.setPos(self.m_initPos)
        self.scene.clearSelection()


class MoveCommand(QUndoCommand):
    def __init__(self, item: BezierEdge, oldPos: QPointF):
        super(MoveCommand, self).__init__()
        self.shape = item
        self.m_oldPos = oldPos
        self.m_newPos = self.shape.pos()

    def redo(self):
        self.shape.setPos(self.m_newPos)
        self.setText("图形移动到%d,%d" % (self.shape.pos().x(), self.shape.pos().y()))

    def undo(self):
        self.shape.setPos(self.m_oldPos)
        self.setText("图形移动到%d,%d" % (self.shape.pos().x(), self.shape.pos().y()))
