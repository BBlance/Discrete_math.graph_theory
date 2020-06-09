from random import random

from PySide2.QtCore import QPointF
from PySide2.QtWidgets import QUndoCommand, QGraphicsScene

from BezierEdge import BezierEdge
from BezierNode import BezierNode
from PointItem import ItemType


class AddCommand(QUndoCommand):
    def __init__(self, scene: QGraphicsScene, item):
        super(AddCommand, self).__init__()

        self.scene = scene
        self.item = item
        className = str(type(item))
        if className.find("BezierNode") >= 0:
            self.setText(f'添加顶点V{self.item.data(2)}')
        elif className.find("BezierEdge") >= 0:
            self.setText(f'添加边e{self.item.data(3)}')
        elif className.find("BezierText") >= 0:
            self.setText(f'添加注释{self.item.data(4)}')

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

        self.scene.removeItem(self.item)  # 删除绘图项


class MoveCommand(QUndoCommand):
    def __init__(self, item, oldPos: QPointF):
        super(MoveCommand, self).__init__()
        self.item = item

        self.m_oldPos = oldPos
        self.m_newPos = self.item.pos()
        self.data=''

        className = str(type(item))
        if className.find("BezierNode") >= 0:

            self.data=f"顶点V{self.item.data(2)}移动到"
        elif className.find("BezierEdge") >= 0:
            self.data = f"边e{self.item.data(3)}移动到"
        elif className.find("BezierText") >= 0:
            self.data = f"注释{self.item.data(4)}移动到"

    def redo(self):
        self.item.setPos(self.m_newPos)
        self.data=f"{self.data}x:{self.item.pos().x()},y:{self.item.pos().y()}"
        self.setText(self.data)

    def undo(self):
        self.item.setPos(self.m_oldPos)
        self.data = f"{self.data}x:{self.item.pos().x()},y:{self.item.pos().y()}"
        self.setText(self.data)
