extends Control


# Called when the node enters the scene tree for the first time.
func _ready():
	$Panel/VBoxContainer/ScaleSlider.add_to_group("scale_slider")


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_scale_slider_value_changed(value):
	var grid_container = get_tree().get_first_node_in_group("grid_containers")
	
	
	if grid_container:
		grid_container.scale = Vector2(value, value)


func _on_close_button_pressed():
	$".".visible = false
