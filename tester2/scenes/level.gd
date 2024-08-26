extends Node2D


var enemy1_scene: PackedScene = preload("res://scenes/enemy_1.tscn")

var character_scene: PackedScene = preload("res://scenes/character.tscn")
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var character = character_scene.instantiate()
	character.position = %CharacterStart.global_position
	%CharacterStart.add_child(character)
	
	var enemy1 = enemy1_scene.instantiate()
	enemy1.position = %Enemy1Marker.global_position
	add_child(enemy1)
	var enemy2 = enemy1_scene.instantiate()
	enemy2.position = %Enemy1Marker2.global_position
	add_child(enemy2)
	


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass
	
		
		
