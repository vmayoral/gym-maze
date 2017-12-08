from . import maze_env

class MazeWaco(maze_env.MazeEnv):
    """
    Environment definition
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__(filename='waco.txt')
