extends Node2D
class_name Crumb

@onready var player: CharacterBody2D
@onready var enemies: Array
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	player = get_tree().get_first_node_in_group("player")
	enemies = get_tree().get_nodes_in_group("enemies")
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass

func place_crumb(spot):
	$".".position = spot
	
func _on_timer_timeout() -> void:
	queue_free()


func _on_crumb_area_body_entered(body: Node2D) -> void:
	
	if body is Enemy1:
		queue_free()
			
