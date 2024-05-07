from creatures import Creature
from player import Player
import random
import csv

def main():
    creatures = []
    Names = ["Lao", "Lien", "Krez", "Mien", "Dro", "Ikzel", "Mer", "Plid", "Swar", "Qer",
             "Jin", "Vum", "Far", "Bern", "Xer", "Zemmy", "Artp", "Clort", "Urd", "Natsu", "Grey",
             "Erza", "Elf-man", "Nirvana", "Mirajane", "Lizzana", "Tsukyo", "Sawada", "Chomu", "Indra",
             "Mix", "Troy", "Wart", "Blope", "Squat"]
    
    HP = [25,26,27,28,29,30]
    AP = [15,16,17,18,19]
    stats = [3,4,5,6,7,8]

    while len(Names) > 0:
        chosen_name = random.choice(Names)
        hp = random.choice(HP)
        ap = random.choice(AP)
        att = random.choice(stats)
        deff = random.choice(stats)

        creatures.append(
            Creature(chosen_name, hp, ap, att, deff)
        )

        Names.remove(chosen_name)
    
    with open("Creatures.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Name", "HP", "AP", "Att", "Deff"])

        for cre in creatures:
            writer.writerow([cre.name, cre.HP, cre.AP, cre.a, cre.d])

    
main()