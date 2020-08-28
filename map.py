# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""
import numpy as np
import random


class Map:
    def __init__(self, random_map=False):
        self.height = 0
        self.width = 0
        self.game_map = None
        self.map = None
        self.pellets = []
        self.walls = []

        """
        The Map can be of any size, but the UI is hardcoded for 19x19.
        For a map of size 38x38 change the block size attribute in Engine class accordingly.
        """

        if random_map:
            i = random.randint(0, 10)
            if i < 3:
                self.map = self._load_standard2()
            elif i < 6:
                self.map = self._load_standard()
            else:
                self.map = self.load_random_map
        else:
            self.map = self._load_standard()
        self._create_pellets()

    @property
    def load_random_map(self):
        """
        This method creates a random labyrinth with size (x,y).
        Pretty hacky code and probably 5 years old :D

        Returns:
            Map (ndarray with shape (x, y))
        """

        def get_walls(x_coord, y_coord):
            return [x_coord - 1, x_coord + 1, x_coord, x_coord], [y_coord, y_coord, y_coord - 1, y_coord + 1]

        def get_corners(x_coord, y_coord):
            return [x_coord - 1, x_coord - 1, x_coord + 1, x_coord + 1], [y_coord - 1, y_coord + 1, y_coord - 1, y_coord + 1]

        x = random.randint(10, 50)
        if x % 2 == 0:
            x += 1

        y = x

        self.game_map = np.zeros((x, y)) + 1
        self.width = self.game_map.shape[0]
        self.height = self.game_map.shape[1]

        half_width = int(self.width / 2.)
        half_height = int(self.height / 2.)

        self.game_map[half_width, half_height] = 0
        self.walls.append(np.array([half_width - 1, half_height]))
        self.walls.append(np.array([half_width + 1, half_height]))
        self.walls.append(np.array([half_width, half_height - 1]))
        self.walls.append(np.array([half_width, half_height + 1]))

        # dirs = [np.array([0, 1]), np.array([0, -1]), np.array([1, 0]), np.array([-1, 0])]
        for i in range(50000):
            lw = len(self.walls)
            rindex = random.randint(0, lw - 1)
            new_wall = self.walls[rindex]
            x_direction, y_direction = new_wall

            if self.game_map[x_direction, y_direction] == 1:
                xx, yy = get_walls(x_direction, y_direction)
                xx2, yy2 = get_corners(x_direction, y_direction)

                try:
                    a = self.game_map[xx, yy]
                    b = self.game_map[xx2, yy2]
                except IndexError():
                    self.walls.pop(rindex)
                    continue

                if sum(self.game_map[xx, yy]) == 3 and sum(self.game_map[xx2, yy2]) > 2:
                    self.game_map[x_direction, y_direction] = 0
                    self.walls.pop(rindex)

                    for index, ii in enumerate(xx):
                        if self.game_map[xx[index], yy[index]] == 1:
                            self.walls.append(np.array([xx[index], yy[index]]))

        self.game_map[:, 0] = 1
        self.game_map[:, -1] = 1
        self.game_map[0, :] = 1
        self.game_map[-1, :] = 1

        # Clear Starting Location
        xcoord = int(self.game_map.shape[0] / 2.)
        ycoord = int(self.game_map.shape[1] / 2.)
        self.game_map[1:-1, ycoord] = 0

        # Create Fight Pit
        width = int(self.game_map.shape[0] * 0.1)
        height = int(self.game_map.shape[1] * 0.1)
        self.game_map[xcoord - width:xcoord + width + 1, ycoord - height:ycoord + height + 1] = 0

        return self.game_map

    def _load_standard2(self):
        random_size = random.randint(10, 50)
        if random_size % 2 == 0: random_size += 1

        w = random.choice([2, 3])
        self.game_map = np.zeros((random_size, random_size))

        self.game_map[:, 0] = 1
        self.game_map[:, -1] = 1
        self.game_map[0, :] = 1
        self.game_map[-1, :] = 1

        for i in np.arange(random_size)[::w]:
            self.game_map[i, ::w] = 1
        return self.game_map

    def _load_standard(self):
        self.game_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                         [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                         [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                         [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                         [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1],
                         [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                         [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                         [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                         [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                         [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                         [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                         [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                         [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                         [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.game_map = np.array(self.game_map)
        self.game_map = self.game_map.T
        return self.game_map

    def _create_pellets(self):
        for xindex, x in enumerate(self.map):
            for yindex, y in enumerate(x):
                if y == 0:
                    self.pellets.append((xindex, yindex))


M = Map()
