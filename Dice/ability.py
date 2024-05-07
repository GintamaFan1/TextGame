from creatures import Creature
from dice import *
from stage import *
from player import Player

class Ability:
    def __init__(self, stage, name, cost, ai_agent):
        self.stage = stage
        self.name = name
        self.cost = cost
        self.agent = ai_agent

    def __str__(self):
        return f"{self.name}, cost:{self.cost}"

    def activate(self, user, target):
        pass

    def get_neighbors(self, point, radius=2):
        neighbors = []

        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i == 0 and j == 0:
                    continue
                new_x, new_y = i + point[0], j + point[1]

                if new_x >= 0 and new_x < self.stage.height and new_y >= 0 and new_y < self.stage.width:
                    neighbors.append((new_x, new_y))

        return neighbors
    
    def get_cross_neighbors(self, point):
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if i == 1 and j == 1:
                    continue
                if i == -1 and j == -1:
                    continue
                if i == -1 and j == 1:
                    continue
                if i == 1 and j == -1:
                    continue
                new_x, new_y = i + point[0], j + point[1]

                if new_x >= 0 and new_x < self.stage.height and new_y >= 0 and new_y < self.stage.width and (new_x, new_y) in self.stage.paths:
                    neighbors.append((new_x, new_y))

        return neighbors
    
    def get_opposite(self, target_loc, user_loc):

        nx = target_loc[0] - user_loc[0]
        ny = target_loc[1] - user_loc[1]

        return(target_loc[0] + nx, target_loc[1] + ny)




class Firestorm(Ability):
    def activate(self, user):
        
        avaiable_targets = self.get_neighbors((user.x, user.y))

        for move in avaiable_targets:
            if move is not None:
                obj = self.stage.tiles[move].artifact
                if isinstance(obj, Creature):
                    obj.HP -= 10
                    print(f"{user.name} deals fire damage to {obj.name}")
                    self.agent.points["Ability"] -= self.cost
        
        

class Push(Ability):
    def activate(self, user, target):
        
        opposite_tile = self.get_opposite((target.x, target.y), (user.x, user.y))
        obj = self.stage.tiles[opposite_tile].artifact

        if isinstance(obj, Box):
            self.stage.unplace_artifact(target)
            self.stage.place_artifact(target, opposite_tile)
            target.HP -= 5
            print(f"{user.name} pushes {target.name} to {opposite_tile} ")
            self.agent.points["Ability"] -= self.cost
        
        elif isinstance(obj, Creature):
            target.HP -= 5
            obj.HP -= 5
            print(f"{user.name} pushes {target.name} into {obj.name}")
            self.agent.points["Ability"] -= self.cost
        else:
            target.HP -= 10
            print(f"{user.name} pushes {target.name} into a wall, double damage!")
            self.agent.points["Ability"] -= self.cost
        

class HealShot(Ability):
    def activate(self, user, target):
    
        avaiable_neighbors = self.get_neighbors((user.x, user.y))
        if target in avaiable_neighbors:
            target.HP += 5
            print(f"{user.name} heals {target.name}")
            if target.HP > target.maxHP:
                target.HP = target.maxHP
            self.agent.points["Ability"] -= self.cost

            

class Teleport(Ability):
    def activate(self, user):
        
        possible_tiles = [tile for tile in self.stage.paths if not isinstance(self.stage.tiles[tile].artifact, Creature)]
        choice = random.choice(possible_tiles)

        if choice:
            self.stage.unplaced_artifact(user)
            self.stage.place_artifact(user, choice)
            

            print(f"{user.name}, teleports to {choice}")
            self.agent.points["Ability"] -= self.cost

        



    





    

    







    