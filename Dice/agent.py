from dice import Dice, roll_three, evaluator
from box import Box
from creatures import Creature
from stage import Stage, Tile
from termcolor import colored
import random
import math
from box import Box
from interactions import *

class Ai_Agent:

    def __init__(self, stage, player, creature_storage, opponent, move, sum, abi):
        self.stage = stage
        self.moves = []
        self.points = {}
        self.player = player
        self.creature_storage = creature_storage
        self.creatures = player.creatures
        self.opponent = opponent
        self.life = 40
        self.dice1 = move
        self.dice2 = sum
        self.dice3 = abi


    def rolling(self):
        roll_three(self.dice1,self.dice2,self.dice3,self.points)

    

    def pick_enemy(self):
        choice = random.choice(self.opponent.creatures)
        return (choice.x, choice.y)
    
    def pick_enemy_endzone(self):
        choice = random.choice(self.opponent.connects)
        return choice
    
    def pick_empty(self):
        empty_tiles = [tile for tile in self.stage.paths if not isinstance(self.stage.tiles[tile].artifact, Creature)]
        
        if empty_tiles:
            random.shuffle(empty_tiles)
            return empty_tiles[0]
        
        else:
            
            print(empty_tiles,"trouble obtaining empty tiles" )

        return None
    
    
    def make_move(self, creature, target):
        print(target, "target")
        crawler = Crawler(self.stage, creature, target)
        moves = crawler.find_move()


        if moves == None:
            print(f"crawler returned empty from {creature.x, creature.y} to {target}")
            return None

        else:
            
            if self.points["Movement"] >= len(moves):
                print("can make the full move")
                print(moves, "moves")
                movements = self.creature_move(creature, moves)
                self.points["Movement"] -= movements

            else:
                print("can only make partial move")
                movements = self.creature_move(creature, moves)
                self.points["Movement"] -= movements
                

    def summon_creature(self):
        random.shuffle(self.creature_storage)
        choice = self.creature_storage.pop(0)
        return choice


    def place_box_on_connect(self, creature):
        creature_box = Box(creature, self.stage, self.player)
        
        tries = 6
        while tries > 0 and creature_box.placed == False:
            
            shape = creature_box.pick_shape()
            tile = creature_box.pick_connect_tile()
            
            
            for i in range(-2, 2):
                for j in range(-2, 2):
                    x, y = tile[0] + i, tile[1] + j
                    if x >= 0 and x < self.stage.height and y >= 0 and y < self.stage.width:
                        print(f"trying version: {x, y}, {shape}")
                        self.connect_fitter(creature_box, shape, (x, y))

                        if creature_box.placed == False:
                            self.stage.unplace_artifact(creature_box)
                        else:
                            break
                if creature_box.placed == True:
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
        

        while tries > 0 and creature_box.placed == False:
            shape = creature_box.pick_shape()
            point = random.choice(self.player.path)
            tile = creature_box.pick_path_tile(point)
            
            if tile:
                for i in range(-2, 2):
                    for j in range(-2, 2):
                        x, y = tile[0] + i, tile[1] + j
                        if x >= 0 and x < self.stage.height and y >= 0 and y < self.stage.width and (x, y) not in self.stage.paths:
            
                            self.path_fitter(creature_box, shape, (x, y), point)

                            if creature_box.placed == False:
                                self.stage.unplace_artifact(creature_box)
                            else:
                                break
                    if creature_box.placed == True:
                        break
                if creature_box.placed == True:
                    break
                
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
        
        print(self.creature_storage, self.creatures, "creatures")

        if len(self.creature_storage) == 0 and len(self.creatures) == 0:
            print("no moves left")
            self.stage.game_over == True
            return

        for cat in self.points:
        
            if cat == "Summon":
                if self.points[cat] >= 10:
                    has_summon = True
            elif cat == "Movement" and self.stage.opponents_connected == True:
                if self.points[cat] > 0:
                    has_movement = True
            elif cat == "Ability":
                if self.points[cat] > 0:
                    has_ability = True
        
        if self.stage.opponents_connected == False:
            connected = self.check_connection()
            if connected:
                self.stage.opponents_connected = True
                print(colored("connected", "magenta"))

        
        if has_movement == True:
            if len(self.creatures) > 0:
                random.shuffle(self.creatures)
                
                creature = self.creatures[0]

                empty = ""
                enemy = "enemy"
                endzone = "endzone"

                options = [empty, enemy, endzone]

                random.shuffle(options)

                choice = options[0]

                if self.stage.opponents_connected == False:
                    target = self.pick_empty()
                    print(f"{target}")
                    self.make_move(creature, target)
                    

                elif choice == "empty":
                    target = self.pick_empty()
                    print(f"{target}")
                    self.make_move(creature, target)
                elif choice == "enemy":
                    if len(self.opponent.creatures) > 0:
                        target = self.pick_enemy()
                        print(f"{target}")
                        self.make_move(creature, target)
                    else:
                        target = self.pick_empty()
                        print(f"{target}")
                        self.make_move(creature, target)

                elif choice == "endzone":
                    target = self.pick_enemy_endzone()
                    print(f"{target}")
                    self.make_move(creature, target)


        if has_ability == True:
            print("abilities are avaiable")
            print(self.points,self.player.name, "points")

        if has_summon == True and len(self.creature_storage) > 0:
            if len(self.creatures) == 0:
                
                creature = self.summon_creature()

                self.place_box_on_connect(creature)
            else:
                creature = self.summon_creature()

                self.place_box_on_path(creature)
        

    def connect_fitter(self, box, shape, tile):
        self.stage.place_artifact(box, tile)
        box.define_shapes()
        box.fit_shape_to_connect(shape)

    def path_fitter(self, box, shape, tile, point):
        
        self.stage.place_artifact(box, tile)
        box.define_shapes()
        box.fit_shape_to_path(shape, point)

    def check_connection(self):
        connects = False
        for sets in self.player.path:
            for sets2 in self.opponent.path:
                neighbors = self.get_tile_neighbors(sets)
                if sets2 in neighbors:
                    connects = True
                    break
            if connects == True:
                break
    
        return connects 
    
    def get_tile_neighbors(self, point):
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

                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width and (new_i,new_j):
                    neighbors.append((new_i, new_j))
        
        return neighbors    

    def creature_move(self, creature, moves):

        moves_made = 0
        if moves_made >= self.points["Movement"]:
            return moves_made

        for move in moves:

            starting_tile = (creature.x, creature.y)
            
            object = self.stage.tiles[move].artifact

            if not isinstance(object, Creature):
            
                self.stage.unplace_artifact(creature)
                self.stage.place_artifact(object, starting_tile)
                
                
                self.stage.place_artifact(creature, move)
                

                
                moves_made += 1
            else:
                if creature.owner == object.owner:
                    print(f"{object.name, object.owner.name} was in the way of {creature.name, creature.owner.name}")
                    moves_made += 1
                    continue
                battle(creature, object)
                died(object)

                path = Box(Creature, self.stage, self.player)

                self.stage.unplace_artifact(object)
                self.stage.unplace_artifact(creature)
                self.stage.place_artifact(path, starting_tile)
                self.stage.place_artifact(creature, move)

                break
        
        return moves_made

                


    

        
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
                if i == 1 and j == -1:
                    continue
                if i == -1 and j == 1:
                    continue
                if i == 1 and j == 1:
                    continue

                new_i, new_j = i + self.x, j + self.y

                if new_i >= 0 and new_i < self.stage.height  and new_j >= 0 and new_j < self.stage.width and (new_i, new_j) in self.stage.paths:
                    available_moves.append((new_i, new_j))
        
        return available_moves

    def find_move(self):
        available = self.available_moves()
        sorted_value = self.distance_value(available)
    
        for move in sorted_value:
            if self.solved == False:
                self.current_search.append(move)
                self.moves_made.append(move)
                self.make_move(move)
                if self.solved == False:
                    self.current_search.remove(move)
                if self.solved == True:
                    break
            

        if self.solved == True:
            return self.current_search
        else:
            print("no path available for this crawler")
            return None

    def make_move(self, move):
        
        if self.x == self.ending[0] and self.y == self.ending[1]:
            self.solved = True
            
            return
            
        
        self.x = move[0]
        self.y = move[1]

        available = self.available_moves()

        sorted_value = self.distance_value(available)

        if len(available) == 1:
            return
        
        for move2 in sorted_value:
            if move2 not in self.moves_made and move2 != self.ending and self.solved == False:
                self.moves_made.append(move2)
                self.current_search.append(move2)
                self.make_move(move2)
                
                if self.solved == False:
                    self.current_search.remove(move2)
                if self.solved == True:
                
                    return
            elif move2 == self.ending:
                
                self.moves_made.append(move2)
                self.current_search.append(move2)
                self.solved = True
                return 
        
        return
        
        
    def distance(self, point1, point2):
        distance = math.sqrt((point2[0] - point1[0])** 2 + (point2[1] - point1[1])** 2)

        return distance
    
    def distance_value(self, list):
        dictio = {}
        for move in list:
            distance = self.distance(move, self.ending)
            dictio[move] = distance
        
        sorted_value = sorted(dictio.items(), key=lambda x: x[1])
        sorted_value = dict(sorted_value)

        return sorted_value
    
    

    

    
    




            

