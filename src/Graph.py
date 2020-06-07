import sys
from PySide2.QtCore import QPoint
from numpy import zeros, identity, mat, array
from pandas import value_counts


class Graph:
    def __init__(self):
        self.__vertDict = {}
        self.__numVertices = 0
        self.__numEdges = 0
        self.__mode = True
        self.__edgeDict = {}
        self.__time = 0

    #  向图中添加一个顶点实例
    def addVertex(self, key, point=QPoint()):
        x, y = point.x(), point.y()
        self.__numVertices = self.__numVertices + 1
        newVertex = Vertex(key, x, y)
        self.__vertDict[key] = newVertex
        return newVertex

    #  在图中找到名为vertKey的顶点
    def vertex(self, n):
        if n in self.__vertDict:
            return self.__vertDict[n]
        else:
            return None

    def edgeNumber(self):
        return self.__numEdges

    def edges(self):
        return self.__edgeDict

    def edge(self, fromVert, toVert):
        edgeList = []
        if type(fromVert) is Vertex:
            fromVert = fromVert.id()
        if type(toVert) is Vertex:
            toVert = toVert.id()
        for edge in self.__edgeDict.values():
            if fromVert == edge.fromVert().id() and toVert == edge.toVert().id():
                edgeList.append(edge)
        return edgeList

    def mode(self):
        return self.__mode

    def setMode(self, mode):
        self.__mode = mode

    def __contains__(self, n):
        return n in self.__vertDict

    #  向图中添加一条有向边，用于连接顶点fromVert和toVert
    def addEdge(self, fromVert, toVert, cost=0):

        if fromVert not in self.__vertDict:
            nv = self.addVertex(fromVert)

        if toVert not in self.__vertDict:
            nv = self.addVertex(toVert)

        if self.__mode:
            self.__vertDict[fromVert].addNeighbor(self.__vertDict[toVert], cost)
            self.__vertDict[fromVert].addEdge(Edge(self.__numEdges, self.__vertDict[fromVert], self.__vertDict[toVert],
                                                   cost, self.__mode), cost)

        else:
            self.__vertDict[fromVert].addNeighbor(self.__vertDict[toVert], cost)
            self.__vertDict[fromVert].addEdge(Edge(self.__numEdges, self.__vertDict[fromVert], self.__vertDict[toVert],
                                                   cost, self.__mode), cost)
            if fromVert != toVert:
                self.__vertDict[toVert].addNeighbor(self.__vertDict[fromVert], cost)
                self.__vertDict[toVert].addEdge(
                    Edge(self.__numEdges, self.__vertDict[toVert], self.__vertDict[fromVert],
                         cost, self.__mode), cost)
        newEdge = Edge(self.__numEdges, self.__vertDict[fromVert], self.__vertDict[toVert],
                       cost, self.__mode)
        self.__edgeDict[self.__numEdges] = newEdge
        self.__numEdges = self.__numEdges + 1

        return newEdge

    #  以列表的形式返回途中的所有顶点
    def vertices(self):
        return self.__vertDict.keys()

    #  根据坐标获取顶点名称
    def vertexKey(self, point):
        x, y = point.__x(), point.__y()
        for vertices in self.__vertDict.values():
            x2, y2 = vertices.coordinates()
            if x2 == x and y2 == y:
                return vertices.__id()
        return False

    #  判断坐标是否存在
    def IsContainsPoint(self, point):
        x, y = point.__x(), point.__y()
        for vertices in self.__vertDict.values():
            x2, y2 = vertices.coordinates()
            if x2 == x and y2 == y:
                return True
        return False

    #  根据ID获取坐标
    def idToCoordinates(self, id):
        for vertices in self.__vertDict.values():
            if id == vertices.__id():
                return vertices.coordinates()
        return False

    def __iter__(self):
        return iter(self.__vertDict.values())

    #  清空所有数据
    def clearAllDetails(self):
        self.__vertDict = {}
        self.__edgeDict = {}
        self.__numEdges = 0
        self.__numVertices = 0

    # 关联矩阵函数
    def incidenceMatrix(self):
        matrix = zeros((self.__numVertices, self.__numEdges))
        if self.__mode:
            for item in self.__vertDict.values():
                item: Vertex
                for num, edge in self.__edgeDict.items():
                    if item.id() == edge[0].id():
                        matrix[item.id()][num] = 1
                    if item.id() == edge[1].id():
                        matrix[item.id()][num] = -1
        else:
            for item in self.__vertDict.values():
                item: Vertex
                for num, edge in self.__edgeDict.items():
                    if item.id() == edge[0].id() or item.id() == edge[1].id():
                        if item.id() == edge[0].id() and item.id() == edge[1].id():
                            matrix[item.id()][num] = 2
                        else:
                            if item.id() == edge[0].id() or item.id() == edge[1].id():
                                matrix[item.id()][num] = 1
        return mat(matrix)

    # 邻接矩阵
    def adjacentMatrix(self):
        matrix = zeros((len(self.__vertDict), len(self.__vertDict)))

        for item in self.__vertDict.values():
            item: Vertex
            num = value_counts(item.vertConnections())
            for x in num.index:
                matrix[item.id()][x.id()] = num[x]
        return mat(matrix)

    #  可达矩阵
    def reachableMatrix(self):
        AMatrix = self.adjacentMatrix()
        IMatrix = identity(len(AMatrix))
        newMatrix = AMatrix + IMatrix
        oldMatrix = newMatrix
        flag = 0
        step = 1
        while flag == 0:
            oldMatrix = newMatrix
            newMatrix = oldMatrix * (AMatrix + IMatrix)
            for i in range(0, len(newMatrix)):
                for j in range(0, len(newMatrix)):
                    if newMatrix[i, j] >= 1:
                        newMatrix[i, j] = 1
            step += 1
            if (oldMatrix == newMatrix).all():
                flag = 1

        return newMatrix, step

    #  连通性判断
    def connectivity(self):

        pass

    #  图的度的计算
    def degrees(self):
        degreesDict = {}
        inDegreeDict = {}
        outDegreeDict = {}
        matrix = array(self.incidenceMatrix())
        for x in range(self.__numVertices):
            value = value_counts(matrix[x]).drop(0)
            if self.__mode:
                if -1 in value.index:
                    inDegreeDict[x] = value[-1]
                else:
                    inDegreeDict[x] = 0

                if 1 in value.index:
                    outDegreeDict[x] = value[1]
                else:
                    outDegreeDict[x] = 0

            else:
                if 1 in value.index:
                    degreesDict[x] = value[1]
                else:
                    degreesDict[x] = 0

        if self.__mode:
            return outDegreeDict, inDegreeDict
        else:
            return degreesDict

    def pathAndLoop(self, step):
        martix = self.adjacentMatrix()
        return pow(martix, step)

    def findPath(self, start, end, pathway=[]):
        pathway = pathway + [self.__vertDict[start]]
        if start == end:
            return pathway
        for node in self.__vertDict[start].vertConnections():
            if node not in pathway:
                edges = self.edge(pathway[len(pathway) - 1].id(), node.id())
                pathway.append(edges[0])
                newPath = self.findPath(node.id(), end, pathway)
                if newPath:
                    return newPath
        return None

    def findAllPathWithoutEdge(self, start, end, pathway=[]):  # 只有结点
        pathway = pathway + [self.__vertDict[start]]

        if start == end:
            return [pathway]
        pathways = []
        for node in self.__vertDict[start].vertConnections():
            if node not in pathway:

                newPaths = self.findAllPathWithoutEdge(node.id(), end, pathway)
                for newPath in newPaths:
                    pathways.append(newPath)
        return pathways

    def findPathWay(self, start, end, pathway=[]):
        pathway = pathway + [self.__vertDict[start]]
        if start == end:
            return [pathway]
        pathways = []
        for edge in self.__vertDict[start].edgeConnections():

            if edge not in pathway:
                if edge.toVert() not in pathway:
                    pathway = pathway + [edge]
                    newPaths = self.findPathWay(edge.toVert().id(), end, pathway)
                    for newPath in newPaths:
                        pathways.append(newPath)
        return pathways

    # def pathway(self, start, end):
    #     if start == end:
    #         return []
    #     pathway=[self.__vertDict[start]]
    #     for edge in self.__vertDict[start].edgeConnections():
    #         if edge.toVert() not in pathway:
    #             if

    def findAllPathWithEdge(self, start, end, pathway=[]):
        pathways = self.findPathWay(start, end, pathway)
        for pathway in pathways:
            for y in range(len(pathway)):
                if y>=len(pathway):
                    break
                if type(pathway[y]) is Edge:
                    z = y
                    while type(pathway[z]) is Edge:
                        z = z + 1
                    if len(pathway[y:z]) != 1:
                        del pathway[y:z-1]

        return pathways

    # def isEulerGraph(self):

#  Vertex类表示图中的每一个顶点
class Vertex:
    #  初始化ID，以及字典connectedTo
    def __init__(self, key, weight=0, x=0, y=0):
        self.__id = key
        self.__weight = weight
        self.__x = x
        self.__y = y
        self.__connectedTo = []
        self.__edges = {}
        self.__color = 'white'
        self.__dist = sys.maxsize
        self.__disc = 0
        self.__fin = 0
        self.__predecessor = None

    #  添加从一个顶点到另一个顶点的连接， 由connectedTo来表示
    def addNeighbor(self, nbr, weight=0):
        self.__connectedTo.append((nbr, weight))

    def addEdge(self, edge, weight):
        self.__edges[edge] = weight

    # 返回邻接表中所有的顶点
    def __str__(self):
        return "v" + str(self.__id) + ':(vertConnectedTo:' + str(
            ["v" + str(x.__id) for x in self.vertConnections()]) + ' (edgeConnectedTo:' + str(
            ["e" + str(x.id()) for x in self.edgeConnections()]) + " color:" + self.__color + " disc: " + str(
            self.__disc) + " fin:" + str(
            self.__fin) + " dist:" + str(self.__dist) + ") pred:[" + str(self.__predecessor) + "]"

    def setColor(self, color):
        self.__color = color

    def setDistance(self, distance):
        self.__dist = distance

    def setPred(self, pred):
        self.__predecessor = pred

    def setDiscovery(self, dtime):
        self.__disc = dtime

    def setFinish(self, ftime):
        self.__fin = ftime

    def finish(self):
        return self.__fin

    def discovery(self):
        return self.__disc

    def distance(self):
        return self.__dist

    def pred(self):
        return self.__predecessor

    def color(self):
        return self.__color

    def vertConnections(self):
        vertList = []
        for connections in self.__connectedTo:
            vertList.append(connections[0])
        return vertList

    def edgeConnections(self):
        return self.__edges.keys()

    def id(self):
        return self.__id

    def coordinates(self):
        return self.__x, self.__y

    def weight(self, nbr):
        for connection in self.__connectedTo:
            connection: tuple
            print(connection)
            if connection[0] == nbr:
                return connection[1]
        return None

    def vertexWeight(self):
        return self.__weight


# Edge类表示图中的每一条边
class Edge:
    def __init__(self, id, fromVert, toVert, weight, mode=True):
        self.__id = id
        self.__fromVert = fromVert
        self.__toVert = toVert
        self.__edge = (fromVert, toVert)
        self.__weight = weight
        self.__mode = mode

    def __str__(self):
        x = " -> " if self.__mode else " - "
        return "e" + str(self.__id) + ":" + "v" + str(self.__fromVert.id()) + x + "v" + str(
            self.__toVert.id()) + "\tweight:" + str(self.__weight)

    def __contains__(self, item):
        return item in self.__edge

    def id(self):
        return self.__id

    def weight(self):
        return self.__weight

    def edge(self):
        return self.__edge

    def fromVert(self):
        return self.__fromVert

    def toVert(self):
        return self.__toVert


if __name__ == '__main__':
    g = Graph()

    for i in range(4):
        g.addVertex(i)

    # g.addEdge(0, 1, 5)
    # g.addEdge(0, 5, 2)
    # g.addEdge(1, 2, 4)
    # g.addEdge(2, 3, 9)
    # g.addEdge(3, 4, 7)
    # g.addEdge(3, 5, 3)
    # g.addEdge(4, 0, 1)
    # g.addEdge(5, 4, 8)
    # g.addEdge(5, 2, 1)

    # g.addEdge(0, 1, 2)
    # g.addEdge(3, 0, 0)
    # g.addEdge(1, 3, 0)
    # g.addEdge(3, 1, 0)
    # g.addEdge(1, 2, 0)

    g.addEdge(0, 0, 5)
    g.addEdge(0, 1, 1)
    g.addEdge(0, 1, 3)
    g.addEdge(0, 2, 2)
    g.addEdge(1, 2, 8)
    g.addEdge(2, 3, 7)
    g.addEdge(3, 2, 6)

    # paths = g.findAllPath(0, 2)
    # for path in paths:
    #     for vert in path:
    #         print(vert.id(), end="\t")
    #     print()
    paths = g.findAllPathWithEdge(0, 2)
    # path = value_counts(paths)
    #
    # print(path.index[0])

    for path in paths:
        for vert in path:
            if type(vert) is Edge:
                print("e" + str(vert.id()), end="\t")
            elif type(vert) is Vertex:
                print("v" + str(vert.id()), end="\t")

        print()
    print()

    # edges = g.edge(0, 5)
    # for x in edges:
    #     print(x.id(), x.weight())

    # for vert in g:
    #     print(vert)
