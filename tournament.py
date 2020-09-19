# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 13:05:09 2020

@author: chris
"""
from bot import Bot, PelletChaser, SafePelletChaser
from map import Map
from team import Team
from game import Game as OG
from funcs import get_name
import random
import pylab
import matplotlib.animation as animation
import numpy as np
import pygame
import copy

#Try available Audio engines: Currently only Windows and macOS are supported (sapi5, nsss, espeak)
try: 
    import pyttsx
    SPEECH = True
except:
    SPEECH = False

opt = {"Respawn on Kill": True,
       "Points for Kill": 10,
       "Timeout in Seconds": 1,
       "Deathmatch Mode": True,
       "Timelimit": 25,
       "Debug": False,
       "LowGraphic": False
       }

class Game(OG):

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
        stop = True
        exit_game = False

        # Init Bots
        for team in self.teams:
            for bot in team.bots:
                try:
                    bot.init()
                except Exception:
                    traceback.print_exc()
                    team.code_warns += 1

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.fps = 1
                    if event.key == pygame.K_2: self.fps = 3
                    if event.key == pygame.K_3: self.fps = 10
                    if event.key == pygame.K_4: self.fps = 20
                    if event.key == pygame.K_5: self.fps = 40
                    if event.key == pygame.K_6: self.fps = 0
                    if event.key == pygame.K_0 and self.tick < self.opt["Timelimit"]: stop = not stop
                    if event.key == pygame.K_q: exit_game = True
                    if event.key == pygame.K_t: self.opt["LowGraphic"] = not self.opt["LowGraphic"]
                    if event.key == pygame.K_r: 
                        self._reset_game()
                        self.opt = opt

            self.__draw()
            if not stop:
                self.tick += 1
                for team in self.teams:
                    for bot in team.bots:
                        if bot.is_alive():
                            self._handle_movement(bot, team)
                            self.__draw()

                    bots_copy = copy.copy(team.bots)
                    for bot in bots_copy:
                        if not bot.is_alive(): team.bots.remove(bot)

                if self.tick >= self.opt["Timelimit"] and self.opt["Timelimit"]: stop = True
            if exit_game == True: return True

class Tournament:
    def __init__(self, *args, **kwargs):
        """
        Tournament class that handles a complete tournament. Each Team plays each other 
        team three times on three different maps.
        
        Arguments:
            *args (Team): Instances of Team class that participate in tournament
            
        Keyword Arguments:
            
            
        Returns:
            None
        """
        
        self.teams = [arg for arg in args]
        self.team_totalpoints = [0 for i in self.teams]
        self.team_score = [0 for i in self.teams]
        self.match_ups = None
        self._create_matchups()
        
        # Definition of tourmanent rules
        self.opt = opt
        
        if SPEECH: 
            self.engine = pyttsx.init()            
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id)        
        self.run()
        
    def _create_matchups(self):
        """
        Creates the specific match ups
        """
        self.match_ups = []
        index = 0
        for tindex, team in enumerate(self.teams):
            index += 1
            for t2index in range(index, len(self.teams)):
                self.match_ups.append((tindex, t2index))
        random.shuffle(self.match_ups)

    def _setup_teams(self, matchup):
        """
        Sets up the teams (id, starting position)
        """
        for index, mu in enumerate(matchup):
            self.teams[mu].__init__(self.teams[mu].bots[0], self.teams[mu].bots[1], id = index + 1, name = self.teams[mu].name)       
        
    def run(self):
        """
        Runs the tournament
        """
        
        #Init dummy Team & Map
        TMap = Map(False, 2)
        B1 = SafePelletChaser()
        B2 = SafePelletChaser()
        T1 = Team(B1, B2, name="AI Challenge Team 1")
        
        self._init_result()
        
        self.game = Game(TMap, T1, T1)
        
        if SPEECH == True:
            self._introduction_speech()
        
        for mu in self.match_ups:
            if SPEECH == True: self._newRound_speech(mu)
            for M in [Map(False, 2), Map(False, 1), Map(False, 4)]:
                self._setup_teams(mu)
                self.game.__init__(M, self.teams[mu[0]], self.teams[mu[1]])
                self.game.opt = self.opt
                self.game.fps = 30
                if not self.game.run():
                    exit()
                for team in self.game.teams:
                    for bot in team.bots:
                        bot.reset()
                self._update_result(mu)
                
    def _update_result(self, mu):
        """
        Updates the plot results
        """
        tindex1 = mu[0]
        tindex2 = mu[1]
        
        self.team_totalpoints[tindex1] += self.teams[tindex1].score
        self.team_totalpoints[tindex2] += self.teams[tindex2].score
        
        if self.teams[tindex1].score > self.teams[tindex2].score:
            self.team_score[tindex1] +=1
        elif self.teams[tindex1].score < self.teams[tindex2].score:
            self.team_score[tindex2] +=1
        
        self.score_data[0].set_ydata([0] + self.team_score) 
        self.point_data[0].set_ydata([0] + self.team_totalpoints)
        
        if max(self.team_score) != min(self.team_score):
            self.ax1.set_ylim(0, max(self.team_score) * 1.1)
        
        if max(self.team_totalpoints)!=min(self.team_totalpoints):
            self.ax2.set_ylim(0, max(self.team_totalpoints) * 1.1)
        
        pylab.draw()
    
    def _init_result(self):
        """
        Initializes plot for the score screen
        """
        self.fig = pylab.figure(figsize = (6,12))
        self.ax1 = self.fig.add_subplot(311)
        self.ax1.set_ylabel("Total Score")
        self.ax1.set_title("Score & Points Overview")
        self.ax2 = self.fig.add_subplot(312)
        self.ax2.set_ylabel("Total Points")
        
        self.ax1.set_xlim(0, len(self.teams))
        self.ax2.set_xlim(0, len(self.teams))
        
        team_names = [team.name for team in self.teams]
        
        self.ax1.set_xticklabels(["" for i in team_names], rotation="vertical")
        self.ax2.set_xticklabels(team_names, rotation="vertical")
        
        self.score_data = self.ax1.plot([""] + team_names, [0] + self.team_score, color = "r", drawstyle = "steps", lw = 5)
        self.point_data = self.ax2.plot([""] + team_names, [0] + self.team_totalpoints, drawstyle = "steps", lw = 5)
        
    def _introduction_speech(self):
        """
        TODO
        """
        
        intro = "Welcome to the first Louisenlunder Ai Challenge tournament. Our todays contestants are. "
        for t in self.teams: intro = intro+t.name +" . "
        
        intro = intro+"Let the Games begin."
        
        self.engine.say(intro)
        self.engine.runAndWait()
        
    def _newRound_speech(self, mu):
        """
        TODO
        """
        self.engine.setProperty('rate', random.randint(200, 400))
        text = "The current score is: . "
        for tindex, team in enumerate(self.teams):
            text = text + team.name + " . Total Wins: " + str(self.team_score[tindex]) + " . total points: "+ str(self.team_totalpoints[tindex]) + " . "
        
        
        
        text = text + "The next matchup is. "+self.teams[mu[0]].name+" . also known as . "+get_name()
        
        text = text + ". versus . "
        text = text + self.teams[mu[1]].name+" . also known as . " + get_name() + " . "
        text = text + "May the better AI win. "
        
        self.engine.say(text)
        self.engine.runAndWait()
        
        

B1 = SafePelletChaser()
B2 = SafePelletChaser()
T1 = Team(B1, B2, name="AI Challenge Team 1")

B3 = PelletChaser()
B4 = PelletChaser()
T2 = Team(B3, B4, name="AI Challenge Team 2")

B3 = PelletChaser()
B4 = PelletChaser()
T3 = Team(B3, B4, name="AI Challenge Team 3")

B3 = PelletChaser()
B4 = PelletChaser()
T4 = Team(B3, B4, name="AI Challenge Team 4")

T = Tournament(T1, T2, T3, T4)

#M = Map()

#G = Game(M, T1, T2)
#G.run()