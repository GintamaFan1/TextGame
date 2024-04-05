import random

class Box:

    def __init__(self, creature, stage):
        self.sides = 6
        self.creature = creature
        self.path = "O"
        self.stage = stage
        self.shape_tiles = {}
        self.shapes = ["t", "w", "T", "z"]
        self.define_shapes()
        self.x = None
        self.Y = None
    
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
    
    def fit_shape(self, result):
        if self.x != None and self.y != None:
            blocks = self.shape_tiles[result]
            center = (self.x, self.y)

            for sets in blocks:
                if sets != center:
                    self.stage.tiles[sets].place_artifact(self.path)
                else:
                    self.stage.tiles[sets].place_artifact(self.creature)
            
        else:
            print("Box was not placed correctly")
            

                

            
        



