from creatures import Creature
from box import Box
from termcolor import colored
import random

class Stage:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tiles = {}
        self.paths = []
        self.create_stage()
        self.top_connect = []
        self.bottom_connect = []
        self.define_connects()
        self.opponents_connected = False
        self.game_over = False
        self.color_dict = {}
    
    def __str__(self):
        return f"Game Stage"

    def create_stage(self):
        for i in range(self.height):
            for j in range(self.width):
                self.tiles[(i,j)] = Tile(i,j)

    def show_stage(self):
        
        colors = ["red", "grey", "magenta", "yellow", "blue", "cyan", "light_green", "light_yellow", "light_blue", "red",
                  "grey", "magenta", "yellow", "blue", "cyan", "light_green"]
        for i in range(self.height):
            for j in range(self.width):
                tile = self.tiles[(i,j)]
                if isinstance(tile.board, Box):
                    if tile.board.creature not in self.color_dict:
                        self.color_dict[tile.board.creature] = random.choice(colors)
                if tile.artifact == None and tile.board == None:
                    print("_ ", end="")
                elif isinstance(tile.artifact, Creature):
                    if tile.artifact.owner.is_player1:
                        print(colored("P ", "green"), end="")
                    else:
                        print("P ", end="")
                    
                elif tile.artifact == None and isinstance(tile.board, Box):
                    if tile.board.owner.is_player1 == True:
                        print(colored("O ", self.color_dict[tile.board.creature]), end="")
                    else:
                        print(colored("O ", self.color_dict[tile.board.creature]), end="")
            print("")


    def place_artifact(self, obj, coords):
        self.tiles[coords].add_artifact(obj)

    def unplace_artifact(self, obj):
        self.tiles[(obj.x, obj.y)].remove_artifact(obj)

    def define_connects(self):
        for i in range(self.width):
            self.top_connect.append((i,0))
        
        for j in range(self.width):
            self.bottom_connect.append((j,self.width - 1))



class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.artifact = None
        self.board = None

    def __str__(self):
        if self.artifact != None:
            return f"Tile containing {self.artifact} at {self.x, self.y}"
            
    
    def add_artifact(self, obj):
        self.artifact = obj
        obj.x = self.x
        obj.y = self.y
        
    

    def remove_artifact(self, obj):
        if obj == self.artifact:
            self.artifact = None
            obj.x = None
            obj.y = None
        else:
            print(f"{obj} not in tile")




    

