import random, csv
from maps import Map, Tile
from characters import Hero, Villain
from item import Item
from skills import Skills
from AIagent import AIAgent
from operator import attrgetter
import copy
import time
from termcolor import colored
import pygame





def pick_character(all_characters):
    for char in all_characters:
        print(char.name, char.nature, all_characters.index(char))
    
    char = int(input("Choose a character "))

    return all_characters[char].name

    
class Game:
    def __init__(self,width, height, heroes, villains, items, skills):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.font.init()
        self.map = Map("Agaroth", 21, 15)
        self.map.create_map()
        self.map.place_characters(heroes, villains)
        self.map.place_items(skills, items)
        self.heroes = heroes
        self.villains = villains
        self.items = items
        self.skills = skills
        self.ai_agents = [AIAgent(self.map, hero, self.heroes, self.villains) for hero in self.heroes] + \
                        [AIAgent(self.map, villain, self.heroes, self.villains) for villain in self.villains]


    def run(self):
        running = True
        turn = 1
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.map.show_map()
            

            for agent in self.ai_agents:
                agent.make_move()
                
                

                agent.character.HP = round(agent.character.HP, 1)

                agent.character.HP += 2

                if agent.character.nature == "Hero":
                    if agent.character.HP > 100:
                        agent.character.HP = 100
                else:
                    if agent.character.HP > 150:
                        agent.character.HP = 150
            
            
            
                self.draw()
                pygame.display.flip()
                time.sleep(.3)
            print("turn",turn)
            
            turn += 1

            if len(self.heroes) == 0:
                running = False
                print("Villains Win")
            if len(self.villains) == 0:
                running = False
                print("Heroes Win") 

    def draw(self):
    
        self.window.fill((0, 0, 0))
        self.map.draw(self.window)
        for agent in self.ai_agents:
            agent.draw(self.window)
            

def main():
    Heroes = []
    
    Villains = []

    Items = []
    Skill = []
    Location = []

    


    with open("character_villain.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for line in reader:
            name, str_val, int_val, agi_val, nature = line
            str_val = int(str_val)
            int_val = int(int_val)
            agi_val = int(agi_val)
            if nature == "Hero":
                Heroes.append(Hero(name, str_val, int_val, agi_val))
            else:
                average = (str_val + int_val + agi_val) / 3
                Villains.append(Villain(name, str_val, int_val, agi_val, round(average)))

    with open("items.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for line in reader:
            name, str_val, int_val, agi_val, category = line
            str_val = int(str_val)
            int_val = int(int_val)
            agi_val = int(agi_val)
            
            Items.append(Item(name, str_val, int_val, agi_val, category))

    with open("skills.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

        for line in reader:
            name, category, damage, cost = line
            damage = int(damage)
            cost = int(cost)

            Skill.append(Skills(name, category, damage, cost))

    
    game = Game(1440, 1080, Heroes, Villains, Items, Skill)
    
    
    game.run()
    
    
main()










        
