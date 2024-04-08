
class Player:

    def __init__(self, stage, name, bool):
        self.name = name
        self.tiles = []
        self.is_player1 = bool
        self.connects = []
        self.connect()
        self.path = []
    
    def connect(self):
        if self.is_player1 == True:
            for cord in self.stage.top_connect:
                self.connects.append(cord)
        else:
            for cord in self.stage.bottom_connect:
                self.connects.append(cord)
    def add_path(self, coord):
        if coord not in self.path:
            self.path.append(coord)
