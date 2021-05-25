# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:11:52 2020

@author: chris
"""
import random
import copy


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
        self._id = -1
        self._pos = (0, 9)
        self._kill = False
        self._alive = True
        self._last_pos = []
        self._game = None

        self.pc = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E": (1, 0), "O": (0, 0)}

    def init(self):
        """
        Method that runs once during the start of the the match. Use it to initialize attributes and such.
            
        Returns:
            None       
        """
        pass

    def _get_opposing_team(self):
        """
        Returns the opposing team of the bot
        """
        teams = self._game.teams
        for t in teams:
            for b in t.bots:
                if self._id == b._id:
                    return [team for team in self._game.teams if team != t][0]

    def set_last_pos(self):

        if len(self._last_pos) < 11:
            self._last_pos.append(self._pos)
        else:
            self._last_pos.pop(0)
            self._last_pos.append(self._pos)

    def is_alive(self):
        return self._alive

    def reset(self):
        self._last_pos = []

    def get_pellets(self):
        """
        Method that returns a list of coordinates of all existing pellets on the map
            
        Returns:
            pellets ((list) of (tuples) of two (int)):
                Contains the coordinated of all pellets.
                Example: [(1, 4), (6, 9), (3, 12)]
        """
        return self._game.game_map.pellets

    def get_map(self):
        """
        Method that returns the currently played map
            
        Returns:
            map (ndarray): 2-dimensional ndarray of the currently played map. 
                '1' stands for a wall ; '0' stands for a floor tile
        """
        return self._game.game_map.map

    def get_enemy(self):
        """
        Method that returns a list of coordinates of all existing enemies on the map
            
        Returns:
            enemies ((list) of (tuples) of two (int)):
                Contains the coordinated of all enemies.
                Example: [(1, 4), (6, 9), (3, 12)]
        """
        teams = self._game.teams
        for team in teams:
            if team.get_id() != self._id:
                bot_positions = []
                for bot in team.bots: bot_positions.append(bot.get_position())
                return bot_positions

    def get_position(self):
        """
        Method that returns the current position as a tuple
            
        Returns:
            position (tuple): Position of the bot
        """
        return self._pos

    def get_last_position(self):
        """
        Method that returns the previous position as a tuple

        Returns:
            position (tuple): Previous position of the bot
        """
        return self._last_pos

    def get_enemy_starting_location(self):
        """
        Method that returns a list of the enemy starting location (which you are not allowed to enter!)
            
        Returns:
            locations ((list) of (tuples) of two (int)s): enemy spawn locations
        """
        opposing_team = self._get_opposing_team()
        return opposing_team.start_positions

    def _get_last_positions(self):
        return copy.copy(self._last_pos)

    def get_teammates(self):
        """
        Method that returns a list of coordinates of all existing teammates on the map
            
        Returns:
            teammates ((list) of 'Bot' instances): Contains all teammates
            teammate_positions ((list) of (tuples) of two (int)):
                Contains the coordinated of all teammates.
        """
        for team in self._game.teams:
            if team.get_id() == self._id:
                bot_positions, bots = [], []
                for bot in team.bots:
                    if bot != self:
                        bot_positions.append(bot.get_position())
                        bots.append(bot)
                return bots, bot_positions

    def make_move(self):
        """
        Method that is called to decided the next move. Can be 'N', 'S', 'W' or 'E'.
        Translation to coordinated is according to class attribute self.pc
            
        Returns:
            move (str): Can be 'N', 'S', 'W' or 'E'
        """
        return random.choice(["N", "E", "S", "W"])


class PelletChaser(Bot):
    """
    Basic Bot that checks for adjacent pellets and walks onto them. Makes only valid moves.
    """

    def make_move(self):
        pmoves, pcoords = self.get_possible_moves()
        if len(pmoves) == 0: return "O"
        best_moves, best_coords = self.get_best_move(pmoves, pcoords)
        if len(best_moves) == 0: return random.choice(pmoves)
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
        game_map = self.get_map()
        pos = self.get_position()

        possible_moves = []
        possible_coords = []
        if game_map[pos[0] + 0, pos[1] + 1] == 0:
            possible_moves.append("N")
            possible_coords.append((pos[0] + 0, pos[1] + 1))

        if game_map[pos[0] + 0, pos[1] - 1] == 0:
            possible_moves.append("S")
            possible_coords.append((pos[0] + 0, pos[1] - 1))

        if game_map[pos[0] - 1, pos[1] + 0] == 0:
            possible_moves.append("W")
            possible_coords.append((pos[0] - 1, pos[1] + 0))

        if game_map[pos[0] + 1, pos[1] + 0] == 0:
            possible_moves.append("E")
            possible_coords.append((pos[0] + 1, pos[1] + 0))

        # Make sure the bot tries not to walk into enemy spawn location
        starting_location = self.get_enemy_starting_location()

        for index, p in enumerate(possible_coords):
            if p in starting_location:
                possible_moves.pop(index)
                possible_coords.pop(index)
        return possible_moves, possible_coords


class SafePelletChaser(PelletChaser):
    """
    Basic Bot that checks for adjacent pellets and walks onto them. Makes only valid moves.
    Avoids floor tiles that can lead to death by being eating by the enemy.
    """

    def make_move(self):
        possible_moves, pcoords = self.get_possible_moves()
        possible_moves, pcoords = self.get_safe_moves(possible_moves, pcoords)
        if len(possible_moves) == 0: return "O"
        best_moves, best_coords = self.get_best_move(possible_moves, pcoords)
        if len(best_moves) == 0: return random.choice(possible_moves)
        return random.choice(best_moves)

    def get_safe_moves(self, pmoves, pcoords):
        safe_moves = []
        safe_coords = []

        possible_ecoords = []
        epositions = self.get_enemy()

        for epos in epositions:
            for direction in self.pc:
                possible_ecoord = (epos[0] + self.pc[direction][0], epos[1] + self.pc[direction][1])
                possible_ecoords.append(possible_ecoord)

        for i, pcoord in enumerate(pcoords):
            if pcoord not in possible_ecoords:
                safe_moves.append(pmoves[i])
                safe_coords.append(pcoord)

        return safe_moves, safe_coords
