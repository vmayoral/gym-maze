# -*- coding: utf-8 -*-
"""
A simple maze environment written in Python with OpenAI gym's APIs whereto
demonstrate and validate different RL techniques.

    NOTE: tkinter seem to have relevant differences between its Python 2 and 3
    implementations. Events (e.g.: <Espace>) aren't capture with Python 3.
"""
import random
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from . import cellular
# import gym_maze.envs.cellular as cellular

class Cell(cellular.Cell):
    """
    A basic class representing an individual cell
    """
    wall = False
    def colour(self):
        if self.wall:
            return 'black'
        else:
            return 'white'

    def load(self, data):
        if data == 'X':
            self.wall = True
        else:
            self.wall = False

class Destination(cellular.Agent):
    """
    An cell in the maze representing the destination position (high reward)
    """
    colour = 'green'
    def update(self):
        pass

class Agent(cellular.Agent):
    """
    A class to abstract the agent that will "act" in the environment.
    """
    colour = 'yellow'

    def __init__(self):
        pass

    def update(self):
        pass

class MazeEnv0(gym.Env):
    """
    Environment definition
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.directions = 8

        self.delay = -1024 # delay in the simulation, less implies faster
                            # simulation, does not seem to work with Python 3
        self.renderizing = False
        # Create the agents
        self.agent = Agent()
        self.destination = Destination()
        # Create the world
        # waco.txt
        """
        XXXXXXXXXXXXXX
        X            X
        X XXX X   XX X
        X  X  XX XXX X
        X XX      X  X
        X    X  X    X
        X X XXX X XXXX
        X X  X  X    X
        X XX   XXX  XX
        X    X       X
        XXXXXXXXXXXXXX
        """
        self.world = cellular.World(Cell, directions=self.directions, filename='waco.txt')
        self.world.age = 0 # start from age 0
        # Add agents
        self.world.addAgent(self.destination, cell=self.pickRandomLocation())
        self.world.addAgent(self.agent)

        #  make the environment partially observable.
        lookdist = 2
        self.lookcells = []

        # populate lookcells
        for i in range(-lookdist,lookdist+1):
            for j in range(-lookdist,lookdist+1):
                if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
                    self.lookcells.append((i,j))

        # Set up observation and state spaces
            # state encoded as 0 (empty), 1 (wall) or 2 (goal)
        self.observation_space = spaces.Box(np.zeros(len(self.lookcells)),
            np.array([2.]*len(self.lookcells))) # [0, 0, ..., 0] - [2., 2., ..., 2.], Box(12,)

        # One action for each board position, pass, and resign
        self.action_space = spaces.Discrete(self.directions) # 0, 1, 2, ... self.directions -1, Discrete(8)

    def calcState(self):
        """
        Auxiliary method to representate the state on each cell as:
            0: (empty),
            1: (wall) or
            2: (goal)
        """
        def cellvalue(cell):
            # if cat.cell is not None and (cell.x == cat.cell.x and
            #                              cell.y == cat.cell.y):
            #     return 3
            if self.destination.cell is not None and (self.agent.cell.x == self.destination.cell.x and
                                              self.agent.cell.y == self.destination.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0

        return tuple([cellvalue(self.world.getWrappedCell(self.agent.cell.x + j, self.agent.cell.y + i))
                      for i,j in self.lookcells])


    def pickRandomLocation(self):
        while 1:
            x = random.randrange(self.world.width)
            y = random.randrange(self.world.height)
            cell = self.world.getCell(x, y)
            if not (cell.wall or len(cell.agents) > 0):
                return cell

    def _step(self, action):
        """
        Execute action and return feedback from the environment.

        Parameters
        ----------
        action: Discrete(8), corresponds with action_space
            elements characterizing the Ag or the Ab as list (each element should be printable)

        Returns
        -------
        observation: object
            an environment-specific object representing your observation of the environment. For example,
            pixel data from a camera, joint angles and joint velocities of a robot, or the board state in
            a board game.
        reward: float
            amount of reward achieved by the previous action. The scale varies between environments, but
            the goal is always to increase your total reward.
        done: boolean
            whether it's time to reset the environment again. Most (but not all) tasks are divided up into
            well-defined episodes, and done being True indicates the episode has terminated. (For example,
            perhaps the pole tipped too far, or you lost your last life.)
        info: dict
            diagnostic information useful for debugging. It can sometimes be useful for learning (for example,
            it might contain the raw probabilities behind the environment's last state change). However,
            official evaluations of your agent are not allowed to use this for learning.
        """
        # execute action
        success = self.agent.goInDirection(action)
        # calculate reward
        reward = -1 # default reward of taking a step
        if success:
            if self.agent.cell == self.destination.cell:
                reward = 50
        else:
            reward = -5 # if hits the wall, penalize

        # Calculate if the environment has been solved
        done = (self.agent.cell == self.destination.cell)
        # caculate obsevation and return it
        state_list = self.calcState()
        observation=np.asarray(state_list)

        # Update the world accordingly
        self.world.updateMaze()
        if self.renderizing:
            self.world.display.activate(size=30)
            self.world.display.delay = self.delay

        return observation, reward, done, None

    def _reset(self):
        # reset agent's location (random)
        self.agent.cell = self.pickRandomLocation()
        # Update the world accordingly
        self.world.updateMaze()
        if self.renderizing:
            self.world.display.activate(size=30)
            self.world.display.delay = self.delay
        # caculate state and return it
        state_list = self.calcState()
        return np.asarray(state_list)

    def _render(self, mode='human', close=False):
        # display the environment
        self.world.display.activate(size=30)
        self.world.display.delay = self.delay
        self.renderizing = True
        # self.world.updateMaze()

def test():
    env = MazeEnv0()
    # env.render()
    # print(env.observation_space)
    # print(env.action_space)
    print(env.reset())
    while 1:
        observation, reward, done, info = env.step(env.action_space.sample())
        # print("observation: ",observation)
        print("reward: ",reward)
        # print("done: ",done)
        # print("info: ",info)

        if done:
            print("done: ",done)
            env.reset()
