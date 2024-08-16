extends Control


var highlight = false
# Called when the node enters the scene tree for the first time.
func _ready():
	$PanelContainer/VBoxContainer/HSlider.add_to_group("scale_slider")
	$PanelContainer/VBoxContainer/SoundSlider.add_to_group("volume_slider")
	if AudioManager.playing == true:
		$PanelContainer/VBoxContainer/HBoxContainer/PlayButton.text = "Pause"
	else:
		$PanelContainer/VBoxContainer/HBoxContainer/PlayButton.text = "Play"
	
	update_song_name()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_close_button_pressed():
	$".".visible = false


func _on_h_slider_value_changed(value):
	var grid_container = get_tree().get_first_node_in_group("grid_containers")
	
	if grid_container:
		grid_container.scale = Vector2(value, value)


func _on_sound_slider_value_changed(value):
	AudioManager.set_volume(value)


func _on_play_button_pressed():
	AudioManager.toggle_music()
	if AudioManager.playing == true:
		$PanelContainer/VBoxContainer/HBoxContainer/PlayButton.text = "Pause"
	else:
		$PanelContainer/VBoxContainer/HBoxContainer/PlayButton.text = "Play"



func _on_next_button_pressed():
	AudioManager.play_next()
	update_song_name()

func _on_previous_button_pressed():
	AudioManager.play_previous()
	update_song_name()

func _on_shuffle_button_pressed():
	AudioManager.shuffle()
	update_song_name()

func update_song_name():
	$PanelContainer/VBoxContainer/CurrentSongLabel.text = AudioManager.show_song()
	$PanelContainer/VBoxContainer/CurrentSongLabel/AnimationPlayer.play("Name mover")


func _on_loop_button_pressed():
	if AudioManager.loop == true:
		AudioManager.loop = false
		highlight = false
	else:
		AudioManager.loop = true
		highlight = true
	
	if highlight == true:
		$PanelContainer/VBoxContainer/HBoxContainer/LoopButton.text = $PanelContainer/VBoxContainer/HBoxContainer/LoopButton.text.to_upper()
	else:
		$PanelContainer/VBoxContainer/HBoxContainer/LoopButton.text = $PanelContainer/VBoxContainer/HBoxContainer/LoopButton.text.capitalize()
