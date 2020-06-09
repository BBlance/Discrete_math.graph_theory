from PySide2.QtWidgets import (QApplication, QWidget, QFileDialog,
                               QToolBar, QVBoxLayout, QFontDialog)

from PySide2.QtCore import QItemSelectionModel, Qt

from PySide2.QtGui import QStandardItemModel, QStandardItem

from ui_DataDetails import Ui_DataDetails, QAbstractItemView, QHeaderView, QLabel


class ShowDataWidget(QWidget):

    def __init__(self, parent=None, items=None, graph=None, name=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowOpacity(0.9)
        self.ui = Ui_DataDetails()
        self.ui.setupUi(self)
        self.parent = parent
        self.__graph = graph
        self.layout = self.ui.verticalLayout
        self.items = items
        self.rowCount = 0
        self.columnCount = 0
        self.horizontalHeaderList = []
        self.verticalHeaderList = []
        self.dataDetailView = self.ui.dataTable
        self.dataDetailView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataModel = QStandardItemModel(self.rowCount, self.columnCount, self)
        self.dataSelectionModel = QItemSelectionModel(self.dataModel)

        self.dataModel.clear()

        self.dataDetailView.setModel(self.dataModel)
        self.dataDetailView.setSelectionModel(self.dataSelectionModel)
        self.dataDetailView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.dataDetailView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dataDetailView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dataDetailView.setAlternatingRowColors(True)
        if name == '边的权重':
            self.edgeDetails()
            pass
        elif name == '结点度':
            self.nodeDetails()
            pass
        elif name == '出度' or name == '入度':
            self.nodeDetails(name)
            pass
        elif name == '简单通路':
            pass
        elif name == '复杂通路':
            pass
        elif name == '最短路径':
            pass
        elif name == '关键路径':
            pass
        elif name == '欧拉回路':
            pass
        elif name == '欧拉通路':
            pass
        elif name == '哈密顿回路':
            pass
        self.setWindowTitle(name)

        if not graph:
            parent.disconnectGraph()

    def edgeDetails(self):
        self.horizontalHeaderList = ['ID', '权重']
        self.rowCount = len(self.items)
        self.columnCount = len(self.horizontalHeaderList)
        self.dataModel.setRowCount(self.rowCount)
        self.dataModel.setColumnCount(self.columnCount)
        self.dataModel.clear()
        self.dataModel.setHorizontalHeaderLabels(self.horizontalHeaderList)
        self.horizontalHeaderList.reverse()
        for i in range(self.rowCount):
            strList = [f'e{self.items[i].data(3)}', f'{self.items[i].weight()}']
            for j in range(self.columnCount):
                item = QStandardItem(strList[j])
                self.dataModel.setItem(i, j, item)

    def nodeDetails(self, mode='度'):
        self.horizontalHeaderList = ['ID']
        if self.parent.ui.actionDigraph_Mode.isChecked():
            if mode == "出度":
                self.horizontalHeaderList.append('出度')
            elif mode == "入度":
                self.horizontalHeaderList.append('入度')
            elif mode == "度":
                self.horizontalHeaderList.append("度")
            self.columnCount += 1
        else:
            self.horizontalHeaderList.append("度")
            self.columnCount += 1
        self.rowCount = len(self.items)
        self.columnCount = len(self.horizontalHeaderList)
        self.dataModel.setRowCount(self.rowCount)
        self.dataModel.setColumnCount(self.columnCount)
        self.dataModel.clear()
        self.dataModel.setHorizontalHeaderLabels(self.horizontalHeaderList)
        self.items.reverse()
        for i in range(self.rowCount):
            strList = [f'V{self.items[i].data(2)}']
            if self.parent.ui.actionDigraph_Mode.isChecked():
                if mode == "出度":
                    strList.append(f'{self.items[i].digraphDegrees(True)[1]}')
                elif mode == "入度":
                    strList.append(f'{self.items[i].digraphDegrees(True)[0]}')
                elif mode == '度':
                    strList.append(f'{self.items[i].digraphDegrees(False)}')
            else:
                strList.append(f'{self.items[i].digraphDegrees(False)}')
            for j in range(self.columnCount):
                item = QStandardItem(strList[j])
                self.dataModel.setItem(i, j, item)
