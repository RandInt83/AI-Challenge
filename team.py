# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:16:26 2020

@author: chris
"""

from itertools import count


class Team:
    _ids = count(1)

    def __init__(self, *args, **kwargs):
        self._id = kwargs["id"] if kwargs.__contains__("id") else next(self._ids)
        self.name = kwargs["name"]
        self.color = (255, 255, 255)
        self.bots = []
        self.start_positions = []

        for bot in args:
            self.bots.append(bot)
            bot._id = self._id

        self.score = 0
        self.kills = 0
        self.move_warns = 0
        self.code_warns = 0
        self.timeout_warns = 0

        # self.__set_botposition()
        self.__set_color()

    def get_id(self):
        return self._id

    def set_botposition(self, game_map):
        
        """
        if self._id == 1:
            shift = 1
            xstart = 1
        else:
            shift = -1
            xstart = game_map.game_map.shape[0] - 2
        """
        if self._id == 1:
            positions = game_map.teamRedPosition[:]
        elif self._id == 2: 
            positions = game_map.teamBluePosition[:]   
        elif self._id == 3: 
            positions = game_map.teamGreenPosition[:]
        else:
            positions = game_map.teamYellowPosition[:]
        
        
        for bindex, b in enumerate(self.bots):
            b._pos = positions.pop()
            self.start_positions.append(b._pos)
            
    def __set_color(self):
        if self._id == 1:
            self.color = (255, 0, 0)
        if self._id == 2:
            self.color = (0, 0, 255)
        elif self._id == 3:
            self.color = (0, 255, 50)
        elif self._id == 4:
            self.color = (255, 255, 50)


"""
B1 = Bot()
B2 = Bot()

T1 = Team(B1, B2, name = "AI Challenge Team")
print T1.id, T1.name, B1._Team__pos, B2._Team__pos

B1 = Bot()
B2 = Bot()

T2 = Team(B1, B2, name = "AI Challenge Team 2")
print T1.id, T2.name, B1._Team__pos, B2._Team__pos
"""
