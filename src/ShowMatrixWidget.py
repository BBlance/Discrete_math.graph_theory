import sys, os  # codecs

from PySide2.QtWidgets import (QApplication, QWidget, QFileDialog,
                               QToolBar, QVBoxLayout, QFontDialog)

from PySide2.QtCore import QItemSelectionModel, Qt

from PySide2.QtGui import QStandardItemModel, QStandardItem

from ui_ShowMatrix import Ui_ShowMatrix, QAbstractItemView, QHeaderView, QLabel


class ShowMatrixWidget(QWidget):

    def __init__(self, parent=None, graph=None, name=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowOpacity(0.9)
        self.ui = Ui_ShowMatrix()
        self.ui.setupUi(self)
        self.__graph = graph
        data = None
        HorizontalHeaderList = []
        VerticalHeaderList = []
        dataDetailView = self.ui.dataView
        dataDetailView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        if name == "邻接矩阵":
            self.setWindowTitle(name)
            data = self.__graph.adjacentMatrix()
            for node in self.__graph:
                HorizontalHeaderList.append(f'V{node.id()}')
            VerticalHeaderList = HorizontalHeaderList
        elif name == "可达矩阵":
            temp = self.__graph.reachableMatrix()
            data = temp[0]
            step = temp[1]
            for node in self.__graph:
                HorizontalHeaderList.append(f'V{node.id()}')
            VerticalHeaderList = HorizontalHeaderList
            self.setWindowTitle(f'{name},步数：{step}')
            label = QLabel(f"步数{step}")
            self.ui.layout.addWidget(label)

        elif name == "关联矩阵":
            self.setWindowTitle(name)
            VerticalHeaderList.clear()
            HorizontalHeaderList.clear()
            for node in self.__graph:
                VerticalHeaderList.append(f'V{node.id()}')

            for edge in self.__graph.edges():
                print(edge)
                HorizontalHeaderList.append(f'e{edge}')

            data = self.__graph.incidenceMatrix()
            HorizontalHeaderList.reverse()
            VerticalHeaderList.reverse()

        HorizontalHeaderList.reverse()
        colCount = data.shape[1]
        rowCount = data.shape[0]
        data = data.tolist()

        dataModel = QStandardItemModel(rowCount, colCount, self)
        dataSelectionModel = QItemSelectionModel(dataModel)
        dataModel.clear()
        dataModel.setHorizontalHeaderLabels(HorizontalHeaderList)
        dataModel.setVerticalHeaderLabels(VerticalHeaderList)
        dataDetailView.setModel(dataModel)
        dataDetailView.setSelectionModel(dataSelectionModel)
        dataDetailView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        dataDetailView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        dataDetailView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        dataDetailView.setAlternatingRowColors(True)

        for i in range(rowCount):
            strList = []
            for x in data[i]:
                strList.append(f"{x}")
            for j in range(colCount):
                item = QStandardItem(strList[j])
                dataModel.setItem(i, j, item)

        dataModel.setRowCount(rowCount)

        parent.disconnectGraph()
