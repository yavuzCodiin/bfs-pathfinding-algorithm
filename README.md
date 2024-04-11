# bfs-pathfinding-algorithm
This repository contains material related to the BFS path-finding algorithm, from creating the maze to using the algorithm and creating an interactive demo.

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/bc925365-3cd8-432b-9f73-a1a3c8205474)

## <u>Installing</u>

`python3 -m pip install -U pygame`

## <u>How to use</u>
1. `mkdir path-finding`
2. `cd path-finding`
3. `git clone https://github.com/yavuzCodiin/bfs-pathfinding-algorithm.git`
4. `python3 main_interactive.py`

## <u>What is Pathfinding?</u>

Pathfinding is the computational process of finding a path between two points. It is a fundamental concept in computer science, used in various fields such as robotics, video games, transportation, and network data flow. The goal of pathfinding algorithms is to find the most efficient route from the starting point to the destination, often while navigating through possible obstacles and adhering to certain rules or constraints.

* For example, in GPS navigation systems used in cars and smartphones. These systems calculate the shortest or fastest route from your current location to your desired destination.

* In robotics, pathfinding algorithms enable autonomous robots to navigate through environments, from simple vacuum cleaning robots that need to cover an entire floor efficiently without retracing their steps, to more complex industrial robots that move materials between different points in a manufacturing plant. 

* In video games, non-player characters (NPCs) must navigate the game world. Algorithms like A* and its variations are commonly used to calculate paths for characters to move from one point to another, ensuring that they can find their way around obstacles and interact with the player and the environment in a realistic manner.

## <u>Common Pathfinding Algorithms</u>

### <u>A* (A-Star) Algorithm</u>
The A* algorithm is one of the most popular and widely used pathfinding algorithms, known for its efficiency and accuracy. It combines features of Dijkstra's Algorithm (which focuses on finding the shortest path) and the Best-First-Search, making it highly effective in a variety of scenarios. A* uses a heuristic to estimate the cost from the current node to the goal, reducing the number of nodes it needs to explore. This makes it particularly suitable for applications where a balance between speed and accuracy is crucial, such as in video games or robotic path planning.

### <u>Dijkstra's Algorithm</u>
Dijkstra's Algorithm is a foundational algorithm for finding the shortest path between nodes in a graph. It works by systematically exploring all possible paths, starting from the initial node, and continuously expanding the closest node until it reaches the destination. While it guarantees the shortest path, it can be slower than A* because it doesn't use a heuristic to guide its search.

### <u>Floyd-Warshall Algorithm</u>
The Floyd-Warshall algorithm is a comprehensive algorithm used for finding shortest paths in a weighted graph with positive or negative edge weights (but with no negative cycles). It's capable of finding the shortest paths between all pairs of nodes. While not as commonly used in real-time applications due to its computational complexity, it's extremely powerful for pre-calculating paths or analyzing dense networks.

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/8a07a3bf-9e2c-4078-a13e-2c14efa684de)

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/c1f3db80-e8d3-47e8-85b4-e89190f3918b)

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/deeaed27-9ccb-4331-94a8-74a2e21628f9)

### <u>Best-First Search</u>
Best-First Search (BFS) is an algorithm used for traversing or searching tree or graph data structures. It starts at a selected node (often the root in the case of trees, or any arbitrary node for graphs) and explores all of the neighbor nodes at the present depth prior to moving on to the nodes at the next depth level. It's called "Best-First" because it expands the frontier between discovered and undiscovered nodes uniformly across the Best of the frontier.

## <u>General Process</u>

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/4f89370b-48b6-4a7a-bc40-629870e6b0f1)

## <u>Path Finding</u>
In this project, I started by figuring out how to construct a maze. Once I had a grasp on that, I moved on to understanding the pathfinding algorithm and how it could work within the maze I created. My next step was to think about how to visually represent both the maze and the algorithm's pathfinding process. This is where Pygame came into play. I used Pygame to not only create the maze but also to visualize the algorithm in action. Finally, I wanted to make the whole experience interactive, so I added the ability for users to control the visualization, allowing them to move forwards and backwards through the steps of the algorithm. This approach helped me connect all the different parts of my project, from the maze creation to the algorithm implementation and visualization.

- ### <u>Creating Maze</u>
I tried to give well documented clear code and every function has its docstring but I will also add my comments too this is same for other parts of the project too.
 
```python
import copy, random, types
from enum import Enum
```
I first created Cell structure, each cell will have two type, one of them will be `Empty` which our algorithm can move and search through and `Block` for walls of our maze  
```python
class CellType(Enum):
    Empty = 1
    Block = 2
```
We have marks on cells so one will be for `Start` and `End` and `No` for rest 
```python
class CellMark(Enum):
    No = 0
    Start = 1
    End = 2
```
Here cell is initialized each cell will have these attributes `type`, and `mark` as we defined previously, `position`, `count` for counting steps, `path_from` for storing where it came from
```python
class Cell:
    def __init__(self, type = CellType.Empty, pos = None):
        self.type = type
        self.pos = pos
        self.count = 0
        self.path_from = None
        self.mark = CellMark.No
```
A cell network formed by the combination of cell objects
```python
class Cell_Network:
    def __init__(self, board):
        self.board = board
```
With `get_size` we get board's height and width.

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/b629159a-9f1e-42e2-a25f-9f30e2f34ac6)

```python
    def get_size(self):
        """

        Get the size of the board. This method returns the dimensions of the board as a list, where the first element is the number of rows (height) and the second element is the number of columns (width).

        Parameters:
        ----------
        self : object
            The instance of the class from which this method is called. It must have a `board` attribute, which is a list of lists representing the grid.

        Returns:
        -------
        list of int
            A list containing two integers:
            - The first integer represents the number of rows(height) in the board.
            - The second integer represents the number of columns(width) in the board.

        """
        return [len(self.board), len(self.board[0])]
```
We will get our cell position located `at` specified position
```python
    def at(self, pos):
        """

        Retrieve the cell object at a specified position in the board.

        Parameters:
        ----------
        self : object
            The instance of the class from which this method is called.
        
        pos : list or tuple of int
            A list or tuple containing the [row_index, column_index] of the cell.

        Returns:
        -------
        Cell
          The cell object located at the specified position.

        """
        return self.board[pos[0]][pos[1]]
```
Simply cloning the board
```python
    def clone(self):
        """
        Clone the board.
        
        Parameters:
        ----------
        self : object
            The instance of the class from which this method is called.

        Returns:
        -------
        Cell_Network
          A copy of the board.

        """
        return Cell_Network(copy.deepcopy(self.board))
```
Clearing the board with specified count for example at the beginning we have infinite possibilities right, so we give count = math.inf to make count of each cell equals to infinity

```python
    def clear_count(self, count):
        """

        Clear the count of each cell

        Parameters:
        -----------
          self (object):
            The instance of the class from which this method is called.

          count (int): The number we want to give all the cell count.
        
        Returns:
        --------
          None  
        
        """
        for o in self.board:
            for i in o:
                i.count = count
                i.path_from = None
```
We need to make sure if the position is valid point, and that it appears within the boundaries of the board. 

```python
    def is_valid_point(self, pos):
        """

        Check if the given position is within the bounds of the board.
    
        Parameters:
        ----------
        self : object
            The instance of the class from which this method is called.
        
        pos : list or tuple of int
            A list or tuple containing the [row_index, column_index] of the cell.
    
        Returns:
        -------
        bool
          True if the position is within the bounds of the board, False otherwise.

        """
        sz = self.get_size()
        return (pos[0] >=0) and (pos[1] >= 0) and (pos[0] < sz[0]) and (pos[1] < sz[1])
```

We create empty maze with `create_empty_maze` it takes width and height of maze and returns namespace with attributes like `board` which is created by combination of cells, also we have `start` and `end` positions.

```python
def create_empty_maze(x, y): #create empty maze with board, start, end attributes
    """
    
    Create a empty maze and return its structure along with start and end points

    Parameters:
    ----------
    x (int):
        The width of the maze (number of cells horizontally).
 
    y (int):
        The height of the maze (number of cells vertically).

    Returns
    -------
    types.SimpleNamespace
        A namespace with the following attributes:
          - board : list of list of Cell objects
              The maze structure represented as a 2D grid.
          - start : list of int
              The starting coordinates [x, y] in the maze.
          - end : list of int
              The ending coordinates [x, y] in the maze.

    """
    return types.SimpleNamespace(
        board = Cell_Network( [[Cell(type=CellType.Empty, pos=[ix, iy]) for iy in range(y) ] for ix in range(x)] ),
        start=[random.randrange(0, x), random.randrange(0, y)],
        end= [random.randrange(0, x), random.randrange(0, y) ]
    )
```

With `create_wall_maze` we created a whole maze with walls, again it returns namespace with same attributes as `create_empty_maze`.

```python
def create_wall_maze(x, y):
    """

    Create a maze with walls and return its structure along with start and end points.

    Parameters:
    ----------
    x (int):
        The width of the maze (number of cells horizontally).
    y (int):
        The height of the maze (number of cells vertically).

    Returns:
    -------
    types.SimpleNamespace
        A namespace with the following attributes:
            - board : list of list of Cell objects
                The maze structure represented as a 2D grid.
            - start : list of int
                The starting coordinates [x, y] in the maze.
            - end : list of int
                The ending coordinates [x, y] in the maze.
    """
    #board creation
    board = [[Cell(type = CellType.Empty, pos=[ix,iy]) for iy in range(y)] for ix in range(x)]
    
    #wall creation
    for i in range(0,x):
        board[i][int(y/2)].type = CellType.Block
    for i in range(0,y):
        board[int(x/2)][i].type = CellType.Block

    #Wall Opening Creation    
    board[random.randint(0, x/2-1)][int(y/2)].type = CellType.Empty #random opening in the left half of the vertical wall
    board[random.randint(x/2+1, x-1)][int(y/2)].type = CellType.Empty #random opening in the right half of the vertical wall
    board[int(x/2)][random.randint(0, y/2-1)].type = CellType.Empty #random opening in the top half of the horizontal wall
    board[int(x/2)][random.randint(y/2+1, y-1)].type = CellType.Empty #random opening in the bottom half of the horizontal wall

    return types.SimpleNamespace( board = Cell_Network(board),
		start = [random.randrange(0,x/2), random.randrange(y/2+1,y)],
		end = [random.randrange(x/2+1,x), random.randrange(0,y/2)] )
```

I used `add_point` function to calculate the position of neighboring cells. For example if I have [2,3] as position, to move left neighbor I can add [2,3] with [-1,0] 

```python
def add_point(a, b):
    """
    
    Add two points represented by their coordinates.

    This function is typically used to calculate the position of neighboring cells by adding their relative positions to the current cell's position.

    Parameters:
    ----------
    a : list or tuple of int
        The [x, y] coordinates of the first point.
    b : list or tuple of int
        The [x, y] coordinates of the second point, often representing a relative position.

    Returns:
    -------
    list of int
        A list containing the resulting [x, y] coordinates after addition.
    
    """

    return [a[0]+ b[0], a[1]+ b[1]]
```

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/1d0471c9-aaa4-4f3b-95e8-acb9177ae881)

So this is our maze with `Cell`, `CellMark`, `CellType`, `Cell_Network` we have four classes and they have their attributes so along the way we will use them to create algorithm, finding path and visualizing this let's see how our algorithm works.

### <u>Algorithm</u>

> Greedy BeFS 
> Using a greedy algorithm, expand the first successor of the parent. After a successor is generated:
>1. If the successor's heuristic is better than its parent, the successor is set at the front of the queue (with the parent reinserted directly behind it), and the loop restarts.
>
>2. Else, the successor is inserted into the queue (in a location determined by its heuristic value). The procedure will evaluate the remaining successors (if any) of the parent.

Below you can see how our algorithm works in pseudocode to have more information you can visit [wikipedia](https://en.wikipedia.org/wiki/Best-first_search#Greedy_BeFS)

```rust
procedure GBS(start, target) is:
  mark start as visited
  add start to queue
  while queue is not empty do:
    current_node ← vertex of queue with min distance to target
    remove current_node from queue
    foreach neighbor n of current_node do:
      if n not in visited then:
        if n is target:
          return n
        else:
          mark n as visited
          add n to queue
  return failure
```

Our shortest path algorithm requires a board, a start point, an end point, and the maximum distance allowed for the path. It begins by cloning the board, and then it operates on this cloned version. As previously discussed in the context of the cell network, we initialize each cell's count to math.inf. Next, we mark the start and end points on the board. The first position is added to the open list, which we will use to check the cells, setting the start cell's count to 0. We then define our neighbors as [left, right, down, up]. As long as there are cells in the open list, our function continues to operate. It starts by popping the first cell from the list and designating it as the current position. We retrieve the cell at the current position and proceed to check its neighbors. For a neighbor to be considered, it must be a valid point, and its type must be empty. If these conditions are met, we increment the current cell's count by 1 to determine the distance. If this distance is less than the maximum allowed, we assign this distance to the neighbor's count and record the cell it originated from. Finally, we add the neighbor's position to the open list to continue the search process.

While measuring the distance we will use something called Manhattan Distance, it is named after grid shape of streets in Manhattan and in this streets we can't move diagonally so we either move in x or y never both at the same time, so we can't use euclidean distance.

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/c2d007c2-46a2-4377-b1fe-bbc594a57fa7)

This function calculates the distance from start for every cell, not only destination, this is helpful when we think about robots navigation where robot might need to navigate to various points in an environment efficiently. We can use it to calculate the shortest path to any of the nodes. However, if optimization is our priority we'd change the algorithm, when it finds destination it stops.

```python
import my_maze
import math

def fill_shortest_path(board, start, end, max_distance=math.inf):
    """

    Finds and marks the shortest path in a maze from a start point to an end point.

    Parameters:
    ----------
    board (my_maze.Board):
        The board represents the maze structure, where each cell can be empty or a wall.
    
    start (tuple):
        A tuple of two integers representing the starting position (row, column) in the maze.
    
    end (tuple):
        A tuple of two integers representing the ending position (row, column) in the maze.
    
    max_dist (int, optional):
        The maximum distance allowed for the path. If the shortest path exceeds this distance,
        the search is aborted. By default, it is set to `math.inf`, allowing for the maximum
        possible distance.

    Returns:
    -------
    my_maze.Board
        A clone of the original `board` object with the shortest path marked.

"""    
    nboard = board.clone()
    nboard.clear_count(math.inf) #infinite possibilities at start

    nboard.at( start ).mark = my_maze.CellMark.Start
    nboard.at( end ).mark = my_maze.CellMark.End

    open_list = [ start ]
    nboard.at( start ).count = 0
    neighbours = [[-1, 0], [1, 0], [0, 1], [0, -1]]

    while open_list:
        current_pos = open_list.pop(0)
        current_cell = nboard.at( current_pos )
        for neighbour in neighbours:
            ncell_pos = my_maze.add_point(current_pos, neighbour)
            if not nboard.is_valid_point(ncell_pos):
                continue
            cell = nboard.at( ncell_pos )
            
            if cell.type != my_maze.CellType.Empty:
                continue
            
            dist = current_cell.count+1
            if dist > max_distance:
                continue
            
            if cell.count > dist: #math.inf > 1
                cell.count = dist # cell.count = 1
                cell.path_from = current_cell # Records which cell we came from to reach this neighbor
                open_list.append(ncell_pos) #now we will search this This backtracking information
                                            #is used to reconstruct the path once the end cell is reached.
    return nboard
```

We will use backtracking to find shortest path, it works as follows:
1. Start from destination cell.
2. Scan neighbours and pick with lowest number.
3. Repeat the process until you reach start cell.

```python
def backtrack_to_start(board, end):
    """

    Parameters:
    -----------
       board (my_maze.Board):
         The maze board object. The board represents the maze structure, where
         each cell can be empty or a wall.
       
       end (tuple):
         A tuple of two integers representing the ending position (row, column) in the maze.
    
    Returns:
    --------
      list:
        A list of `Cell` objects representing the path from the end position to the start
        position.

    """

    cell = board.at( end )
    path = []
    while cell != None:
        path.append(cell)
        cell = cell.path_from
    
    return path
```

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/d4312888-75ed-4c25-83bc-de6334c14e26)

### <u>Drawing Maze and Path</u>
Until here we created structure of our maze, then we created our shortest path finding algorithm now we will visualize them.

```python
import pygame, math
import my_maze

pygame.init()
pygame.display.set_caption("Demo => Path Finding")
cell_font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
```

This function `trans_rect` is designed to move a rectangle by a specified offset without altering its size.

```python
def trans_rect(r, offset):
    """

    This function takes rect( => x, y, w, h <= ) then adjusts the position of rectangle by applying an offset to it
    
    Parameters:
    -----------
        r (list): This parameter represents rectangle.

        offset (list): This parameter represents the offset by which you want to move the rectangle. 
    
    Returns:
    --------
        (list):
            - The new x-coordinate of the rectangle's top-left corner.
            - The new y-coordinate of the rectangle's top-left corner.
            - The original width of the rectangle.
            - The original height of the rectangle
    
    """
    return [r[0]+offset[0], r[1]+offset[1], r[2], r[3]]
```

Our main loop for controlling the application 

```python
def main_loop(ui):
    """
    
    Run the main event loop of the application.

    This function initializes the display, handles user input events, and updates the display based on the user interface (UI) object's draw method. The loop runs indefinitely until the user quits the application or presses the escape key.

    Parameters
    ----------
      ui : object
        An instance of a user interface class that has `step`, `reset`, and `draw` methods.

    Returns
    -------
      None

    """
    
    screen = pygame.display.set_mode((1000,800))

    clock = pygame.time.Clock()
    clock.tick()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_ESCAPE:
                break
            if event.key == pygame.K_LEFT:
                ui.step(-1)
            if event.key == pygame.K_RIGHT:
                ui.step(1)
            if event.key == pygame.K_r:
                ui.reset()
        
        ui.draw(screen)

        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
```

The Finder class is designed to manage and visualize a board and a path.

```python
class Finder:
    def __init__(self):
        self.board = None
        self.path = None
```

```python
    def set_board(self, board):
        """

        Set the board attribute of the instance.

        Parameters
        ----------
          self : object
            The instance of the class from which this method is called.
        
          board : Board
            The board object to be set for the instance.

        Returns
        -------
          None

        """
        self.board = board
```
```python
    def set_path(self, path):
        """

        Set the path attribute of the instance.

        Parameters
        ----------
          self : object
            The instance of the class from which this method is called.
        
          path : list of tuples/lists
            The path to be set for the instance, typically a list of positions.

        Returns
        -------
          None
        
        """
        self.path = path
```
```python
    def run(self):
        """

        Start the main event loop of the application.

        This method calls the main_loop function, passing the current instance as an argument.

        Parameters
        ----------
          self : object
            The instance of the class from which this method is called.

        Returns
        -------
          None

        """
        main_loop(self)
```

```python
    def draw(self, surface):
        """
        Draw the board and path on the given surface.

        This method draws the board on the provided surface. If a path is set, it also draws the path.
    
        Parameters
        ----------
          self : object
            The instance of the class from which this method is called.
        
          surface : pygame.Surface
            The Pygame surface on which the board and path will be drawn.
    
        Returns
        -------
          None
        
        """
        if self.board == None:
            return
        
        draw_board(surface, surface.get_rect(), self.board)
        if self.path != None:
            draw_path(surface, surface.get_rect(), self.board, self.path)
```
Next I will talk about metrics of board which we will use them to draw our cell, maze, path.

This class will help us to locate specific parts of the board, including the left, top, height, and bottom. Additionally, it will help us to determine cell's x and y coordinates, allowing us to create a cell rectangle.  

```python
class BoardMetrics:
    def __init__(self, area, board):
        self.area = area #area of the board which is surface.rect() object rect<x,y,w,h> board is what we created in my_maze.py
        self.spacing = 3 #spacing for cell's and board
        self.left = area[0] + self.spacing #left is starting position of cell 1 with spacing
        self.top = area[1] + self.spacing  # same for left but for top side
        self.height = area[3] - area[1] - 2 * self.spacing #height of board - 2 spacing from each side
        self.width = area[2] - area[0] - 2 * self.spacing #width of board - 2 spacing from each side
        self.num_y = board.get_size()[1] #board height with number of rows[[][]---]
        self.num_x = board.get_size()[0] #board width with number of columns[[1,2,3,4...]]
        self.cx = self.width / self.num_x #cell's x found by dividing width of board to num of cell's
        self.cy = self.height / self.num_y #cell's y found by dividing height of board to num of cell's
```

![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/d206eca1-74e7-4298-87da-4698b6c4903f)

This function will take position of the cell we will insert to board/maze and use it to get cell rectangle and create the board with them.

```python
    def cell_rect(self, pos):
        """

        This function takes position and returns rectangle object at that position as a list with its [x,y,w,h]
        
        Parameters:
        -----------
           pos (list): This parameter represents the position of the cell.

        Returns:
        --------
          list:
            The new x-coordinate of the rectangle's top-left corner.
            The new y-coordinate of the rectangle's top-left corner.
            The original width of the rectangle.
            The original height of the rectangle.

        """
        return [self.left + pos[0]*self.cx, self.top + pos[1]*self.cy, self.cx - self.spacing, self.cy - self.spacing]
```

To draw path from center of each cell we will use the following function.

```python
    def cell_center(self, pos):
        """

        This function takes position and returns position of cell's center as a list 
        
        Parameters:
        -----------
          pos (list): This parameter represents the position of the cell

        Returns:
        --------
          list:
            x-coordinate of rectangle's center
            y-coordinate of rectangle's center

        """
        rct = self.cell_rect(pos)
        return [rct[0]+rct[2]/2, rct[1] + rct[3]/2]
```
![image](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/b684009e-2f8c-4aba-b78b-100f664cda70)

Until here we calculated board metrics, with them we created cell rectangle, and we found its center to visualize the path, now we will use all of them to draw complete board, and path.

```python
def draw_board(surface, area, board):
    """

     This function takes board and draws it on surface.
     
     Parameters:
     -----------
        surface (pygame.Surface): This parameter represents the surface on which the board will be drawn.

        area (list): This parameter represents the area of the board.

        board (my_maze.Board): This parameter represents the board.

     Returns:
     --------
        None

    """
    pygame.draw.rect(surface, (0, 0, 0), area)
    metrics = BoardMetrics(area, board)

    colors = {

        my_maze.CellType.Empty : (40, 40, 40),
        my_maze.CellType.Block : (128, 79, 179)
    }

    marks = {
        my_maze.CellMark.Start : (0, 204, 152),
        my_maze.CellMark.End : (153, 0, 102)
    }
    for iy in range(metrics.num_y):
        for ix in range(metrics.num_x):     
            cell = board.at([ix, iy])
            clr = colors.get(cell.type, (129, 100, 0))
            cell_rect = metrics.cell_rect( [ix, iy] )
        
            pygame.draw.rect(surface, clr, cell_rect)

            if cell.count != math.inf:
                number = cell_font.render( "{}".format(cell.count), True, (255,255,255))
                surface.blit(number, trans_rect(number.get_rect(), 
                    [cell_rect[0] + (cell_rect[2] - number.get_rect()[2])/2, 
                    cell_rect[1] + (cell_rect[3] -number.get_rect()[3])/2]
                ))
        
            mark = marks.get(cell.mark, None)
            if mark != None:
                pygame.draw.rect(surface, mark, cell_rect, metrics.spacing)


def draw_path(surface, area, board, path):
    """

     This function takes board and draws it on surface.

     Parameters:
     ----------
        surface (pygame.Surface): This parameter represents the surface on which the board will be drawn.

        area (list): This parameter represents the area of the board.

        board (my_maze.Board): This parameter represents the board.

        path (list): This parameter represents the path.

     Returns:
     --------
        None

    """
    metrics = BoardMetrics(area, board)
    for i in range(len(path)-1):
        center_a = metrics.cell_center(path[i].pos)
        center_b = metrics.cell_center(path[i+1].pos)
        pygame.draw.line(surface, (1, 99, 148),  center_a, center_b, metrics.spacing )
```

So I divided my project into three parts and up to here I tried to talk about how I constructed the basic structure of the maze, the shortest path, the backtracking algorithm, and how to visualise the project using them. Now it is time to combine them to create an interactive experience.

## <u>Main Interactive</u>

```python
import algo as solver_algo
import my_maze as maze
import draw_s_path as draw

class the_finder(draw.Finder):
    def __init__(self):
        self.reset()

    def step(self, frames):
        """

        This is a function for animating path finding process.

        Parameters:
        -----------
          frames (int): Number of frames to animate from current position
        
        Returns:
        --------
          None

        """
        self.max_distance = max(0, self.max_distance + frames)
        self.result = solver_algo.fill_shortest_path(self.wall_maze.board, self.wall_maze.start, self.wall_maze.end, max_distance =self.max_distance)
        self.set_board(self.result)
        path = solver_algo.backtrack_to_start(self.result, self.wall_maze.end)
        self.set_path(path)


    def reset(self):
        """
        
        Resets the maze to its initial state with walls, and sets the maximum distance. 

        Parameters:
        -----------
          self (object):
            The instance of the class from which this method is called. It modifies the `wall_maze`, `max_distance`, and calls the `step` method on itself.

        Returns:
        --------
          None
  
        """
        self.wall_maze = maze.create_wall_maze(30, 22)
        self.max_distance = 30
        self.step(0)
    
menu_text = """Keys:
    Left - Lower maximum distance
    Right - Increase maximum distance
    R - create a new maze
    Esc - Exit
    """

print(menu_text)

finder = the_finder()
finder.run()

```

So here we have two method/function one of them for controlling steps to find shortest path visualization, and other to reset simulation. 

#### Method => step(self, frames)
1. Adjusts `self.max_distance` by adding the number of frames, which represents the maximum distance the pathfinding algorithm can explore in each animation step.

2. `Solver_algo.fill_shortest_path` to compute the shortest path in the maze up to `self.max_distance`.

3. Updates the state of the maze with the result using `self.set_board`.

4. Retrieves the path from the result using `solver_algo.backtrack_to_start` and updates the visual path on the board with `self.set_path`.

#### Method => reset(self)

1. Creates a new maze with walls using `maze.create_wall_maze`

2. Set `self.max_distance`.

3. `self.step(0)` to initialize the maze state for the starting point.


## <u>Demo</u>

![pathfinding_demo](https://github.com/yavuzCodiin/bfs-pathfinding-algorithm/assets/82445309/3a1dfb26-d368-4817-a314-4ced292c4d7d)




