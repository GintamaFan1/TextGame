
class Creature:

    def __init__(self,name, HP, AP, Attk, Def):
        self.name = name
        self.maxHP = HP
        self.maxAP = AP
        self.HP = HP
        self.AP = AP
        self.a = Attk
        self.d = Def
        self.x = None
        self.y = None
        self.flavor = ""
        self.owner = None
        self.died = False
        
    def __str__(self):
        return f"{self.name}, HP: {self.HP}, AP: {self.AP}, Att: {self.a}, Def: {self.d}, Owner: {self.owner}, Description: {self.flavor} "
        

    


