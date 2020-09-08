# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 09:28:47 2020

@author: chris
"""
from bot import Bot, PelletChaser, SafePelletChaser
from map import Map
from team import Team
from game import Game


class MyBot(Bot):
    def __init__(self):
        super().__init__()
        self.name = "MyBot"

    def init(self):
        pass

    def make_move(self):
        """ Always moves north """
        return "N"


B1 = SafePelletChaser()
B2 = SafePelletChaser()
T1 = Team(B1, B2, name="My Team 2")

B3 = PelletChaser()
B4 = PelletChaser()
T2 = Team(B3, B4, name="AI Challenge Team")

M = Map()

G = Game(M, T1, T2)
G.run()
