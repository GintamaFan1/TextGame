
class Stage:

    def __init__(self):
        self.height = 20
        self.width = 30
        self.tiles = {}


class Tiles:

    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.exploded = False
        self.frozen = False
        self.broken = False
        self.character_placed_here = False
        self.condition = None
        
    



