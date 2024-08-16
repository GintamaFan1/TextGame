extends Node2D

var train_speed: float = 1.2
var enemy_tally = 1

@onready var character_scene: PackedScene = preload("res://Scenes/Games2/Enemies/character.tscn")
@onready var red_enemy_scene: PackedScene = preload("res://Scenes/Games2/Enemies/red_enemy.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	var curve: Curve2D = $TrainHandler/TrainTracks.get_curve()
	var last_point: Vector2 = curve.get_point_position(5)
	var character = character_scene.instantiate()
	character.position = last_point
	add_child(character)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	$TrainHandler/TrainTracks/Conductor.progress += train_speed 

func first_wave():
	var usuable_markers: Array = [$Speed85Enemies/Marker2D, $Speed135Enemies/Marker2D, $Speed45Enemies/Marker2D,$Speed45Enemies/Marker2D2]
	
	summon_enemies(usuable_markers)
	
func second_wave():
	var usuble_markers: Array = [$Speed135Enemies, $Speed45Enemies/Marker2D, $Speed135Enemies/Marker2D2]
		
	summon_enemies(usuble_markers)

func _on_enemy_trigger_area_shape_entered(_area_rid, _area, _area_shape_index, _local_shape_index):
	first_wave()

func summon_enemies(list):
	
	for marker in list:
		var red = red_enemy_scene.instantiate()
		red.position = marker.position
		red.name = "red_enemy" + str(enemy_tally)
		if marker.get_parent().name == "Speed135Enemies":
			red.speed = 135
		elif marker.get_parent().name == "Speed85Enemies":
			red.speed = 85
		elif marker.get_parent().name == "Speed45Enemies":
			red.speed = 45
		get_tree().root.call_deferred("add_child",red)
		enemy_tally += 1
	


func _on_enemy_trigger_2_area_shape_entered(_area_rid, _area, _area_shape_index, _local_shape_index):
	second_wave()
