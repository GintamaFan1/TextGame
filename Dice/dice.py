import random

class Dice:

    def __init__(self, faces, category):
        self.faces = faces
        self.face = {}
        self.create_dice()
        self.value = None
        self.category = category

    def __str__(self):
        print(f"{self.faces} sided dice")

    def create_dice(self):
        numbers = []
        for i in range(1, self.faces + 1):
            if i not in numbers:
                numbers.append(i)
        numbers2 = numbers.copy()
        random.shuffle(numbers2)
       
        for num in numbers:
            if num not in self.face:
                index = numbers.index(num)
                self.face[num] = numbers2[index]

    def roll(self):
        numbers = []
        for i in range(1, self.faces):
            numbers.append(i)
        
        random.shuffle(numbers)
        
        self.value = self.face[numbers[0]]

def evaluator(dice1, dict):

    dice1.roll()
    result = dice1.value
    print(f"{dice1.category}, {result}")
    if dice1.category not in dict:
        dict[dice1.category] = result
    else:
        dict[dice1.category] += result

def roll_three(dice1, dice2, dice3, dict):
    evaluator(dice1, dict)
    evaluator(dice2, dict)
    evaluator(dice3, dict)

    




 

            



