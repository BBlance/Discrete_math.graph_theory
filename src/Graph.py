import sys
from PySide2.QtCore import QPoint
from numpy import zeros, identity, mat, array
from pandas import value_counts

from pythonds.graphs import PriorityQueue


class Graph:
    def __init__(self):
        self.__vertDict = {}
        self.__numVertices = 0
        self.__numEdge = 0
        self.__mode = True
        self.__edgeDict = {}
        self.__time = 0

    #  向图中添加一个顶点实例
    def addVertex(self, key, point=QPoint()):
        x, y = point.x(), point.y()
        self.__numVertices = self.__numVertices + 1
        newVertex = Vertex(key)
        self.__vertDict[key] = newVertex
        return newVertex

    #  在图中找到名为vertKey的顶点
    def vertex(self, n):
        if n in self.__vertDict:
            return self.__vertDict[n]
        else:
            return None

    def edgeNumber(self):
        return self.__numEdge

    def edges(self):
        return self.__edgeDict.values()

    def edge(self, fromVert, toVert):
        edgeList = []
        if type(fromVert) is Vertex:
            fromVert = fromVert.id()
        if type(toVert) is Vertex:
            toVert = toVert.id()
        for edge in self.__edgeDict.values():
            if self.__mode:
                if fromVert == edge.fromVert().id() and toVert == edge.toVert().id():
                    edgeList.append(edge)
            else:
                if (fromVert == edge.fromVert().id() and toVert == edge.toVert().id()) or (
                        fromVert == edge.toVert().id() and toVert == edge.fromVert().id()):
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
            self.__vertDict[fromVert].addEdge(Edge(self.__numEdge, self.__vertDict[fromVert], self.__vertDict[toVert],
                                                   cost, self.__mode), cost)

        else:
            self.__vertDict[fromVert].addNeighbor(self.__vertDict[toVert], cost)
            self.__vertDict[fromVert].addEdge(Edge(self.__numEdge, self.__vertDict[fromVert], self.__vertDict[toVert],
                                                   cost, self.__mode), cost)
            if fromVert != toVert:
                self.__vertDict[toVert].addNeighbor(self.__vertDict[fromVert], cost)
                self.__vertDict[toVert].addEdge(
                    Edge(self.__numEdge, self.__vertDict[toVert], self.__vertDict[fromVert],
                         cost, self.__mode), cost)
        newEdge = Edge(self.__numEdge, self.__vertDict[fromVert], self.__vertDict[toVert],
                       cost, self.__mode)
        self.__edgeDict[self.__numEdge] = newEdge
        self.__numEdge = self.__numEdge + 1

        return newEdge

    #  以列表的形式返回途中的所有顶点
    def vertices(self):
        return self.__vertDict.values()

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
    def clearAllData(self):
        self.__vertDict = {}
        self.__edgeDict = {}
        self.__numEdge = 0
        self.__numVertices = 0

    # 有向图转无向图
    def diToUndigraph(self):
        graph = Graph()
        graph.setMode(False)
        for edge in self.__edgeDict.values():
            graph.addEdge(edge.fromVert().id(), edge.toVert().id(), edge.weight())
        return graph

    # 关联矩阵函数
    def incidenceMatrix(self):
        matrix = zeros((self.__numVertices, self.__numEdge))
        if self.__mode:
            for item in self.__vertDict.values():
                item: Vertex
                for num, edge in self.__edgeDict.items():
                    if item.id() == edge.fromVert().id():
                        matrix[item.id()][num] = 1
                    if item.id() == edge.toVert().id():
                        matrix[item.id()][num] = -1
        else:
            for item in self.__vertDict.values():
                item: Vertex
                for num, edge in self.__edgeDict.items():
                    if item.id() == edge.fromVert().id() or item.id() == edge.toVert().id():
                        if item.id() == edge.fromVert().id() and item.id() == edge.toVert().id():
                            matrix[item.id()][num] = 2
                        else:
                            if item.id() == edge.fromVert().id() or item.id() == edge.toVert().id():
                                matrix[item.id()][num] = 1
        return mat(matrix)

    # 邻接矩阵
    def adjacentMatrixWithEdges(self):
        matrix = zeros((len(self.__vertDict), len(self.__vertDict)))

        for item in self.__vertDict.values():
            item: Vertex
            num = value_counts(item.vertConnections())
            for x in num.index:
                matrix[item.id()][x.id()] = num[x]
        return mat(matrix)

    def adjacentMatrixWithWeight(self):
        matrix = zeros((len(self.__vertDict), len(self.__vertDict)))
        for item in self.__vertDict.values():
            item: Vertex
            num = value_counts(item.vertConnections())
            for x in num.index:
                matrix[item.id()][x.id()] = num[x]
        return mat(matrix)

    #  可达矩阵
    def reachableMatrix(self):
        AMatrix = self.adjacentMatrixWithEdges()
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

    # 简单图与多重图的判定
    # 若为简单图则返回FALSE，多重图则返回平行边
    def multipleOrSimple(self):
        edges = list(self.__edgeDict.values())
        parallelSides = []

        for x in range(len(edges)):
            for y in range(x + 1, len(edges)):
                if self.__mode:
                    if (edges[x].fromVert() == edges[y].fromVert()) and (edges[x].toVert() == edges[y].toVert()):
                        if edges[x] not in parallelSides:
                            parallelSides.append(edges[x])
                        if edges[y] not in parallelSides:
                            parallelSides.append(edges[y])
                else:
                    if ((edges[x].fromVert() == edges[y].fromVert()) and (edges[x].toVert() == edges[y].toVert())) or (
                            (edges[x].fromVert() == edges[y].toVert()) and (edges[x].toVert() == edges[y].fromVert())):
                        if edges[x] not in parallelSides:
                            parallelSides.append(edges[x])
                        if edges[y] not in parallelSides:
                            parallelSides.append(edges[y])
        if not len(parallelSides):
            for edge in edges:
                if edge.fromVert() == edge.toVert():
                    return False
        return parallelSides

    # 完全图判定
    def completeGraph(self):
        if self.multipleOrSimple():
            return False
        for fromVert in self.__vertDict.values():
            if len(fromVert.vertConnections()) != len(self.__vertDict.values()) - 1:
                return False
            x = set(fromVert.vertConnections())
            y = set(self.__vertDict.values())

            if fromVert not in y - x and len(y - x) != 1:
                return False

        return self.__numVertices

    #  子母图判定
    #  返回0为无关系，1, self为子图，2, self为母图,None则为两图类型不同无法比较
    def sub_motGraph(self, graph) -> [int, str]:
        graph: Graph
        if graph.mode() != self.__mode:
            return "Error:两图类型不同无法比较"
        vertices = {x.id() for x in self.__vertDict.values()}
        edges1 = {(x.fromVert().id(), x.toVert().id()) for x in self.__edgeDict.values()}
        verts = {x.id() for x in graph.vertices()}
        edges2 = {(x.fromVert().id(), x.toVert().id()) for x in graph.edges()}

        if graph == self or ((vertices.union(verts) == verts) and (edges1.union(edges2) == edges2)):
            return 1
        elif (vertices.union(verts) == vertices) and (edges1.union(edges2) == edges1):
            return 2
        return 0

    # 补图判定
    # True 则互为补图 FALSE则不是
    def supplementGraph(self, graph) -> [bool, str]:
        graph: Graph
        if graph.mode() != self.__mode:
            return "Error:两图类型不同无法比较"
        if graph.multipleOrSimple():
            return False
        if self.multipleOrSimple():
            return False
        vertices = {x.id() for x in self.__vertDict.values()}
        edges1 = {(x.fromVert().id(), x.toVert().id()) for x in self.__edgeDict.values()}
        verts = {x.id() for x in graph.vertices()}
        edges2 = {(x.fromVert().id(), x.toVert().id()) for x in graph.edges()}

        intersect = edges1.intersection(edges2)
        if verts == vertices:

            if intersect == set():
                return True

        return False

    # 连通性判断
    # True为连通图，False为非连通图,1为单向连通，2为强连通
    def connectivity(self) -> [bool, int]:
        if len(self.__edgeDict) == 0 and len(self.__vertDict) == 1:
            return True
        graph = None
        vertices = None
        if self.__mode:
            graph = self.diToUndigraph()
            vertices = list(graph.vertices())
        else:
            graph = self
            vertices = self.__vertDict
        # 判断是否为连通图
        for x in range(len(vertices)):
            for y in range(x + 1, len(vertices)):
                if not len(graph.findSimplePathway(vertices[x].id(), vertices[y].id())):
                    return False
        if self.__mode:
            for x in range(len(self.__vertDict)):
                for y in range(x + 1, len(self.__vertDict)):
                    if len(self.findSimplePathway(self.__vertDict[x].id(), self.__vertDict[y].id())):
                        if not len(self.findSimplePathway(self.__vertDict[y].id(), self.__vertDict[x].id())):
                            break
                    else:
                        return True
                else:
                    continue
                return 1
            else:
                return 2
        return True

    #  图的度的计算
    def degrees(self):
        degreesDict = {}
        inDegreeDict = {}
        outDegreeDict = {}
        matrix = array(self.incidenceMatrix())
        for x in range(self.__numVertices):
            value = value_counts(matrix[x])
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
        martix = self.adjacentMatrixWithEdges()
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

    # 简单通路
    def findSimplePathway(self, start, end, pathway=[]):
        if type(start) is Edge:
            pathway = pathway + [start]
            start = start.toVert().id()
        pathway = pathway + [self.__vertDict[start]]

        pathways = []
        if len(pathway) > 1:
            if start == end:
                pathways.append(pathway)
        for edge in self.__vertDict[start].edgeConnections():
            if edge not in pathway:
                newPaths = self.findSimplePathway(edge, end, pathway)
                for newPath in newPaths:
                    pathways.append(newPath)
        return pathways

    # 简单回路
    def findSimpleLoop(self, start, pathway=[]):
        pathways = self.findSimplePathway(start, start, pathway)
        return pathways

    # 初级通路
    def findPrimaryPathway(self, start, end, pathway=[]):
        pathways = self.findSimplePathway(start, end, pathway)
        newPaths = []
        for x in range(len(pathways)):
            for y in range(len(pathways[x])):
                for z in range(y + 1, len(pathways[x]) - 1):
                    if pathways[x][y] == pathways[x][z]:
                        break
                else:
                    continue
                break
            else:
                if pathways[x] not in newPaths:
                    newPaths.append(pathways[x])

        return newPaths

    # 初级回路
    def findPrimaryLoop(self, start, pathway=[]):
        pathways = self.findPrimaryPathway(start, start, pathway)
        return pathways

    def findAllPathWithEdge(self, start, end, pathway=[]):
        pathways = self.findPathWay(start, end, pathway)
        for pathway in pathways:
            for y in range(len(pathway)):
                if y >= len(pathway):
                    break
                if type(pathway[y]) is Edge:
                    z = y
                    while type(pathway[z]) is Edge:
                        z = z + 1
                    if len(pathway[y:z]) != 1:
                        del pathway[y:z - 1]

        return pathways

    def shortestPath(self, start, end, pathway=[]):
        self.dijkstra(start)
        pathway = pathway + [self.__vertDict[end]]
        if start == end:
            pathway.reverse()
            return pathway
        if self.__vertDict[end].pred():
            for edge in self.edge(self.__vertDict[end].pred(), end):
                if min(x.weight() for x in self.edge(self.__vertDict[end].pred(), end)) == edge.weight():
                    pathway.append(edge)
            newPath = self.shortestPath(start, self.__vertDict[end].pred().id(), pathway)
            if newPath:
                return newPath
        return newPath

    def dijkstra(self, start):
        if type(start) is not Vertex:
            for vert in self:
                if vert.id() == start:
                    start = vert
        start: Vertex
        pq = PriorityQueue()
        start.setDistance(0)
        pq.buildHeap([(v.distance(), v) for v in self])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.vertConnections():
                weight = min([x.weight() for x in self.edge(currentVert, nextVert)])
                newDist = currentVert.distance() + weight
                if newDist < nextVert.distance():
                    nextVert.setDistance(newDist)
                    nextVert.setPred(currentVert)
                    pq.decreaseKey(nextVert, newDist)

    def isProjectNetwork(self):
        if not self.__mode:
            return False
        outDegree, inDegree = self.degrees()
        if 0 not in outDegree.values():
            return False
        if 0 not in inDegree.values():
            return False

        for x in range(len(self.__vertDict)):
            for y in range(x + 1, len(self.__vertDict)):
                if len(self.edge(self.__vertDict[x], self.__vertDict[y])) > 1 or len(
                        self.edge(self.__vertDict[y], self.__vertDict[x])) > 1:
                    return False

        for vert in self.__vertDict.values():
            if len(self.findSimpleLoop(vert.id())):
                return False
        end = max([x for x in outDegree if outDegree[x] == 0])
        for vert in self.__vertDict.values():
            if end == vert.id():
                continue
            if vert.id() > end:
                return False

        return True

    # 通用深度优先搜索
    def dfs(self):
        for vert in self:
            vert.setColor('white')
            vert.setPred(-1)
        for vert in self:
            if vert.color() == 'white':
                self.dfsVisit(vert)

    def dfsVisit(self, start):
        start.setColor("gray")
        self.__time += 1
        start.setDiscovery(self.__time)
        for nextVert in start.vertConnections():
            if nextVert.color() == 'white':
                nextVert.setPred(start)
                self.dfsVisit(nextVert)
        start.setColor("black")
        self.__time += 1
        start.setFinish(self.__time)

    def topologySort(self):
        if not self.__mode:
            return None
        for vert in self.__vertDict.values():
            if len(self.findSimpleLoop(vert.id())):
                return None

        self.dfs()
        topology = []
        time = [x.finish() for x in self]
        time.sort(reverse=True)
        for t in time:
            for vert in self:
                if vert.finish() == t:
                    topology.append(vert)

        return topology

    def findCriticalPath(self, pathway=[]):
        if not self.isProjectNetwork():
            return pathway

        def ES():
            esList = {}
            esList[0] = 0
            for x in range(1, len(self.__numVertices)):
                pass

    # def isEulerGraph(self):


#  Vertex类表示图中的每一个顶点
class Vertex:
    #  初始化ID，以及字典connectedTo
    def __init__(self, key, weight=0):
        self.__id = key
        self.__weight = weight
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

    def setWeight(self, weight):
        self.__weight = weight

    def edge(self):
        return self.__edge

    def fromVert(self):
        return self.__fromVert

    def toVert(self):
        return self.__toVert


if __name__ == '__main__':
    g = Graph()
    s = Graph()

    # g.addEdge(0, 0, 5)
    # g.addEdge(0, 1, 1)
    # g.addEdge(1, 0, 3)
    # g.addEdge(0, 2, 1)
    # g.addEdge(1, 2, 8)
    # g.addEdge(2, 3, 7)
    # g.addEdge(3, 2, 6)

    # g.addEdge(1, 0)
    # g.addEdge(0, 2)
    # g.addEdge(3, 1)
    # g.addEdge(2, 3)
    # g.addEdge(0, 3)

    # g.addEdge(0, 1)
    # g.addEdge(2, 0)
    # g.addEdge(1, 3)
    # g.addEdge(2, 3)
    # g.addEdge(2, 1)

    # g.addEdge(1, 0)
    # g.addEdge(2, 0)
    # g.addEdge(1, 3)
    # g.addEdge(2, 3)
    # g.addEdge(1, 2)

    # g.addEdge(0, 1, 0)
    # g.addEdge(0, 2, 0)
    # g.addEdge(0, 3, 0)
    # g.addEdge(1, 2, 0)
    # g.addEdge(1, 3, 0)
    # g.addEdge(2, 3, 0)

    # g.setMode(False)
    # s.setMode(False)

    # g.addEdge(0, 1, 0)
    # g.addEdge(1, 0, 0)
    # g.addEdge(0, 2, 0)
    # g.addEdge(2, 0, 0)
    # g.addEdge(1, 2, 0)
    # g.addEdge(2, 1, 0)

    # s.addVertex(0)
    #
    # s.addEdge(2, 1, 1)
    # s.addEdge(1, 2, 1)
    # s.addEdge(0, 2, 1)
    # s.addEdge(2, 0, 1)

    # for path in paths:
    #     for item in path:
    #         if type(item) is Edge:
    #             print(f"e{item.id()}", end='\t')
    #         if type(item) is Vertex:
    #             print(f"v{item.id()}", end='\t')
    #     print()
    # print()
    # for path in paths2:
    #     for item in path:
    #         if type(item) is Edge:
    #             print(f"e{item.id()}", end='\t')
    #         if type(item) is Vertex:
    #             print(f"v{item.id()}", end='\t')
    #     print()

    # g.addEdge(0, 1, 1)
    # g.addEdge(0, 2, 4)
    # g.addEdge(1, 2, 2)
    # g.addEdge(1, 4, 5)
    # g.addEdge(1, 3, 7)
    # g.addEdge(2, 4, 1)
    # g.addEdge(3, 4, 3)
    # g.addEdge(3, 5, 2)
    # g.addEdge(4, 5, 6)

    # g.addEdge(0, 1, 3)
    # g.addEdge(0, 2, 10)
    # g.addEdge(1, 3, 9)
    # g.addEdge(1, 4, 13)
    # g.addEdge(2, 4, 12)
    # g.addEdge(2, 5, 7)
    # g.addEdge(3, 6, 8)
    # g.addEdge(3, 7, 4)
    # g.addEdge(4, 7, 6)
    # g.addEdge(5, 7, 11)
    # g.addEdge(6, 8, 2)
    # g.addEdge(7, 8, 5)

    g.addEdge(0, 1, 1)
    g.addEdge(0, 2, 2)
    g.addEdge(0, 3, 3)
    g.addEdge(1, 3, 0)
    g.addEdge(1, 4, 3)
    g.addEdge(2, 3, 2)
    g.addEdge(2, 6, 4)
    g.addEdge(2, 5, 4)
    g.addEdge(3, 4, 4)
    g.addEdge(4, 5, 1)
    g.addEdge(5, 7, 1)
    g.addEdge(6, 7, 6)
    g.dfs()

    for s in g:
        print(s.discovery(), end='\t')
    print()
    for s in g:
        print(s.finish(), end='\t')


