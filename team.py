# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:16:26 2020

@author: chris
"""

from bot import Bot
from itertools import count

class Team:
    _ids = count(1)
    def __init__(self, *args, **kwargs):
        if kwargs.__contains__("id"):
            self.id = kwargs["id"]
        else:
            self.id = next(self._ids)
        self.name = kwargs["name"]
        self.color = (255, 255, 255)
        self.bots = []
        self.start_positions = []
        
        for b in args:
            self.bots.append(b) 
            b._id = self.id
            
        
        self._score = 0
        self._kills = 0
        self._moveWarning = 0
        self._codeWarning = 0
        self._timeoutWarning = 0
        
        #self.__set_botposition()
        self.__set_color()
    def _set_botposition(self, M):
        
        Map = M
        
        shift = 1
        if self.id == 1: 
            shift = 1
            xstart = 1
        else:
            shift = -1
            xstart = Map.shape[0]-2
        
        for bindex,b in enumerate(self.bots):
            b._pos=(int(xstart+bindex*shift), int(Map.shape[1]/2.))
            self.start_positions.append(b._pos)
    def __set_color(self):
        if self.id == 1:
            self.color = (255, 0, 0)
        if self.id == 2:
            self.color = (0, 0, 255)
        elif self.id == 3:
            self.color = (50, 50, 50)
            
        
        
            



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
