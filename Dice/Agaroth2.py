from creatures import Creature
from box import Box
from dice import *
from player import Player
from stage import Stage, Tile
from agent import Ai_Agent, Crawler
import random
import csv
import time

def main():
    Creatures = []

    with open("Creatures.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for line in reader:
            name, HP, AP, att, deff = line
            hp = int(HP)
            ap = int(AP)
            att = int(att)
            deff = int(deff)
            Creatures.append(Creature(name,hp, ap, att, deff))

    half = round(len(Creatures) // 2)

    creature_set1 = Creatures[:half]
    creature_set2 = Creatures[half:]

    stage = Stage(20,20)

    player1 = Player(stage, "one", True)
    player2 = Player(stage, "two", False)

    movement_die = Dice(6, "Movement")
    ability_die = Dice(6, "Ability")
    summon_die = Dice(6, "Summon")

    turns = 0

    agent1 = Ai_Agent(stage, player1, creature_set1, player2, movement_die, summon_die, ability_die)
    agent2 = Ai_Agent(stage, player2, creature_set2, player1, movement_die, summon_die, ability_die)

    stage.show_stage()

    for creature in creature_set1:
        creature.owner = player1

    for creature in creature_set2:
        creature.owner = player2

    while stage.game_over == False:
        

        agent1.run()
        agent2.run()

        turns += 1
        print(turns)
        stage.show_stage()


        if len(agent1.creature_storage) == 0 and len(agent2.creature_storage) == 0 and stage.opponents_connected == False:
            print("Game tied, failed to connect paths")
            break
    


    





main()
