# -*- coding: utf-8 -*-
"""
@author: Zdravko Baničević

Python 3.4
"""
class Vertice():
    def __init__(self, number = 0, data = None, inDegree = 0, outDegree = 0):
        self.number = number
        if type(data) is list:
            self.data = data
        else:
            self.data = []
        self.inDegree = inDegree
        self.outDegree = outDegree
        
    def getNumber(self):
        return self.number
    def setNumber(self, number):
        self.number = number
        
    def getData(self):
        return self.data
    def setData(self, data):
        self.data = data
    def appendData(self, data):
        self.data.append(data)
        
    def getInDegree(self):
        return self.inDegree
    def setInDegree(self, inDegree):
        self.inDegree = inDegree
        
    def getOutDegree(self):
        return self.outDegree
    def setOutDegree(self, outDegree):
        self.outDegree = outDegree
        
    def incrementInDegreeBy(self, num):
        self.inDegree += num
        
    def incrementOutDegreeBy(self, num):
        self.outDegree += num
        
    def calculateDegree(self):
        return self.inDegree + self.outDegree
        
    def hasEvenDegree(self):
        return ((self.calculateDegree() % 2) == 0)
        
    def __str__(self):
        vStr = "Vertice Number: %s\n" % str(self.number)
        vStr +="Vertice data: "
        
        for i in range(len(self.data)):
            if i < (len(self.data) - 1):
                vStr += str(self.data[i]) + ", "
            else:
                vStr += str(self.data[i]) + "\n"
            
        vStr += "Vertice Degree: " + str(self.calculateDegree())
        vStr += " : (" + str(self.inDegree) + ", " + str(self.outDegree) + ")\n"
        
        return vStr
        
        
class Edge():
    def __init__(self, vertices = None, weigth = 0):
        self.vertices = vertices
        self.weigth = weigth
        
    def getVertices(self):
        return self.vertices
    def setVertices(self, vertices):
        self.vertices = vertices
        
    def getWeigth(self):
        return self.weigth
    def setWeigth(self, weigth):
        self.weigth = weigth
        
    def __str__(self):
        return "Edge: %s - Weigth: %s \n" % (str(self.getVertices()), str(self.getWeigth()))
    

class Graph():
    DIRECTED = "Directed"
    UNDIRECTED = "Undirected"
    
    def __init__(self, vertices = None, components = None, graphType = None):
        if type(vertices) is dict:
            self.vertices = vertices
        else:
            self.vertices = {}
            
        if type(components) is list:
            self.components = components
        else:
            self.components = []
            
        self.type = graphType
        
    def importGraphFromPajekFile(self, fileName):
        
        try:
            file = open(fileName, "r")
        except FileNotFoundError:
            print("Datoteka '" + fileName + "' nije pronađena...")                
        else:
            lineLst = file.readline().strip().split(' ')
            while lineLst[0] is not '':
                if lineLst[0].lower() == "*vertices":
                    self.vertices = self.createVerticesFromPajekFile(file)                    
                            
                elif lineLst[0].lower() == "*arcs":
                    components = self.createComponentsFromPajekFile(file)
                    
                    if len(components) > 0:
                        self.type = Graph.DIRECTED
                        self.components = components
                elif lineLst[0].lower() == "*edges":
                    components = self.createComponentsFromPajekFile(file)
                    
                    if len(components) > 0:
                        self.type = Graph.UNDIRECTED
                        self.components = components
                        
                lineLst = file.readline().strip().split(' ')
        finally:
            file.close()
    
    def createVerticesFromPajekFile(self, file):
        vertices = {}
        isVertice = True
        
        while isVertice:
            filePos = file.tell()
            lineLst = file.readline().strip().split(' ')
            try:
                v = Vertice()
                v.setNumber(int(lineLst[0]))
                
                for i in range(1, len(lineLst)):
                    if lineLst[i] != '':
                        v.appendData(lineLst[i])
                        
                vertices[v.getNumber()] = v
                
            except ValueError:            
                file.seek(filePos)
                isVertice = False
                
            except Exception as e:
                print("Graph.createVerticesFromPajekFile : %s" % str(e))
                isVertice = False
                

        return vertices
            
    def createComponentsFromPajekFile(self, file):
        
        components = []
        
        while True:
            filePos = file.tell()
            lineLst = file.readline().strip().split(' ')
            
            if len(lineLst) == 1:
                break
            
            edge = self.createEdgeFromLineLst(lineLst)
            
            if type(edge) is not Edge:
                break
            
            self.incrementVerticesDegreeFromEdge(edge)
            
            self.addEdgeToComponents(edge, components)
            
        file.seek(filePos)
        
        return components
    
    def createEdgeFromLineLst(self, lineLst):
        edge = []
        
        if len(lineLst) < 2:
            return None
        
        try:
            for i in range(len(lineLst)):
                if lineLst[i] != '':
                    edge.append(int(lineLst[i]))
                    
            if len(edge) == 2:
                return Edge(tuple(edge))
            elif len(edge) > 2:
                return Edge(tuple(edge[:len(edge)-1]), edge[len(edge)-1])
        except Exception as e:
            print("Graph.createEdgeFromLineLst : %s" % str(e))
            return e
    
    def incrementVerticesDegreeFromEdge(self, edge):
        try:
            self.vertices[edge.getVertices()[0]].incrementOutDegreeBy(1)
            self.vertices[edge.getVertices()[1]].incrementInDegreeBy(1)
        except Exception as e:
            print("Grapgh.incrementVerticesDegreeFromEdge : %s" % (str(e)))
            
    def addEdgeToComponents(self, edge, components = None):
        if components is None:
            components = self.components
            
        iComponentOfEdgeOut = None
        iComponentOfEdgeIn = None
        
        for iComponent in range(len(components)):
            for cEdge in components[iComponent]:
                if edge.getVertices()[0] in cEdge.getVertices():
                    iComponentOfEdgeOut = iComponent
                    
                    if iComponentOfEdgeIn is not None:
                        break
                elif edge.getVertices()[1] in cEdge.getVertices():
                    iComponentOfEdgeIn = iComponent
                    
                    if iComponentOfEdgeOut is not None:
                        break
                    
            if ((iComponentOfEdgeOut is not None) and (iComponentOfEdgeIn is not None)):
                break
            
        if iComponentOfEdgeOut is not None and iComponentOfEdgeIn is None:
            components[iComponentOfEdgeOut].append(edge)
        elif iComponentOfEdgeOut is None and iComponentOfEdgeIn is not None:
            components[iComponentOfEdgeIn].append(edge)
        elif iComponentOfEdgeOut is None and iComponentOfEdgeIn is None:
            components.append([edge])
        elif iComponentOfEdgeOut == iComponentOfEdgeIn:
            components[iComponentOfEdgeOut].append(edge)
        elif iComponentOfEdgeOut != iComponentOfEdgeIn:
            components[iComponentOfEdgeOut] = components[iComponentOfEdgeOut] + components[iComponentOfEdgeIn]
            components[iComponentOfEdgeOut].append(edge)
            del components[iComponentOfEdgeIn]
                    
    def getVertices(self):
        return self.vertices
        
    def setVertices(self, vertices):
        self.vertices = vertices     
        
    def getComponents(self):
        return self.components
        
    def setComponents(self, components):
        self.components = components
        
    def findAllEdges(self):
        edges = []
        for component in self.components:
            for edge in component:
                edges.append(edge)
                
        return edges
        
    def getType(self):
        return self.type
        
    def setType(self, graphType):
        self.type = graphType
    
    def __str__(self):
        edgeType = ""
        
        if self.type is Graph.DIRECTED:
            edgeType += "\nARCS:\n"
        elif self.type is Graph.UNDIRECTED:
            edgeType += "\nEDGES:\n"
        
        gStr = str(self.type) + "\n"
        gStr += "VERTICES:\n"
        for verticeNumber in self.vertices:
            gStr += (str(self.vertices[verticeNumber]) + "\n")
        gStr += "COMPONENTS: " + str(len(self.components)) + "\n"
        
        for i in range(len(self.components)):
            gStr += "Component Number: " + str(i+1)
            gStr += edgeType
            for edge in self.components[i]:
                gStr += (str(edge))
            gStr += "\n"
            
        return gStr