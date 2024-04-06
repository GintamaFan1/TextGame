
class Creature:

    def __init__(self,name, HP, AP, Attk, Def, owner):
        self.name = name
        self.HP = HP
        self.AP = AP
        self.a = Attk
        self.d = Def
        self.x = None
        self.y = None
        self.flavor = ""
        self.owner = owner
        
    def __str__(self):
        print(f"Name: {self.name}, HP:{self.HP}, AP:{self.AP}, Attack:{self.a}, Defence:{self.d}, Owner: {self.owner}")
        print(f"Description: {self.flavor}")

    


