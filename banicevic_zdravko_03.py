# -*- coding: utf-8 -*-
"""
@author: Zdravko Baničević

Python 3.4
"""
from banicevic_zdravko_000 import Graph

EULER_KUCICA = "euler.net"
FOOTBALL = "football.net"

FILE = EULER_KUCICA

def graphHasEulerianPath(graph):
    if len(graph.getComponents()) == 1:
        
        if graph.getType() is Graph.UNDIRECTED:
            nbrOfOddDegrees = 0
            
            for verticeNumber in graph.getVertices():
                if not graph.getVertices()[verticeNumber].hasEvenDegree():
                    nbrOfOddDegrees += 1
                    if nbrOfOddDegrees > 2:
                        return False
                    
            if nbrOfOddDegrees == 0 or nbrOfOddDegrees == 2:
                return True
            else:
                return False
                
        elif graph.getType() is Graph.DIRECTED:
            hasInGreaterByOne = False
            hasOutGreaterByOne = False
            
            for verticeNbr in graph.getVertices():
                if graph.getVertices()[verticeNbr].getInDegree() != graph.getVertices()[verticeNbr].getOutDegree():
                    if graph.getVertices()[verticeNbr].getInDegree() + 1 == graph.getVertices()[verticeNbr].getOutDegree():
                        if not hasInGreaterByOne:
                            hasInGreaterByOne = True
                        else:
                            return False
                    elif graph.getVertices()[verticeNbr].getOutDegree() + 1 == graph.getVertices()[verticeNbr].getInDegree():
                        if not hasOutGreaterByOne:
                            hasOutGreaterByOne = True
                        else:
                            return False
                    
                    else:
                        return False
                    
            if hasInGreaterByOne and hasOutGreaterByOne:
                return True
                
    else:
        return False
            
        

def findEulerianPath(graph):
    startVertex = findStartVertexForEulerianPath(graph)
    
    if startVertex is not None:
        if graph.getType() is Graph.UNDIRECTED:
            paths = []
            nbrOfEdges = len(graph.getComponents()[0])
            sameEdges = findEdgesOccuringMultipleTimes(graph)
            
            paths.append(([], startVertex)) # TRAVERSED PATH , CURRENT VERTEX
                    
            while True:
                path = paths.pop(0)
                
                edges = findNextEdges(graph, path[1], path[0], sameEdges)
                
                for edge in edges:
                    
                    tPath = [e for e in path[0]]
                    tPath.append(edge)
                    cVertex = None
                    
                    if len(tPath) == nbrOfEdges:
                        return formatPath(startVertex, tPath)
                    
                    
                    if edge[0] != path[1].getNumber():
                        cVertex = graph.getVertices()[edge[0]]
                    else:
                        cVertex = graph.getVertices()[edge[1]]
                    
                    paths.append((tPath, cVertex))
                
                    
        elif graph.getType() is Graph.DIRECTED:
            pass
        
def findStartVertexForEulerianPath(graph):
    if graphHasEulerianPath(graph):
        if graph.getType() is Graph.UNDIRECTED:
            
            for vertexNbr in graph.getVertices():
                if not graph.getVertices()[vertexNbr].hasEvenDegree():
                    return graph.getVertices()[vertexNbr]
                    
        elif graph.getType() is Graph.DIRECTED:
            for vertexNbr in graph.getVertices():
                if graph.getVertices()[vertexNbr].getOutDegree() + 1 == graph.getVertices()[vertexNbr].getInDegree():
                    return graph.getVertices()[vertexNbr]
        
        return graph.getVertices()[0]
    else:
        return None

def findEdgesOccuringMultipleTimes(graph):
    multipleEdges = {}
    edges = graph.findAllEdges()    
    
    for i in range(len(edges)):
        occurences = 0
        if edges[i].getVertices() not in multipleEdges.keys():
            for j in range(i, len(edges)):
                if edges[i].getVertices() == edges[j].getVertices():
                    occurences += 1
        
        if occurences > 1: 
            multipleEdges[edges[i].getVertices()] = occurences
            
    return multipleEdges

def findNextEdges(graph, currentVertex, traversedPath, multipleSameEdges):
    
    if graph.getType() is Graph.UNDIRECTED:
        return findNextEdgesOfUndirectedGraph(graph, currentVertex, traversedPath, multipleSameEdges)
    elif graph.getType() is Graph.DIRECTED:
        return findNextEdgesOfDirectedGraph(graph, currentVertex, traversedPath, multipleSameEdges)
    
def findNextEdgesOfUndirectedGraph(graph, currentVertex, traversedPath, multipleSameEdges):
    edges = []
    
    for edge in graph.findAllEdges():
        if currentVertex.getNumber() in edge.getVertices():
            
            if edge.getVertices() in traversedPath:
                handleEdgesOccuringMultipleTimes(edges, edge, traversedPath, multipleSameEdges)                        
            else:
                edges.append(edge.getVertices())
                
    return edges
    
def findNextEdgesOfDirectedGraph(graph, currentVertex, traversedPath, multipleSameEdges):
    edges = []
    
    for edge in graph.findAllEdges():
        if currentVertex.getNumber() == edge.getVertices()[0]:
            
            if edge.getVertices() in traversedPath:
                handleEdgesOccuringMultipleTimes(edges, edge, traversedPath, multipleSameEdges)                        
            else:
                edges.append(edge.getVertices())
                
    return edges
            
def handleEdgesOccuringMultipleTimes(nextEdges, currentEdge, traversedPath, multipleSameEdges):
    if currentEdge.getVertices() in multipleSameEdges.keys():
        nbrOfSameEdge = 0
        for segment in traversedPath:
            if segment == currentEdge.getVertices():
                nbrOfSameEdge += 1
        
        if nbrOfSameEdge < multipleSameEdges[currentEdge.getVertices()]:
            nextEdges.append(currentEdge.getVertices())
            
def formatPath(startVertex, path):
    currentVertex = startVertex.getNumber()
    formattedPath = str(currentVertex)
    
    if len(path) > 1:
        formattedPath += " -> "
        for i in range(len(path)):
            if currentVertex == path[i][0]:
                currentVertex = path[i][1]
                formattedPath += str(currentVertex)
                    
            elif currentVertex == path[i][1]:
                currentVertex = path[i][0]
                formattedPath += str(currentVertex)
                
            if i < len(path)-1:
                formattedPath += " -> "
            else:
                formattedPath += "\n"
                
    return formattedPath
                
    
def main():
    g = Graph()
    g.importGraphFromPajekFile(FILE)
    
    
    print(findEulerianPath(g))
        
    

if __name__ == "__main__":
    main()