import rich
from rich import print

RED = "rgb(255,0,0)"
BLUE = "rgb(0,0,255)"
BROWN = "rgb(155,50,155)"
PURPLE = "rgb(255,0,255)"

class Stage:
    def __init__(self):
        self.height = 20
        self.width = 30
        self.tiles = {}
        for i in range(self.height):
            for j in range(self.width):
                self.tiles[(i,j)] = Tiles((i,j))
    
    def show_stage(self):
        for i in range(self.height):
            for j in range(self.width):
                tile = self.tiles[(i,j)]

                if tile.exploded == True:
                    print(f"[{RED}]__ [/{RED}]", end="")
                else:
                    print(f"__ ", end="")




class Tiles:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.exploded = False
        self.frozen = False
        self.broken = False
        self.character_placed_here = False
        self.condition = None
        self.character = None
        
    



