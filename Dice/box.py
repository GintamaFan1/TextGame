import random

class Box:

    def __init__(self, creature, stage, owner):
        self.sides = 6
        self.creature = creature
        self.path = self
        self.stage = stage
        self.shape_tiles = {}
        self.shape_rotations = {}
        self.shapes = ["t", "w", "T", "z", "twist"]
        self.owner = owner
        self.x = None
        self.y = None
        self.placed = False

    def __str__(self):
        return f"{self.creature.name}'s box path at {self.x, self.y} belongs to {self.owner}"
    
    
        
    
    def define_shapes(self):
        self.shape_tiles["t"] = [(self.x, self.y), (self.x - 1, self.y), (self.x, self.y - 1),
                                  (self.x + 1, self.y), (self.x, self.y + 1), (self.x, self.y + 2)]
        self.shape_tiles["T"] = [(self.x, self.y), (self.x - 1, self.y), (self.x + 1, self.y), 
                                 (self.x, self.y + 1), (self.x, self.y + 2), (self.x, self.y + 3)]
        self.shape_tiles["w"] = [(self.x, self.y), (self.x - 1, self.y + 1), (self.x, self.y - 1), 
                                 (self.x, self.y + 1), (self.x + 1, self.y - 1), (self.x + 1, self.y - 2)]
        self.shape_tiles["z"] = [(self.x, self.y), (self.x, self.y + 1), (self.x, self.y + 2), 
                                 (self.x + 1, self.y + 2), (self.x - 1, self.y), (self.x - 2, self.y)]
        self.shape_tiles["twist"] = [(self.x, self.y), (self.x, self.y - 1), (self.x, self.y + 1), 
                                     (self.x, self.y + 2), (self.x - 1, self.y - 1), (self.x + 1, self.y)]
        
        self.shape_rotations["t"] = {
            90: [(self.x, self.y), (self.x, self.y - 1), (self.x - 1, self.y), (self.x, self.y + 1), (self.x + 1, self.y), (self.x + 2, self.y)],
            180: [(self.x, self.y), (self.x + 1, self.y), (self.x, self.y + 1), (self.x - 1, self.y), (self.x, self.y - 1), (self.x, self.y - 2)],
            270: [(self.x, self.y), (self.x, self.y + 1), (self.x + 1, self.y), (self.x, self.y - 1), (self.x - 1, self.y), (self.x - 2, self.y)]
        }
        self.shape_rotations["T"] = {
            90: [(self.x, self.y), (self.x, self.y - 1), (self.x, self.y + 1), (self.x + 1, self.y), (self.x + 2, self.y), (self.x + 3, self.y)],
            180: [(self.x, self.y), (self.x + 1, self.y), (self.x - 1, self.y), (self.x, self.y - 1), (self.x, self.y - 2), (self.x, self.y - 3)],
            270: [(self.x, self.y), (self.x, self.y + 1), (self.x, self.y - 1), (self.x - 1, self.y), (self.x - 2, self.y), (self.x - 3, self.y)]
        }
        self.shape_rotations["w"] = {
            90: [(self.x, self.y), (self.x + 1, self.y), (self.x + 2, self.y), (self.x + 2, self.y + 1), (self.x, self.y - 1), (self.x - 1, self.y - 2)],
            180: [(self.x, self.y), (self.x , self.y - 1), (self.x, self.y - 2), (self.x + 1, self.y - 2), (self.x - 1, self.y), (self.x - 1, self.y + 1)],
            270: [(self.x, self.y), (self.x - 1, self.y), (self.x - 2, self.y), (self.x - 2, self.y - 1), (self.x, self.y + 1), (self.x + 1, self.y + 1)]
        }
        self.shape_rotations["z"] = {
            90: [(self.x, self.y), (self.x, self.y + 1), (self.x , self.y + 2), (self.x - 2, self.y - 1), (self.x -2, self.y), (self.x - 1, self.y)],
            180: [(self.x, self.y), (self.x, self.y - 1), (self.x, self.y - 2), (self.x - 1, self.y - 2), (self.x + 1, self.y), (self.x + 2, self.y)],
            270: [(self.x, self.y), (self.x, self.y - 1), (self.x, self.y - 2), (self.x - 1, self.y), (self.x - 2, self.y), (self.x - 2, self.y + 1)]
        }
        self.shape_rotations["twist"] = {
            90: [(self.x, self.y), (self.x - 1, self.y), (self.x + 1, self.y), (self.x + 2, self.y), (self.x - 1, self.y + 1), (self.x, self.y - 1)],
            180: [(self.x, self.y), (self.x, self.y + 1), (self.x, self.y - 1), (self.x, self.y - 2), (self.x - 1, self.y), (self.x + 1, self.y + 1)],
            270: [(self.x, self.y), (self.x + 1, self.y), (self.x - 1, self.y), (self.x - 2, self.y), (self.x + 1, self.y - 1), (self.x, self.y + 1)]
        }

    def rotate_shape(self, shape, degree):
        rotated_shape = self.shape_rotations[shape].get(degree)
        if rotated_shape:
            self.shape_tiles[shape] = rotated_shape
            return self.shape_tiles[shape]
        else:
            print(f"Invalid rotation degree: {degree}")
            return self.shape_tiles[shape]
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

    
            
    def fit_shape_to_path(self, result, point):
        fit = True
        out_of_bounds = False
        touches_path = False
        tiles_to_connect = self.find_neighbors(point)
        
        blocks = self.shape_tiles[result]

        rotate = ["yes", "no"]

        choice = random.choice(rotate)
        degrees = None

        if choice == "yes":
            degrees = [90, 180, 270]

        if degrees:
            degree = random.choice(degrees)
            blocks = self.rotate_shape(result, degree)

        center = (self.x, self.y)
        
        for sets in blocks:
            if sets in self.stage.paths:
                fit = False
        for sets in blocks:
            if sets not in self.stage.tiles: 
                out_of_bounds = True
        for sets in blocks:
            if sets in tiles_to_connect:
                touches_path = True
    
        if fit == True and out_of_bounds == False and touches_path == True:
            for sets in blocks:
                if sets != center:
                    self.stage.tiles[sets].board = self  
                else:
                    self.stage.place_artifact(self.creature, sets)
                    self.stage.tiles[sets].board = self
                if sets not in self.owner.path:
                    self.owner.add_path(sets)
                if sets not in self.stage.paths:
                    self.stage.paths.append(sets)
            self.placed = True
            
    
    def fit_shape_to_connect(self, shape):
        blocks = self.shape_tiles[shape]
        touches_connect = False
        out_of_bounds = False
        overlaps_path = False
        center = (self.x, self.y)

        for sets in blocks:
            if sets in self.owner.connects:
                touches_connect = True
        for sets in blocks:
            if sets not in self.stage.tiles:
                out_of_bounds = True
        for sets in blocks:
            if sets in self.stage.paths:
                overlaps_path = True
        
        if touches_connect == True and out_of_bounds == False and overlaps_path == False:
            for sets in blocks:
                if sets != center:
                    self.stage.tiles[sets].board = self
                else:
                    self.stage.place_artifact(self.creature, sets)
                    self.stage.tiles[sets].board = self
                if sets not in self.owner.path:
                    self.owner.add_path(sets)
                if sets not in self.stage.paths:
                    self.stage.paths.append(sets)
            self.placed = True
        
        
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

                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width:
                    available_moves.append((new_i, new_j))
        
        return available_moves    
        
    def find_neighbors(self, point):
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

                new_i, new_j = i + point[0], j + point[1]

                if new_i >= 0 and new_i < self.stage.height and new_j >= 0 and new_j < self.stage.width and (new_i,new_j) not in self.stage.paths:
                    available_moves.append((new_i, new_j))
        
        return available_moves    


