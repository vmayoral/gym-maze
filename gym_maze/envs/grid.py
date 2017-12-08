from . import maze_env

class MazeGrid(maze_env.MazeEnv):
    """
    Environment definition
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__(filename='grid.txt')
