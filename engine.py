# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:11:37 2020

@author: chris
"""
import numpy as np
import pygame


from map import Map
from bot import Bot

py_white = (255, 255, 255)
py_black = (0, 0, 0)
py_green = (0, 255, 0)

class Engine:
    def __init__(self, game):
        
        self.game = game
        pygame.init()
        
        # Graphical Options
        self.res = (1000,1000)
        self.block_size = (35, 35)
        self.pellet_size = 5
        self.bot_size = 15
        self.gap = 2
        self.trace_width = 2
        self.UI_height = 300
        
        self.screen = pygame.display.set_mode(self.res)
        self.screen.fill(py_black)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        ### Fonts
        self.fontS = pygame.font.SysFont("lucidasans", 30)
        self.fontW = pygame.font.SysFont("lucidasans", 12)  
        self.fontSmall = pygame.font.SysFont("lucidasans", 9)  
        
        # Resize Engine to fit the map
        self._resize_tileset(self.game.M)
        self.__load_textures()
        
        # Textures
        #self.tex_wall = pygame.image.load("Mauer2.png")
    def __load_textures(self):
        self.tex = {}        
        self.tex["Wall"] = pygame.transform.scale(pygame.image.load("textures/Wall_brick.png"), (self.block_size[0], self.block_size[1]))
        self.tex["Floor"] = pygame.transform.scale(pygame.image.load("textures/Weg1.png"), (self.block_size[0], self.block_size[1]))
        
    def _resize_tileset(self, M):
        """
        Changes the tileset size according to the map size
        """
        
        ssize = (19., 19.)
        msize = M.map.shape 
        scale = (ssize[0]/msize[0]*1., ssize[1]/msize[1]*1.)
        
        self.block_size = int(self.block_size[0]*scale[0]), int(self.block_size[1]*scale[1])
        self.pellet_size = int(self.pellet_size * scale[0])
        self.bot_size = int(self.bot_size * scale[0])
        self.gap = int(self.gap * scale[0])

        
    def convert_grid_to_screen_coord(self, gridcoord):
        
        y_screen = gridcoord[0] * (self.block_size[0]+self.gap) + 50
        x_screen = self.res[1]-self.UI_height-gridcoord[1] * (self.block_size[1]+self.gap)
        
        return y_screen, x_screen
    def update(self, fps = 30):
        self.screen.fill(py_black)
        self.clock.tick(fps)
    def draw_map(self,Map):
        
        for xgrid, row in enumerate(Map):
            for ygrid, content in enumerate(row):
                xs, ys = self.convert_grid_to_screen_coord((xgrid,ygrid))
                r = pygame.Rect(xs,ys,self.block_size[0],self.block_size[1])
                if content == 1:
                    if self.game.opt["LowGraphic"]:
                        pygame.draw.rect(self.screen, py_green, r, 0)
                    else:
                        self.screen.blit(self.tex["Wall"], r)
                else:
                    if self.game.opt["LowGraphic"] != True:
                        self.screen.blit(self.tex["Floor"], r)
                    
    def draw_pellets(self, pellets):
        for p in pellets:
            xs, ys = self.convert_grid_to_screen_coord((p[0],p[1]))
            if self.game.opt["LowGraphic"] != True: pygame.draw.circle(self.screen, py_black, (int(xs+self.block_size[0]/2.)+1,int(ys+self.block_size[1]/2.)+1), self.pellet_size)
            pygame.draw.circle(self.screen, py_white, (int(xs+self.block_size[0]/2.),int(ys+self.block_size[1]/2.)), self.pellet_size)
    def draw_bot(self, bots, color):
        for b in bots:
            xs, ys = self.convert_grid_to_screen_coord((b._pos[0],b._pos[1]))
            if self.game.opt["LowGraphic"] != True: pygame.draw.circle(self.screen, py_black, (int(xs+self.block_size[0]/2.+2),int(ys+self.block_size[1]/2.)+2), self.bot_size)
            pygame.draw.circle(self.screen, color, (int(xs+self.block_size[0]/2.),int(ys+self.block_size[1]/2.)), self.bot_size)
            
            for lindex, lp in enumerate(b._last_pos):
                xs, ys = self.convert_grid_to_screen_coord((lp[0],lp[1]))
                pygame.draw.circle(self.screen, color, (int(xs+self.block_size[0]/2.),int(ys+self.block_size[1]/2.)), int(0.5*self.bot_size*(lindex+1)/11.+self.trace_width), self.trace_width)
    def draw_UI(self, teams) :
        """
        Hacky Code ... nobody likes UI implementation :[
        """
        
        text = self.fontS.render(teams[0].name+" "+"%03d"%teams[0]._score, True, teams[0].color)
        warning = self.fontW.render("Movement Warnings "+"%03d"%(teams[0]._moveWarning), True, teams[0].color)   
        warning2 = self.fontW.render("Code Warnings "+"%03d"%(teams[0]._codeWarning), True, teams[0].color) 
        warning3 = self.fontW.render("TimeOut Warnings "+"%03d"%(teams[0]._timeoutWarning), True, teams[0].color)
        kills = self.fontW.render("Kills "+"%03d"%(teams[0]._kills), True, teams[0].color)         
        self.screen.blit(text, ((self.res[0]-200)/2-10-text.get_width(), self.res[1] - self.UI_height * 0.8))
        self.screen.blit(kills, ((self.res[0]-200)/2-10-kills.get_width(), self.res[1] - self.UI_height * 0.65))
        self.screen.blit(warning, ((self.res[0]-200)/2-10-warning.get_width(), self.res[1] - self.UI_height * 0.6))
        self.screen.blit(warning2, ((self.res[0]-200)/2-10-warning2.get_width(), self.res[1] - self.UI_height * 0.55))
        self.screen.blit(warning3, ((self.res[0]-200)/2-10-warning3.get_width(), self.res[1] - self.UI_height * 0.5))
     
        text = self.fontS.render("%03d "%(teams[1]._score)+teams[1].name, True, teams[1].color)
        warning = self.fontW.render("%03d"%(teams[1]._moveWarning)+" Movement Warnings", True, teams[1].color) 
        warning2 = self.fontW.render("%03d"%(teams[1]._codeWarning)+" Code Warnings", True, teams[1].color) 
        warning3 = self.fontW.render("%03d"%(teams[1]._codeWarning)+" Timeout Warnings", True, teams[1].color) 
        kills = self.fontW.render("%03d"%(teams[1]._kills)+" Kills", True, teams[1].color)         
        self.screen.blit(text, ((self.res[0]-200)/2+10, self.res[1] - self.UI_height * 0.8))          
        self.screen.blit(kills, ((self.res[0]-200)/2+10, self.res[1] - self.UI_height * 0.65))   
        self.screen.blit(warning, ((self.res[0]-200)/2+10, self.res[1] - self.UI_height * 0.6))
        self.screen.blit(warning2, ((self.res[0]-200)/2+10, self.res[1] - self.UI_height * 0.55))
        self.screen.blit(warning3, ((self.res[0]-200)/2+10, self.res[1] - self.UI_height * 0.5))
        
        
        # Create Time UI
        text = self.fontW.render("Game Tick: "+str(self.game.tick), True, (255, 255, 255))
        self.screen.blit(text, (810, 50))
        
        # Create Option List
        
        for index, opt in enumerate(self.game.opt):
            text = self.fontSmall.render(opt+": "+str(self.game.opt[opt]), True, (255, 255, 255))
            self.screen.blit(text, (810, 100+10*index))
        
        

"""
M=Map()
B1 = Bot()

E = Engine()
E.draw_map(M.map)
E.draw_pellets(M.pellets)
E.draw_bot([B1],(255,0,0))
E.draw()
"""