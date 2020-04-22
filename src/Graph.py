from PyQt5.QtCore import QPoint
from src.OperatorFile import OperatorData
from pythonds.graphs import PriorityQueue


class Graph:
    #
    def __init__(self):
        self.vertDict = {}
        self.numVertices = 0

    #  向图中添加一个顶点实例
    def addVertex(self, key, point=QPoint()):
        x, y = point.x(), point.y()
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key, x, y)
        self.vertDict[key] = newVertex
        return newVertex

    #  在图中找到名为vertKey的顶点
    def getVertex(self, n):
        if n in self.vertDict:
            return self.vertDict[n]
        else:
            return None

    #  获取总顶点数
    def getTotalVertex(self):
        return self.numVertices

    def __contains__(self, n):
        return n in self.vertDict

    #  向图中添加一条有向边，用于连接顶点fromVert和toVert
    def addEdge(self, fromVert, toVert, cost=0):

        if fromVert not in self.vertDict:
            nv = self.addVertex(fromVert)

        if toVert not in self.vertDict:
            nv = self.addVertex(toVert)

        self.vertDict[fromVert].addNeighbor(self.vertDict[toVert], cost)

    #  以列表的形式返回途中的所有顶点
    def getVertices(self):
        return self.vertDict.keys()

    #  根据坐标获取顶点名称
    def get_VertexKey(self, point):
        x, y = point.x(), point.y()
        for vertices in self.vertDict.values():
            x2, y2 = vertices.getCoordinates()
            if x2 == x and y2 == y:
                return vertices.getId()
        return False

    #  判断坐标是否存在
    def IsContainsPoint(self, point):
        x, y = point.x(), point.y()
        for vertices in self.vertDict.values():
            x2, y2 = vertices.getCoordinates()
            if x2 == x and y2 == y:
                return True
        return False

    #  根据ID获取坐标
    def getIdToCoordinates(self, id):
        for vertices in self.vertDict.values():
            if id == vertices.getId():
                return vertices.getCoordinates()
        return False

    def __iter__(self):
        return iter(self.vertDict.values())

    def getTotalEdge(self):
        for v in self.vertDict.values():
            for w in v.getConnections():
                print(v.getId(), '->', w.getId())

    #  判断是否有边，有则返回边数
    def IsEmptyEdge(self, edge_num=0):

        for v in self.vertDict.values():
            for w in v.getConnections():
                edge_num = edge_num + 1
        return edge_num

    # 判断边是否存在
    def IsContainsEdge(self, line):
        fromVert, toVert = self.get_VertexKey(line.p1()), self.get_VertexKey(line.p2())
        for v in self.vertDict.values():
            for w in v.getConnections():
                if v.getId() == fromVert and w.getId() == toVert:
                    return True

        for v in self.vertDict.values():
            for w in v.getConnections():
                if v.getId() == toVert and w.getId() == fromVert:
                    return True
        return False

    # 打印所有的边的详细信息
    def PrintDetails(self):
        for vertices in self.vertDict.values():
            for vert in vertices.getConnections():
                print("{ %s-%s -> %s-%s }" % (
                    vertices.getId(), vertices.getCoordinates(), vert.getId(), vert.getCoordinates()))

    #  清空所有数据
    def ClearAllDetails(self):
        self.vertDict = {}
        self.numVertices = 0

    def getStandardData(self):
        standardData = {}
        for vertices in self.vertDict.values():
            listDict = []
            vertices.getCoordinates()
            for vert in vertices.getConnections():
                listDict.append(vert.getId())
            standardData[vertices.getId()] = {vertices.getCoordinates(): listDict}
        return standardData

    def setGraphData(self, standardData):
        vertexToCoordinates = {}
        vertexToConnectionsTo = {}
        for vertices, midData in standardData.items():
            for coordinates, connectionsTo in midData.items():
                vertexToCoordinates[vertices] = coordinates
                vertexToConnectionsTo[vertices] = connectionsTo
        for vertices, coordinates in vertexToCoordinates.items():
            point = QPoint(coordinates[0], coordinates[1])
            self.addVertex(vertices, point)

        for vertices, connectionsTo in vertexToConnectionsTo.items():
            for connection in connectionsTo:
                self.addEdge(vertices, connection)

    def dijkstra(self, aGraph, start):
        pq =PriorityQueue()
        start.setDistence(0)
        pq.buildHeap([])



#  Vertex类表示图中的每一个顶点
class Vertex:
    #  初始化ID，以及字典connectedTo
    def __init__(self, key, x=0, y=0):
        self.id = key
        self.x = x
        self.y = y
        self.connectedTo = {}

    #  添加从一个顶点到另一个顶点的连接， 由connectedTo来表示
    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    # 返回邻接表中所有的顶点
    def __str__(self):
        return str(self.id) + '->' \
               + str([x.id for x in self.connectedTo])

    #  返回当前顶点到以参数传入顶点之间边的权重
    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getCoordinates(self):
        return self.x, self.y

    def getWeight(self, nbr):
        return self.connectedTo[nbr]


if __name__ == '__main__':
    g = Graph()
    #
    # for i in range(6):
    #     g.addVertex(i)
    #
    # g.addEdge(0, 1, 5)
    # g.addEdge(0, 5, 2)
    # g.addEdge(1, 2, 4)
    # g.addEdge(2, 3, 9)
    # g.addEdge(3, 4, 7)
    # g.addEdge(3, 5, 3)
    # g.addEdge(4, 0, 1)
    # g.addEdge(5, 4, 8)
    # g.addEdge(5, 2, 1)

    # # for v in g:
    # #     print(v.getCoordinates())
    #
    # print(g.getStandardData())

    s = OperatorData()
    g.setGraphData(s.open_Graph('sss.graph'))
    g.PrintDetails()
