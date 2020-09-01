# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:11:18 2020

@author: chris
"""
import traceback

from bot import Bot, PelletChaser, SafePelletChaser
from map import Map
from engine import Engine
from team import Team

import pygame
import random
import copy
import time


class Game:
    def __init__(self, game_map, *args, **kwargs):
        """
        Main game class that handles the game logic
        
        Arguments:
            game_map (Map): Instance of the Map class
            *args (Team): Instances of Bot class. Number of instances should be between 1 and 3
            
        Keyword Arguments:
            debug (boolean): Set to True for Error Traceback and Error Messages
            
        Returns:
            None
        """

        self.game_map = game_map

        self.teams = [arg for arg in args]
        for team in self.teams:
            for bot in team.bots:
                bot._game = self
            team.set_botposition(self.game_map.map)

        self.debug = False
        if kwargs.__contains__("debug"):
            if kwargs["debug"]:
                self.debug = True

        # Game Options
        self.opt = {
            "Respawn on Kill": True,
            "Points for Kill": 10,
            "Timeout in Seconds": 1,
            "Deathmatch Mode": True,
            "Timelimit": False,
            "Debug": False,
            "LowGraphic": True
        }

        # Init Game
        self.tick = 0
        self.running = True

        # Constants 
        self.pc = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E": (1, 0), "O": (0, 0)}

    def _handle_movement(self, bot, team):
        pc = (0, 0)

        if not self.opt["Debug"]:
            # Check if make_move method of Bot runs. If not increment CodeWarning
            try:
                # Check if the runtime is below 1 second, else raise a timeoutWarning
                start = time.time()
                move = bot.make_move()
                runtime = time.time() - start
                if runtime > self.opt["Timeout in Seconds"]:
                    team.timeout_warns += 1

            except Exception as e:
                print(traceback.format_exc())
                team.code_warns += 1
                move = (0, 0)
        else:
            move = bot.make_move()

        if move in ["N", "E", "S", "W"]:
            pc = self.pc[move]

        new_pos = bot._pos[0] + pc[0], bot._pos[1] + pc[1]

        if self._check_valid(new_pos, team):
            bot._pos = new_pos
            bot.set_last_pos()
            self._check_pellet(new_pos, team)

            if self.opt["Deathmatch Mode"]:
                self._check_kill(new_pos, team)
        else:
            team.move_warns += 1

    def _check_pellet(self, new_pos, team):
        if new_pos in self.game_map.pellets:
            self.game_map.pellets.remove(new_pos)
            team.score += 1

    def _check_valid(self, new_pos, own_team):
        """
        Method to check the validity of the new bot position. 
        A Bot is not allowed to walk on wall tiles or to enter the spawn location of the opposing team
        
        Arguments:
            new_pos (Tuple of ints): New Bot position

        Returns:
            boolean
        """
        opposing_team = [team for team in self.teams if team != own_team][0]

        # Check if the new Position is on a floor tile and not in the spawn location of the opposing teams
        if self.game_map.map[new_pos[0], new_pos[1]] == 0 and new_pos not in opposing_team.start_positions:
            return True
        else:
            return False

    def _check_kill(self, new_pos, team):
        for t2 in self.teams:
            if t2.get_id() != team.get_id():
                for bot in t2.bots:
                    if new_pos == bot._pos:
                        if not self.opt["Respawn on Kill"]:
                            bot._alive = False
                            team.kills += 1
                            team.score += self.opt["Points for Kill"]
                        else:
                            team.kills += 1
                            team.score += self.opt["Points for Kill"]
                            bot._pos = random.choice(t2.start_positions)

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
        self.run()

    def run(self):
        """
        Method to run the game
        
        Returns:
            None
        """

        # Init Bots
        for team in self.teams:
            for bot in team.bots:
                try:
                    bot.init()
                except Exception:
                    traceback.print_exc()
                    team.code_warns += 1

        maps, pellets, botposition_1, botposition_2 = self.game_map.map, [], [], []

        while self.running:
            pellets.append(self.game_map.pellets)
            botposition_1.append((self.teams[0].bots[0]._pos, self.teams[0].bots[1]._pos))
            botposition_2.append((self.teams[1].bots[0]._pos, self.teams[1].bots[1]._pos))

            self.tick += 1
            for team in self.teams:
                for bot in team.bots:
                    if bot.is_alive():
                        self._handle_movement(bot, team)

                bots_copy = copy.copy(team.bots)
                for bot in bots_copy:
                    if not bot.is_alive(): team.bots.remove(bot)

            if self.tick >= self.opt["Timelimit"] and self.opt["Timelimit"]: self.running = False

        return (maps, pellets, botposition_1, botposition_2)

class Data_Generator:

    def __init__(self, runterm, timelimit, bot1, bot2):
        self.runterm = runterm
        self.timelimit = timelimit
        self.bot1 = bot1
        self.bot2 = bot2

    def run(self):
        matches = []
        for i in range(self.runterm):
            b1, b2 = self.bot1(), self.bot2()
            T1 = Team(b1, b1, name = "Bot 1")
            T2 = Team(b2, b2, name = "Bot 2")
            M = Map(False)
            G = Game(M, T1, T2)
            G.opt["Timelimit"] = self.timelimit
            matches.append(G.run())
        return matches

print(Data_Generator(10, 20, SafePelletChaser, PelletChaser).run())
