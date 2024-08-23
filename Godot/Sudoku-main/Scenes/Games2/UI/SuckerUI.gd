extends CanvasLayer

var stage_selector = preload("res://Scenes/Games2/UI/stage_selector.tscn")
# Called when the node enters the scene tree for the first time.
func _ready():
	$ColorRect.show()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	
	$Control/HBoxContainer/HealthContainer/CharacterHealthBar.value = Sucker.character_health
	$Control/HBoxContainer/HealthContainer/TrainHealthBar.value = Sucker.train_health
	$Control/HBoxContainer/AbilityContainer/LungCapicityBar.value = Sucker.lung_capacity
	
	$Control/HBoxContainer/HealthContainer/CharacterHealthLabel.text = "Character Health: %d%%" % ($Control/HBoxContainer/HealthContainer/CharacterHealthBar.value)
	$Control/HBoxContainer/HealthContainer/TrainHealthLabel.text = "Train Health: %d%%" % ($Control/HBoxContainer/HealthContainer/TrainHealthBar.value / 2)
	$Control/HBoxContainer/AbilityContainer/LungCapacityLabel.text = "Lung Capacity: %d%%" % ($Control/HBoxContainer/AbilityContainer/LungCapicityBar.value / 1.2)
	if Sucker.selected_stage_path != null:
		$ColorRect/AnimationPlayer.play_backwards("fade_in")

func load_scene(scene):
	var level = scene.instantiate()
	var container_children = $Control/SceneContainer.get_children()
	for child in container_children:
		child.queue_free()
		
	$Control/SceneContainer.add_child(level)
	
	Sucker.selected_stage_path = null
	

func _on_animation_player_animation_finished(anim_name):
	$ColorRect.hide()
	if Sucker.selected_stage_path != null:
		load_scene(load(Sucker.selected_stage_path))
	else:
		load_scene(stage_selector)



func _on_animation_player_animation_started(anim_name):
	$ColorRect.show()
