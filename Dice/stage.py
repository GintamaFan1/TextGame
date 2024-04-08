

class Stage:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tiles = {}
        self.paths = []
        self.create_stage()
        self.top_connect = []
        self.bottom_connect = []
        self.define_connects()
    
    def __str__(self):
        print(f"Game Stage")

    def create_stage(self):
        for i in range(self.height):
            for j in range(self.width):
                self.tiles[(i,j)] = Tile(i,j)

    def place_artifact(self, obj, coords):
        self.tiles[coords].add_artifact(obj)

    def unplace_artifact(self, obj):
        self.tiles[(obj.x, obj.y)].remove_artifact(obj)

    def define_connects(self):
        for i in range(self.width):
            self.top_connect.append((i,0))
        
        for j in range(self.width):
            self.bottom_connect.append((j,self.width - 1))



class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.artifact = None

    def __str__(self):
        print(f"Tile at {self.x, self.y}")
    
    def add_artifact(self, obj):
        if obj != self.artifact:
            self.artifact = obj
            obj.x = self.x
            obj.y = self.y
        else:
            print(f"{obj} already in tile")

    def remove_artifact(self, obj):
        if obj == self.artifact:
            self.artifact = None
            obj.x = None
            obj.y = None
        else:
            print(f"{obj} not in tile")




    

