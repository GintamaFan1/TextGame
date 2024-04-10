from box import Box
from creatures import Creature
from stage import Tile, Stage
from dice import *
from player import Player

def battle(attacker, defender):
    print(f"battle between {attacker.name} and {defender.name}")

def died(creature):
    creature.owner.creatures.remove(creature)
    print(f"{creature.name} died")

