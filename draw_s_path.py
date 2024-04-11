import pygame, math
import my_maze

pygame.init()
pygame.display.set_caption("Demo => Path Finding")
cell_font = pygame.font.SysFont(pygame.font.get_default_font(), 25)

def trans_rect(r, offset):
    """

    This function takes rect( => x,y,w,h <= ) then adjusts the position of rectangle by applying an offset to it
    
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


class Finder:
    def __init__(self):
        self.board = None
        self.path = None

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






