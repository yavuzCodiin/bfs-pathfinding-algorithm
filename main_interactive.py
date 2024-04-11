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
