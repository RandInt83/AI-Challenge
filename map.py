# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""
import numpy as np
import random

class Map:
    def __init__(self, randomMap = False):
        """
        The Map can be of any size, but the UI is hardcoded for 19x19.
        For a map of size 38x38 change the block size attribute in Engine class accordingly.
        """
        self.map = np.zeros((19,19))
        self.pellets = []
        
        if randomMap:
            i=random.randint(0,10)
            if i<3:
                self.map = self._load_standard2()
            elif i<6:
                self.map = self._load_standard()
            else:
                self.map = self.load_random_map()
        else:
            self.map = self._load_standard()
        self._create_pellets()
    def load_random_map(self):
        """
        This method creates a random labyrinth with size (x,y).
        Pretty hacky code and probably 5 years old :D
        
        Arguments:
            x (int): x dimension of the map
            y (int): y dimension of the map
            
        Returns:
            Map (ndarray with shape (x, y))
        """    
        def get_walls(X, Y):
            return [X-1, X+1, X, X], [Y, Y, Y-1, Y+1]
        
        def get_corners(X, Y):
             return [X-1, X-1, X+1, X+1], [Y-1, Y+1, Y-1, Y+1]
        
        x = random.randint(10,50)
        if x%2==0: x+=1
        y=x
        
        self.M = np.zeros((x, y)) + 1
        self.xM = self.M.shape[0]
        self.yM = self.M.shape[1]
        
        self.walls = []
        
        sX=random.randint(0, self.xM)
        sY=random.randint(0, self.yM)
        sX=int(self.xM/2.)
        sY=int(self.yM/2.)
        self.M[sX, sY]=0
        self.walls.append(np.array([sX-1, sY]))
        self.walls.append(np.array([sX+1, sY]))
        self.walls.append(np.array([sX, sY-1]))
        self.walls.append(np.array([sX, sY+1]))
        
        
        dirs = [np.array([0,1]), np.array([0,-1]), np.array([1,0]), np.array([-1,0])]
        for i in range(50000):
            lw=len(self.walls)
            rindex=random.randint(0, lw-1)
            nW = self.walls[rindex]
            Xdir, Ydir=nW
            if self.M[Xdir, Ydir] == 1:
                xx,yy = get_walls(Xdir, Ydir)
                xx2,yy2 = get_corners(Xdir, Ydir)
                try:
                    a = self.M[xx, yy]
                    b = self.M[xx2, yy2]
                except:
                    self.walls.pop(rindex)
                    continue
                if sum(self.M[xx, yy]) == 3 and sum(self.M[xx2, yy2]) > 2:
					self.M[Xdir, Ydir] = 0
					self.walls.pop(rindex)
					for index, ii in enumerate(xx):
						if self.M[xx[index], yy[index]] == 1:
							self.walls.append(np.array([xx[index], yy[index]]))
        self.M[:, 0] = 1; self.M[:, -1] = 1
        self.M[0, :] = 1; self.M[-1, :] = 1
        
        #Clear Starting Location
        xcoord = int(self.M.shape[0]/2.) 
        ycoord = int(self.M.shape[1]/2.)      
        self.M[1:-1, ycoord] = 0
          
        
        # Create Fight Pit
        width = int(self.M.shape[0]*0.1)
        height = int(self.M.shape[1]*0.1)
        self.M[xcoord-width:xcoord+width+1, ycoord-height:ycoord+height+1] = 0
        
        return self.M
    def _load_standard2(self):
        random_size = random.randint(10,50)
        if random_size%2 == 0: random_size+=1
        
        w = random.choice([2,3])
        self.M = np.zeros((random_size, random_size))
        
        self.M[:, 0] = 1; self.M[:, -1] = 1
        self.M[0, :] = 1; self.M[-1, :] = 1
        
        for i in np.arange(random_size)[::w]:
            self.M[i,::w]=1
        return self.M
        
    def _load_standard(self):       
        self.M = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
                    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
                    [1,0,0,1,0,1,1,0,0,1,0,0,1,1,0,1,0,0,1],
                    [1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1],
                    [1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1],
                    [1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
                    [1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
                    [1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1],
                    [1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1],
                    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
                    [1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        
        self.M=np.array(self.M)
        self.M = self.M.T
        return self.M
    def _create_pellets(self):
        for xindex, x in enumerate(self.map):
            for yindex, y in enumerate(x):
                if y == 0:
                    self.pellets.append((xindex,yindex))
        

M = Map()     


