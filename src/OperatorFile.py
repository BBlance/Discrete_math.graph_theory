from PySide2.QtCore import QDataStream, Qt, QIODevice, QDir, QFile, QFileInfo
from PySide2.QtWidgets import QFileDialog, QMessageBox
from pandas import DataFrame, ExcelWriter, read_excel
from pandas.io.excel import ExcelFile
from numpy import isnan

Dir = QDir()


def saveGraphData(parent=None, graphData=None):
    curPath = Dir.currentPath()
    title = "选择文件"
    filt = "Excel文件(*.xlsx);;图数据文件(*.graph)"
    fileName, flt = QFileDialog.getSaveFileName(parent, title, curPath, filt)
    if fileName == "":
        return
    if flt.find('xlsx') >= 0:
        if not saveExcel(fileName, graphData):
            return
    elif flt.find('graph') >= 0:
        saveGraph()
    return fileName


def openGraphData(parent=None):
    curPath = Dir.currentPath()
    title = "选择文件"
    filt = "Excel文件(*.xlsx);;图数据文件(*.graph)"
    fileName, flt = QFileDialog.getOpenFileName(parent, title, curPath, filt)
    if fileName == "":
        return
    if flt.find('xlsx') >= 0:
        return openExcel(fileName)
    elif flt.find('graph') >= 0:
        saveGraph()

    return False


def saveExcel(fileName, graph: list):
    nodeColumns = ['图形ID', '顶点ID', '权重', 'x坐标', 'y坐标']

    edgeColumns = ['图形ID', '边ID', '始点', '终点', '权重', '1点x坐标', '1点y坐标', '2点x坐标', '2点y坐标', '3点x坐标', '3点y坐标', '4点x坐标',
                   '4点y坐标', '中心点x坐标', '中心点y坐标']
    textColumns = ['图形ID', '文本ID', '文本内容', 'x坐标', 'y坐标']
    if len(graph[1]) > 0:
        maxLength = max([len(node) for node in graph[1]]) - len(nodeColumns)
        for i in range(maxLength):
            nodeColumns = nodeColumns + ['连接顶点ID']

    file_full = QFileInfo(fileName)
    if file_full.exists():
        result = QMessageBox.question(None, "警告", '文件即将被覆盖！', QMessageBox.Yes | QMessageBox.Cancel)
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
            QMessageBox.warning(None, "Permission denied", str(e))

    elif result == QMessageBox.Cancel:
        return
    return True


def saveGraph(parent=None):
    return True


def openExcel(fileName):
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
            if not isnan(textFrame.iloc[i, j]):
                data.append(int(textFrame.iloc[i, j]))
        if len(data) >= 2:
            textDataList.append(data)

    return [graphName, mode, nodeDataList, edgeDataList, textDataList]


def openGraph(parent=None):
    return True
