from dice import Dice, roll_three, evaluator
from box import Box
from creatures import Creature
from stage import Stage, Tile
from termcolor import colored
import random

class Ai_Agent:

    def __init__(self, stage, player):
        self.stage = stage
        self.moves = []
        self.points = {}
        self.player = player


    def rolling(self, dice1, dice2, dice3):
        roll_three(dice1,dice2,dice3,self.points)

    def move_creature(self):
        
        available_creatures = [tile for tile in self.stage.tiles.objects if isinstance(tile.artifact, Creature) 
                            and tile.artifact.owner == self.player]
        if available_creatures:
            random.shuffle(available_creatures)

            self.pick_path(available_creatures[0])

            
        


