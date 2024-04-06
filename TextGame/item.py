import random
import pygame

class Item:
    def __init__(self, name, str, int, agi,  category):
        self.name = name
        self.str = str
        self.int = int
        self.agi = agi
        self.category = category
        self.x = None
        self.y = None

    def equip_to(self, character):
       
        character.str += self.str
        character.int += self.int
        character.agi += self.agi
    
        character.items.append(self)
        
        
    def unequip_from(self, character):
        character.str -= self.str
        character.int -= self.int
        character.agi -= self.agi
        character.items.remove(self)


    def draw(self, surface, x, y):
        TILE_SIZE = 1
        self.x = x
        self.y = y
        item_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, (0, 255, 0), item_rect)
        font = pygame.font.Font(None, 18)
        text = font.render(self.name, True, (255, 255, 255))
        surface.blit(text, (x * TILE_SIZE + 10, y * TILE_SIZE + 10))
        text = font.render(f"STR: {self.str}, INT: {self.int}, AGI: {self.agi}", True, (255, 255, 255))
        surface.blit(text, (x * TILE_SIZE + 10, y * TILE_SIZE + 30))