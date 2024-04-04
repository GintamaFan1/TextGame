import random
from skills import Skills
from item import Item
from characters import Hero, Villain
from termcolor import colored

class Map:
    def __init__(self,name, height, width):
        self.name = name
        self.height = height
        self.width = width
        self.tiles = {}
        self.hero_explored = []
        self.villain_explored = []
    
    def create_map(self, block_percentage=0.1):
        for i in range(self.height):
            for j in range(self.width):
                self.tiles[(i,j)] = Tile((i,j))
        
        total_tiles = self.height * self.width
        num_blocked_tiles = int(total_tiles * block_percentage)
        blocked_tiles = random.sample(list(self.tiles.values()), num_blocked_tiles)

        for tile in blocked_tiles:
            tile.add_object("Blocked")
    
    def show_map(self):
        for i in range(self.height):
            for j in range(self.width):
                has_item_or_skill = False
                is_player = False
                for obj in self.tiles[(i,j)].objects:
                    if isinstance(obj, Item) or isinstance(obj,Skills):
                        has_item_or_skill = True
                        break
                    if isinstance(obj, Hero) or isinstance(obj, Villain):
                        if obj.is_player == True:
                            is_player = True
                            break
                    

                if "Blocked" in self.tiles[(i,j)].objects:
                    print("X ",end="")
                elif  len(self.tiles[(i,j)].objects) == 0:
                    print("_ ", end="")
                elif has_item_or_skill == True:
                    print(colored("I ", "yellow"), end="")
                elif is_player == True:
                    print(colored("P ", "green"), end="")
                elif isinstance(obj, Hero):
                    print(colored("P ", "blue"), end="")
                else:
                    print(colored("V ", "red"),end="")
                    
            print("")

class Tile:
    
    def __init__(self, coords):
        self.tile = coords
        self.objects = []
    
    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
    
    def check(self):
        if "Blocked" in self.objects:
            return True
        else:
            return False

    
        

    

       
        