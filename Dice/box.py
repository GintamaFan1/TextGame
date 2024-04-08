import random

class Box:

    def __init__(self, creature, stage, owner):
        self.sides = 6
        self.creature = creature
        self.path = "O"
        self.stage = stage
        self.shape_tiles = {}
        self.shapes = ["t", "w", "T", "z"]
        self.define_shapes()
        self.owner = owner
        self.x = None
        self.Y = None
        self.placed = False
    
    def define_shapes(self):
        self.shape_tiles["t"] = [(self.x - 1, self.y), (self.x, self.y), (self.x, self.y - 1),
                                 (self.x + 1, self.y), (self.x, self.y + 1), (self.x, self.y + 2)]
        self.shape_tiles["T"] = [(self.x - 1, self.y), (self.x, self.y), (self.x + 1, self.y),
                                 (self.x, self.y + 1), (self.x, self.y + 2), (self.x, self.y + 3)]
        self.shape_tiles["w"] = [(self.x - 1, self.y + 1), (self.x, self.y + 1), (self.x, self.y),
                                 (self.x, self.y - 1), (self.x + 1, self.y - 1), (self.x + 1, self.y - 2)]
        self.shape_tiles["z"] = [(self.x, self.y), (self.x, self.y + 1), (self.x, self.y + 2),
                                 (self.x + 1, self.y + 2), (self.x + 1, self.y), (self.x + 2, self.y)]
        
    def pick_shape(self):
        result = []
        for shape, coords in self.shape_tiles:
            result.append(shape)
        random.shuffle(result)

        return result[0]
    
    def target(self, shape, point):
        target = None
        blocks = self.shape_tiles[shape]

        for set in blocks:
            if set in self.owner.connect:
    
    def fit_shape(self, result, target):
        

        if self.x != None and self.y != None:
            fit = True
            out_of_bounds = False
            
            blocks = self.shape_tiles[result]
            center = (self.x, self.y)

            

            for sets in blocks:
                if sets in self.stage.paths:
                    print("can't place here")
                    fit = False
            for sets in blocks:
                if sets not in self.stage.tiles:
                    out_of_bounds = True
            if fit == True and out_of_bounds == False:
                for sets in blocks:
                    if sets != center:
                        self.stage.tiles[sets].place_artifact(self.path)
                    else:
                        self.stage.tiles[sets].place_artifact(self.creature)
                self.placed = True
            else:
                print("fit equals false or out of bounds")
            
        else:
            print("Box was not placed correctly")
            

    def check_touch(self, shape, target):
        available = self.available_moves(target)

        for move in available:
            



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
        



