# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 13:05:09 2020

@author: chris
"""
from bot import Bot, PelletChaser, SafePelletChaser
from map import Map
from team import Team
from game import Game
import random

#Try available Audio engines: Currently only Windows and macOS are supported (sapi5, nsss, espeak)
try: 
    import pyttsx
    SPEECH = True
except:
    SPEECH = False

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
        self.match_ups = None
        self._create_matchups()
        print(self.match_ups)
        
        # Definition of tourmanent rules
        self.opt = {
            "Respawn on Kill": True,
            "Points for Kill": 10,
            "Timeout in Seconds": 1,
            "Deathmatch Mode": True,
            "Timelimit": 25,
            "Debug": False,
            "LowGraphic": False
        }
        
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
        
    def start_game(self):
        """
        Sets up a game in the tournament setup
        """
        for team in self.game.teams:
            team.code_warns = 0
            team.move_warns = 0
            team.score = 0
            team.kills = 0

            for bot in team.bots:
                bot.reset()
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
                self.game.run()
                
    def _update_result(self):
        pass
    
    def _show_result(self):
        pass
    
    def _introduction_speech(self):
        """
        TODO
        """
        
        intro = "Welcome to the first Louisenlunder Ai Challenge tournament. Our todays contestants are. "
        for t in self.teams: intro = intro+t.name +" . "
        
        intro = intro+"Let the Games begin. UIUIUIUIUI"
        
        engine = pyttsx.init()
        engine.say(intro)
        engine.runAndWait()
        
    def _newRound_speech(self, mu):
        """
        TODO
        """
        text = "The next matchup is. "+self.teams[mu[0]].name+" . versus . "+self.teams[mu[1]].name+" . "
        text = text + "May the better AI win. "
        
        engine = pyttsx.init()
        engine.say(text)
        engine.runAndWait()
        
        

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