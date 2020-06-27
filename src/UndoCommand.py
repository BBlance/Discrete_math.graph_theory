from random import random

from PySide2.QtCore import QPointF, QCoreApplication
from PySide2.QtWidgets import QUndoCommand, QGraphicsScene

from BezierEdge import BezierEdge
from BezierNode import BezierNode
from PointItem import ItemType


class AddCommand(QUndoCommand):
    _tr = QCoreApplication.translate

    def __init__(self, parent, scene: QGraphicsScene, item):
        super(AddCommand, self).__init__()

        self.scene = scene
        self.item = item
        self.parent = parent
        className = str(type(item))
        if className.find("BezierNode") >= 0:
            text = self._tr("AddCommand", '添加顶点V')
            self.setText(f'{text}{self.item.data(2)}')
        elif className.find("BezierEdge") >= 0:
            text = self._tr("AddCommand", '添加边e')
            self.setText(f'{text}{self.item.data(3)}')
        elif className.find("BezierText") >= 0:
            text = self._tr("AddCommand", '添加注释')
            self.setText(f'{text}{self.item.data(4)}')

    def undo(self):
        self.do_deleteItem()
        self.scene.update()

    def redo(self):
        self.scene.addItem(self.item)
        self.scene.clearSelection()

    def do_deleteItem(self):
        if str(type(self.item)).find("BezierNode") >= 0:
            self.item: BezierNode
            for edge in self.item.bezierEdges:
                for node, itemType in edge.items():
                    if itemType == ItemType.SourceType:
                        node.setSourceNode(None)
                    elif itemType == ItemType.DestType:
                        node.setDestNode(None)
            nodeNum = self.parent.nodeNum()
            nodeNum -= 1
        elif str(type(self.item)).find("BezierEdge") >= 0:
            self.item: BezierEdge
            sourceNode: BezierNode = self.item.sourceNode
            destNode: BezierNode = self.item.destNode
            if sourceNode:
                sourceNodeList = sourceNode.bezierEdges
                for sourceEdge in sourceNodeList:
                    for edge in sourceEdge.keys():
                        if self.item is edge:
                            sourceNodeList.remove(sourceEdge)

            if destNode:
                destNodeList = destNode.bezierEdges
                for destEdge in destNodeList:
                    for edge in destEdge.keys():
                        if self.item is edge:
                            destNodeList.remove(destEdge)
            edgeNum = self.parent.edgeNum()
            edgeNum -= 1
        self.scene.removeItem(self.item)  # 删除绘图项


class MoveCommand(QUndoCommand):
    _tr = QCoreApplication.translate

    def __init__(self, item, oldPos: QPointF):
        super(MoveCommand, self).__init__()
        self.item = item

        self.m_oldPos = oldPos
        self.m_newPos = self.item.pos()
        self.data = ''
        move = self._tr("MoveCommand", '移动到')
        className = str(type(item))
        if className.find("BezierNode") >= 0:
            text = self._tr("MoveCommand", '顶点V')
            self.data = f"{text}{self.item.data(2)}{move}"
        elif className.find("BezierEdge") >= 0:
            text = self._tr("MoveCommand", '边e')
            self.data = f"{text}{self.item.data(3)}{move}"
        elif className.find("BezierText") >= 0:
            text = self._tr("MoveCommand", '注释')
            self.data = f"{text}{self.item.data(4)}{move}"

    def redo(self):
        self.item.setPos(self.m_newPos)
        self.data = f"{self.data}x:{self.item.pos().x()},y:{self.item.pos().y()}"
        self.setText(self.data)

    def undo(self):
        self.item.setPos(self.m_oldPos)
        self.data = f"{self.data}x:{self.item.pos().x()},y:{self.item.pos().y()}"
        self.setText(self.data)
