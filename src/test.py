class PathNode:
    def __init__(self, x, w):
        self.data = x
        self.weight = w
        self.next = None


class Solution:
    def findCriticalPath(self, vexs, edges):
        """
        :type vexs: int
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        vexNum = len(vexs)
        if vexNum < 1:
            return []
        if len(edges) < 1:
            res = [i for i in range(vexNum)]
            return res

        edgeNum = len(edges)
        # 构建邻接表
        vset = [PathNode(i, 0) for i in range(vexNum)]
        indegree = [0] * vexNum  # 统计入度
        for e in range(edgeNum):
            vex1 = vset[edges[e][0]]
            vex2 = vset[edges[e][1]]
            indegree[edges[e][1]] += 1
            # visited=[True]*numCourses
            while vex1.next != None:
                vex1 = vex1.next
            vex1.next = PathNode(edges[e][1], edges[e][2])
        # 进行拓扑排序
        res = []
        cnt = vexNum
        ve = [0] * vexNum
        vl = [0] * vexNum
        index = [0] * vexNum

        old_cnt = cnt
        pos = 0
        while cnt > 0:
            pos += old_cnt - cnt
            old_cnt = cnt
            for i in range(vexNum):
                if indegree[i] == 0:
                    indegree[i] = -1
                    res.append(i)
                    pos = i
                    cnt -= 1
                    # 删除以入度为0的头点的弧
                    tmp = vset[i]
                    while tmp.next != None:
                        tmp = tmp.next
                        indegree[tmp.data] -= 1
                        if ve[tmp.data] < ve[pos] + tmp.weight:
                            ve[tmp.data] = ve[pos] + tmp.weight
                        if vl[pos] > vl[tmp.data] - tmp.weight:
                            vl[pos] = vl[tmp.data] - tmp.weight
                            index[pos] = tmp.data

            # 如果没有新的入度为0的节点，说明存在环
            if old_cnt == cnt:
                return []

        vl[vexNum - 1] = ve[vexNum - 1]
        pos = vexNum - 2
        while pos > -1:
            vl[pos] += vl[index[pos]]
            pos -= 1

        ##        print(ve)
        ##        print(vl)
        ##        print(res)
        path = []
        for i in range(vexNum):
            if ve[i] == vl[i]:
                path.append(i)
        start = 0
        mov = 1
        paths=[]
        pathWay=[]
        # 输出一条关键路径
        while mov < len(path):
            tmp = vset[path[start]]
            while tmp.next != None:
                tmp = tmp.next
                if tmp.data == path[mov]:
                    if start == 0:
                        new
                        print(path[start])
                    print(path[mov])
                    start = mov
                    break
            mov += 1

        return path


if __name__ == '__main__':
    g = Solution()
    vertex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    edge = [[0, 1, 3], [0, 2, 10], [1, 3, 9], [1, 4, 13], [2, 4, 12], [2, 5, 7], [3, 6, 8], [3, 7, 4], [4, 7, 6],
            [5, 7, 11], [6, 8, 2], [7, 8, 5]]
    print(g.findCriticalPath(vertex, edge))
