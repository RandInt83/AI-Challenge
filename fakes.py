import copy

class FakeBot:
    def __init__(self):
        self._id = -1
        self._pos = (0, 9)
        self._kill = False
        self._alive = True
        self._last_pos = []

class FakeTeam:
    def __init__(self):
        self._id = None
        self.name = None
        self.bots = []
        self.start_positions = []
    def get_id(self):
        return self._id

class FakeMap:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.game_map = None
        self.map = None
        self.pellets = []
        self.walls = []

class FakeGame:
    def __init__(self):
        self.teams = []
        self.game_map = FakeMap()

def init_Game(fakeGame, Game):
    for i in range(len(Game.teams)):
        fakeGame.teams.append(FakeTeam())
        fakeGame.teams[i]._id = Game.teams[i]._id
        fakeGame.teams[i].name = Game.teams[i].name
        fakeGame.teams[i].start_positions = copy.copy(Game.teams[i].start_positions)
        for j in range(len(Game.teams[i].bots)):
            fakeGame.teams[i].bots.append(FakeBot())
            fakeGame.teams[i].bots[j]._id = fakeGame.teams[i]._id
    fakeGame.game_map.game_map = copy.copy(Game.game_map.game_map)
    fakeGame.game_map.map = copy.copy(Game.game_map.map)
    fakeGame.game_map.walls = copy.copy(Game.game_map.walls)
    fakeGame.game_map.height = Game.game_map.height
    fakeGame.game_map.width = Game.game_map.width

def update_Game(fakeGame, Game):
    for i in range(len(fakeGame.teams)):
        for j in range(len(fakeGame.teams[i].bots)):
            fakeGame.teams[i].bots[j]._pos = Game.teams[i].bots[j]._pos
            fakeGame.teams[i].bots[j]._kill = Game.teams[i].bots[j]._kill
            fakeGame.teams[i].bots[j]._alive = Game.teams[i].bots[j]._alive
            fakeGame.teams[i].bots[j]._last_pos = copy.copy(Game.teams[i].bots[j]._last_pos)
    fakeGame.game_map.pellets = copy.copy(Game.game_map.pellets)
