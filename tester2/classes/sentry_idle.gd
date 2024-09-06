extends State

class_name SentryIdle

@export var enemy: StaticBody2D


var move_direction: Vector2
var wander_time: float


func randomize_wander():
	$"../../Sprite2D".rotation = randf_range(0,360)
	wander_time = randf_range(6, 8)

func Enter():
	randomize_wander()

func Update(delta:float):
	if wander_time > 0:
		wander_time -= delta
	else:
		randomize_wander()

func Physics_Update(_delta: float):
	var player = get_tree().get_first_node_in_group("player")
	
		
	if enemy.player_seen:
		Transitioned.emit(self, "aim")
