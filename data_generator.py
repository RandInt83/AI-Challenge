# -*- coding: utf-8 -*-
'''
This is a data generator for AI frameworks like TensorFlow or PyTorch. 
The class Data_Generator returns the data in the matches which includes the information of the map und all the coordinates of pellets and bots for each tick. 
The following code is based on the game.py. 
'''
import numpy as np
from bot import Bot, PelletChaser, SafePelletChaser
from map import Map
from team import Team

import random
import copy
import time
from funcs import timeouthandler, TimeOutException

class Game:
    def __init__(self, M, *args, **kwargs):
        """
        Main game class that handles the game logic
        
        Arguments:
            M (Map): Instance of the Map class
            *args (Bot): Instances of Bot class. Number of instances should be between 1 and 3
            
        Keyword Arguments:
            debug (boolean): Set to True for Error Traceback and Error Messages
            
        Returns:
            None
        """
        self.M = M
        
        self.teams = [arg for arg in args]
        for t in self.teams: 
            for b in t.bots:
                b._g = self
            t._set_botposition(self.M.map)

        self.debug = False        
        if kwargs.__contains__("debug"):
            if kwargs["debug"]==True:
                self.debug = True
      
        # Game Options
        self.opt = {}
        self.opt["Respawn on Kill"]=True #Determines whether a player respawned if killed
        self.opt["Points for Kill"]=10 
        self.opt["Timeout in Seconds"]=1
        self.opt["Deathmatch Mode"]=True #Enables Kills
        self.opt["Timelimit"] = False
        self.opt["Debug"] = False
        self.opt["LowGraphic"] = True
               
        # Init Game
        self.tick = 0
        self.running = True
        
        # Constants 
        self.pc = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E":(1, 0), "O": (0, 0)}
        
    def _handle_movement(self, b, t):
        
        pc = (0, 0)
        old_pos = b._pos
        
        if self.opt["Debug"]!=True:
            # Check if make_move method of Bot runs. If not increment CodeWarning
            try:
                # Check if the runtime is below 1 second, else raise a timeoutWarning
                start = time.clock()
                move = b.make_move()
                runtime = time.clock() - start
                if runtime > self.opt["Timeout in Seconds"]:
                    t._timeoutWarning +=1
            except:
                t._codeWarning += 1
                move = (0, 0)
        else:
            move = b.make_move()
        
        if move in ["N", "E", "S", "W"]:
            pc = self.pc[move]
        
        new_pos = b._pos[0] + pc[0], b._pos[1] + pc[1]
        
        if self._check_valid(new_pos, t):
            b._pos = new_pos
            b._set_lastpos(old_pos)
            self._check_pellet(new_pos, t)
            
            if self.opt["Deathmatch Mode"]==True:
                self._check_kill(new_pos, b, t)
        else:
            t._moveWarning += 1
            
    def _check_pellet(self, new_pos, T):
        if new_pos in self.M.pellets:
            self.M.pellets.remove(new_pos)
            T._score += 1
            
    def _check_valid(self, new_pos, t):
        """
        Method to check the validity of the new bot position. 
        A Bot is not allowed to walk on wall tiles or to enter the spawn location of the opposing team
        
        Arguments:
            new_pos (Tuple of ints): New Bot position
            t (Instance of class 'Team'): The Team instance of the Bot
        
        Returns:
            boolean
        """
        opposing_team = [team for team in self.teams if team!=t][0]  
        
        # Chech if the new Position is on a floor tile and not in the spawn location of the opposing teams
        if self.M.map[new_pos[0], new_pos[1]]==0 and new_pos not in opposing_team.start_positions:
            return True
        else:
            return False
        
    def _check_kill(self, new_pos, b, t):
        for t2 in self.teams:
            if t2.id!=t.id:
                for bot in t2.bots:
                    if new_pos == bot._pos:
                        if self.opt["Respawn on Kill"] != True:
                            bot._alive = False
                            t._kills += 1
                            t._score+=self.opt["Points for Kill"]
                        else:
                            t._kills += 1
                            t._score+=self.opt["Points for Kill"]
                            bot._pos = random.choice(t2.start_positions)  
        
    def run(self):   
        """
        Method to run the game
        
        Arguments:
            None
            
        Keyword Arguments:
            None
        
        Returns:
            None
        """

        
        # Init Bots
        for t in self.teams:
            for b in t.bots:
                try:
                    b.init()
                except:
                    t._codeWarning += 1
        
        maps, pellets, botposition_1, botposition_2 = self.M.map, [], [], []

        while self.running:
            pellets.append(self.M.pellets)
            botposition_1.append((self.teams[0].bots[0]._pos, self.teams[0].bots[1]._pos))
            botposition_2.append((self.teams[1].bots[0]._pos, self.teams[1].bots[1]._pos))

            self.tick+=1
            for t in self.teams:
                for b in t.bots:
                    if b._alive:
                        self._handle_movement(b, t)
                botsC = copy.copy(t.bots)
                for bot in botsC:
                    if not bot._alive: t.bots.remove(bot)
                        
            if self.tick>=self.opt["Timelimit"] and self.opt["Timelimit"]: 
                self.running = False

        return [maps, pellets, botposition_1, botposition_2]


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

#print(Data_Generator(10, 20, SafePelletChaser, PelletChaser).run())
            