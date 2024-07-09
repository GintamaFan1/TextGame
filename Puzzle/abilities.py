import math

class Ability:

    def __init__(self, name):
        self.name = name
        self.x = None
        self.y = None


    def activate(self, point, map):
        pass

    def place(self, point):
        self.x = point[0]
        self.y = point[1]


    def get_diagonal_tiles(self,radius=100):
        neighbors = []
        for i in range(-radius, radius):
            for j in range(-radius, radius):
                
                if abs(i) != abs(j):
                    continue

                dx, dy = self.x + i, self.y + j

                if 0 <= dx < 100 and 0 <= dy < 100:
                    neighbors.append((dx,dy)) 
        
        return neighbors
    
    def get_cross_tiles(self, radius=100):
        neighbors = []
        for i in range(-radius, radius):
            for j in range(-radius, radius):
                if i != 0 and j != 0:
                    continue

                dx, dy = self.x + i, self.y + j

                if 0 <= dx < 100 and 0 <= dy < 100:
                    neighbors.append((dx,dy)) 
        
        return neighbors
    
    def get_all_neighbors(self, radius=100):
        neighbors = []
        for i in range(-radius, radius):
            for j in range(-radius, radius):

                
                dx, dy = self.x + i, self.y + j

                if 0 <= dx < 100 and 0 <= dy < 100:
                    neighbors.append((dx,dy)) 
        
        return neighbors





class Star(Ability):

    def activate(self, map):
        neighbors = self.get_diagonal_tiles()

        for tiles in neighbors:
            if tiles in map.tiles:
                map.tiles[tiles].exploded = True

        
class Cross(Ability):

    def activate(self, map):
        neighbors = self.get_cross_tiles()

        for tiles in neighbors:
            if tiles in map.tiles:
                map.tiles[tiles].frozen = True



