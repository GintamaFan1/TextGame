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
def place_characters(self,heroes, villains):
        row = 4
        col = 4
        heroes_copy = heroes.copy()
        villains_copy = villains.copy()
        for i in range(row  ):
            for j in range(col ):
                if len(self.tiles[(i,j)].objects) == 0 and len(heroes_copy) != 0:
                    random.shuffle(heroes_copy)
                    random_hero = heroes_copy.pop(0)
                    self.tiles[(i,j)].add_object(random_hero)
                    
        
        for i in range(self.height - row  , self.height ):
            for j in range(self.width - col  , self.width ):
                if len(self.tiles[(i,j)].objects) == 0 and len(villains_copy) != 0:
                    random.shuffle(villains_copy)
                    random_villain = villains_copy.pop(0)
                    self.tiles[(i,j)].add_object(random_villain)

def place_items(self, skills, items):
    # Get a list of all empty tiles
    empty_tiles = [tile for tile in self.tiles.values() if len(tile.objects) == 0]
    
    # Shuffle the lists of skills and items
    random.shuffle(skills)
    random.shuffle(items)
    
    # Combine skills and items into a single list
    objects_to_place = skills + items
    
    # Calculate the number of items and skills to place
    items_to_place = len(items)
    skills_to_place = len(skills)
    total_objects_to_place = items_to_place + skills_to_place
    
    # Get a random sample of empty tiles
    num_tiles_to_use = min(total_objects_to_place, len(empty_tiles))
    tiles_to_use = random.sample(empty_tiles, num_tiles_to_use)
    
    # Place items on the randomly selected tiles
    for tile in tiles_to_use[:items_to_place]:
        tile.add_object(items.pop(0))
    
    # Place skills on the remaining randomly selected tiles
    for tile in tiles_to_use[items_to_place:]:
        tile.add_object(skills.pop(0))

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


    Agaroth = Map("Agaroth", 20, 20)
    Agaroth.create_map()

    random.shuffle(Villains)

    one_hero = []
    one_hero.append(Heroes[0])
    short_villains = []
    need = 3

    for vil in Villains:
        if len(short_villains) > need:
            break
        else:
            short_villains.append(vil)
        
    
    combined_characters = Heroes + Villains

    character_order = sorted(combined_characters, key=attrgetter("agi"), reverse=True)
    characters = []
    for character in character_order:
        new_agent = AIAgent(Agaroth, character, Heroes, Villains)
        characters.append(new_agent)

    turns = 1

    place_characters(Agaroth, Heroes,Villains)
    place_items(Agaroth, Skill, Items)
    Agaroth.show_map()

    while len(Heroes) > 0 and len(Villains) > 0:
        
        for char in characters:
            char.make_move()
            
        for char in Heroes:
            char.HP = round(char.HP, 1)
            if char.HP <= 0:
                Heroes.remove(char)
        for char in Villains:
            char.HP = round(char.HP, 1)
            if char.HP <= 0:
                Villains.remove(char)
        print(turns, "turns")
        Agaroth.show_map()

        time.sleep(1)
        
        turns += 1
        

    if len(Heroes) == 0:
        print("Villains win")
        for vil in Villains:
            print(colored(vil.name, "red"))
    else:
        for hero in Heroes:
            print(colored(hero.name, "green"))
            print(hero.str, hero.agi, hero.int,  hero.level, hero.items, hero.skills, hero.exp)
        print("Heroes win")


    


main()










        
