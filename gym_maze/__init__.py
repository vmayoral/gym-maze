from gym.envs.registration import register

register(
    id='maze-v0',
    entry_point='gym_maze.envs:MazeEnv',
)

register(
    id='maze_waco-v0',
    entry_point='gym_maze.envs:MazeWaco',
)

register(
    id='maze_grid-v0',
    entry_point='gym_maze.envs:MazeGrid',
)

register(
    id='maze_barrier2-v0',
    entry_point='gym_maze.envs:MazeBarrier2',
)
