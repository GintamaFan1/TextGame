extends Control

@onready var monster1_scene = preload("res://scenes/Monster Scenes/red_crimson.tscn")
@onready var monster2_scene = preload("res://scenes/Monster Scenes/bone_head.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	place_monster(monster1_scene,$MarkersNode/Position1 )
		
	place_monster(monster2_scene,$MarkersNode/Position2 )


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func place_monster(monster_scene, marker):
	var monster = monster_scene.instantiate()
	
	monster.position = marker.position
	add_child(monster)
	

func _on_area_2d_body_entered(body):
	print(body)
