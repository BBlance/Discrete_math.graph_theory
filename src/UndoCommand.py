from datetime import datetime

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QUndoCommand
from Graph import Graph


class UndoCommand(QUndoCommand):
    def __init__(self, widget):
        super(UndoCommand, self).__init__()

        self.__widget = widget
        self.__graph = widget.getGraph()

        self.__pixmapList = self.__widget.getPixmapList()
        self.__number = len(self.__pixmapList)
        self.setText("步骤")

    def undo(self):
        vert = self.__graph.getNewVertex()
        self.__graph.removeVert(verts)
        if len(self.__pixmapList) >= self.__number:
            if self.__number >= 1:
                self.__number = self.__number - 1
        print(len(self.__pixmapList))
        # self.__widget.saveImage("graph.png", "png")
        self.__widget.setWhiteboard(QPixmap(self.__pixmapList[self.__number-1]))
        self.__widget.update()

    def redo(self):

        vert = self.__graph.getNewVertex()
        x, y = vert.getCoordinates()
        self.setText("node:%d,coordinates:%d,%d" % (vert.getId(), x, y))

        if len(self.__pixmapList) > self.__number:
            self.__number = self.__number + 1
        self.__widget.update()
