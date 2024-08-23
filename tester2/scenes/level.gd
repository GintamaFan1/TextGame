extends Node2D




var character_scene: PackedScene = preload("res://scenes/character.tscn")
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var character = character_scene.instantiate()
	character.position = %CharacterStart.position 
	%CharacterStart.add_child(character)
	


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	
		
		
