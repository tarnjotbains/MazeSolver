import pygame 
from pygame.locals import * 
import random 
from queue import PriorityQueue
from model import MazeNode, Line 
import time

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


def generate_maze_nodes():
    """
    Creates MazeNodes which lie on a 20x20 grid. 

    Returns
    -------
    node_list : list
        A list of created MazeNodes. 

    """
    node_list = []
    for j in range(0,20): 
        for i in range(0,20): 
            node = MazeNode((i,j))
            node.generate_borders()
            node_list.append(node)
    return node_list 

def generate_neighbors(node_list):
    """
    Initializes the neighbors of MazeNodes in a list. 

    Parameters
    ----------
    node_list : list
        A list of MazeNodes. 

    Returns
    -------
    None.

    """
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
    """
    Creates a maze. 
    Uses depth-first-search to navigate a graph of MazeNodes and removes borders
    as it traverses. 

    Parameters
    ----------
    node : MazeNode
        Node that is currently being traversed. 
    node_list : list
        A list of MazeNodes 
    screen : pygame.display
        The screen on which node resides. 

    Returns
    -------
    None.

    """
    node.visited = True 
    random.shuffle(node.neighbor_list) 
    
    # Set drawing paramaters of current node. 
    node.drawn = True 
    node.color = (255,204,255) 
    node.draw_type = 'maze_node'

    # Draw the entire screen (with borders and nodes).
    screen.fill((0,0,0))
    draw_nodes(node_list, screen) 
    draw_borders(node_list, screen)
    pygame.display.update()

    # Draw the color of the current node highlighted. 
    time.sleep(0.04) 
    node.color = (51,0,25) 
    node.draw(screen) 
    pygame.display.update() 

    for neighbor in node.neighbor_list: 
        if neighbor.visited == False: 
            
            # Apply border visuals        
            node.remove_border(neighbor) 
            neighbor.remove_border(node)  
            pygame.display.flip() 

            # Recurse
            carve(neighbor, node_list, screen) 
    return 

def update_neighbors(node_list):
    """
    Based on the borders of nodes in node_list, updates the neighbors so that
    if a node has a border between another node, they are no longer neighbors. 

    Parameters
    ----------
    node_list : list
        A list of MazeNodes 

    Returns
    -------
    None.

    """
    for node in node_list:
        if node.border_left and node.left_neighbor:
            node.neighbor_list.remove(node.left_neighbor) 
            node.left_neighbor = None 
        if node.border_right and node.right_neighbor: 
            node.neighbor_list.remove(node.right_neighbor)
            node.right_neighbor = None
        if node.border_top and node.top_neighbor: 
            node.neighbor_list.remove(node.top_neighbor) 
            node.top_neighbor = None 
        if node.border_bottom and node.bottom_neighbor: 
            node.neighbor_list.remove(node.bottom_neighbor) 
            node.bottom_neighbor = None                 

def run_dijkstras(seeker_node, item_node):
    """
    Creates a priority queue and a order in which to remove failed dijkstra's
    paths and calls helper 'search'.

    Parameters
    ----------
    seeker_node : MazeNode
        The node we wish to start Dijkstra's algorithm from. 
    item_node : MazeNode
        The Node we are searching for. 

    Returns
    -------
    delete_order : list
        A list of all nodes searched in dijkstra's path sorted by traversal. 

    """
    q = PriorityQueue() 
    delete_order = [] 
    search(seeker_node,q, item_node, delete_order)
    return delete_order 

def search(node, queue, node_goal, delete_order):
    """
    Runs Dijkstra's algorithm until node is node_goal, fills delete_order as it
    traverses. 

    Parameters
    ----------
    node : MazeNode
        The node that is currently being viewed in Dijksta's algorithm. 
    queue : queue
        A priority queue which contains nodes by weight. 
    node_goal : MazeNode 
        The node that search is searching for. 
    delete_order : list
        A list of all nodes searched in dijkstra's path sorted by traversal. 

    Returns
    -------
    MazeNode, None 
        DESCRIPTION.

    """
    if node == node_goal: 
        return node 
    if node_goal.visited == True: 
        return node_goal 
    if node.visited == True: 
        return 

    node.visited = True 
    for neighbor in node.neighbor_list:
        delete_order.append(neighbor) 
        neighbor.draw_type = "search"
        neighbor.draw(screen)
        pygame.display.update()
        time.sleep(0.01) 
        
        if not neighbor.visited: 
            if neighbor.weight != -1: 
                if neighbor.weight > node.weight + 1:
                    neighbor.root = node
                    queue.put((node.weight + 1, neighbor))
                    neighbor.weight  =  node.weight + 1
            elif neighbor.weight == -1: 
                neighbor.root = node 
                queue.put((node.weight + 1, neighbor))
                neighbor.weight = node.weight + 1 
    
    node_to_visit = queue.get()[1] 
    search(node_to_visit, queue, node_goal, delete_order) 

def reset_visited(node_list):
    """
    Resets the visited status of all nodes in node_list to False. 

    Parameters
    ----------
    node_list : list
        A list of MazeNodes. 

    Returns
    -------
    None.

    """
    for node in node_list: 
        node.visited = False 

def draw_borders(node_list, screen):
    """
    Draws the border of all nodes in node_list to the screen. 

    Parameters
    ----------
    node_list : list
        A list of MazeNodes. 
    screen : pygame.display
        The screen on which nodes in node_list reside. 

    Returns
    -------
    None.

    """
    for node in node_list:
        for line in node.border_list: 
            pygame.draw.line(screen, (255,0,0), line.start_pos, line.end_pos) 

def draw_prompt(prompt):
    """
    Draws a prompt to screen. 

    Parameters
    ----------
    prompt : str
        The prompt to display. 

    Returns
    -------
    None.

    """
    font = pygame.font.Font('font.ttf', 32) 
    draw_seeker = font.render(prompt, True, (255,255,255)) 
    screen.blit(draw_seeker, (160,200))

def draw_nodes(node_list, screen):
    """
    Draws all nodes in node_list to screen. 

    Parameters
    ----------
    node_list : list
        A list of MazeNodes. 
    screen : pygame.display
        The screen to which nodes will be drawn to. 

    Returns
    -------
    None.

    """
    for node in node_list: 
        if node.drawn:
            node.draw(screen)

def remove_dijkstras_path(delete_order, screen, seekerImg, seekerX, seekerY, node_list): 
    """
    Removes dijkstra's path from screen.

    Parameters
    ----------
    delete_order : list
        The order in which to remove nodes. 
    screen : pygame.display
        The display from which nodes will be removed. 
    seekerImg : pygame.image
        The image containing the seeker. 
    seekerX : int
        X position of seeker. 
    seekerY : int
        Y position of seeker. 
    node_list : list
        A list of MazeNodes. 

    Returns
    -------
    None.

    """    
    for node in delete_order: 
        if not node.path_node:
            node.draw_type = "maze_node"
            draw_nodes(node_list, screen) 
            draw_borders(node_list, screen) 
            screen.blit(seekerImg, (seekerX, seekerY))
            pygame.display.update() 

def draw_path(item_node, seeker_node, screen):
    """
    Draws the optimal path from item_node to seeker_node. 

    Parameters
    ----------
    item_node : MazeNode
        The ending node in Dijkstra's optimal path. 
    seeker_node : MazeNode
        The ending node in Dijkstra's optimal path. 
    screen : pygame.display
        The screen on which path will be drawn. 

    Returns
    -------
    None.

    """
    current_node = item_node
    while current_node != seeker_node: 
        current_node.draw_type = "path"
        current_node.path_node = True 
        current_node.drawing_path = True 
        time.sleep(0.02) 
        current_node.draw(screen) 
        current_node.drawn = True
        pygame.display.update()
        current_node = current_node.root 

def run_maze():
    """
    The Game loop.
    See comments below for a step by step description of what this function
    does. 

    Returns
    -------
    None.

    """
    global screen
    node_list = generate_maze_nodes() 
    generate_neighbors(node_list)

    # Boolean values used to update the view at certain times. 
    maze_carved = False
    seeker_in_position = False 
    item_in_position = False 
    path_generated = False 
    path_drawn = False 
    running = True 

    while running: 

        # Make the background.
        screen.fill((51,0,25))

        # Draw all nodes that have a drawn value of true. 
        draw_nodes(node_list, screen)   

        # Draw borders around nodes
        draw_borders(node_list, screen)
                       
        # Create the maze. 
        if maze_carved == False:
            start_index= random.randint(0,399)
            carve(node_list[start_index], node_list, screen)  
            maze_carved = True 
            pygame.display.update()
            maze_carved = True  
            # Reset state of all nodes to unvisited for Dijkstra's. 
            reset_visited(node_list) 
            update_neighbors(node_list) 

        # Handle Events 
        for event in pygame.event.get(): 
            # If user closes the program. 
            if event.type == QUIT: 
                exit()

            # If user places the item.     
            if event.type == MOUSEBUTTONDOWN and seeker_in_position and not item_in_position:
                mx, my = pygame.mouse.get_pos() 
                mx , my = mx//40 , my//40
                itemX , itemY = (mx*40+10, my*40+10)
                item_in_position = True 

                for maze_node in node_list: 
                    if maze_node.data == (mx,my):
                        item_node = maze_node 

            # If user places the seeker. 
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

        # Run Djikstras 
        if seeker_in_position and item_in_position:
            delete_order = run_dijkstras(seeker_node, item_node) 
            path_generated = True 
        
        # Draw path from seeker to item (frame by frame). 
        if path_generated and not path_drawn:
            draw_path(item_node, seeker_node, screen) 
            remove_dijkstras_path(delete_order, screen, seekerImg, seekerX, seekerY, node_list) 
            path_drawn = True 

        # Update the view. 
        pygame.display.update() 

if __name__ == "__main__":
    run_maze() 