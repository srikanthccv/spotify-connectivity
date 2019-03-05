class Node:
    def __init__(self, nodeType, nodeVal, spotifyLink):
        self.nodeType = nodeType        # could be artist or album
        self.nodeVal = nodeVal          # could be artist name or album name
        self.spotifyLink = spotifyLink  # spotify link to album if node type album, empty otherwise
        self.adjList = {}               # adjacency list for node

    def addAdjNode(self, node):
        self.adjList[node.nodeVal] = node

class SpotifyGraph:
    def __init__(self):
        self.numberOfNodes = 0
        self.nodesList = {}

    def addNode(self, node):
        self.numberOfNodes = self.numberOfNodes + 1
        self.nodesList[node.nodeVal] = node

    def addEdge(self, nodeA, nodeB):
        if nodeA.nodeVal not in self.nodesList:
            self.addNode(nodeA)
        if nodeB.nodeVal not in self.nodesList:
            self.addNode(nodeB)
        self.nodesList[nodeA.nodeVal].addAdjNode(nodeB)
        self.nodesList[nodeB.nodeVal].addAdjNode(nodeA)

    def run(self, start, end):
        startNode, endNode, visitedNodes = self.nodesList[start], self.nodesList[end], {}
        pathList = []
        pathList.append([startNode])
        while len(pathList) != 0:
            currPath = pathList.pop(0)
            lastNode = currPath[-1]
            visitedNodes[lastNode.nodeVal] = True
            if (lastNode.nodeVal == endNode.nodeVal):
                return currPath
            for adjacent in self.nodesList[lastNode.nodeVal].adjList.values():
                if adjacent.nodeVal not in visitedNodes:
                    newPath = list(currPath)
                    newPath.append(adjacent)
                    pathList.append(newPath)

if __name__ == "__main__":
    pass