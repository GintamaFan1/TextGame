from item import Item
from skills import Skills
from characters import Hero, Villain
from maps import Map
import random
from termcolor import colored

def pick_up_item(item, character):

    if isinstance(item, Item):
        if item not in character.items:
            item.equip_to(character)
            
    elif isinstance(item, Skills):
        if item not in character.skills:
            character.skills.append(item)
    

def melee_attack(attacker, defender):
    power = attacker.str
    defence = defender.str
    damage = 4
    skill = None
    
    if attacker.skills:
        physical_skills = []
        for ski in attacker.skills:
            if ski.category == "Physical":
                physical_skills.append(ski)
        if physical_skills:
            if len(physical_skills) > 1:
                skill = random.choice(physical_skills)
            else:
                print(physical_skills, "skills")
                skill = physical_skills[0]

            
    
    if skill != None:
        if attacker.MP >= skill.cost:
            print(colored((f"{attacker.name} uses {skill.name}, DMG: {skill.damage}, Cost:{skill.cost}"), "blue"))
            if power >= defence:
                difference = power - defence
                damage += (damage * .5) + (difference * .2)
                damage += skill.damage
                attacker.MP -= skill.cost
            
            else:
                difference = defence - power
                damage -= (damage * .5) + (difference * .2)
                damage += skill.damage
                attacker.MP -= skill.cost
        else:
            print(colored((f"{attacker.name} gains 5 MP")))
            if power >= defence:
                difference = power - defence
                damage += (damage * .5) + (difference * .2)
                attacker.MP += 5
            
            else:
                difference = defence - power
                damage -= (damage * .5) + (difference * .2)
                attacker.MP += 5

    
    else:
        print(colored((f"{attacker.name} gains 5 MP")))
        if power >= defence:
            difference = power - defence
            damage += (damage * .5) + (difference * .2)
            attacker.MP += 5
        
        else:
            difference = defence - power
            damage -= (damage * .5) + (difference * .2)
            attacker.MP += 5
        
        

    return round(damage,1)

def magical_attack(attacker, defender):
    power = attacker.int
    defence = defender.int
    damage = 4
    skill = None

    if attacker.skills:
        magical_skills = []
        for ski in attacker.skills:
            if ski.category == "Magical":
                magical_skills.append(ski)
        if magical_skills:
            if len(magical_skills) > 1:
                skill = random.choice(magical_skills)
            else:
                skill = magical_skills[0]


    if skill != None:
        if attacker.MP >= skill.cost:
            print(colored((f"{attacker.name} uses {skill.name}, DMG: {skill.damage}, Cost:{skill.cost}"), "blue"))
            if power >= defence:
                difference = power - defence
                damage += (damage * .5) + (difference * .2)
                damage += skill.damage
                attacker.MP -= skill.cost
            
            else:
                difference = defence - power
                damage -= (damage * .5) + (difference * .2)
                damage += skill.damage
                attacker.MP -= skill.cost
        else:
            print(colored((f"{attacker.name} gains 5 MP")))
            if power >= defence:
                difference = power - defence
                damage += (damage * .5) + (difference * .2)
                attacker.MP += 5
            
            else:
                difference = defence - power
                damage -= (damage * .5) + (difference * .2)
                attacker.MP += 5
    
    else:
        print(colored((f"{attacker.name} gains 5 MP")))
        if power >= defence:
            difference = power - defence
            damage += (damage * .5) + (difference * .2)
            attacker.MP += 5
        
        else:
            difference = defence - power
            damage -= (damage * .5) + (difference * .2)
            attacker.MP += 5

    return round(damage,1)

def killed(place, initiator, defender, initiator_cords, defender_coords):
    if defender.HP <= 0:
        if initiator.nature == "Hero":
            initiator.gain_exp(6 + round(defender.rank))
            print(colored((f"{initiator.name} gained {6 + round(defender.rank)} Exp "), "green"))
            print(colored((f"{initiator.name} killed {defender.name} "), "red"))
        
        else:
            initiator.kills.append(defender)
            if initiator.HP < 200:
                initiator.HP + 20
            if initiator.HP > 200:
                initiator.HP = 200
            print(colored((f"{initiator.name} killed {defender.name} "), "red"))
        
        
        place.tiles[defender_coords[0]].remove_object(defender)
        place.tiles[initiator_cords].remove_object(initiator)
        place.tiles[defender_coords[0]].add_object(initiator)

        print(f"{defender.name} died, {initiator.name} moves to {defender_coords}")

        if len(defender.items) > 0:
            print(colored((f"{defender.name} dropped items"), "yellow"))

            for item in defender.items:
                open_space = [tile for tile in place.tiles.values() if len(tile.objects) == 0]
                random.shuffle(open_space)
                open_space[0].add_object(item)
            for item in defender.items:
                item.unequip_from(defender)

        if len(defender.skills) > 0:
            print(f"{defender.name} dropped skills")
            for skill in defender.skills:
                open_space = [tile for tile in place.tiles.values() if len(tile.objects) == 0]
                random.shuffle(open_space)
                open_space[0].add_object(skill)
            for skill in defender.skills:
                defender.skills.remove(skill)

    elif initiator.HP <= 0:
        
        if defender.nature == "Hero":
            defender.gain_exp(6 + round(initiator.rank))
            print(colored((f"{defender.name} gained {6 + round(initiator.rank)} Exp "), "green"))
            print(colored((f"{defender.name} killed {initiator.name} "), "red"))

        
        else:
            defender.kills.append(initiator)
            if defender.HP < 200:
                defender.HP + 20
            if defender.HP > 200:
                defender.HP = 200
            print(colored((f"{defender.name} killed {initiator.name} "), "red"))

        place.tiles[initiator_cords].remove_object(initiator)
        print(f"{defender.name} defended {defender_coords}")
        if len(initiator.items) > 0:
            print(colored((f"{initiator.name} dropped items"), "yellow"))

            for item in initiator.items:
                open_space = [tile for tile in place.tiles.values() if len(tile.objects) == 0]
                random.shuffle(open_space)
                open_space[0].add_object(item)
            for item in initiator.items:
                item.unequip_from(initiator)

        if len(initiator.skills) > 0:
            print(f"{initiator.name} dropped skills")
            for skill in initiator.skills:
                open_space = [tile for tile in place.tiles.values() if len(tile.objects) == 0]
                random.shuffle(open_space)
                open_space[0].add_object(skill)
                print(open_space[0].tile, "open skill")
            for skill in initiator.skills:
                initiator.skills.remove(skill)


def battle(char1, char2):
    damage = 0
        
    if char1.str >= char1.int:
        damage = melee_attack(char1, char2)
    else:
        damage = magical_attack(char1, char2)
    
    if damage <= 1:
        damage = 1
    
    char2.HP -= damage
    round(char2.HP, 1)
    print(colored((f"{char1.name} dealt {damage} points of damage to {char2.name}"), "light_green"))
    

    
        
    

       







