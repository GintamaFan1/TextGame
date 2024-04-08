from dice import Dice, roll_three, evaluator
from box import Box
from creatures import Creature
from stage import Stage, Tile
from termcolor import colored
import random
import math
from box import Box

class Ai_Agent:

    def __init__(self, stage, player, creature_storage):
        self.stage = stage
        self.moves = []
        self.points = {}
        self.player = player
        self.creature_storage = creature_storage


    def rolling(self, dice1, dice2, dice3):
        roll_three(dice1,dice2,dice3,self.points)

    def pick_creature(self):
        
        available_creatures = [tile for tile in self.stage.tiles.objects if isinstance(tile.artifact, Creature) 
                            and tile.artifact.owner == self.player]
        if available_creatures:
            random.shuffle(available_creatures)

            return available_creatures[0]
        else:
            print("no creatures to select")

    def pick_enemy(self):
        available_creatures = [tile for tile in self.stage.tiles.objects if isinstance(tile.artifact, Creature) 
                            and tile.artifact.owner != self.player]
        if available_creatures:
            random.shuffle(available_creatures)

            return available_creatures[0]
        else:
            print("no enemies to pick")

        return None
    
    def pick_empty(self):
        empty_tiles = [tile for tile in self.stage.tiles.objects if len(tile.artifact) == 0 and (tile.x,tile.y) in self.stage.paths]
        
        if empty_tiles:
            random.shuffle(empty_tiles)

            return empty_tiles[0]
        else:
            print("trouble obtaining empty tiles" )

        return None
    
    
    def make_move(self, creature, target):
        crawler = Crawler(self.stage, creature, target)
        moves = crawler.find_move()

        if moves == None:
            print("crawler returned empty")
            return None

        else:
            if len(self.points["Movement"]) == len(moves):
                print("move made")

    def summon_creature(self):
        creature = None
        random.shuffle(self.creature_storage)
        return self.creature_storage[0]



    def summon(self, creature):
        creature = Box(self.stage, creature, self.player)
        creature.pick_shape()
        
    
    def run(self):
        self.rolling()


                

        

    

        
class Crawler:

    def __init__(self, stage, creature, ending):
        self.stage = stage
        self.creature = creature
        self.moves_made = []
        self.current_search = []
        self.ending = ending
        self.x = creature.x
        self.y = creature.y
        self.solved = False

    def available_moves(self):
        available_moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if i == -1 and j == 1:
                    continue
                if i == 2 and j == -1:
                    continue
                if i == -1 and j == 2:
                    continue
                if i == 2 and j == 2:
                    continue

                new_i, new_j = i + self.x, j + self.y

                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width and (new_i, new_j) in self.stage.paths:
                    available_moves.append((new_i, new_j))
        
        return available_moves

    def find_move(self):
        
        available = self.available_moves()
        available_value = {}

        for move in available:
            distance = self.distance(move, self.ending)
            available_value[move] = distance
        
        sorted_value = sorted(available_value.items(), key=lambda x: x[1])

        sorted_value = dict(sorted_value)

        

        for move, value in sorted_value:
            self.current_search.append(move)
            self.moves_made.append(move)
            self.make_move(move)

        if self.solved == True:
            return self.current_search
        else:
            print("no path available for this crawler")
            return None

    def make_move(self, move):
        if move.x == self.ending.x and move.y == self.ending.y:
            self.solved = True
            return
        
        self.x = move.x
        self.y = move.y

        available = self.available_moves()

        if len(available) == 1:
            self.current_search.remove(move)
            return
        
        for move in available:
            if move not in self.moves_made:
                self.moves_made.append(move)
                self.current_search.append(move)
                self.make_move(move)
        
        
    def distance(self, point1, point2):
        distance = math.sqrt((point2.x - point1.x)** 2 + (point2.y - point1.y)** 2)

        return distance
    

    def find_neighbors(self, point):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_i, new_j = i + point.x, j + point.y

                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width and (new_i, new_j) in self.stage.paths:
                    neighbors.append((new_i, new_j))
        return neighbors
    
    




            

