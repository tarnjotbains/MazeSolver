import pygame 
from pygame.locals import * 
import random 

class Line():
    """
    A class that represents a line. 
    
    Attributes
    ----------
    start_pos : Tuple
        X and Y coordinates for where line begins.
    end_pos : Tuple
        X and Y coordinates of where line ends.
        
    """ 
    def __init__(self, start_pos, end_pos):
        """
        Initializes a line. 

        Parameters
        ----------
        start_pos : Tuple
            X and Y coordinates for where line begins.
        end_pos : Tuple
            X and Y coordinates of where line ends.

        Returns
        -------
        None.

        """
        self.start_pos = start_pos
        self.end_pos = end_pos


class MazeNode:
    """
    A class that represents a node on a graph called maze.  
    
    Attributes
    ----------
    data: Tuple
        X and Y coordinates for where the MazeNode resides.  
    
    visited: bool
        True if the tuple has been visited in graph navigation. 
        
    left_neighbor: MazeNode 
        A pointer to the left neighbor, if it exists. 
    
    right_neighbor: MazeNode 
        A pointer to the right neighbor, if it exists. 
    
    top_neighbor: MazeNode 
        A pointer to the top neighbor, if it exists. 
    
    bottom_neighbor: MazeNode 
        A pointer to the bottom neighbor, if it exists. 
        
    neighbor_list: list
        A list of neighbors. 
    
    border_left: Line
        A line representing the border between MazeNode and it's left neighbor. 
    
    border_right: Line
        A line representing the border between MazeNode and it's right neighbor. 
    
    border_top: Line
        A line representing the border between MazeNode and it's top neighbor. 
    
    border_bottom: Line
        A line representing the border between MazeNode and it's bottom neighbor. 
        
    border_list: list
        A list of borders. 
        
    root: MazeNode 
        Represents the neighbor that was visited prior in graph navigation. 
    
    weight: int
        Represents the weight of the path that was taken to MazeNode, 
        -1 if it has not been visited yet.
        
    drawn: bool
        True iff MazeNode is currently being drawn to a screen. 
        
    draw_type: str
        A string representing the current state of the node, MazeNode if it's
        not being traversed, path if it lies on a path, search if its currently
        being traversed by dijkstra's. 
    
    color: Tuple
        An RGB tuple representing the color of the node.

    path_node: bool
        True iff MazeNode resides on a path. 
    
    path_type: str
        A string representing whether MazeNode lies on a optimal or non-optimal
        path, exists iff MazeNode lies on a path. 
    
    drawing_path: bool
        True iff MazeNode exists on a path and that path is currently being drawn
        to the screen. 
        
    """
    def __init__(self, data):
        """
        Initializes a maze node with position: data. 

        Parameters
        ----------
        data : Tuple
            An X and Y coordinate of where MazeNode resides on graph. 

        Returns
        -------
        None.

        """
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

        # For Djikstras
        self.root = None 
        self.weight = -1

        # For visualization purposes
        self.drawn = False 
        self.draw_type = ""
        self.color = None
        self.path_node = False 
        self.path_type = None 
        self.drawing_path = None 
    
    def generate_borders(self):
        """
        Creates borders between MazeNode and all of it's neighbors. 

        Returns
        -------
        None.

        """
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
        """
        Removes the border between MazeNode and the specified neighbor. 

        Parameters
        ----------
        neighbor : MazeNode 
            Neighbor with whom the border will be removed from. 

        Returns
        -------
        None.

        """
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
        """
        For every border in border_list, draws those borders to the screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to which MazeNode will be drawn. 

        Returns
        -------
        None.

        """
        for line in self.border_list: 
            pygame.draw.line(screen, (255,0,0), line.start_pos, line.end_pos)
            

    def draw(self, screen): 
        """
        Draws MazeNode to screen. 

        Parameters
        ----------
        screen : pygame.display
            The screen to which MazeNode will be drawn. 

        Returns
        -------
        None.

        """
        if self.draw_type == 'maze_node': 
            pygame.draw.rect(screen, self.color, pygame.Rect(self.data[0]*40 + 1, self.data[1]*40 + 1, 40,40))

        if self.draw_type == 'path':
            pygame.draw.line(screen, (255,255,0), (self.data[0]*40 +20, self.data[1]*40+20), (self.root.data[0]*40+20, self.root.data[1]*40+20))

        if self.draw_type == 'search': 
            pygame.draw.rect(screen, (153,0,76) , pygame.Rect(self.data[0]*40+15, self.data[1]*40 + 15, 10,10))

    def __lt__(self,other):
        """
        Returns true if MazeNode's weight is less than "others" weight. 

        Parameters
        ----------
        other : MazeNode
            The other node to which comparison will be made. 

        Returns
        -------
        bool
            self explanatory. 

        """
        return self.weight < other.weight



    


    

    

