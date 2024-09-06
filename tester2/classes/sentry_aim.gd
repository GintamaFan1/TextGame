extends State

class_name SentryAim

@export var enemy: StaticBody2D

var player: CharacterBody2D
var timer: Timer

func Enter():
	player = get_tree().get_first_node_in_group("player")
	if timer != null:
		
		timer.get_parent().remove_child(timer)
		timer.queue_free()
		timer = null
	if timer == null:
		
		timer = Timer.new()
		timer.wait_time = 2.5
		timer.one_shot = false
		timer.timeout.connect(switch_to_shoot)
		add_child(timer)
		timer.start()
	

func Physics_Update(_delta: float):
	
	var direction = player.global_position - enemy.global_position
	
	$"../../Sprite2D".rotation = direction.angle()
	

	if direction.length() > 270 or enemy.player_seen == false:
		if timer:
			timer.get_parent().remove_child(timer)
			timer.queue_free()
		Transitioned.emit(self, "idle")

func switch_to_shoot():
	if timer:
		timer.get_parent().remove_child(timer)
		timer.queue_free()
	Transitioned.emit(self,"shoot")
	
