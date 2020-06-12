import sys

from PySide2.QtWidgets import (QApplication, QWidget, QFileDialog,
                               QToolBar, QVBoxLayout, QFontDialog)

from PySide2.QtCore import QItemSelectionModel, Qt, QRegExp

from PySide2.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator, QCloseEvent

from Graph import Graph
from ui_DataDetails import Ui_DataDetails, QAbstractItemView, QHeaderView, QLabel, QLineEdit, QPushButton, QMessageBox


class ShowDataWidget(QWidget):

    def __init__(self, parent=None, items=None, graph=None, name=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowOpacity(0.9)
        self.ui = Ui_DataDetails()
        self.ui.setupUi(self)
        self.parent = parent
        self.__graph: Graph() = graph
        self.toolWidget = self.ui.toolWidget
        self.layout = self.toolWidget.layout()
        self.items = items
        self.rowCount = 0
        self.columnCount = 0
        self.horizontalHeaderList = []
        self.verticalHeaderList = []

        self.toolWidget.setVisible(False)

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


        # if name == '结点度':
        #     self.nodeDetails()
        #     pass
        # if name == '出度' or name == '入度':
        #     self.nodeDetails(name)
        #     pass
        # elif name == '简单通路':
        #     if not self.easyPath(self.items):

        if name == '复杂通路':
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

    def __iniToolWidget(self):

        self.toolWidget.setVisible(True)
        self.startLabel = QLabel("始点")
        self.endLabel = QLabel("终点")
        self.startNodeEdit = QLineEdit(self)
        self.endNodeEdit = QLineEdit(self)
        self.searchBtn = QPushButton("search", self)

        rx = QRegExp(r'^[A-Z][\d+]{5}$')
        validator1 = QRegExpValidator(rx, self.startNodeEdit)
        validator2 = QRegExpValidator(rx, self.endNodeEdit)

        self.startNodeEdit.setValidator(validator1)
        self.endNodeEdit.setValidator(validator2)

        self.startNodeEdit.setInputMask("A999")
        self.endNodeEdit.setInputMask("A999")

        self.startNodeEdit.setText("V000")
        self.endNodeEdit.setText("V000")

        self.startNodeEdit.setMinimumWidth(40)
        self.endNodeEdit.setMinimumWidth(40)

        self.startNodeEdit.setCursor(Qt.IBeamCursor)
        self.endNodeEdit.setCursor(Qt.IBeamCursor)

        self.searchBtn.clicked.connect(self.do_searchBtn)

        self.layout.addStretch()
        self.layout.addWidget(self.startLabel)
        self.layout.addWidget(self.startNodeEdit)
        self.layout.addStretch()
        self.layout.addWidget(self.endLabel)
        self.layout.addWidget(self.endNodeEdit)
        self.layout.addStretch()
        self.layout.addWidget(self.searchBtn)
        self.layout.addStretch()

    def easyPath(self):
        startNode = self.items[0].data(2)
        endNode = self.items[1].data(2)
        paths = self.__graph.findAllPathWithEdge(startNode, endNode)
        if len(paths) == 0:
            self.dataModel.clear()
            QMessageBox.information(None, "Sorry", "没有符合条件的通路")
            return False
        self.rowCount = len(paths)
        self.dataModel.setRowCount(self.rowCount)
        self.dataModel.setColumnCount(self.columnCount)
        self.dataModel.clear()
        for i in range(self.rowCount):
            for j in range(len(paths[i])):
                if str(type(paths[i][j])).find("Edge") >= 0:
                    item = QStandardItem(f'e{paths[i][j].id()}')
                    self.dataModel.setItem(i, j, item)
                elif str(type(paths[i][j])).find("Vertex") >= 0:
                    item = QStandardItem(f'V{paths[i][j].id()}')
                    self.dataModel.setItem(i, j, item)

        return True

    def do_searchBtn(self):
        start = int(self.startNodeEdit.text().strip('V'))
        end = int(self.endNodeEdit.text().strip('V'))
        paths = self.__graph.findAllPathWithEdge(start, end)
        if len(paths) == 0:
            self.dataModel.clear()
            QMessageBox.information(None, "Sorry", "没有符合条件的通路")
            return
        self.easyPath(paths)

    def closeEvent(self, event: QCloseEvent):
        if self.__graph:
            self.parent.disconnectGraph()

        super().closeEvent(event)


if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = ShowDataWidget()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
