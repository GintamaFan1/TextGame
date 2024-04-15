from box import Box
from creatures import Creature
from stage import Tile, Stage
from dice import *
from player import Player

def battle(attacker, defender):

    damage = attack(attacker, defender)

    defender.HP -= damage

    print(f"{attacker.name}, does {damage} to {defender.name}")


    if defender.HP <= 0:
        died(defender)
        

    else:
        damage = attack(defender, attacker)

        attacker.HP -= damage

        print(f"{defender.name} does {damage} in retaliation {attacker.name}")

        if attacker.HP <= 0:
            died(attacker)




def died(creature):
    creature.owner.creatures.remove(creature)
    print(f"{creature.name} died")

def attack(attacker, defender):
    power = attacker.a
    defence = defender.d
    damage = 4
    modifier1 = .25
    modifier2 = .5

    if power >= defence:
        damage += ((modifier1 * damage) + (defence * modifier2))
    
    else:
        damage -= (modifier1 * damage)

    if damage < 1:
        damage = 1

    return round(damage)


