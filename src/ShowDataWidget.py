from PySide2.QtWidgets import QWidget

from PySide2.QtCore import QItemSelectionModel, Qt, QRegExp, QEvent, QModelIndex, Signal, QCoreApplication

from PySide2.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator, QCloseEvent

from BezierNode import BezierNode
from Graph import Graph
from GraphicsScene import GraphicsScene
from ui_DataDetails import Ui_DataDetails, QAbstractItemView, QHeaderView, QLabel, QLineEdit, QPushButton, QMessageBox


class ShowDataWidget(QWidget):
    pathSignal = Signal(list)
    _tr = QCoreApplication.translate

    def __init__(self, parent=None, items=None, graph=None, name=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowOpacity(0.9)
        self.ui = Ui_DataDetails()
        self.ui.setupUi(self)
        self.parent = parent
        self.scene: GraphicsScene = self.parent.scene()
        self.__graph: Graph = graph
        self.toolWidget = self.ui.toolWidget
        self.path = []

        self.layout = self.toolWidget.layout()
        self.items = items
        self.rowCount = 0
        self.columnCount = 0
        self.horizontalHeaderList = []
        self.verticalHeaderList = []

        source = self._tr("BezierShowDataWidget", '始点')
        dest = self._tr("BezierShowDataWidget", '终点')
        self.startLabel = QLabel(source)
        self.endLabel = QLabel(dest)

        self.startNodeEdit = QLineEdit(self)
        self.endNodeEdit = QLineEdit(self)
        btnStr = self._tr("BezierShowDataWidget", '搜索')
        self.searchBtn = QPushButton(btnStr, self)
        self.searchBtn.setVisible(False)
        self.startNodeEdit.setVisible(False)
        self.endNodeEdit.setVisible(False)

        self.scene.itemNode.connect(self.do_updateNode)

        self.toolWidget.setVisible(False)

        self.dataDetailView = self.ui.dataTable
        self.dataDetailView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dataDetailView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataModel = QStandardItemModel(self.rowCount, self.columnCount, self)

        self.dataSelectionModel = QItemSelectionModel(self.dataModel)
        self.dataSelectionModel.currentChanged.connect(self.do_emitPathList)
        self.dataModel.clear()

        self.dataDetailView.setModel(self.dataModel)
        self.dataDetailView.setSelectionModel(self.dataSelectionModel)
        self.dataDetailView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.dataDetailView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dataDetailView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dataDetailView.setAlternatingRowColors(True)
        self.setWindowTitle(name)

    def updateToolWidget(self, mode=0, path=0):
        self.searchBtn.setVisible(True)
        self.startNodeEdit.setVisible(True)
        self.endNodeEdit.setVisible(True)
        rx = QRegExp(r'^[A-Z][\d+]{5}$')
        validator1 = QRegExpValidator(rx, self.startNodeEdit)
        validator2 = QRegExpValidator(rx, self.endNodeEdit)
        if mode == 1:
            self.endLabel.setVisible(False)
            self.endNodeEdit.setVisible(False)
            self.startNodeEdit.setValidator(validator1)
            self.startNodeEdit.setInputMask("A99")
            self.startNodeEdit.setMinimumWidth(40)
            self.startNodeEdit.setCursor(Qt.IBeamCursor)
            if path == 0:
                self.searchBtn.clicked.connect(self.do_searchBtnEasyLoop)
            elif path == 1:
                self.searchBtn.clicked.connect(self.do_searchBtnPrimaryLoop)
            elif path == 2:
                self.searchBtn.clicked.connect(self.do_searchBtnShortestPath)
        else:

            self.startNodeEdit.setValidator(validator1)
            self.endNodeEdit.setValidator(validator2)

            self.startNodeEdit.setInputMask("A99")
            self.endNodeEdit.setInputMask("A99")

            self.startNodeEdit.setMinimumWidth(40)
            self.endNodeEdit.setMinimumWidth(40)

            self.startNodeEdit.setCursor(Qt.IBeamCursor)
            self.endNodeEdit.setCursor(Qt.IBeamCursor)
            if path == 0:
                self.searchBtn.clicked.connect(self.do_searchBtnEasyPath)
            elif path == 1:
                self.searchBtn.clicked.connect(self.do_searchBtnPrimaryPath)

        self.toolWidget.setVisible(True)

        self.layout.addStretch()
        self.layout.addWidget(self.startLabel)
        self.layout.addWidget(self.startNodeEdit)
        self.layout.addStretch()
        self.layout.addWidget(self.endLabel)
        self.layout.addWidget(self.endNodeEdit)
        self.layout.addStretch()
        self.layout.addWidget(self.searchBtn)
        self.layout.addStretch()

    @classmethod
    def iniStartEnd(cls, nodeList):
        if nodeList[0][1] < nodeList[1][1]:
            start = nodeList[0][0].data(2)
            end = nodeList[1][0].data(2)
            return start, end
        else:
            start = nodeList[1][0].data(2)
            end = nodeList[0][0].data(2)
            return start, end

    def easyPath(self):

        if not self.startNodeEdit.text():
            startNode = self.iniStartEnd(self.items)[0]
        else:
            startNode = int(self.startNodeEdit.text().strip('V'))
        if not self.endNodeEdit.text():
            endNode = self.iniStartEnd(self.items)[1]
        else:
            endNode = int(self.endNodeEdit.text().strip('V'))
        paths = self.__graph.findSimplePathway(startNode, endNode)
        if len(paths) == 0:
            self.dataModel.clear()
            QMessageBox.information(None, "Sorry", self._tr("BezierShowDataWidget", "没有符合条件的通路"))
            return False
        self.rowCount = len(paths)
        self.dataModel.setRowCount(self.rowCount)
        self.dataModel.setColumnCount(self.columnCount)
        self.dataModel.clear()
        for i in range(self.rowCount):
            for j in range(len(paths[i])):
                if str(type(paths[i][j])).find("Edge") >= 0:
                    item = QStandardItem(f'e{paths[i][j].id()}')
                    item.setFlags(Qt.NoItemFlags)
                    self.dataModel.setItem(i, j, item)
                elif str(type(paths[i][j])).find("Vertex") >= 0:
                    item = QStandardItem(f'V{paths[i][j].id()}')
                    item.setFlags(Qt.NoItemFlags)
                    self.dataModel.setItem(i, j, item)

        return True

    def primaryPath(self):
        if not self.startNodeEdit.text():
            startNode = self.iniStartEnd(self.items)[0]
        else:
            startNode = int(self.startNodeEdit.text().strip('V'))
        if not self.endNodeEdit.text():
            endNode = self.iniStartEnd(self.items)[1]
        else:
            endNode = int(self.endNodeEdit.text().strip('V'))
        paths = self.__graph.findPrimaryPathway(startNode, endNode)
        if len(paths) == 0:
            self.dataModel.clear()
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "没有符合条件的通路"))
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
                    item.setFlags(Qt.NoItemFlags)
                elif str(type(paths[i][j])).find("Vertex") >= 0:
                    item = QStandardItem(f'V{paths[i][j].id()}')
                    item.setFlags(Qt.NoItemFlags)
                    self.dataModel.setItem(i, j, item)

        return True

    def easyLoop(self):
        if not self.startNodeEdit.text():
            startNode = self.items[0][0].data(2)
        else:
            startNode = int(self.startNodeEdit.text().strip('V'))
        paths = self.__graph.findSimpleLoop(startNode)
        if len(paths) == 0:
            self.dataModel.clear()
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "没有符合条件的回路"))
            return False
        self.rowCount = len(paths)
        self.dataModel.setRowCount(self.rowCount)
        self.dataModel.setColumnCount(self.columnCount)
        self.dataModel.clear()
        for i in range(self.rowCount):
            for j in range(len(paths[i])):
                if str(type(paths[i][j])).find("Edge") >= 0:
                    item = QStandardItem(f'e{paths[i][j].id()}')
                    item.setFlags(Qt.NoItemFlags)
                    self.dataModel.setItem(i, j, item)
                elif str(type(paths[i][j])).find("Vertex") >= 0:
                    item = QStandardItem(f'V{paths[i][j].id()}')
                    item.setFlags(Qt.NoItemFlags)
                    self.dataModel.setItem(i, j, item)

        return True

    def primaryLoop(self):
        if not self.startNodeEdit.text():
            startNode = self.items[0][0].data(2)
        else:
            startNode = int(self.startNodeEdit.text().strip('V'))
        paths = self.__graph.findPrimaryLoop(startNode)
        if len(paths) == 0:
            self.dataModel.clear()
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "没有符合条件的回路"))
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
                    item.setFlags(Qt.NoItemFlags)
                elif str(type(paths[i][j])).find("Vertex") >= 0:
                    item = QStandardItem(f'V{paths[i][j].id()}')
                    item.setFlags(Qt.NoItemFlags)
                    self.dataModel.setItem(i, j, item)

        return True

    def multipleOrSimple(self):
        edges = self.items
        self.rowCount = len(edges)
        self.dataModel.setRowCount(self.rowCount)
        self.dataModel.setColumnCount(self.columnCount)
        self.dataModel.clear()
        for i in range(self.rowCount):
            for j in range(1):
                item = QStandardItem(f'e{edges[i]}')
                self.dataModel.setItem(i, j, item)
                item.setFlags(Qt.NoItemFlags)

    def shortestPath(self):
        if not self.startNodeEdit.text():
            startNode = self.items[0][0].data(2)
        else:
            startNode = int(self.startNodeEdit.text().strip('V'))
        paths = []
        for node in self.scene.singleItems(BezierNode):
            path = self.__graph.shortestPath(startNode, node.data(2))
            if path is not None and len(path) > 2 and path not in paths:
                paths.append(path)
        if len(paths) == 0:
            self.dataModel.clear()
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "没有符合条件的路径"))
            return False
        self.rowCount = len(paths)
        self.dataModel.setRowCount(self.rowCount)
        self.dataModel.setColumnCount(self.columnCount)
        self.dataModel.clear()
        for i in range(self.rowCount):
            for j in range(len(paths[i])):
                if str(type(paths[i][j])).find("Edge") >= 0:
                    item = QStandardItem(f'e{paths[i][j].id()}')
                    item.setFlags(Qt.NoItemFlags)
                    self.dataModel.setItem(i, j, item)
                elif str(type(paths[i][j])).find("Vertex") >= 0:
                    item = QStandardItem(f'V{paths[i][j].id()}')
                    item.setFlags(Qt.NoItemFlags)
                    self.dataModel.setItem(i, j, item)

        return True

    def closeEvent(self, event: QCloseEvent):
        if self.__graph:
            self.parent.disconnectGraph()
        super().closeEvent(event)

    def leaveEvent(self, event: QEvent):
        self.parent.disconnectGraph()

    def enterEvent(self, event: QEvent):
        self.parent.disconnectGraph()
        self.parent.connectGraph()
        self.__graph = self.parent.graph()

    def do_searchBtnEasyPath(self):
        start = int(self.startNodeEdit.text().strip('V'))
        end = int(self.endNodeEdit.text().strip('V'))
        if start > self.__graph.nodeNumber() or end > self.__graph.nodeNumber():
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "超出上限"))
            return
        self.easyPath()

    def do_searchBtnPrimaryPath(self):
        start = int(self.startNodeEdit.text().strip('V'))
        if start > self.__graph.nodeNumber() - 1:
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "超出上限"))
            return
        self.primaryPath()

    def do_searchBtnEasyLoop(self):
        start = int(self.startNodeEdit.text().strip('V'))
        if start > self.__graph.nodeNumber() - 1:
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "超出上限"))
            return
        self.easyLoop()

    def do_searchBtnPrimaryLoop(self):
        start = int(self.startNodeEdit.text().strip('V'))
        if start > self.__graph.nodeNumber() - 1:
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "超出上限"))
            return
        self.easyLoop()

    def do_searchBtnShortestPath(self):
        start = int(self.startNodeEdit.text().strip('V'))
        if start > self.__graph.nodeNumber() - 1:
            QMessageBox.information(None, self._tr("BezierShowDataWidget", "对不起"),
                                    self._tr("BezierShowDataWidget", "超出上限"))
            return
        self.shortestPath()

    def do_updateNode(self, nodeList):
        if len(nodeList) == 1:
            start = nodeList[0][0].data(2)
            self.startNodeEdit.setText(f'V{start}')
        elif len(nodeList) == 2:
            if nodeList[0][1] < nodeList[1][1]:
                start = nodeList[0][0].data(2)
                end = nodeList[1][0].data(2)
                self.startNodeEdit.setText(f'V{start}')
                self.endNodeEdit.setText(f'V{end}')
                self.startNodeEdit.setText(f'V{start}')
                self.endNodeEdit.setText(f'V{end}')


            else:
                start = nodeList[1][0].data(2)
                end = nodeList[0][0].data(2)
                self.startNodeEdit.setText(f'{start}')
                self.endNodeEdit.setText(f'{end}')
                self.startNodeEdit.setText(f'{start}')
                self.endNodeEdit.setText(f'{end}')

    def do_emitPathList(self, current, previous):
        if current is not None:
            self.path.clear()
            item = self.dataModel.index(current.row(), current.column(), QModelIndex())
            for i in range(self.dataModel.columnCount()):
                item = self.dataModel.index(current.row(), i, QModelIndex())
                if item:
                    self.path.append(item.data())

            self.pathSignal.emit(self.path)
