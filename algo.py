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


