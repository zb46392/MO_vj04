# -*- coding: utf-8 -*-
"""
@author: Zdravko Baničević

Python 3.4
"""

from banicevic_zdravko_00 import Graph, Matrix

EULER_KUCICA = "euler.net"
FOOTBALL = "football.net"

FILE = EULER_KUCICA

def main():
    g = Graph()
    g.importGraphFromPajekFile(FILE)
    adjacencyMatrix = Matrix.createAdjacencyMatrix(g.getVertices(), g.getArcs(), g.getEdges())
    #incidenceMatrix = Matrix.createIncidenceMatrix(g.getVertices(), g.getArcs(), g.getEdges())
    #adjacencyList = Matrix.createAdjacencyList(g.getVertices(), g.getArcs(), g.getEdges())
    
    print(adjacencyMatrix)
    adjacencyMatrix.convertTo(Matrix.ADJACENCY_LIST)
    print(adjacencyMatrix)
    adjacencyMatrix.convertTo(Matrix.INCIDENCE_MATRIX)
    print(adjacencyMatrix)
    adjacencyMatrix.convertTo(Matrix.ADJACENCY_MATRIX)
    print(adjacencyMatrix)
    
    

if __name__ == "__main__":
    main()