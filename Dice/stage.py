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
        self.colors = ["red", "grey", "magenta", "yellow", "blue", "cyan", "light_green", "light_yellow", "light_blue", "red",
                  "grey", "magenta", "yellow", "blue", "cyan", "light_green","red", "grey", "magenta", "yellow", "blue", "cyan", "light_green",
                  "grey", "magenta", "yellow", "blue", "cyan", "light_green","light_green", "light_yellow", "light_blue"]
    
    def __str__(self):
        return f"Game Stage"

    def create_stage(self):
        for i in range(self.height):
            for j in range(self.width):
                self.tiles[(i,j)] = Tile(i,j)

    def show_stage(self):
        
        
        
        print("x: ",end="")
        for i in range(self.width):
            print(f"{i}".ljust(3), end="")
        print("")
        for i in range(self.height):
            print(f"{i}:".ljust(3), end="")
            for j in range(self.width):
                tile = self.tiles[(i,j)]
                if isinstance(tile.board, Box):
                    if tile.board.creature not in self.color_dict:
                        self.color_dict[tile.board.creature] = self.colors.pop(0)
                if tile.artifact == None and tile.board == None:
                    print("_  ".ljust(2), end="")
                elif isinstance(tile.artifact, Creature):
                    if tile.artifact.owner.is_player1:
                        print(colored("P  ".ljust(2), "green"), end="")
                    else:
                        print("P  ".ljust(2), end="")
                    
                elif tile.artifact == None and isinstance(tile.board, Box):
                    if tile.board.owner.is_player1 == True:
                        print(colored("O  ", self.color_dict[tile.board.creature]), end="")
                    else:
                        print(colored("O  ", self.color_dict[tile.board.creature]), end="")
            print("")


    def place_artifact(self, obj, coords):
        self.tiles[coords].add_artifact(obj)

    def unplace_artifact(self, obj):
        self.tiles[(obj.x, obj.y)].remove_artifact(obj)

    def define_connects(self):
        for i in range(self.height):
            self.top_connect.append((i,0))
        
        for j in range(self.width):
            self.bottom_connect.append((j,self.width - 1))

    def get_empty_touching_tiles(self, player):
        empty = []
        for tile in self.paths:
            if self.tiles[tile].board.owner == player:
                neighbors = self.get_four_neighbors(tile)
                for neigh in neighbors:
                    if self.tiles[neigh].board == None:
                        empty.append(neigh)
        return empty



    def get_four_neighbors(self, point):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if i == -1 and j == -1:
                    continue
                if i == 1 and j == -1:
                    continue
                if i == -1 and j == 1:
                    continue
                if i == 1 and j == 1:
                    continue
                new_i, new_j = i + point[0], j + point[1]
                if new_i >= 0 and new_i < self.height and new_j >= 0 and new_j < self.width:
                    neighbors.append((new_i, new_j))
        return neighbors




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




    

