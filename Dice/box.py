import random

class Box:

    def __init__(self, creature, stage, owner):
        self.sides = 6
        self.creature = creature
        self.path = self
        self.stage = stage
        self.shape_tiles = {}
        self.shapes = ["t", "w", "T", "z"]
        self.owner = owner
        self.x = None
        self.y = None
        self.placed = False
        
    
    def define_shapes(self):
        self.shape_tiles["t"] = [(self.x - 1, self.y), (self.x, self.y), (self.x, self.y - 1),
                                 (self.x + 1, self.y), (self.x, self.y + 1), (self.x, self.y + 2)]
        self.shape_tiles["T"] = [(self.x - 1, self.y), (self.x, self.y), (self.x + 1, self.y),
                                 (self.x, self.y + 1), (self.x, self.y + 2), (self.x, self.y + 3)]
        self.shape_tiles["w"] = [(self.x - 1, self.y + 1), (self.x, self.y + 1), (self.x, self.y),
                                 (self.x, self.y - 1), (self.x + 1, self.y - 1), (self.x + 1, self.y - 2)]
        self.shape_tiles["z"] = [(self.x, self.y), (self.x, self.y + 1), (self.x, self.y + 2),
                                 (self.x + 1, self.y + 2), (self.x - 1, self.y), (self.x - 2, self.y)]
        
    def pick_shape(self):
        return random.choice(self.shapes)
    
    def pick_connect_tile(self):
        moves = self.owner.connects
        random.shuffle(moves)

        for move in moves:
            if move not in self.stage.paths:
                return move
                
    def pick_path_tile(self, point):
        neighbors_not_in_path = self.find_neighbors(point)
        random.shuffle(neighbors_not_in_path)

        for move in neighbors_not_in_path:
            return move
            
    def fit_shape_to_path(self, result):
        
        
        fit = True
        out_of_bounds = False
        
        blocks = self.shape_tiles[result]
        center = (self.x, self.y)
        
        for sets in blocks:
            if sets in self.stage.paths:
                fit = False
        for sets in blocks:
            if sets not in self.stage.tiles: 
                out_of_bounds = True

        print(len(blocks), "blocks")
        print(blocks)
        if fit == True and out_of_bounds == False:
            for sets in blocks:
                if sets != center:
                    self.stage.place_artifact(self.path, sets)
                    
                    print(f"placing in {sets} ")
                else:
                    self.stage.place_artifact(self.creature, sets)
                    print("placing creature")
                    
                if sets not in self.owner.path:
                    self.owner.add_path(sets)
            self.placed = True
            
        else:
            print("fit equals false or out of bounds")
        
    
    
    def fit_shape_to_connect(self, shape):
        blocks = self.shape_tiles[shape]
        touches_connect = True
        out_of_bounds = False
        overlaps_path = False
        center = (self.x, self.y)

        for sets in blocks:
            if sets not in self.owner.connects:
                touches_connect = False
        for sets in blocks:
            if sets not in self.stage.tiles:
                out_of_bounds = True
        for sets in blocks:
            if sets in self.stage.paths:
                overlaps_path = True

        

        
        if touches_connect == True and out_of_bounds == False and overlaps_path == False:
            for sets in blocks:
                if sets != center:
                    self.stage.place_artifact(self.path)
                else:
                    self.stage.place_artifact(self.creature)

            self.placed = True
        
        



        
            

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

                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width:
                    available_moves.append((new_i, new_j))
        
        return available_moves    
        
    def find_neighbors(self, point):
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

                new_i, new_j = i + point.x, j + point.y

                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width and (new_i,new_j) not in self.stage.paths:
                    available_moves.append((new_i, new_j))
        
        return available_moves    


