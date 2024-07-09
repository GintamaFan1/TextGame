from abilities import *
from stage import *

star = "star"
cross = "cross"
abilities = [star, cross]

stage = Stage()

turns = 1

while turns < 9:
    print(stage.level, "Level")
    set_abilities = []
    for i in range(stage.level):
        ability = random.choice(abilities)

        if ability == "star":
            abi = Star("star")
        elif ability == "cross":
            abi = Cross("cross")


        stage.place_ability(abi)
        if isinstance(abi, Star):

            stage.tiles[(abi.x, abi.y)].exploded = True
        elif isinstance(abi, Cross):
            stage.tiles[(abi.x, abi.y)].frozen = True

        set_abilities.append(abi)

    

    stage.show_stage()

    print("Where will you place character? ")

    answer = input("")
    print("")

    for abi in set_abilities:
        abi.activate(stage)

    stage.show_stage()
    print("")

    stage.reset()
    stage.level += 1


    turns += 1