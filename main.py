import pygame 
from pygame.locals import * 
from model import Node
import random 


#initialize pygame
pygame.init() 

#title and icon
pygame.display.set_caption("Maze Solver")
icon = pygame.image.load('icon.png') 
pygame.display.set_icon(icon) 

#create a screen
screen = pygame.display.set_mode((800,800))



node_list = []
edge_list = [] 

for i in range(0,20): 
    for j in range(0,20): 
        node = Node((i,j))
        if i == 0: 
            node.left[1] = True
        if i == 19:
            node.right[1] = True
        if j == 0:
            node.top[1] = True
        if j == 19: 
            node.bottom[1] = True
        node_list.append(node)

        if j != 0:
            node_list[-1].left[0] = node_list[-2] 
            if j != 19:
                node_list[-2].right[0] = node_list[-1]
        if i!= 0: 
            node_list[-1].top[0] = node_list[-21]
            if i != 19:
                node_list[-21].bottom[0] = node_list[-1]


def carve_passages(node): 

    random.shuffle(node_list) 
    global screen
    color = (0,0,255)

    if not node: 
        return False
    
    if node.left[1] and node.right[1] and node.top[1] and node.bottom[1]:
        pygame.draw.rect(screen,color, pygame.Rect(node.data[0]*40+1, node.data[1]*40 + 1, 35,35) )
        pygame.display.flip() 
        return True 
    
    if not node.left[1]: 
        node.left[1] = True
        if carve_passages(node.left[0]) == True: 
            pygame.draw.line(screen, (255,45,255), (node.data[0]*40, node.data[1]*40), (node.data[0]*40, node.data[1]*40 + 40))

    elif not node.right[1]:
        node.right[1] = True
        carve_passages(node.right[0]) 
    elif not node.top[1]:
        node.top[1] = True
        carve_passages(node.top[0]) 
    elif not node.bottom[1]:
        node.bottom[1] = True
        carve_passages(node.bottom[0]) 



def redraw(): 
    global screen
    screen.fill((255,255,255))
    
    
    for i in range(0,20): 
        pygame.draw.line(screen, (0,255,255), (0,i*40), (800,i*40))
        pygame.draw.line(screen, (0,255,255), (i*40,0), (i*40, 800))

    pygame.display.update() 


def run_game(): 
    global screen
    global node_list
    redraw() 
    clicking = False

    #gameloop
    running = True 
    print("about to run carve") 
    while running: 
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                exit() 
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1: 
                    clicking = True 
            if event.type == MOUSEBUTTONUP:
                if event.button == 1: 
                    clicking = False
        
        if clicking == True: 
            mx, my = pygame.mouse.get_pos()
            mx , my = mx//40, my//40
            

            color = (0,0,255)
            pygame.draw.rect(screen,color, pygame.Rect(mx*40+1, my*40 + 1, 39,39) )

            pygame.display.flip() 
            

    
        carve_passages(node_list[0]) 
        
            


    pygame.display.update() 


run_game() 