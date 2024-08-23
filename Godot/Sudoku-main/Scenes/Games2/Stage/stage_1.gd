extends Node2D


var test_speed = Sucker.test_speed
var original_train_speed: float = 1.2
var train_speed: float = 1.2 * test_speed
var enemy_tally = 1
var game_won = null
var scene_path = "res://Scenes/Games2/Stage/stage_1.tscn"
@onready var character_scene: PackedScene = preload("res://Scenes/Games2/Enemies/character.tscn")
@onready var red_enemy_scene: PackedScene = preload("res://Scenes/Games2/Enemies/red_enemy.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	var hbox = get_tree().get_first_node_in_group("bars")
	if hbox:
		hbox.show()
	
	var curve: Curve2D = $TrainHandler/TrainTracks.get_curve()
	var last_point: Vector2 = curve.get_point_position(5)
	var character = character_scene.instantiate()
	character.position = last_point
	add_child(character)
	Sucker.character_health = Sucker.orignal_character_health
	Sucker.train_health = Sucker.original_train_health
	Sucker.lung_capacity = Sucker.original_lung_capacity
	var red_enemies = get_tree().get_nodes_in_group("red_enemies")
	for child in red_enemies:
		child.queue_free()
	var items = get_tree().get_nodes_in_group("items")
	for child in items:
		child.queue_free()
	Sucker.code_executed = false
	
	character.game_won.connect(_character_lost)
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	$TrainHandler/TrainTracks/Conductor.progress += train_speed 
	
	if game_won == true and Sucker.code_executed == false:
		
		Sucker.game_over_info.clear()
		Sucker.game_over_info = {
			"game_won" : true,
			"stage" : scene_file_path,
			"stage_name": self.name
			
		}
		Sucker.selected_stage_path = "res://Scenes/Games2/UI/round_end.tscn"
		Sucker.update_score()
		Sucker.get_highscore()
		Sucker.code_executed = true
		
	elif game_won == false and Sucker.code_executed == false:
		Sucker.game_over_info.clear()
		Sucker.game_over_info = {
			"game_won" : false,
			"stage": scene_file_path,
			"stage_name": self.name
		}
		Sucker.selected_stage_path = "res://Scenes/Games2/UI/round_end.tscn"
		Sucker.update_score()
		Sucker.get_highscore()
		
		Sucker.code_executed = true

func first_wave():
	var usuable_markers: Array = [$Speed85Enemies/Marker2D, $Speed135Enemies/Marker2D,$Speed45Enemies/Marker2D3,
	 $Speed45Enemies/Marker2D,$Speed45Enemies/Marker2D2,$Speed135Enemies/Marker2D4]
	
	summon_enemies(usuable_markers)
	
func second_wave():
	var usuble_markers: Array = [$Speed45Enemies/Marker2D2,$Speed135Enemies/Marker2D3,
	 $Speed135Enemies/Marker2D2,$Speed85Enemies/Marker2D2,$Speed85Enemies/Marker2D3 ]
		
	summon_enemies(usuble_markers)
	
func third_wave():
	var usuable_markers: Array = [
		$Speed45Enemies/Marker2D5,$Speed45Enemies/Marker2D4,$Speed85Enemies/Marker2D4,$Speed85Enemies/Marker2D,
		
	]
	summon_enemies(usuable_markers)

func _on_enemy_trigger_area_shape_entered(_area_rid, _area, _area_shape_index, _local_shape_index):
	first_wave()

func summon_enemies(list):
	
	for marker in list:
		var red = red_enemy_scene.instantiate()
		red.position = marker.position
		red.name = "red_enemy" + str(enemy_tally)
		if marker.get_parent().name == "Speed135Enemies":
			red.speed = (135 * test_speed)
		elif marker.get_parent().name == "Speed85Enemies":
			red.speed = 85 * test_speed
		elif marker.get_parent().name == "Speed45Enemies":
			red.speed = 45 * test_speed
		get_tree().root.call_deferred("add_child",red)
		enemy_tally += 1
	


func _on_enemy_trigger_2_area_shape_entered(_area_rid, _area, _area_shape_index, _local_shape_index):
	second_wave()


func _on_train_game_won(result):
	if result == true and Sucker.code_executed == false:
		DisplayMessage.display_alert_message("You've Completed this Level!", "Notice")
		game_won = true
	elif result == false and Sucker.code_executed == false:
		DisplayMessage.display_alert_message("You've Lost,Try Again", "Notice")
		game_won = false


func _on_enemy_trigger_3_area_shape_entered(_area_rid, _area, _area_shape_index, _local_shape_index):
	third_wave()

func _character_lost(result):
	if result == true:
		DisplayMessage.display_alert_message("You've Completed this Level!", "Notice")
		game_won = true
	else:
		DisplayMessage.display_alert_message("You've Lost,Try Again", "Notice")
		game_won = false
	
