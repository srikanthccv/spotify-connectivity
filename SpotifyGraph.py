import json


class Node:
    def __init__(self, nodeType, nodeVal, spotifyLink):
        self.nodeType = nodeType        # could be artist or album
        self.nodeVal = nodeVal          # could be artist name or album name
        # spotify link to album if node type album, empty otherwise
        self.spotifyLink = spotifyLink
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
        startNode, endNode, visitedNodes = self.nodesList[start], self.nodesList[end], {
        }
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


def makeSpotifyGraph(location):
    g = SpotifyGraph()
    with open(location) as file:
        for line in file.readlines():
            line = eval(line)
            albumNode = Node('Album', line['album'], line['album_url'])
            for artist in line['artists']:
                artistNode = Node('Artist', artist, '')
                g.addEdge(albumNode, artistNode)
    return g


if __name__ == "__main__":
    # run some simple test
    g = SpotifyGraph()
    x1 = Node('Album', 'Slumdog Millionaire',
              'https://open.spotify.com/album/28tUf89XzjZ5O5yOnvVTqM')
    a1 = Node('Artist', 'A.R. Rahman', '')
    a2 = Node('Artist', 'Sanjay Joseph', '')
    x2 = Node('Album', 'Dil Ne Jise Apna Kaha',
              'https://open.spotify.com/album/2aeSrDnUhcPA5rbq1Oefc3')
    a3 = Node('Artist', 'Himesh Reshammiya', '')
    g.addEdge(x1, a1)
    g.addEdge(x1, a2)
    g.addEdge(x2, a3)
    g.addEdge(x2, a1)
    expectedSol = ['Sanjay Joseph', 'Slumdog Millionaire',
                   'A.R. Rahman', 'Dil Ne Jise Apna Kaha', 'Himesh Reshammiya']
    returnSol = [n.nodeVal for n in g.run(
        'Sanjay Joseph', 'Himesh Reshammiya')]
    assert(expectedSol == returnSol)
