# -*- coding: utf-8 -*-
"""
@author: Zdravko Baničević

Python 3.4
"""

class Matrix():
    ADJACENCY_MATRIX = "Adjacency Matrix"
    INCIDENCE_MATRIX = "Incidence Matrix"
    ADJACENCY_LIST = "Adjacency List"
    MATRIX = "Matrix"
    
    
    def __init__(self, matrix = None):
        if matrix is not None:
            self.matrix = matrix.getMatrix()
            self.type = matrix.getType()
        else:
            self.matrix = []
            self.type = Matrix.MATRIX
    
    def getMatrix(self):
        return self.matrix
        
    def getType(self):
        return self.type
        
    def setMatrix(self, matrix):
        self.matrix = matrix
    
    def setType(self, matrixType):
        self.type = matrixType
        
    def createTransposedMatrix(self, matrix = None):
        if matrix is None:
            matrix = self.matrix
            
        transposedMatrix = []
        nbrOfRows = len(matrix)
        
        
        if nbrOfRows > 0:
            nbrOfColumns = len(matrix[0])
            
            for c in range(nbrOfColumns):
                transposedMatrix.append([])
                for r in range(nbrOfRows):
                    transposedMatrix[c].append(matrix[r][c])
                    
        m = Matrix()
        m.matrix = transposedMatrix
        
        return m
    
    @staticmethod    
    def generateAdjacencyMatrix(vertices, arcs, edges):
        adjacencyMatrix = [[0 for i in range(len(vertices))] for i in range(len(vertices))]
        
        if len(edges) > 0: # degree = sum of rows or collumns
            for edge in edges:
                if edge[0] == edge[1]:
                    adjacencyMatrix[edge[0] - 1][edge[1] - 1] += 2
                else:
                    adjacencyMatrix[edge[0] - 1][edge[1] - 1] += 1
                    adjacencyMatrix[edge[1] - 1][edge[0] - 1] += 1
                    
        elif len(arcs) > 0: # out-degree = sum of rows , in-degree sum of columns
            for arc in arcs:
                adjacencyMatrix[arc[0] - 1][arc[1] - 1] += 1
        
        return adjacencyMatrix
    
    @staticmethod
    def generateIncidenceMatrix(vertices, arcs, edges):
        # row = vertices , column = edges    
    
        incedenceMatrix = []
        
        if len(edges) > 0:    
            incedenceMatrix = [[0 for i in range(len(edges))] for i in range(len(vertices))]
            
            for i in range(len(edges)):
                incedenceMatrix[edges[i][0] - 1][i] += 1
                incedenceMatrix[edges[i][1] - 1][i] += 1
                
        elif len(arcs) > 0:
            incedenceMatrix = [[0 for i in range(len(arcs))] for i in range(len(vertices))]
            
            for i in range(len(arcs)):
               # pointing to itself ??? 
               incedenceMatrix[arcs[i][0] - 1][i] -= 1
               incedenceMatrix[arcs[i][1] - 1][i] += 1 
        
        return incedenceMatrix
    
    @staticmethod    
    def generateAdjacencyList(vertices, arcs, edges):
        adjecencyList = {}
        
        for vertice in vertices:
            adjecencyList[vertice] = []
        
        if len(edges) > 0:
            for edge in edges:
                adjecencyList[edge[0]].append(edge[1])
                adjecencyList[edge[1]].append(edge[0])
        
        elif len(arcs) > 0:
            for arc in arcs:
                adjecencyList[arc[0]].append(arc[1])
                
        return adjecencyList
    
    def isMatrixSymmetric(self, matrix = None):
        if matrix is None:
            matrix = self.matrix
        
        if len(matrix) > 0:
            nbrOfRows = len(matrix)
            nbrOfColumns = len(matrix[0])
            
            if nbrOfRows != nbrOfColumns:
                return False
        
            for i in range(nbrOfRows):
                for j in range(nbrOfColumns):
                    if matrix[i][j] != matrix[j][i]:
                        return False
        # else ???
                    
        return True
    
    @staticmethod
    def createAdjacencyMatrix(vertices, arcs, edges):
        adjacencyMatrix = Matrix()
        adjacencyMatrix.matrix = Matrix.generateAdjacencyMatrix(vertices, arcs, edges)
        adjacencyMatrix.type = Matrix.ADJACENCY_MATRIX
        
        return adjacencyMatrix
        
    @staticmethod
    def createIncidenceMatrix(vertices, arcs, edges):
        incidenceMatrix = Matrix()
        incidenceMatrix.matrix = Matrix.generateIncidenceMatrix(vertices, arcs, edges)
        incidenceMatrix.type = Matrix.INCIDENCE_MATRIX
        
        return incidenceMatrix
        
    @staticmethod
    def createAdjacencyList(vertices, arcs, edges):
        adjacencyList = Matrix()
        adjacencyList.matrix = Matrix.generateAdjacencyList(vertices, arcs, edges)
        adjacencyList.type = Matrix.ADJACENCY_LIST
        
        return adjacencyList
    
    def convertTo(self, matrixType):
        vertices = []
        edges = []
        arcs = []
        
        if self.type is Matrix.ADJACENCY_MATRIX:
            vertices = [i+1 for i in range(len(self.matrix))]
            
            if self.representsDirectedGraph():
                for i in range(len(vertices)):
                    for j in range(len(vertices)):
                        if self.matrix[i][j] != 0:
                            arcs.append((i+1, j+1))                
            else:
                for i in range(len(vertices)):
                    for j in range(i, len(vertices)):
                        if self.matrix[i][j] != 0:
                            edges.append((i + 1, j + 1))
                
                            
        elif self.type is Matrix.INCIDENCE_MATRIX:
            vertices = [i+1 for i in range(len(self.matrix))]
            
            if self.representsDirectedGraph():
                for i in range(len(self.matrix[0])):
                    arc = {}
                    for j in range(len(self.matrix)):
                        if self.matrix[j][i] == -1:
                            arc[0] = (j+1)
                        elif self.matrix[j][i] == 1:
                            arc[1] = (j+1)
                            
                    arcs.append((arc[0], arc[1]))
            else:
                for i in range(len(self.matrix[0])):
                    edge = []
                    for j in range(len(self.matrix)):
                        if self.matrix[j][i] != 0:
                            edge.append(j+1)
                            
                    edges.append(tuple(edge))
                    
        elif self.type is Matrix.ADJACENCY_LIST:
            vertices = [i+1 for i in range(len(self.matrix))]
            
            if self.representsDirectedGraph():
                for i in self.matrix:
                    for j in self.matrix[i]:
                        arcs.append((i, j))
                        
            else:
                addedEdges = []
                for i in self.matrix:
                    for j in self.matrix[i]:
                        if {i, j} not in addedEdges:
                            edges.append((i, j))
                            addedEdges.append({i, j})
        
        if matrixType is Matrix.ADJACENCY_MATRIX:
            self.matrix = Matrix.generateAdjacencyMatrix(vertices, arcs, edges)
            self.type = Matrix.ADJACENCY_MATRIX
        elif matrixType is Matrix.INCIDENCE_MATRIX:
            self.matrix = Matrix.generateIncidenceMatrix(vertices, arcs, edges)
            self.type = Matrix.INCIDENCE_MATRIX
        elif matrixType is Matrix.ADJACENCY_LIST:
            self.matrix = Matrix.generateAdjacencyList(vertices, arcs, edges)
            self.type = Matrix.ADJACENCY_LIST
            
    def representsDirectedGraph(self):
        if self.type is Matrix.ADJACENCY_MATRIX:
            return not self.isMatrixSymmetric()
            
        if self.type is Matrix.INCIDENCE_MATRIX:
            return not (self.sumOfColumn() == 2)
            
        if self.type is Matrix.ADJACENCY_LIST:
            for i in self.matrix:
                for j in self.matrix[i]:
                    if i not in self.matrix[j]:
                        return True
            return False
            
            
    
    def sumOfColumn(self, column = 0):
        if len(self.matrix) > 0 and column <= (len(self.matrix[0]) - 1):
            columnSum = 0
            
            for i in range(len(self.matrix)):
                columnSum += self.matrix[i][column]
                
            return columnSum
            
        # else ???
    def __str__(self):
        mStr = "TYPE: " + str(self.type) + "\n"
        
        for r in self.matrix:
            if self.type == Matrix.ADJACENCY_LIST:
                mStr += str(r) + ": " + str(self.matrix[r]) + "\n"
            else:
                mStr += str(r) + "\n"
            
        return mStr

class Graph():
    def __init__(self):
        self.vertices = {}
        self.edges = []
        self.arcs = []
        
    def importGraphFromPajekFile(self, fileName):
        try:
            file = open(fileName, "r")
        except FileNotFoundError:
            print("Datoteka '" + fileName + "' nije pronađena...")                
        else:
            lineLst = file.readline().strip().split(' ')
            
            while lineLst[0] is not '':
                if lineLst[0] == "*Vertices":
                    while True:
                        lineLst = file.readline().strip().split(' ')
                        try:
                            data = []
                            
                            for i in range(1, len(lineLst)):
                                if lineLst[i] != '':
                                    data.append(lineLst[i])
                                    
                            self.vertices[int(lineLst[0])] = data
                        except:
                            break
                        
                elif lineLst[0] == "*Arcs":
                    while True:
                        lineLst = file.readline().strip().split(' ')
                        
                        if len(lineLst) == 1:
                            break
                        
                        try:
                            arcs = []
                            for i in range(len(lineLst)):
                                if lineLst[i] != '':
                                    arcs.append(int(lineLst[i]))
                            
                            self.arcs.append(tuple(arcs))
                        except:
                            break
                elif lineLst[0] == "*Edges":
                    while True:
                        lineLst = file.readline().strip().split(' ')
                        
                        if len(lineLst) == 1:
                            break
                        
                        try:    
                            edges = []
                            for i in range(len(lineLst)):
                                if lineLst[i] != '':
                                    edges.append(int(lineLst[i]))
                            self.edges.append(tuple(edges))
                        except:
                            break
                        
                else:
                    lineLst = file.readline().strip().split(' ')
        finally:
            file.close()
    
    def getVertices(self):
        return self.vertices
        
    def getArcs(self):
        return self.arcs
        
    def getEdges(self):
        return self.edges
        
    def setVertices(self, vertices):
        self.vertices = vertices
        
    def setArcs(self, arcs):
        self.arcs = arcs
        
    def setEdges(self, edges):
        self.edges = edges
    
    def __str__(self):
        gStr = "VERTICES:\n"
        for i in self.vertices:
            gStr += ("    " + str(i) + " : " + str(self.vertices[i]) + "\n")
        gStr += "\nARCS:\n"
        for arc in self.arcs:
            gStr += ("    " + str(arc) + "\n")
        gStr += "\nEDGES:\n"
        for edge in self.edges:
            gStr += ("    " + str(edge) + "\n")
            
        return gStr