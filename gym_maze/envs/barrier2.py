from . import maze_env

class MazeBarrier2(maze_env.MazeEnv):
    """
    Environment definition
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__(filename='barrier2.txt')
