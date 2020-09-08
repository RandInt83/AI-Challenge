# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""
import numpy as np
from PIL import Image
import random



class Map:
    def __init__(self, random_map=False):
        self.height = 0
        self.width = 0
        self.game_map = None
        self.map = None
        self.pellets = []
        self.walls = []
        
        self.teamRedPosition = []
        self.teamBluePosition = []
        self.teamGreenPosition = []
        self.teamYellowPosition = []
        
        if random_map == True:
            self.map = self._load_from_file(random.randint(1,4))
        else:
            self.map = self._load_from_file(4)
            
        self._create_pellets()

    def _load_from_file(self, map_number = 1):
        """
        Loads a map from png File 
        
        Color Code ###
        Black: Wall
        White: Pellet
        Red, Green, Blue, Yellow: Team Starting Positions
        """
        Map = np.array(Image.open("maps/M%s.png"%(map_number)))
        self.game_map = np.zeros((Map.shape[0], Map.shape[1]))
        print(Map.shape)
        for x in range(0, Map.shape[0]):
            for y in range(0, Map.shape[1]):
                if np.sum(Map[x, y, :]) < 256:
                    self.game_map[x, y] = 1
                if Map[x, y, 0] == 255 and Map[x, y, 1]  == 0 and Map[x, y, 2] == 0:
                    print(x, y, Map[x, y, 0], "red")
                    self.teamRedPosition.append((x, y))
                if Map[x, y, 0] == 0 and Map[x, y, 1]  == 0 and Map[x, y, 2] == 255:
                    print(x, y, Map[x, y, 0], "blue")
                    self.teamBluePosition.append((x, y))
                if Map[x, y, 0] == 0 and Map[x, y, 1]  == 255 and Map[x, y, 2] == 0:
                    print(x, y, Map[x, y, 0], "green")
                    self.teamGreenPosition.append((x, y))
                if Map[x, y, 0] == 255 and Map[x, y, 1]  == 255 and Map[x, y, 2] == 0:
                    print(x, y, Map[x, y, 0], "yellow")
                    self.teamYellowPosition.append((x, y))
        return self.game_map
        
    def _create_pellets(self):
        for xindex, x in enumerate(self.map):
            for yindex, y in enumerate(x):
                if y == 0:
                    self.pellets.append((xindex, yindex))


M = Map()
