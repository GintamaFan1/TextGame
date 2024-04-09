from dice import Dice, roll_three, evaluator
from box import Box
from creatures import Creature
from stage import Stage, Tile
from termcolor import colored
import random
import math
from box import Box

class Ai_Agent:

    def __init__(self, stage, player, creature_storage, opponent, move, sum, abi):
        self.stage = stage
        self.moves = []
        self.points = {}
        self.player = player
        self.creature_storage = creature_storage
        self.creatures = player.creatures
        self.opponent = opponent
        self.life = 3
        self.dice1 = move
        self.dice2 = sum
        self.dice3 = abi


    def rolling(self):
        roll_three(self.dice1,self.dice2,self.dice3,self.points)

    

    def pick_enemy(self):
        return random.choice(self.opponent.creatures)
    
    def pick_empty(self):
        empty_tiles = [tile for tile in self.stage.paths if self.stage.tiles[tile].artifact == None]
        
        if empty_tiles:
            random.shuffle(empty_tiles)

            return empty_tiles[0]
        else:
            
            print(empty_tiles,"trouble obtaining empty tiles" )

        return None
    
    
    def make_move(self, creature, target):
        crawler = Crawler(self.stage, creature, target)
        moves = crawler.find_move()


        if moves == None:
            print("crawler returned empty")
            return None

        else:
            if len(self.points["Movement"]) == len(moves):
                print("can make the full move")
            else:
                print("can only make partial move")
                print(len(self.points["Movement"]), "movement points")
                print(len(moves), "len of moves")

    def summon_creature(self):
        random.shuffle(self.creature_storage)
        return self.creature_storage[0]



    def place_box_on_connect(self, creature):
        creature_box = Box(creature, self.stage, self.player)
        
        tries = 6
        while tries > 0 and creature_box.placed == False:
            shape = creature_box.pick_shape
            tile = creature_box.pick_connect_tile()
            
            for i in range(-2, 2):
                for j in range(-2, 2):
                    self.connect_fitter(creature_box, shape, (tile[0] + i, tile[0] + j))

                    if creature_box.placed == False:
                        self.stage.tiles[tile[0] + i, tile[1] + j].unplace_artifact(creature_box)
                    else:
                        break
            if creature_box.placed == True:
                break

            tries -= 1
        
        if creature_box.placed == True:
            self.creatures.append(creature)
            self.points["Summon"] -= 10
            print("creature placed")

               
    def place_box_on_path(self, creature):
        creature_box = Box(creature, self.stage, self.player)
        tries = 6

        while tries > 6 and creature_box
            shape = creature_box.pick_shape
            tile = creature_box.pick_connect_tile()

            for i in range(-2, 2):
                for j in range(-2, 2):
                    self.path_fitter(creature_box, shape, (tile[0] + i, tile[1] + j))

                    if creature_box.placed == False:
                        self.stage.tiles[(tile[0] + i, tile[1] + j)]
                    else:
                        break
                if 
            
            tries -= 1
                
        
        if creature_box.placed == True:
            self.creatures.append(creature)
            self.points["Summon"] -= 10
            print("creature placed")
    
    def run(self):
        self.rolling()

        has_movement = False
        has_ability = False
        has_summon = False

        for cat in self.points:
            print(self.points[cat], f"{cat}")
            if cat == "Summon":
                if self.points[cat] >= 10:
                    has_summon = True
            elif cat == "Movement":
                if self.points[cat] > 0:
                    has_movement = True
            elif cat == "Ability":
                if self.points[cat] > 0:
                    has_ability = True

            
        

                    
        
        if has_movement == True:
            if len(self.creatures) > 0:
                random.shuffle(self.creatures)
                
                creature = self.creatures[0]

                empty = "empty"
                enemy = "enemy"

                options = [empty, enemy]

                random.shuffle(options)

                choice = options[0]

                if len(self.opponent.creatures) == 0:
                    target = self.pick_empty()
                    self.make_move(creature, target)

                elif choice == "empty":
                    target = self.pick_empty()
                    self.make_move(creature, target)
                else:
                    target = self.pick_enemy()
                    self.make_move(creature, target)


        if has_ability == True:
            print("abilities are avaiable")

        if has_summon == True:
            creature = self.summon_creature()

            self.place_box(creature)


    def connect_fitter(self, box, shape, tile):
        self.stage.tiles[tile].place_artifact(box)
        box.define_shapes()
        box.fit_shape_to_connect(shape)

    def path_fitter(self, box, shape, tile):
        self.stage.tiles[tile].place_artifact(box)
        box.define_shapes()
        box.fit_shape_to_path(shape)


        




                

        

    

        
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

                if new_i >= 0 and new_i < self.stage.height  and new_j >= 0 and new_j < self.stage.width and (new_i, new_j) in self.stage.paths:
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
    
    




            

