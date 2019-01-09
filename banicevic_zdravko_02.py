# -*- coding: utf-8 -*-
"""
@author: Zdravko Baničević

Python 3.4
"""
EULER_KUCICA = "euler.net"
FOOTBALL = "football.net"

FILE = FOOTBALL


from banicevic_zdravko_00 import Graph

def calculateNumberOfVertices(graph):
    return len(graph.getVertices())

def calculateNumberOfEdges(graph):
    if len(graph.getArcs()) > 0:
        return len(graph.getArcs())
    else:
        return len(graph.getEdges())

def calculateVerticeDegree(graph):
    verticesDegree = {}
    
    for vertice in graph.getVertices():
            verticesDegree[vertice] = 0
    
    if len(graph.getArcs()) > 0:        
        for arc in graph.getArcs():
            verticesDegree[arc[0]] += 1
            verticesDegree[arc[1]] += 1
    else:            
        for edge in graph.getEdges():
            verticesDegree[edge[0]] += 1
            verticesDegree[edge[1]] += 1
            
    return verticesDegree
            
    
def findVerticesWithMostIncidentEdges(graph):
    
    verticesDegrees = calculateVerticeDegree(graph)
    verticesWithMaxIncidentEdges = [0, []] # ( number of edges , vertices )
    
    for verticeDegree in verticesDegrees:
        if verticesDegrees[verticeDegree] > verticesWithMaxIncidentEdges[0]:
            verticesWithMaxIncidentEdges[1].clear()
            verticesWithMaxIncidentEdges[0] = verticesDegrees[verticeDegree]
            verticesWithMaxIncidentEdges[1].append(verticeDegree)
            
        elif verticesDegrees[verticeDegree] == verticesWithMaxIncidentEdges[0]:
            verticesWithMaxIncidentEdges[1].append(verticeDegree)
    
    return verticesWithMaxIncidentEdges
    
def main():
    g = Graph()
    g.importGraphFromPajekFile(FILE)
    
    print("Broj čvorova: " + str(calculateNumberOfVertices(g)))
    print("Broj bridova: " + str(calculateNumberOfEdges(g)))
    
    verticesDegrees = calculateVerticeDegree(g)
    print("Stupnjevi čvorova:")
    for verticeDegree in verticesDegrees:
        print("  " + str(verticeDegree) + ": " + str(verticesDegrees[verticeDegree]))
        
    print("Vrh(ovi) s maximalnim brojem incidentnih bridova:")
    verticesWithMaxIncidentEdges = findVerticesWithMostIncidentEdges(g)
    print("  Broj bridova: " + str(verticesWithMaxIncidentEdges[0]))
    print("  Vrh(ovi): ")    
    for vertice in verticesWithMaxIncidentEdges[1]:
        print("   " + str(vertice))
    

if __name__ == "__main__":
    main()