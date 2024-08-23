extends PopupPanel

signal board_selected(board_name: String)

@onready var option_button =  $VBoxContainer/OptionButton
@onready var load_button =  $VBoxContainer/HBoxContainer/LoadButton
@onready var cancel_button =  $VBoxContainer/HBoxContainer/CancelButton


# Called when the node enters the scene tree for the first time.
func _ready():
	load_button.pressed.connect(_on_load_pressed)
	cancel_button.pressed.connect(_on_cancel_pressed)
	


func populate_dropdown():
	option_button.clear()
	
	var dir = DirAccess.open("user://maps/")
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			if file_name.ends_with(".save"):
				option_button.add_item(file_name.get_basename())
			file_name = dir.get_next()
			
	else:
		print("An error occured gaining access to path")
	
func _on_load_pressed():
	if option_button.selected >= 0:
		emit_signal("board_selected", option_button.get_item_text(option_button.selected))
	hide()
func _on_cancel_pressed():
	hide()
