
class Player:

    def __init__(self, stage, name, bool):
        self.name = name
        self.stage = stage
        self.is_player1 = bool
        self.connects = []
        self.connect()
        self.path = []
        self.is_AI = True
        self.creatures = []
    
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
    def check_creatures(self):
        creatures = []
        for creature in self.creatures:
            if creature.died == True:
                continue
            elif creature.HP <= 0:
                creature.died = True
                continue
            else:
                creatures.append(creature)
    
        self.creatures = creatures
        
                
