import pygame 
from pygame.locals import * 
import random 

#initialize pygame
pygame.init() 

#title and icon
pygame.display.set_caption("Maze Solver")
icon = pygame.image.load('icon.png') 
pygame.display.set_icon(icon) 

#create a screen
screen = pygame.display.set_mode((800,800))

#load images
seekerImg = pygame.image.load('seeker.png')
itemImg = pygame.image.load('item.png')


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
        self.weight = 1
    
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

    def draw_border(self): 
        for line in self.border_list: 
            pygame.draw.line(screen, (255,0,0), line.start_pos, line.end_pos) 





def generate_maze_nodes(): 
    node_list = []
    for j in range(0,20): 
        for i in range(0,20): 
            node = MazeNode((i,j))
            node.generate_borders()
            node_list.append(node)
    return node_list 

def generate_neighbors(node_list): 
    for i in range(0,len(node_list)): 
        node = node_list[i]
        if node.data[0] != 0: 
            node.left_neighbor = node_list[i - 1]
            node.neighbor_list.append(node.left_neighbor)
        if node.data[0] != 19: 
            node.right_neighbor = node_list[i + 1]
            node.neighbor_list.append(node.right_neighbor)
        if node.data[1] != 0: 
            node.top_neighbor = node_list[ i - 20] 
            node.neighbor_list.append(node.top_neighbor)
        if node.data[1] != 19:  
            node.bottom_neighbor = node_list[i + 20]
            node.neighbor_list.append(node.bottom_neighbor)


def carve(node, node_list, screen): 
    node.visited = True 


    random.shuffle(node.neighbor_list) 
    screen.fill((0,0,0))
    draw_borders(node_list, screen)
    pygame.display.update() 
    for neighbor in node.neighbor_list: 
        if neighbor.visited == False: 
            node.remove_border(neighbor) 
            neighbor.remove_border(node)  
            pygame.display.flip() 
            carve(neighbor, node_list, screen) 

    
    return 


#Djikstras: Still working on this.... 
"""def search(node, node_goal): 

    if node == node_goal: 
        #do something 
    
    unvisited_neighbors = [] 
    min_distance = 0 
    for neighbor in node.neighbor_list: 
        if neighbor.visited == False: 
            if neighbor.weight > neighbor.weight + node.distance
                neighbor.weight += node.distance 
                if min_distance == 0 or neighbor.weight < min_distance:
                    min_distance = neighbor.weight 

            unvisited_neighbors.append(neighbor) 
    
    for unvisited_neighbor in unvisited_neighbors: 
        if unvisited_neighbor.distance == min_distance: 
            node.visited = True 
            search(unvisited_neighbor)""" 


    





def reset_visited(node_list): 
    for node in node_list: 
        node.visited = False 

def draw_borders(node_list, screen): 
    for node in node_list:
        for line in node.border_list: 
            pygame.draw.line(screen, (255,0,0), line.start_pos, line.end_pos) 



def draw_prompt(prompt):
    font = pygame.font.Font('font.ttf', 32) 
    draw_seeker = font.render(prompt, True, (255,255,255)) 
    screen.blit(draw_seeker, (160,200))

node_list = generate_maze_nodes() 
generate_neighbors(node_list) 
pygame.display.update() 

def run_maze(): 
    global screen 
    running = True 


    global node_list 
    
    

    maze_carved = False
    seeker_in_position = False 
    item_in_position = False 

    while running: 
        screen.fill((0,0,0))

        draw_borders(node_list, screen) 
        if maze_carved == False: 
            carve(node_list[45], node_list, screen)  
            maze_carved = True 
            pygame.display.update()
            maze_carved = True  

        # Reset state of all nodes to unvisited so we can use djikstras. 
        reset_visited(node_list) 

        for event in pygame.event.get(): 
            if event.type == QUIT: 
                exit()
            if event.type == MOUSEBUTTONDOWN and seeker_in_position and not item_in_position:
                mx, my = pygame.mouse.get_pos() 
                mx , my = mx//40 , my//40
                itemX , itemY = (mx*40+10, my*40+10)
                item_in_position = True 


            if event.type == MOUSEBUTTONDOWN and maze_carved and not seeker_in_position: 
                mx, my = pygame.mouse.get_pos() 
                mx , my = mx//40 , my//40
                seekerX , seekerY = (mx*40+5, my*40+5)
                seeker_in_position = True 

                # Find starting node in node_list. 
                for maze_node in node_list: 
                    if maze_node.data == (mx,my):
                        seeker_node = maze_node
                        seeker_node.weight = 0               


        # Player prompt to place seeker. 
        if maze_carved == True and not seeker_in_position: 
            mx, my = pygame.mouse.get_pos() 
            mx , my = mx//40 , my//40  
            screen.blit(seekerImg, (mx*40+5, my*40+5))
            draw_prompt("use mouse to place seeker")  
            

        # Player prompt to place item. 
        if seeker_in_position and not item_in_position:
            mx, my = pygame.mouse.get_pos()
            mx , my = mx//40 , my//40  
            screen.blit(itemImg, (mx*40+10, my*40+10))
            draw_prompt("use mouse to place the item") 


        # Draw seeker and item on screen.  
        if seeker_in_position:
            screen.blit(seekerImg, (seekerX, seekerY))
        if item_in_position:
            screen.blit(itemImg, (itemX, itemY))

        pygame.display.update() 

        

    
        

    



run_maze() 