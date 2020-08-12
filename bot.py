# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:11:52 2020

@author: chris
"""
import random
import copy
import time

class Bot:
    def __init__(self):
        """
        Basic Bot class that handles the Bot behaviour ingame. Class is meant to be inherited from.
        
        Arguments:
            None
            
        Keyword Arguments:
            None
            
        Returns:
            None
        """
        self.id = -1
        
        self._pos = (0, 9)
        self._kill = False
        self._alive = True
        self._last_pos = []
        self._g = None
        
        self.pc = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E":(1, 0), "O": (0, 0)}
    def init(self):
        """
        Method that runs once during the start of the the match. Use it to initialize attributes and such.
        
        Arguments:
            None
            
        Keyword Arguments:
            None
            
        Returns:
            None       
        """
        pass
    
    def _get_opposing_team(self):
        """
        Returns the opposing team of the bot
        """
        teams = self._g.teams
        for t in teams:
            for b in t.bots:
                if self == b:
                    return [team for team in self._g.teams if team!=t][0]
        
    def _set_lastpos(self, p):
        
        if len(self._last_pos) < 11:
            self._last_pos.append(self._pos)
        else:
            self._last_pos.pop(0)
            self._last_pos.append(self._pos)
        
    def get_pellets(self):
        """
        Method that returns a list of coordinates of all existing pellets on the map
        
        Arguments:
            None
        
        Keyword Arguments:
            None
            
        Returns:
            pellets ((list) of (tuples) of two (int)):
                Contains the coordinated of all pellets.
                Example: [(1, 4), (6, 9), (3, 12)]
        """
        return self._g.M.pellets
    
    def get_map(self):
        """
        Method that returns the currently played map
        
        Arguments:
            None
        
        Keyword Arguments:
            None
            
        Returns:
            map (ndarray): 2-dimensional ndarray of the currently played map. 
                '1' stands for a wall ; '0' stands for a floor tile
        """
        return self._g.M.map
    
    def get_enemy(self):
        """
        Method that returns a list of coordinates of all existing enemies on the map
        
        Arguments:
            None
        
        Keyword Arguments:
            None
            
        Returns:
            enemies ((list) of (tuples) of two (int)):
                Contains the coordinated of all enemies.
                Example: [(1, 4), (6, 9), (3, 12)]
        """
        teams = self._g.teams      
        for t in teams:
            if t.id != self._id:
                bpos = []
                for b in t.bots: bpos.append(b._pos)
                return bpos
            
    def get_position(self):
        """
        Method that returns the current position as a tuple
        
        Arguments:
            None
        
        Keyword Arguments:
            None
            
        Returns:
            position (tuple): Position of the bot
        """
        return self._pos
    
    def get_enemy_starting_location(self):
        """
        Method that returns a list of the enemy starting location (which you are not allowed to enter!)
        
        Arguments:
            None
            
        Keyword Arguments:
            None
            
        Returns:
            locations ((list) of (tuples) of two (int)s): enemy spawn locations
        """
        opposing_team =  self._get_opposing_team()
        return opposing_team.start_positions            
            
    def _get_lastpositions(self):
        return copy(self._last_pos)
    
    def get_teammates(self):
        """
        Method that returns a list of coordinates of all existing teammates on the map
        
        Arguments:
            None
        
        Keyword Arguments:
            None
            
        Returns:
            teammates ((list) of 'Bot' instances): Contains all teammates
            teammate_positions ((list) of (tuples) of two (int)):
                Contains the coordinated of all teammates.
        """
        for t in self._g.teams:
            if t.id == self.id:
                bpos, bots = [], []
                for b in t.bots: 
                    if b!=self:
                        bpos.append(b._pos)
                        bots.append(b)
                return b, bpos
            
    def make_move(self):
        """
        Method that is called to decided the next move. Can be 'N', 'S', 'W' or 'E'.
        Translation to coordinated is according to class attribute self.pc
        
        Arguments:
            None
        
        Keyword Arguments:
            None
            
        Returns:
            move (str): Can be 'N', 'S', 'W' or 'E'
        """
        return random.choice(["N","E","S","W"])
   
class PelletChaser(Bot):
    """
    Basic Bot that checks for adjacent pellets and walks onto them. Makes only valid moves.
    
    Arguments:
        None
        
    Keyword Arguments:
        None
        
    Returns:
        None
    """
    def make_move(self):
        pmoves, pcoords = self.get_possible_moves()
        if len(pmoves)==0: return "O"
        best_moves, best_coords = self.get_best_move(pmoves, pcoords)
        if len(best_moves)==0: return random.choice(pmoves)
        return random.choice(best_moves)
    
    def get_best_move(self, pmoves, pcoords):
        
        best_moves = []
        best_coords = []
        pellets = self.get_pellets()
        for i, pcoord in enumerate(pcoords):
            if pcoord in pellets:
                best_moves.append(pmoves[i])
                best_coords.append(pcoord)
        return best_moves, best_coords
        
    def get_possible_moves(self):
        M=self.get_map()
        pos = self.get_position()
        
        pmoves = []
        pcoords = []
        if M[pos[0]+0,pos[1]+1]==0:
            pmoves.append("N")
            pcoords.append((pos[0]+0,pos[1]+1))
        
        if M[pos[0]+0,pos[1]-1]==0:
            pmoves.append("S")
            pcoords.append((pos[0]+0,pos[1]-1))
            
        if M[pos[0]-1,pos[1]+0]==0:
            pmoves.append("W")
            pcoords.append((pos[0]-1,pos[1]+0))
            
        if M[pos[0]+1,pos[1]+0]==0:
            pmoves.append("E")
            pcoords.append((pos[0]+1,pos[1]+0))
        
        # Make sure the bot tries not to walk into enemy spawn location
        pmovesC, pcoordsC = copy.deepcopy(pmoves), copy.deepcopy(pcoords)
        s_loc = self.get_enemy_starting_location()
        
        for index, p in enumerate(pcoords):
            if p in s_loc:
                pmoves.pop(index)
                pcoords.pop(index)
        return pmoves, pcoords

class SafePelletChaser(PelletChaser):
    """
    Basic Bot that checks for adjacent pellets and walks onto them. Makes only valid moves.
    Avoids floor tiles that can lead to death by being eating by the enemy.
    
    Arguments:
        None
        
    Keyword Arguments:
        None
        
    Returns:
        None
    """
    def make_move(self):
        pmoves, pcoords = self.get_possible_moves()
        pmoves, pcoords = self.get_safe_moves(pmoves, pcoords)
        if len(pmoves)==0: return "O"
        best_moves, best_coords = self.get_best_move(pmoves, pcoords)
        if len(best_moves)==0: return random.choice(pmoves)
        return random.choice(best_moves)
    
    def get_safe_moves(self, pmoves, pcoords):
        safe_moves = []
        safe_coords = []
        
        possible_ecoords = []
        epositions = self.get_enemy()
        
        for epos in epositions:
            for direction in self.pc:
                possible_ecoord = (epos[0]+self.pc[direction][0], epos[1]+self.pc[direction][1])
                possible_ecoords.append(possible_ecoord)
        
        for i, pcoord in enumerate(pcoords):
            if pcoord not in possible_ecoords:
                safe_moves.append(pmoves[i])
                safe_coords.append(pcoord)
        
        return safe_moves, safe_coords
        
        
        
            
        