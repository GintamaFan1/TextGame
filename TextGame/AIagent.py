from characters import Hero, Villain
from maps import Map
from collections import defaultdict
from skills import Skills
from item import Item
from interactions import *
import copy
import math
import numpy as np
from termcolor import colored
import pygame
class AIAgent:
    def __init__(self, place, character, heroes, villains):
        self.place = place
        self.character = character
        self.moves_made = []
        self.heroes = heroes
        self.villains = villains
        self.x = None
        self.y = None

    def location(self):
        for tile in self.place.tiles.values():
            if self.character in tile.objects:
                self.x = tile.x
                self.y = tile.y
                return ((tile.x, tile.y), self.character)
        self.x = None
        self.y = None
        return None

    
    def get_neighbors(self, x, y, radius=2):
        neighbors = []

        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i == 0 and j == 0:
                    continue
                new_i, new_j = i + x, j + y
                if new_i >= 0 and new_i <= self.place.height - 1 and new_j >= 0 and new_j <= self.place.width - 1:
                    neighbors.append((new_i, new_j))
        
        return neighbors
    
    def evaluate_neighbors(self, neighbors, moves_made, hero, vil):
        neighbor_values = defaultdict(list)

        for nx, ny in neighbors:
            if self.place.tiles[(nx,ny)].objects:
                for obj in self.place.tiles[(nx, ny)].objects:
                    if isinstance(obj, Hero) or isinstance(obj, Villain):
                        if obj.nature != self.character.nature:
                            neighbor_values[4].append((nx,ny))
                        else:
                            neighbor_values[-2].append((nx,ny))
                        
                    elif "Blocked" in self.place.tiles[(nx,ny)].objects:
                        neighbor_values[-2].append((nx,ny))
                    elif isinstance(obj, Item) or isinstance(obj, Skills):
                        neighbor_values[5].append((nx, ny))
                    
            elif (nx,ny) in moves_made:
                neighbor_values[0].append((nx,ny))
            elif self.character.nature == "Hero" and (nx,ny) in hero:
                neighbor_values[2].append((nx,ny))
            elif self.character.nature == "Villain" and (nx,ny) in vil:
                neighbor_values[2].append((nx,ny))
            else:
                neighbor_values[3].append((nx,ny))

        return neighbor_values

    def move_score(self, sorted_value, neighbor_values):
        move_score = {}
        for value in sorted_value:
            if neighbor_values[value]:
                for Current_location in neighbor_values[value]:
                    move_score[(Current_location)] = value
        return move_score
    
    def predicter(self, Moving_to):
        moves_made_copy = self.moves_made.copy()
        hero_copy = self.place.hero_explored.copy()
        vil_copy = self.place.villain_explored.copy()
        if Moving_to not in moves_made_copy:
            moves_made_copy.append(Moving_to)
        if self.character.nature == "Hero":
            if Moving_to not in hero_copy:
                hero_copy.append(Moving_to)
        else:
            if Moving_to not in vil_copy:
                vil_copy.append(Moving_to)

        neighbors = self.get_neighbors(Moving_to[0], Moving_to[1])

        neighbor_values = self.evaluate_neighbors(neighbors, moves_made_copy, hero_copy, vil_copy)
       
        sorted_values = sorted(neighbor_values.keys(), reverse=True)

        move_score = self.move_score(sorted_values, neighbor_values)
       
        return move_score
    
    def deep_search(self, dict):
        future_score = {}
        for move in dict.keys():
            future_score = self.predicter(move)
        
        return future_score
    
    def adder(self, dict1, dict2, dict3):
        for move in dict1.keys():
            for move2 in dict2.keys():
                if move != move2:
                    if (move,move2) not in dict3:
                        dict3[(move,move2)] = 0
                    dict3[(move,move2)] += dict1[move] + dict2[move2]
            
        
    def pick_move(self):
        Moving_to = self.location()
        sorted_best_move = {}
        best_move = []
        distance_value = {}
        normalized_distance_value = {}
        next_move = {}
        if Moving_to:
            Current_location, player = Moving_to
            x, y = Current_location 
            if (x,y) not in self.moves_made:
                self.moves_made.append((x,y))
            if self.character.nature == "Hero":
                if (x,y) not in self.place.hero_explored:
                    self.place.hero_explored.append((x,y))
            else:
                if (x,y) not in self.place.villain_explored:
                    self.place.villain_explored.append((x,y))
             
            next_move = self.predicter(Current_location)
            sorted_best_move = sorted(next_move.items(), key=lambda x: x[1], reverse=True)

        for move, value in sorted_best_move:
            x,y = move
            center = (round(self.place.height/2), round(self.place.width/2))
            distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            distance_value[(x,y)] = distance
        
        
        if distance_value:
            d = np.array(list(distance_value.values()))
            a = d.min()
            b = d.max()
            nd = (d-a) / (b-a)
            normalized_distance_value = {key: round(value,2) for key, value in zip(distance_value.keys(), nd)}
            

        for move, value in sorted_best_move:
            
            for coord, norm_val in normalized_distance_value.items():
                if coord == move:
                    next_move[move] -= norm_val

        sorted_best_move = sorted(next_move.items(), key=lambda x: x[1], reverse=True)
        
        
        for move, value in sorted_best_move:
            best_move.append(move)
            break
            
        return best_move 
    
    def simulate_attack(self, initiator, defender):
        damage = 6
        if damage >= initiator.HP:
            return True
        return False
    
    def run_away(self):
        location = self.location()
        if location:
            current_location, char = location

            neighbors = self.get_neighbors(current_location[0], current_location[1])

            available_moves = []

            for neigh in neighbors:
                if len(self.place.tiles[neigh].objects) == 0:
                    available_moves.append(neigh)
            
            random.shuffle(available_moves)
            print(available_moves, "run away moves")
            if available_moves:
                return available_moves[0]
            
    def player_move(self):
        location = self.location()
        print(f"Player is at {location[0]}")

        Current_location, player = location


        available_moves = self.get_neighbors(Current_location[0], Current_location[1])
        for moves in available_moves:
            print(moves, self.place.tiles[moves].objects)
        move_x = int(input("enter x value: "))
        move_y = int(input("enter y value: "))

        Moving_to = (move_x, move_y)
        available_moves.remove(Moving_to)

        territory_objects = self.place.tiles[Moving_to].objects

        
        if territory_objects:
            territory = territory_objects[0]
        else:
            territory = None
        print(f"Player tries to move to {territory}")

        if isinstance(territory, Item) or isinstance(territory, Skills):
            print("player encounters an item")
            self.place.tiles[Moving_to].remove_object(territory)
            self.place.tiles[Current_location].remove_object(self.character)
            self.place.tiles[Moving_to].add_object(self.character)
            pick_up_item(territory, self.character)
        
            print(colored((f"The Player picks up {territory.name}"), "cyan"))
            
            return
        
        elif isinstance(territory, Hero) or isinstance(territory, Villain):
            print(self.character.name, self.character.HP, self.character.str, self.character.MP,
                    self.character.int, self.character.agi)

            print(f"Enemy: {territory.name}, {territory.HP}, {territory.MP}, {territory.str}, {territory.int}, {territory.agi}")

            choice = input("will you fight? Enter yes or no ")

            if choice == "Yes" or choice == "YES" or choice == "yes":
                print(f"{self.character.name} Attacks {territory.name} ")
                exp = 2

                if self.character.agi >= territory.agi:
                    battle(self.character, territory)

                    if territory.HP <= 0:
                        killed(self.place, self.character, territory, Current_location, Moving_to)
                        if territory.nature == "Hero":
                            for char in self.heroes:
                                if char == territory:
                                    self.heroes.remove(territory)
                        else:
                            for char in self.villains:
                                if char == territory:
                                    self.villains.remove(territory)
                    
                    else:
                        if self.character.nature == "Hero":
                            self.character.gain_exp(exp) 
                            print(colored((f"{self.character.name} gained {exp} Exp "), "green"))
                        else:
                            territory.gain_exp(exp) 
                            print(colored((f"{territory.name} gained {exp} Exp"), "green"))
                    
                        battle(territory, self.character)

                        if self.character.HP <= 0:
                            killed(self.place, self.character, territory, Current_location, Moving_to)
                            if self.character.nature == "Hero":
                                for char in self.heroes:
                                    if char == self.character:
                                        self.heroes.remove(self.character)
                            else:
                                for char in self.villains:
                                    if char == self.character:
                                        self.villains.remove(self.character)
                else:
                    battle(territory, self.character)

                    if self.character.HP <= 0:
                        killed(self.place, self.character, territory, Current_location, Moving_to)
                        if self.character.nature == "Hero":
                            for char in self.heroes:
                                if char == self.character:
                                    self.heroes.remove(self.character)
                        else:
                            for char in self.villains:
                                if char == self.character:
                                    self.villains.remove(self.character)
                    
                    else:
                        if territory.nature == "Hero":
                            territory.gain_exp(exp) 
                            print(colored((f"{territory.name} gained {exp} Exp "), "green"))
                        else:
                            self.character.gain_exp(exp) 
                            print(colored((f"{self.character.name} gained {exp} Exp"), "green"))
                    
                        battle(self.character, territory)

                        if territory.HP <= 0:
                            killed(self.place, self.character, territory, Current_location, Moving_to)
                            if territory.nature == "Hero":
                                for char in self.heroes:
                                    if char == territory:
                                        self.heroes.remove(territory)
                            else:
                                for char in self.villains:
                                    if char == territory:
                                        self.villains.remove(territory)
            
            else:
                safe_move = self.run_away()
                if safe_move and self.character.MP >= 20:
                    print(colored((f"Player runs away to {safe_move}"), "light_magenta"))
                    self.character.MP -= 20
                    self.place.tiles[Current_location].remove_object(self.character)
                    self.place.tiles[safe_move].add_object(self.character)
                    if safe_move not in self.moves_made:
                        self.moves_made.append(safe_move)
                    if self.character.nature == "Hero":
                        if safe_move not in self.place.hero_explored:
                            self.place.hero_explored.append(safe_move)
                    else:
                        if safe_move not in self.place.villain_explored:
                            self.place.villain_explored.append(safe_move)
                    return
        
        else:
            print(f"Player moves to {Moving_to}")
            self.place.tiles[Current_location].remove_object(self.character)
            self.place.tiles[Moving_to].add_object(self.character)
            if Moving_to not in self.moves_made:
                self.moves_made.append(Moving_to)
            if self.character.nature == "Hero":
                if Moving_to not in self.place.hero_explored:
                    self.place.hero_explored.append(Moving_to)
            else:
                if Moving_to not in self.place.villain_explored:
                    self.place.villain_explored.append(Moving_to)
            return

         





    def make_move(self):
        Moving_to = self.pick_move()
        
        if Moving_to:
            needs_removal = None
            location = self.location()
            if location == None:
                if self.character.nature == "Hero":
                    for hero in self.self.heroes:
                        if hero == self.character:
                            needs_removal.append(hero)
                else:
                    for vil in self.self.villains:
                        if vil == self.character:
                            needs_removal.append(vil)
            if needs_removal != None:
                if self.character.nature == "Hero":
                    self.self.heroes.remove(needs_removal)
                else:
                    self.self.villains.remove(needs_removal)

            Current_location, player = location

           
            print(Current_location, "Start")
            territory_objects = self.place.tiles[Moving_to[0]].objects
            
            if territory_objects:
                territory = territory_objects[0]
            else:
                territory = None

            print(f"{self.character.name, self.character.HP, self.character.MP, self.character.nature} STR:{self.character.str}, INT: {self.character.int} AGI: {self.character.agi} moves to {Moving_to}")

            if isinstance(territory, Item) or isinstance(territory,Skills):
                self.place.tiles[(Moving_to[0][0], Moving_to[0][1])].remove_object(territory)
                self.place.tiles[Current_location].remove_object(self.character)
                self.place.tiles[(Moving_to[0][0], Moving_to[0][1])].add_object(self.character)
                pick_up_item(territory, self.character)
            
                print(colored((f"{self.character.name} picks up {territory.name}"), "cyan"))
                
                return

                
            elif isinstance(territory,Hero) or isinstance(territory, Villain):
                
                if territory.nature == self.character.nature:
                    return 
                    
                

                death = self.simulate_attack(self.character, territory)

                safe_move = None

                if death == True:
                    safe_move = self.run_away()

                if safe_move and self.character.MP >= 20:
                    print(colored((f"{self.character.name} runs away to {safe_move}"), "light_magenta"))
                    self.character.MP -= 20
                    self.place.tiles[Current_location].remove_object(self.character)
                    self.place.tiles[safe_move].add_object(self.character)
                    if safe_move not in self.moves_made:
                        self.moves_made.append(safe_move)
                    if self.character.nature == "Hero":
                        if safe_move not in self.place.hero_explored:
                            self.place.hero_explored.append(safe_move)
                    else:
                        if safe_move not in self.place.villain_explored:
                            self.place.villain_explored.append(safe_move)
                    return

                print(f"{self.character.name} Attacks {territory.name} ")
                exp = 2

                if self.character.agi >= territory.agi:
                    battle(self.character, territory)

                    if territory.HP <= 0:
                        killed(self.place, self.character, territory, Current_location, Moving_to)
                        if territory.nature == "Hero":
                            for char in self.heroes:
                                if char == territory:
                                    self.heroes.remove(territory)
                        else:
                            for char in self.villains:
                                if char == territory:
                                    self.villains.remove(territory)
                    
                    else:
                        if self.character.nature == "Hero":
                            self.character.gain_exp(exp) 
                            print(colored((f"{self.character.name} gained {exp} Exp "), "green"))
                        else:
                            territory.gain_exp(exp) 
                            print(colored((f"{territory.name} gained {exp} Exp"), "green"))
                    
                        battle(territory, self.character)

                        if self.character.HP <= 0:
                            killed(self.place, self.character, territory, Current_location, Moving_to)
                            if self.character.nature == "Hero":
                                for char in self.heroes:
                                    if char == self.character:
                                        self.heroes.remove(self.character)
                            else:
                                for char in self.villains:
                                    if char == self.character:
                                        self.villains.remove(self.character)
                else:
                    battle(territory, self.character)

                    if self.character.HP <= 0:
                        killed(self.place, self.character, territory, Current_location, Moving_to)
                        if self.character.nature == "Hero":
                            for char in self.heroes:
                                if char == self.character:
                                    self.heroes.remove(self.character)
                        else:
                            for char in self.villains:
                                if char == self.character:
                                    self.villains.remove(self.character)
                    
                    else:
                        if territory.nature == "Hero":
                            territory.gain_exp(exp) 
                            print(colored((f"{territory.name} gained {exp} Exp "), "green"))
                        else:
                            self.character.gain_exp(exp) 
                            print(colored((f"{self.character.name} gained {exp} Exp"), "green"))
                    
                        battle(self.character, territory)

                        if territory.HP <= 0:
                            killed(self.place, self.character, territory, Current_location, Moving_to)
                            if territory.nature == "Hero":
                                for char in self.heroes:
                                    if char == territory:
                                        self.heroes.remove(territory)
                            else:
                                for char in self.villains:
                                    if char == territory:
                                        self.villains.remove(territory)
                    
            else:
                self.place.tiles[Current_location].remove_object(self.character)
                self.place.tiles[(Moving_to[0][0], Moving_to[0][1])].add_object(self.character)
                if (Moving_to[0][0], Moving_to[0][1]) not in self.moves_made:
                    self.moves_made.append((Moving_to[0][0], Moving_to[0][1]))
                if self.character.nature == "Hero":
                    if (Moving_to[0][0], Moving_to[0][1]) not in self.place.hero_explored:
                        self.place.hero_explored.append((Moving_to[0][0], Moving_to[0][1]))
                else:
                    if (Moving_to[0][0], Moving_to[0][1]) not in self.place.villain_explored:
                        self.place.villain_explored.append((Moving_to[0][0], Moving_to[0][1]))
                return
        else:
            return

    def draw(self, surface):
        TILE_SIZE = 64
        if self.x is not None and self.y is not None:
            # Render the AI agent on the Pygame surface
            agent_rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if self.character.nature == "Hero":
                pygame.draw.rect(surface, (0, 255, 100), agent_rect)
            else:
                pygame.draw.rect(surface, (255, 123, 67), agent_rect)
            
            ID = None
            if self.character.nature == "Hero":
                ID = self.character.level
            else:
                ID = self.character.rank
            font = pygame.font.Font(None, 20)
            text = font.render(f"{ID}", True, (100, 200, 100))
            surface.blit(text, (self.x * TILE_SIZE + 10, self.y * TILE_SIZE + 1))
            
            font = pygame.font.Font(None, 18)
            text = font.render(self.character.name, True, (100, 100, 100))
            surface.blit(text, (self.x * TILE_SIZE + 10, self.y * TILE_SIZE + 10))
            font = pygame.font.Font(None, 13)
            text = font.render(f"HP:{self.character.HP}, MP:{self.character.MP}", True, (100, 100, 100))
            surface.blit(text, (self.x * TILE_SIZE, self.y * TILE_SIZE + 20))
            text = font.render(f"STR:{self.character.str}, INT:{self.character.int}, AGI:{self.character.agi}", True, (100, 100, 100))
            surface.blit(text, (self.x * TILE_SIZE, self.y * TILE_SIZE + 30))
                          

                        

                    


                    


            


        
            



        
    