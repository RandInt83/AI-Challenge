import traceback

from game import Game as OG
from map import Map
from bot import Bot, PelletChaser, SafePelletChaser
from team import Team

import random
import copy
import time


class Game(OG):

    def __init__(self, game_map, *args, **kwargs):
        self.game_map = game_map

        self.teams = [arg for arg in args]
        for team in self.teams:
            for bot in team.bots:
                bot._game = self
            team.set_botposition(self.game_map)

        self.debug = False
        if kwargs.__contains__("debug"):
            if kwargs["debug"]:
                self.debug = True

        self.opt = {
            "Respawn on Kill": True,
            "Points for Kill": 10,
            "Timeout in Seconds": 1,
            "Deathmatch Mode": True,
            "Timelimit": False,
            "Debug": False,
            "LowGraphic": True
        }

        self.tick = 0
        self.running = True

        self.pc = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E": (1, 0), "O": (0, 0)}

    def _reset_game(self):
        game_map = Map()

        for team in self.teams:
            team.code_warns = 0
            team.move_warns = 0
            team.score = 0
            team.kills = 0

            for bot in team.bots:
                bot.reset()

        self.__init__(game_map, self.teams[0], self.teams[1])

    def run(self):
        for team in self.teams:
            for bot in team.bots:
                try:
                    bot.init()
                except Exception:
                    traceback.print_exc()
                    team.code_warns += 1

        maps, pellets, botposition_1, botposition_2 = self.game_map.map, [], [], []
        startposition_1 = copy.deepcopy(self.teams[1].bots[0].get_enemy_starting_location())
        startposition_2 = copy.deepcopy(self.teams[0].bots[0].get_enemy_starting_location())

        while self.running:
            pellets.append(copy.deepcopy(self.game_map.pellets))
            botposition_1.append(copy.deepcopy(self.teams[1].bots[0].get_enemy()))
            botposition_2.append(copy.deepcopy(self.teams[0].bots[0].get_enemy()))
            self.tick += 1
            #print('\r Tick '+str(self.tick), end='')
            for team in self.teams:
                for bot in team.bots:
                    if bot.is_alive():
                        self._handle_movement(bot, team)

                bots_copy = copy.copy(team.bots)
                for bot in bots_copy:
                    if not bot.is_alive(): team.bots.remove(bot)

            if self.tick >= self.opt["Timelimit"] and self.opt["Timelimit"]: 
                self.running = False

        return (maps, pellets, botposition_1, botposition_2, startposition_1, startposition_2)

class Data_Generator:

    def __init__(self, runterm, timelimit, bot1, bot2):
        self.runterm = runterm
        self.timelimit = timelimit
        self.b1, self.b2 = bot1(), bot1()
        self.b3, self.b4 = bot2(), bot2()
        self.T1 = Team(self.b1, self.b2, name = "Bot 1")
        self.T2 = Team(self.b3, self.b4, name = "Bot 2")
        self.M = Map(False)
        self.G = Game(self.M, self.T1, self.T2)

    def run(self):
        matches = []
        print('Start simulating matches...')
        for i in range(self.runterm):
            print('\r Simulating Match %d of %d' %(i+1, self.runterm), end='')
            self.G.opt["Timelimit"] = self.timelimit
            matches.append(self.G.run())
            self.G._reset_game()
        print()
        return matches

'''
dg = Data_Generator(10, 10, SafePelletChaser, PelletChaser)
data = dg.run()
for i in data[0][2]:
    print(i)
    pass
data = dg.run()
for i in data[0][2]:
    print(i)
    pass
'''
