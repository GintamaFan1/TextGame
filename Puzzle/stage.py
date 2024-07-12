import rich
from rich import print
import random

RED = "rgb(255,0,0)"
BLUE = "rgb(0,0,255)"
BROWN = "rgb(155,50,155)"
PURPLE = "rgb(255,0,255)"

class Stage:
    def __init__(self):
        self.height = 20
        self.width = 30
        self.level = 1
        self.tiles = {}
        for i in range(self.height):
            for j in range(self.width):
                self.tiles[(i,j)] = Tiles((i,j))
    
    def show_stage(self):
        for i in range(self.height):
            for j in range(self.width):
                tile = self.tiles[(i,j)]
                if tile.exploded == True and tile.frozen == True:
                    print(f"[{PURPLE}]_ [/{PURPLE}]", end="")
                elif tile.exploded == True:
                    print(f"[{RED}]X [/{RED}]", end="")
                elif tile.frozen == True:
                    print(f"[{BLUE}]F [/{BLUE}]", end="")
                else:
                    print(f"_ ", end="")
            print("")

    def place_ability(self, abi):
        random_x = random.randint(0,self.height - 1 )
        random_y = random.randint(0,self.width - 1)

        abi.place((random_x, random_y))

    def reset(self):
        for tile in self.tiles:
            self.tiles[tile].exploded = False
            self.tiles[tile].frozen = False
            self.tiles[tile].broken = False
            self.tiles[tile].character_placed_here = False
            self.tiles[tile].condition = None
            self.tiles[tile].character = None



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
        
    



