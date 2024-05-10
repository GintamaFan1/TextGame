from dice import Dice, roll_three
from box import Box
from creatures import Creature
from stage import Stage, Tile
from termcolor import colored
import random
import math
from box import Box
from interactions import *
import time
from collections import deque
from ability import *

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
        moves = []
        for move in self.stage.paths:
            if move in self.opponent.connects:
                moves.append(move)
        return random.choice(moves)
    
    def pick_empty(self):
        empty_tiles = [tile for tile in self.stage.paths if not isinstance(self.stage.tiles[tile].artifact, Creature)]
        
        if empty_tiles:
            random.shuffle(empty_tiles)
            choice = empty_tiles[0]
            if choice not in self.stage.paths:
                self.pick_empty()
            return choice
        else:
            print(empty_tiles,"trouble obtaining empty tiles" )
        return None
    
    
    def make_move(self, creature, target):
        crawler = Crawler(self.stage, creature, target)
        moves = crawler.find_move()
        if moves == None:
            print(f"crawler returned empty from {creature.x, creature.y} to {target}")
            for moves in self.stage.paths:
                print(moves, "path")
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
    
    def pick_ability(self, creature, abilities):
        push_available = False
        fire_storm_available = False
        heal_shot_available = False
        Teleport_available = False
        four_tiles = self.get_tile_neighbors((creature.x, creature.y))
        for tile in four_tiles:
            if tile in self.stage.paths:
                if isinstance(self.stage.tiles[tile].artifact, Creature):
                    if creature.owner != self.stage.tiles[tile].artifact.owner:
                        push_available = True
        
        long_tile = self.get_long_neighbors((creature.x, creature.y))
        number_of_enemies = 0

        for tile in long_tile:
            obj = self.stage.tiles[tile].artifact

            if isinstance(obj, Creature):
                if obj.owner != creature.owner:
                    number_of_enemies += 1
        
        if number_of_enemies > 1:
            fire_storm_available = True

        if fire_storm_available == False and push_available == False:
            heal_shot_available = True
        
        if fire_storm_available == False and push_available == False and heal_shot_available == False:
            Teleport_available = True

        if push_available == True:
            for abi in abilities:
                if abi.name == "Push":
                    return abi
        
        elif fire_storm_available == True:
            for abi in abilities:
                if abi.name == "Fire Storm":
                    return abi
        
        elif heal_shot_available == True:
            for abi in abilities:
                if abi.name == "Heal Shot":
                    return abi
        
        else:
            for abi in abilities:
                if abi.name == "Teleport":
                    return abi

        

    
    def run(self):
        self.rolling()
        has_movement = False
        has_ability = False
        has_summon = False
    
        if len(self.creature_storage) == 0 and len(self.creatures) == 0:
            print("no moves left")
            self.stage.game_over = True
            return
        
        self.player.check_creatures()
        self.creatures = self.player.creatures
        
        print(self.points, self.player.name)

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
            self.player.check_creatures()
            self.creatures = self.player.creatures
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
                    print(f" empty {target}")
                    self.make_move(creature, target)
                    
                elif choice == "enemy":
                    if len(self.opponent.creatures) > 0:
                        target = self.pick_enemy()
                        print(f" enemy {target}")
                        self.make_move(creature, target)
                    else:
                        target = self.pick_empty()
                        print(f" empty {target}")
                        self.make_move(creature, target)

                elif choice == "endzone":
                    target = self.pick_enemy_endzone()
                    print(f" endzone {target}")
                    self.make_move(creature, target)


        if has_ability == True and self.stage.opponents_connected == True:
            print(colored(f"calling on ability, {self.player.name}", "red"))
            
            self.player.check_creatures()
           
            self.creatures = self.player.creatures

            
            creature = None
            if len(self.creatures) > 0:
                creature = random.choice(self.creatures)
            if creature:
                print(f"{creature.name, creature.HP, creature.x, creature.y}")
                fire_storm = Firestorm(self.stage, "Fire Storm", 50, self)
                heal_shot = HealShot(self.stage, "Heal Shot", 20, self)
                teleport = Teleport(self.stage, "Teleport", 50, self)
                push = Push(self.stage, "Push", 20, self)

                abilities = [fire_storm, heal_shot, teleport, push]
                ability = self.pick_ability(creature, abilities)
                print(colored(f"Ai chose {ability.name}", "cyan"))

            
                if ability.name == push.name and self.points["Ability"] >= ability.cost and creature:
                    four_tiles = self.get_tile_neighbors((creature.x, creature.y))

                    for tile in four_tiles:
                        obj = self.stage.tiles[tile].artifact
                        if isinstance(obj, Creature):
                            print(colored(f"Ai has targets for push", "cyan"))
                            if obj.owner != creature.owner and self.points["Ability"] >= ability.cost:
                                ability.activate(creature, obj)
                                
                elif ability.name == fire_storm.name and self.points["Ability"] >= ability.cost and creature:
                    long_tiles = self.get_long_neighbors((creature.x, creature.y))

                    for tile in long_tiles:
                        obj = self.stage.tiles[tile].artifact
                        if isinstance(obj, Creature):
                            print(colored(f"Ai has targets for fire storm", "cyan"))
                            if obj.owner != creature.owner and self.points["Ability"] >= ability.cost:
                                ability.activate(creature)
                                
                elif ability.name == heal_shot.name and self.points["Ability"] >= ability.cost and creature:
                    if len(self.creatures) >= 2:
                        for char in self.creatures:
                            if creature.name != char.name and self.points["Ability"] >= ability.cost:
                                ability.activate(creature, char)
                                
                
                else:
                    if self.points["Ability"] >= ability.cost and creature:
                        ability.activate(creature)
                        
                    else:
                        print("not enough AP")

            self.stage.show_stage()

        


        if has_summon == True and len(self.creature_storage) > 0:
            if len(self.creatures) == 0:
                
                creature = self.summon_creature()

                self.place_box_on_connect(creature)
            else:
                choices = ["path", "connect"]
                choice2 = random.choice(choices)
                creature = self.summon_creature()
                if choice2 == "path":
                    self.place_box_on_path(creature)
                else:
                    self.place_box_on_path(creature)
        
        print(self.points, "points")
        

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
                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width and (new_i,new_j) in self.stage.paths:
                    neighbors.append((new_i, new_j))
        return neighbors

    def get_long_neighbors(self, point, radius=2):
        neighbors = []
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i == 0 and j == 0:
                    continue
               
                
                new_i, new_j = i + point[0], j + point[1]
                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width and (new_i,new_j) in self.stage.paths:
                    neighbors.append((new_i, new_j))
        return neighbors    
    

    def creature_move(self, creature, moves):
        moves_made = 0
        for move in moves:
            if moves_made >= self.points["Movement"]:
                return moves_made

            
            object = self.stage.tiles[move].artifact
            if not isinstance(object, Creature):
                self.stage.unplace_artifact(creature)
                self.stage.place_artifact(creature, move)
                
                moves_made += 1

            else:
                if creature.owner == object.owner:
                    moves_made += 1
                    continue
                battle(creature, object)
                self.player.check_creatures()

                self.creatures = self.player.creatures
                
                if object.HP <= 0:
                    
                    self.stage.unplace_artifact(object)
                    
                    self.stage.unplace_artifact(creature)
                    
                    self.stage.place_artifact(creature, move)
                    

                    break
                elif creature.HP <= 0:
                    
                    self.stage.unplace_artifact(creature)
                
                    
                    break
                
                else:
                    break


        
        return moves_made
        
    def player_turn(self):
        
        
        print("press any key to roll: ")

        j = input("")

        while j == None:
            j = input("")

        self.rolling()

        print("Result: ",self.points)

        end_turn = False

        while end_turn == False:
            connected = False
            if self.stage.opponents_connected == False:
                connected = self.check_connection()
            if connected:
                self.stage.opponents_connected = True
                print(colored("connected", "magenta"))

            if len(self.creature_storage) == 0 and len(self.creatures) == 0:
                print("no moves left")
                self.stage.game_over = True
                return
            self.stage.show_stage()
            print(self.points)

            print("what would you like to do next? ")

            print("enter 1 to move: ")
            print("enter 2 to activate abilities: ")
            print("enter 3 to summon: ")
            print("enter 4 to end_turn")
            try:
                x = int(input(""))

                while x not in [1, 2, 3, 4]:
                    print("enter valid input")
                    x = int(input(""))

                if x == 1:
                    if self.points["Movement"] <= 0:
                        print(colored("not enough points", "red"))
                        break
                    self.player.check_creatures()
                    self.creatures = self.player.creatures

                    if len(self.creatures) > 0:
                        for creature in self.creatures:
                            index = self.creatures.index(creature)
                            print(f"{index}: {creature}")
                        print("Select creature to move: ")

                        creature_index = int(input(""))

                        while creature_index not in range(len(self.creatures)):
                            print("enter valid creature")

                            for creature in self.creatures:
                                index = self.creature.index(creature)
                                print(f"{index}: {creature}")
                            print("select creature to move: ")

                            creature_index = int(input(""))

                        creature = self.creatures[creature_index]
                        tile_color = {}
                        colors = ["red"]

                        for tile in self.stage.paths:
                            if isinstance(self.stage.tiles[tile].artifact, Creature):
                                tile_color[tile] = colors[0]
                        for tile in self.stage.paths:
                            if tile in tile_color:
                                print(colored(f"{tile}", tile_color[tile] ), end="")
                            else:
                                print(tile, end="")
                        print("")



                        print("enter destination i: ")

                        i = int(input(""))

                        print("enter destination j: ")

                        j = int(input(""))

                        while (i,j) not in self.stage.paths:
                            print(self.stage.paths, "available paths")
                            print("enter valid destination: ")
                            print("enter destination i: ")

                            i = int(input(""))

                            print("enter destination j: ")

                            j = int(input(""))
                        
                        self.make_move(creature, (i,j))
                    else:
                        print("no creatures to move")
                
                if x == 2:
                    fire_storm = Firestorm(self.stage, "Fire Storm", 50, self)
                    heal_shot = HealShot(self.stage, "Heal Shot", 20, self)
                    teleport = Teleport(self.stage, "Teleport", 50, self)
                    push = Push(self.stage, "Push", 20, self)

                    abilities = [fire_storm, heal_shot, teleport, push]

                    print(abilities, "select from available abilities, from 0 t0 3: ")

                    ab_index = int(input(""))
                    try:
                        while ab_index not in range(len(abilities)):
                            abilities = [fire_storm, heal_shot, teleport, push]

                            print(abilities, "select from available abilities, from 0 to 3: ")

                            ab_index = int(input(""))
                    except (ValueError, TypeError):
                        continue
                    try:
                        ability = abilities[ab_index]
                        print(f"{ability.name} chosen")
                        self.player.check_creatures()
                        self.creatures = self.player.creatures

                        if ability.cost > self.points["Ability"]:
                            print("not enout points to use ability")

                        elif len(self.creatures) == 0:
                            print("no avaiable creatures to use ability")

                        else:
                            for creature in self.creatures:
                                index = self.creatures.index(creature)
                                print(f"{index}: {creature}, {creature.x, creature.y}")

                            print("select creature")

                            creature_index = int(input(""))
                            print(f"{creature_index} selected")

                            while creature_index not in range(len(self.creatures)):
                                for creature in self.creatures:
                                    index = self.creatures.index(creature)
                                    print(f"{index}: {creature}, {creature.x, creature.y}")

                                print("select creature")

                                creature_index = int(input(""))
                            
                            creature = self.creatures[creature_index]

                            print(colored(f"{creature} using {ability.name}", "grey"))
                            self.stage.show_stage()

                            if ability.name == fire_storm.name:
                                

                                print("activate ability? yes or no:  ")

                                answer = input("").lower()

                                if answer == "yes":
                                    ability.activate(creature)
                                else:
                                    continue
                            
                            elif ability.name == push.name:
                                four_tiles = self.get_tile_neighbors((creature.x, creature.y))
                                enemies = []

                                for art in four_tiles:
                                    if isinstance(self.stage.tiles[art].artifact, Creature) and self.stage.tiles[art].artifact.owner != self.player:
                                        enemies.append(self.stage.tiles[art].artifact)
                                if len(enemies) > 0:
                                    print(enemies, "choose target, starting from 0")

                                    enemy_index = int(input(""))

                                    while enemy_index not in range(len(enemies)):
                                        print(enemies, "choose target, starting from 0")

                                        enemy_index = int(input(""))
                                    
                                    target = enemies[enemy_index]

                                    ability.activate(creature, target)
                                else:
                                    print(colored("no available targets", "red"))

                            elif ability.name == heal_shot.name:
                                self.player.check_creatures()

                                self.creatures = self.player.creatures

                                if len(self.creatures) > 1 :
                                    for creatures in self.creatures:
                                        if creature.name != creatures.name:
                                            index = self.creatures.index(creatures)
                                            print(f"{index}: {creatures}")
                                    
                                    print("select a creature")

                                    target_index = int(input(""))

                                    while target_index not in range(len(self.creatures)) or target_index == self.creatures.index(creature):
                                        for creatures in self.creatures:
                                            if creature.name != creatures.name:
                                                index = self.creatures.index(creatures)
                                                print(f"{index}: {creatures}")
                                    
                                        print("select a creature")

                                        target_index = int(input(""))

                                    ability.activate(creature, self.creatures[target_index])
                                else:
                                    print(colored("no avaialble target", "red"))

                            else:
                                print("enter tile to teleport to: ")

                                print("enter i: ")

                                i = int(input(""))

                                print("enter j: ")

                                j = int(input(""))

                                if (i,j) not in self.paths:
                                    print("enter tile to teleport to: ")

                                    print("enter i: ")

                                    i = int(input(""))

                                    print("enter j: ")

                                    j = int(input(""))

                                ability.activate(creature, (i,j))
                    except (ValueError, TypeError):
                        continue
                if x == 3:
                    if self.points["Summon"] < 10:
                        print(colored("not enough points to summon", "red"))
                    else:
                        try:
                            for creature in self.creature_storage:
                                index = self.creature_storage.index(creature)
                                print(f"{index}: {creature}")

                            print("select creature to summon")

                            summon_index = int(input(""))

                            while summon_index not in range(len(self.creature_storage)):
                                for creature in self.creature_storage:
                                    index = self.creature_storage.index(creature)
                                    print(f"{index}: creature")

                                print("select creature to summon")

                                summon_index = int(input(""))


                            creature = self.creature_storage.pop(summon_index)

                            box = Box(creature, self.stage, self.player)

                            print(box.shapes)

                            print("Pick box shape: ")

                            shape = input("")
                        except ValueError:
                            continue
                        try:
                            while shape not in box.shapes:
                                print(box.shapes)

                                print("Pick box shape: ")

                                shape = input("")
                        except ValueError:
                            continue
                            
                            
                        try:
                            while box.placed == False:

                                self.stage.show_stage()

                                print("pick a point1")

                                print("enter i: ")

                                i = int(input(""))

                                print("enter j: ")

                                j = int(input(""))

                                while (i,j) not in self.stage.tiles or (i,j) in self.stage.paths:
                                    self.stage.show_stage()

                                    print("pick a point2")

                                    print("enter i: ")

                                    i = int(input(""))

                                    print("enter j: ")

                                    j = int(input(""))
                                
                                point = (i,j)

                                touching_empty = self.stage.get_empty_touching_tiles(self.player)
                                tile_color = {}
                                colors = ["green", "red", "yellow"]
                                for tile in touching_empty:
                                    tile_color[tile] = colors[0]

                                for tile in self.stage.paths:
                                    tile_color[tile] = colors[1]

                                for tile in self.player.connects:
                                    if tile not in self.stage.paths:
                                        tile_color[tile] = colors[2]


                                self.stage.place_artifact(box, point)
                                box.define_shapes()

                                box_position = box.shape_tiles[shape]

                                for tile in box_position:
                                    if tile in tile_color:
                                        print(colored(f"{tile}", tile_color[tile]),end="")
                                    else:
                                        print(tile, end="")

                                print("")

                                accepted = False

                                print("do you accept? yes or no ")

                                answer = input("").lower()

                                if answer == "yes":
                                    accepted = True

                                while accepted == False:
                                    for tile in box_position:
                                        if tile in tile_color:
                                            print(colored(f"{tile}", tile_color[tile]),end="")
                                        else:
                                            print(tile, end="")
                                    print("")

                                    

                                    print("move position left, right, up or down until it fits and touches")

                                    direction = input("").lower()

                                    while direction not in ["down", "up", "right", "left"]:
                                        for tile in box_position:
                                            if tile in tile_color:
                                                print(colored(f"{tile}", tile_color[tile]),end="")
                                            else:
                                                print(tile, end="")

                                        print("")

                                        print("move position left, right, up or down until it fits and touches")

                                        direction = input("").lower()

                                    amount = 1

                                    print("By what amount? ")

                                    amount = int(input(""))

                                    while not isinstance(amount, int):
                                        print("By what amount? ")

                                        amount = int(input(""))


                                    new_position = []
                                    
                                    for set in box_position:
                                        if direction == "down":
                                            new_cords = (set[0] + amount, set[1])
                                        elif direction == "up":
                                            new_cords = (set[0] - amount, set[1])

                                        elif direction == "right":
                                            new_cords = (set[0], set[1] + amount)

                                        else:
                                            new_cords = (set[0], set[1] - amount)
                                        new_position.append(new_cords)
                                    
                                    box_position = new_position

                                    for tile in box_position:
                                        if tile in tile_color:
                                            print(colored(f"{tile}", tile_color[tile]),end="")
                                        else:
                                            print(tile, end="")

                                    print("")

                                    print("do you accept this? ")

                                    answer = input("").lower()

                                    if answer == "yes":
                                        accepted = True
                                    else:
                                        continue
                                
                                print("Do you want to rotate?yes or no ")

                                answer = input("").lower()

                                if answer == "yes":
                                    rotated = False

                                    while rotated == False:
                                        print("Enter degree to rotate:0, 90, 180, 270 ")

                                        degree = int(input(""))

                                        while degree not in [0, 90, 180, 270]:
                                            print("Enter degree to rotate: 90, 180, 270 ")

                                            degree = int(input(""))

                                        box_position = box.rotate_shape(shape, degree)

                                        for tile in box_position:
                                            if tile in tile_color:
                                                print(colored(f"{tile}", tile_color[tile]),end="")
                                            else:
                                                print(tile, end="")

                                        print("")

                                        print("Do you accept? yes or no")

                                        answer = input("").lower()

                                        if answer == "yes":
                                            rotated = True
                                            break
                                        else:
                                            continue

                                
                                fits = True
                                overlaps = False
                                touches_path = False
                                touches_connect = False

                                for set in box_position:
                                    if set not in self.stage.tiles:
                                        fits = False
                                        print(colored("box wont fit", "red"))
                                    if set in self.stage.paths:
                                        overlaps = True
                                    if set in touching_empty:

                                        touches_path = True
                                    if set in self.player.connects:
                                        touches_connect = True

                                        
                                if fits == False or overlaps == True:
                                    print(colored("out of bounds placement", "red"))
                                    self.creature_storage.append(creature)
                                    self.stage.unplace_artifact(box)
                                    break

                                if touches_path == False and touches_connect == False:
                                    print(colored("box is not connected", "red"))
                                    self.creature_storage.append(creature)
                                    self.stage.unplace_artifact(box)
                                    break

                                for set in box_position:
                                    if set == box_position[0]:
                                        self.stage.place_artifact(creature, set)
                                    
                                    self.stage.tiles[set].board = box
                                    if set not in box.owner.path:
                                        box.owner.add_path(set)
                                    if set not in box.stage.paths:
                                        self.stage.paths.append(set)
                                self.player.creatures.append(creature)
                                    
                                self.stage.unplace_artifact(box)
                                box.placed = True
                                self.points["Summon"] -= 10
                        except ValueError:
                            continue
                                
                if x == 4:
                    print(colored("player turn ends", "cyan"))
                    end_turn = True
            except (ValueError, TypeError):
                continue

                
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
                if i == -1 and j == -1:
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
        queue = deque([(move, [move]) for move in sorted_value])
        self.moves_made = []
        self.current_search = []

        while queue:
            current_move, path = queue.popleft()
            self.x, self.y = current_move
            self.moves_made.append(current_move)
            self.current_search = path

            if self.x == self.ending[0] and self.y == self.ending[1]:
                self.solved = True
                return path

            available = self.available_moves()
            sorted_value = self.distance_value(available)

            for move in sorted_value:
                if move not in self.moves_made:
                    queue.append((move, path + [move]))

        print("no path available for this crawler")
        return None

    
        
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
