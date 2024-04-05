import pygame

class Skills:
    def __init__(self, name, category, damage, cost):
        self.name = name
        self.category = category
        self.damage = damage
        self.cost = cost
        self.x = None
        self.y = None
    
    def draw(self, surface, x, y):
        TILE_SIZE = 1
        self.x = x
        self.y = y
        skill_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, (255, 255, 0), skill_rect)
        font = pygame.font.Font(None, 18)
        text = font.render(self.name, True, (0, 0, 0))
        surface.blit(text, (x * TILE_SIZE + 10, y * TILE_SIZE + 10))
        text = font.render(f"Damage: {self.damage}, Cost: {self.cost}", True, (0, 0, 0))
        surface.blit(text, (x * TILE_SIZE + 10, y * TILE_SIZE + 30))
