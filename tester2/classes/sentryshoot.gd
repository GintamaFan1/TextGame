extends State


class_name SentryShoot

@export var enemy: StaticBody2D
var player: CharacterBody2D

	
func Enter():
	player = get_tree().get_first_node_in_group("player")
	enemy.attack()
	
func Physics_Update(_delta: float):
	
	Transitioned.emit(self, "aim")
	
	
