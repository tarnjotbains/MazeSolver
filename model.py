import random 

class graph: 
    def __init__(self, graph_dict):
        self.graph_dict = graph_dict

    def verticies(self):
        return list(self.graph_dict.keys()) 
    
    def edges(self): 
        return self.generate_edges()
    
    def add_vertex(self, vertex): 
        if vertex not in self.verticies(): 
            self.graph_dict[vertex] = [] 

    def add_edge(self, edge): 
        vertex1, vertex2 = edge 

        if vertex1 not in self.verticies():
            self.graph_dict[vertex1].append(vertex2) 
        elif vertex1 in self.verticies(): 
            self.graph_dict[vertex1].append(vertex2)


    def generate_edges(self): 
        edges = [] 
        for vertex in self.graph_dict: 
            for neighbour in self.graph_dict[vertex]: 
                edges.append((vertex, neighbour)) 
        return edges 


class Node: 
    def __init__(self,data): 
        
        self.left= [None, False]
        self.right = [None, False]
        self.top = [None, False]
        self.bottom = [None, False]

        self.data = data
    
    def is_neighbour(self, node2): 

        if self.data[1] == node2.data[1]: 
            if self.data[0] == node2.data[0] -1 or self.data[0] == node2.data[0] + 1: 
                return True 

        if self.data[0] == node2.data[0]: 
            if self.data[1] == node2.data[1] -1 or self.data[1] == node2.data[1] + 1: 
                return True

        return False 
        






    


    

    

