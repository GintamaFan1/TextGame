import random
from skills import Skills
from item import Item
from characters import Hero, Villain
from termcolor import colored
import pygame

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

    def place_object(self, obj, x, y):
        self.tiles[(x, y)].add_object(obj)

    def remove_object(self, obj):
        for tile in self.tiles.values():
            if obj in tile.objects:
                tile.remove_object(obj)
                break
    
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
    
    def draw(self, surface):
        for tile in self.tiles.values():
            tile.draw(surface)

    def place_characters(self,heroes, villains):
        row = 4
        col = 4
        heroes_copy = heroes.copy()
        villains_copy = villains.copy()
        for i in range(row  ):
            for j in range(col ):
                if len(self.tiles[(i,j)].objects) == 0 and len(heroes_copy) != 0:
                    random.shuffle(heroes_copy)
                    random_hero = heroes_copy.pop(0)
                    self.place_object(random_hero, i, j)
                    
        
        for i in range(self.height - row  , self.height ):
            for j in range(self.width - col  , self.width ):
                if len(self.tiles[(i,j)].objects) == 0 and len(villains_copy) != 0:
                    random.shuffle(villains_copy)
                    random_villain = villains_copy.pop(0)
                    self.place_object(random_villain, i, j)

    def place_items(self, skills, items):

        empty_tiles = [tile for tile in self.tiles.values() if len(tile.objects) == 0]
        

        random.shuffle(skills)
        random.shuffle(items)
        
        # Combine skills and items into a single list
        objects_to_place = skills + items
        
        # Calculate the number of items and skills to place
        items_to_place = len(items)
        skills_to_place = len(skills)
        total_objects_to_place = items_to_place + skills_to_place
        
        # Get a random sample of empty tiles
        num_tiles_to_use = min(total_objects_to_place, len(empty_tiles))
        tiles_to_use = random.sample(empty_tiles, num_tiles_to_use)
        
        for tile in tiles_to_use:
            if items_to_place > 0:
                self.place_object(items.pop(0), tile.x, tile.y)
                items_to_place -= 1
            elif skills_to_place > 0:
                self.place_object(skills.pop(0), tile.x, tile.y)
                skills_to_place -= 1


class Tile:
    
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.objects = []
    
    def add_object(self, obj):
        self.objects.append(obj)
        if obj != "Blocked":
            obj.x = self.x
            obj.y = self.y

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
            if obj != "Blocked":
                obj.x = None
                obj.y = None
    
    def check(self):
        if "Blocked" in self.objects:
            return True
        else:
            return False
    
    def draw(self, surface):
        TILE_SIZE = 2
        tile_rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, (128, 128, 128), tile_rect)

        for obj in self.objects:
            if obj != "Blocked":
                print(obj, "obj")
                obj.draw(surface, self.x, self.y)

    
        

    

       
        