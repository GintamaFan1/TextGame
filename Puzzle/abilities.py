
class Ability:

    def __init__(self, name):
        self.name = name

    def activate(self, point, map):
        pass

    def get_diagonal_tiles(self,point,radius=100):
        neighbors = []
        for i in range(-radius, radius):
            for j in range(-radius, radius):
                if i == 0 and j != 0:
                    continue
                elif i != 0 and j == 0:
                    continue

                dx, dy = point[0] + i, point[1] + j

                if 0 < dx < 100 and 0 < dy < 100:
                    neighbors.append((dx,dy)) 
        
        return neighbors
    
    def get_cross_tiles(self, point, radius=100):
        neighbors = []
        for i in range(-radius, radius):
            for j in range(-radius, radius):
                if i != 0 and j != 0:
                    continue

                dx, dy = point[0] + i, point[1] + j

                if 0 < dx < 100 and 0 < dy < 100:
                    neighbors.append((dx,dy)) 
        
        return neighbors
    
    def get_all_neighbors(self, point, radius=100):
        neighbors = []
        for i in range(-radius, radius):
            for j in range(-radius, radius):

                
                dx, dy = point[0] + i, point[1] + j

                if 0 < dx < 100 and 0 < dy < 100:
                    neighbors.append((dx,dy)) 
        
        return neighbors





class Star(Ability):

    def activate(self, point, map):
        neighbors = self.get_diagonal_tiles(point)

        for tiles in neighbors:
            map.board[tiles].exploded = True

        
class Cross(Ability):

    def activate(self, point, map):
        neighbors = self.get_cross_tiles(point)

        for tiles in neighbors:
            map.board[tiles].frozen = True



