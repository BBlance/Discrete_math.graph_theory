from PySide2.QtCore import QDataStream, Qt, QIODevice, QDir, QFile, QFileInfo, QCoreApplication
from PySide2.QtWidgets import QFileDialog, QMessageBox, QWidget
from pandas import DataFrame, ExcelWriter, read_excel
from pandas.io.excel import ExcelFile
from numpy import isnan


class OperatorFile(QWidget):
    _tr = QCoreApplication.translate
    dir = QDir()

    def __init__(self, parent=None):
        super().__init__(parent)

    def saveGraphData(self, graphData=None):
        curPath = self.dir.currentPath()
        title = self._tr("OperatorFile", "保存文件")
        filt = self._tr("OperatorFile", "*.xlsx;;*.graph")
        fileName, flt = QFileDialog.getSaveFileName(self, title, curPath, filt)
        if fileName == "":
            return
        if flt.find('xlsx') >= 0:
            fileName = self.saveExcel(fileName, graphData)
        elif flt.find('graph') >= 0:
            self.saveGraph()
        return fileName

    def openGraphData(self):
        curPath = self.dir.currentPath()
        title = self._tr("OperatorFile", "打开文件")
        filt = self._tr("OperatorFile", "*.xlsx;;*.graph")
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
        if fileName == "":
            return
        if flt.find('xlsx') >= 0:
            return self.openExcel(fileName)
        elif flt.find('graph') >= 0:
            self.saveGraph()
        return False

    def outputData(self, graph):
        curPath = self.dir.currentPath()
        nodeColumns = ['顶点ID', '权重']
        edgeColumns = ['边ID', '始点', '终点', '权重']
        title = self._tr("OperatorFile", "导出图数据")
        filt = self._tr("OperatorFile", "*.xlsx")
        fileName, flt = QFileDialog.getSaveFileName(self, title, curPath, filt)
        if fileName == "":
            return
        file_full = QFileInfo(fileName)
        if file_full.exists():
            title = self._tr("OperatorFile", '警告')
            info = self._tr("OperatorFile", '文件即将被覆盖')
            result = QMessageBox.question(self, title, info, QMessageBox.Yes | QMessageBox.Cancel)
        else:
            result = QMessageBox.Yes

        if result == QMessageBox.Yes:
            graphName = file_full.baseName()
            nodeName = "V" + f'({graphName})'
            edgeName = "E" + f'({graphName})'
            dataDict = ["图名称", "顶点集", "边集", "图类型"]
            graphList = [graphName, nodeName, edgeName, graph[0]]
            graphFrame = DataFrame(graphList, index=dataDict)
            graphFrame = graphFrame.T
            nodeFrame = DataFrame(graph[1], columns=nodeColumns)
            edgeFrame = DataFrame(graph[2], columns=edgeColumns)

            try:
                with ExcelWriter(fileName) as writer:
                    graphFrame.to_excel(writer, sheet_name=graphName, index=None)
                    nodeFrame.to_excel(writer, sheet_name=nodeName, index=None)
                    edgeFrame.to_excel(writer, sheet_name=edgeName, index=None)
                writer.save()
                writer.close()
            except Exception as e:
                text = self._tr("OperatorFile", '权限不足')
                QMessageBox.warning(self, text, str(e))
                return False

        elif result == QMessageBox.Cancel:
            return
        return True

    def inputData(self):
        curPath = self.dir.currentPath()
        title = self._tr("OperatorFile", "打开文件")
        filt = self._tr("OperatorFile", "*.xlsx")
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
        if fileName == "":
            return
        graphData = ExcelFile(fileName)
        sheetNames = graphData.sheet_names
        graphFrame = read_excel(fileName, sheetNames[0])
        nodeFrame = read_excel(fileName, sheetNames[1])
        edgeFrame = read_excel(fileName, sheetNames[2])

        mode = int(graphFrame.iloc[0, 3])
        graphName = str(graphFrame.iloc[0, 0])
        nodeDataList = []
        edgeDataList = []


        for i in range(nodeFrame.shape[0]):
            data = []
            for j in range(nodeFrame.shape[1]):
                if not isnan(nodeFrame.iloc[i, j]):
                    data.append(int(nodeFrame.iloc[i, j]))
                else:
                    QMessageBox.warning(self, QCoreApplication.translate("OperatorFile", "警告！"),
                                        QCoreApplication.translate("OperatorFile", "对不起，您的数据有误，系统无法识别！"))
                    return None

            if len(data) >= 2:
                nodeDataList.append(data)
            else:
                QMessageBox.warning(self, QCoreApplication.translate("OperatorFile", "警告！"),
                                    QCoreApplication.translate("OperatorFile", "顶点ID和权重为必须信息，您的信息不完整，请补充信息后，再次尝试。"))
                return None

        for i in range(edgeFrame.shape[0]):
            data = []
            for j in range(edgeFrame.shape[1]):
                if not isnan(edgeFrame.iloc[i, j]):
                    data.append(int(edgeFrame.iloc[i, j]))
            if len(data) >= 2:
                edgeDataList.append(data)

        return [graphName, mode, nodeDataList, edgeDataList]

    def saveExcel(self, fileName, graph: list):
        nodeColumns = ['顶点ID', '权重', 'x坐标', 'y坐标']

        edgeColumns = ['边ID', '始点', '终点', '权重', '1点x坐标', '1点y坐标', '2点x坐标', '2点y坐标', '3点x坐标', '3点y坐标', '4点x坐标',
                       '4点y坐标', '中心点x坐标', '中心点y坐标']
        textColumns = ['文本ID', '文本内容', 'x坐标', 'y坐标']

        file_full = QFileInfo(fileName)
        if file_full.exists():
            title = self._tr("OperatorFile", '警告')
            info = self._tr("OperatorFile", '文件即将被覆盖')
            result = QMessageBox.question(self, title, info, QMessageBox.Yes | QMessageBox.Cancel)
        else:
            result = QMessageBox.Yes

        if result == QMessageBox.Yes:
            graphName = file_full.baseName()
            nodeName = "V" + f'({graphName})'
            edgeName = "E" + f'({graphName})'
            textName = "T" + f'({graphName})'
            dataDict = ["图名称", "顶点集", "边集", "文本集", "图类型"]
            graphList = [graphName, nodeName, edgeName, textName, graph[0]]
            graphFrame = DataFrame(graphList, index=dataDict)
            graphFrame = graphFrame.T
            nodeFrame = DataFrame(graph[1], columns=nodeColumns)
            edgeFrame = DataFrame(graph[2], columns=edgeColumns)
            textFrame = DataFrame(graph[3], columns=textColumns)

            try:
                with ExcelWriter(fileName) as writer:
                    graphFrame.to_excel(writer, sheet_name=graphName, index=None)
                    nodeFrame.to_excel(writer, sheet_name=nodeName, index=None)
                    edgeFrame.to_excel(writer, sheet_name=edgeName, index=None)
                    textFrame.to_excel(writer, sheet_name=textName, index=None)
                writer.save()
                writer.close()
            except Exception as e:
                text = self._tr("OperatorFile", '权限不足')
                QMessageBox.warning(self, text, str(e))
                return

        elif result == QMessageBox.Cancel:
            return
        return file_full

    # def saveGraph(self):
    #
    #     return True
    def openExcel(self, fileName):
        graphData = ExcelFile(fileName)
        sheetNames = graphData.sheet_names
        graphFrame = read_excel(fileName, sheetNames[0])
        nodeFrame = read_excel(fileName, sheetNames[1])
        edgeFrame = read_excel(fileName, sheetNames[2])
        textFrame = read_excel(fileName, sheetNames[3])

        mode = int(graphFrame.iloc[0, 4])
        graphName = str(graphFrame.iloc[0, 0])
        nodeDataList = []
        edgeDataList = []
        textDataList = []

        for i in range(nodeFrame.shape[0]):
            data = []
            for j in range(nodeFrame.shape[1]):
                if not isnan(nodeFrame.iloc[i, j]):
                    data.append(int(nodeFrame.iloc[i, j]))
                else:
                    QMessageBox.warning(self, QCoreApplication.translate("OperatorFile", "警告！"),
                                        QCoreApplication.translate("OperatorFile", "对不起，您的数据有误，系统无法识别！"))
                    return None

            if len(data) >= 2:
                nodeDataList.append(data)

        for i in range(edgeFrame.shape[0]):
            data = []
            for j in range(edgeFrame.shape[1]):
                if not isnan(edgeFrame.iloc[i, j]):
                    data.append(int(edgeFrame.iloc[i, j]))
            if len(data) >= 2:
                edgeDataList.append(data)
        for i in range(textFrame.shape[0]):
            data = []
            for j in range(textFrame.shape[1]):
                if type(textFrame.iloc[i, j]) is not str:
                    data.append(int(textFrame.iloc[i, j]))
                else:
                    data.append(textFrame.iloc[i, j])
            if len(data) >= 2:
                textDataList.append(data)

        return [graphName, mode, nodeDataList, edgeDataList, textDataList]
