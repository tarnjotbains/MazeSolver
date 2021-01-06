import pygame 
from pygame.locals import * 
import random 

class Line(): 
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos


class MazeNode: 
    def __init__(self, data): 
        self.data = data
        self.visited = False
        
        self.left_neighbor= None
        self.right_neighbor = None
        self.top_neighbor = None
        self.bottom_neighbor = None 
        self.neighbor_list = [] 

        self.border_left = None
        self.border_right = None
        self.border_top = None
        self.border_bottom = None
        self.border_list = []

        #For Djikstras
        self.root = None 
        self.weight = -1
    
    def generate_borders(self): 
        if self.data[0] != 0: 
            start_pos = (self.data[0]*40, self.data[1]*40)
            end_pos = (self.data[0]*40, self.data[1]*40 + 40)
            self.border_left = Line(start_pos, end_pos)
            self.border_list.append(self.border_left) 

        if self.data[0] != 19: 
            start_pos = (self.data[0]*40 + 40, self.data[1]*40)
            end_pos = (self.data[0]*40 + 40, self.data[1]*40 + 40)
            self.border_right = Line(start_pos, end_pos)
            self.border_list.append(self.border_right) 

        if self.data[1] != 0: 
            start_pos = (self.data[0]*40, self.data[1]*40)
            end_pos = (self.data[0]*40 + 40 , self.data[1]*40)
            self.border_top = Line(start_pos, end_pos)
            self.border_list.append(self.border_top) 

        if self.data[1] != 19: 
            start_pos = (self.data[0]*40, self.data[1]*40 +40)
            end_pos = (self.data[0]*40 + 40, self.data[1]*40 + 40)
            self.border_bottom = Line(start_pos, end_pos)
            self.border_list.append(self.border_bottom) 
    
    def remove_border(self, neighbor): 
        if neighbor.data[0] == (self.data[0] + 1): 
            self.border_list.remove(self.border_right)
            self.border_right = None 
        if neighbor.data[0] == (self.data[0] - 1): 
            self.border_list.remove(self.border_left)
            self.border_left = None
        if neighbor.data[1] == (self.data[1] - 1): 
            self.border_list.remove(self.border_top) 
            self.border_top = None
        if neighbor.data[1] == (self.data[1] + 1): 
            self.border_list.remove(self.border_bottom) 
            self.border_bottom = None

    def draw_border(self, screen): 
        for line in self.border_list: 
            pygame.draw.line(screen, (255,0,0), line.start_pos, line.end_pos)

    def draw(self, screen, color): 
        
        pygame.draw.rect(screen,color, pygame.Rect(self.data[0]*40+15, self.data[1]*40 + 15, 10,10) ) 


    def __lt__(self,other): 
        return self.weight < other.weight



    


    

    

