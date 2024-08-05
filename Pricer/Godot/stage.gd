extends Control

const Grid = preload("res://Classes/Tile.gd")
const Scene_m = preload("res://addons/awesome_scene_manager/autoloads/SceneManager.gd")
@onready var load_board_popup = $PopupPanel

const TILE_SIZE = 128
const GRID_SIZE = 9
var current_input: LineEdit = null
const gameOver: PackedScene = preload("res://Scenes/game_over.tscn")

var value1: float = .9
var value2: float = .5555555
var value3: float = .4
var value4: float = .444444444
var value5: float = .3
var value6: float = .333
var value7: float = .7
var difficulty: int = 0
var mistakes: int = 1
var Hints: int = 3
var rng = RandomNumberGenerator.new()


# Called when the node enters the scene tree for the first time.
func _ready():
	$Control.show()
	
	var dir = DirAccess.open("user://")
	if not dir.dir_exists("maps"):
		dir.make_dir("maps")
		
	load_board_popup.connect("board_selected", _on_board_selected)
	$Control/VBoxContainer/LoadButton.pressed.connect(show_load_board_popup)
	
	
func generate_sudoku_board(grid = null):
	print("generating board")
	if $Control:
		$Control.hide()
	
	var grid_width = TILE_SIZE * GRID_SIZE
	var grid_height = TILE_SIZE * GRID_SIZE
	
	var screen_width = get_viewport_rect().size.x
	var screen_height = get_viewport_rect().size.y
	var grid_x = (screen_width - grid_width) / 2
	var grid_y = (screen_height - grid_height) / 2
	
	
	cleanup_grid_container()
	
	
	var grid_container = ColorRect.new()
	grid_container.name = "GridContainer"
	
	grid_container.add_to_group("grid_containers")
	grid_container.set_anchors_preset(PRESET_CENTER)
	grid_container.set_size(Vector2(TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE))
	add_child(grid_container)
	
	
	if grid == null:
		grid = Grid.Grid.new()
		grid.generate()
		grid.difficulty(difficulty)
	
	var tile_texture = preload("res://numbers/grid-tile.png")
	
	for row in range(9):
		
		for col in range(9):
			var tile = grid.get_tile(row, col)
			
			var sprite = tile.ensure_sprite_setup(tile_texture)
			tile.sprite = sprite
			if tile.groupNumber == 0 or tile.groupNumber == 2 or tile.groupNumber == 4 or tile.groupNumber == 6 or tile.groupNumber == 8:
				tile.set_color(value1,value1,value1)
			elif tile.groupNumber == 1 or tile.groupNumber == 3 or tile.groupNumber == 5 or tile.groupNumber == 7:
				tile.set_color(value1,value2,value4)
			
			var button = Button.new()
			var label = Label.new()
			
			
			  # Example text, you can customize it
			
			button.size = Vector2(50,50)
			

			
			label.add_theme_font_size_override("font_size", 40)
			if tile.open == false:
				label.add_theme_color_override("font_color", Color(.3,.123,.7) )
				
			else:
				label.add_theme_color_override("font_color", Color(.2,.5,.7) )
			
			
			button.position = Vector2(col * TILE_SIZE + 50 , row * TILE_SIZE + 45 )
			button.modulate = Color(0,0,0,0)
			label.position = Vector2(col * TILE_SIZE + 50 , row * TILE_SIZE + 45)
		
			
			var font = preload("res://Fonts/fonts/montreal/Montreal-Bold.ttf")  # Load your custom font
			label.add_theme_font_override("font", font)
			label.text = str(tile.value)
			
			
			tile.sprite.position = Vector2(col * TILE_SIZE + 65, row * TILE_SIZE + 65)
			grid_container.add_child(tile.sprite)
			grid_container.add_child(label)
			grid_container.add_child(button)
			
			
			
			
			if tile.open:
				button.pressed.connect(_on_tile_clicked.bind(tile, label, grid, grid_container))
				
	var scale_slider = get_tree().get_first_node_in_group("scale_slider")
	
	if scale_slider:
		$".".scale = Vector2(scale_slider.value,scale_slider.value)
	
	
	add_ui_elements(grid_container, grid)
				
func add_ui_elements(grid_container, grid):
	var mistakes_label = Label.new()
	var hint_label = Label.new()
	var control = Control.new()
	var hint_button = Button.new()
	var save_button = Button.new()
	var load_button = Button.new()
	
	mistakes_label.add_theme_font_size_override("font_size", 40)
	hint_label.add_theme_font_size_override("font_size", 40)
	
	hint_button.size = Vector2(125, 50)
	save_button.size = Vector2(125, 50)
	
	var font = preload("res://Fonts/fonts/montreal/Montreal-Bold.ttf")  # Load your custom font
	mistakes_label.add_theme_font_override("font", font)
	mistakes_label.text = "Mistakes left: %d" % mistakes
	
	hint_label.add_theme_font_override("font", font)
	hint_label.text = "Hints left: %d" % Hints
	
	hint_button.text = "Hint"
	hint_button.add_theme_font_size_override("font_size", 30)
	
	save_button.text = "Save"
	save_button.add_theme_font_size_override("font_size", 25)
	
	load_button.text = "Load"
	load_button.add_theme_font_size_override("font_size", 25)
	
	control.set_anchors_preset(Control.PRESET_FULL_RECT)
	control.anchor_right = 1
	control.anchor_bottom = 1
	control.mouse_filter = Control.MOUSE_FILTER_IGNORE
	
	mistakes_label.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	mistakes_label.anchor_right = .7
	mistakes_label.anchor_bottom = 1
	mistakes_label.add_to_group("mistakes labels")
	
	
	hint_label.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	hint_label.add_to_group("hint button")
	
	hint_button.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	hint_button.anchor_left = .4
	hint_button.pressed.connect(_on_hint_clicked.bind(grid))
	
	save_button.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	save_button.pressed.connect(save_game.bind(grid))
	save_button.anchor_left = .25
	
	load_button.set_anchors_preset(Control.PRESET_TOP_LEFT)
	load_button.pressed.connect(show_load_board_popup)
	load_button.position.y = -100
	
	
	var name_container = HBoxContainer.new()
	name_container.set_anchors_preset(Control.PRESET_CENTER_TOP)
	name_container.position.y = -100  # Position it above the grid

	var name_label = Label.new()
	name_label.text = grid.name
	name_label.add_theme_font_size_override("font_size", 24)
	name_label.add_theme_font_override("font", preload("res://Fonts/fonts/montreal/Montreal-Bold.ttf"))

	var edit_button = Button.new()
	edit_button.text = " Edit"
	edit_button.pressed.connect(_on_edit_name_pressed.bind(name_label, grid))

	name_container.add_child(name_label)
	name_container.add_child(edit_button)
	
	
	control.add_child(load_button)
	control.add_child(save_button)
	control.add_child(name_container)
	control.add_child(hint_label)
	control.add_child(mistakes_label)
	control.add_child(hint_button)
	grid_container.add_child(control)
	if grid_container:
		print("ui added to grid")
	else:
		print("no ui added to grid")
	print("")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass



func _on_tile_clicked(tile, label, grid, grid_container):
	print("tile clicked")
	
	if current_input:
		remove_child(current_input)
		current_input.queue_free()
		current_input = null
		
	current_input = LineEdit.new()
	current_input.size = Vector2(100,100)
	current_input.add_theme_font_size_override("font_size", 30)
	current_input.position = Vector2(tile.sprite.position.x - 60, tile.sprite.position.y - 50)
	current_input.modulate = Color(.9,0.2,.87,1)
	current_input.text = ""
	current_input.grab_focus()
	current_input.text_submitted.connect(_on_input_entered.bind(tile, label, grid))
	grid_container.add_child(current_input)

func _on_input_entered(input_text, tile, label, grid):
	if input_text not in "0123456789":
		input_text = "0"
	var value = input_text.to_int()
	
	if value != tile.trueValue:
		mistakes -= 1
		value = 0
		
		update_mistakes_label()
		check_game_over()
	else:
		grid.openTiles.erase(tile)
		label.add_theme_color_override("font_color", Color(.6,.1,.8) )
		tile.open = false
		
		
		check_win_condition(grid)
	
	
	tile.value = value
	label.text = str(value)
	remove_child(current_input)
	current_input.queue_free()
	current_input = null

func random_choice(array):
	if array.is_empty():
		return null
	
	return array[rng.randi() % array.size()]

func banner(word):
	var old_banner = get_tree().get_first_node_in_group("banner")
	if old_banner:
		
		old_banner.queue_free()
	var banner1 = Label.new()
	
	var grid_container = get_tree().get_first_node_in_group("grid_containers")
	banner1.add_theme_font_size_override("font_size", 50)
	banner1.position = Vector2(100, -75)
	banner1.text = word
	
	banner1.add_to_group("banner")
	if grid_container:
		grid_container.add_child(banner1)
	
func _on_hint_clicked(grid):
	if Hints <= 0:
		banner("No more hints!")
	elif grid.openTiles.size() <= 5:
		banner("Can't Use hints now!")
	else:
		Hints -= 1
		update_hint_button()
		
		var random_tile = grid.openTiles[0]
	
		if random_tile:
			
			banner("Hint: Tile at row %d, column %d has value of %d" % [random_tile.rowNumber + 1, random_tile.colNumber + 1, random_tile.trueValue])
			random_tile.set_color(value5,value2, value6)
		
func update_hint_button():
	var hint_button = get_tree().get_first_node_in_group("hint button")
	
	if hint_button:
		
		hint_button.text = "Hints left: %d" % Hints
	else:
		print("Error getting hint button")
	
func update_mistakes_label():
	var mistakes_label = get_tree().get_nodes_in_group("mistakes labels")
	
	if mistakes_label.size() > 0:
		mistakes_label[0].text = "Mistakes left: %d" % mistakes
	else:
		print("error getting mistakes label")
func check_game_over():
	if mistakes <= 0:
		banner("Ran out of Mistakes, Game Over!")
		Game_over()
		
func check_win_condition(grid):
	if grid.openTiles.is_empty():
		banner("You Solved it!")
		Game_over()
func Game_over():
	SceneManager.swap_scenes("res://Scenes/game_over.tscn", self, SceneManager.Transitions.FADE)
	
func save_game(grid):
	
	var save_data = {
		"name": grid.name,
		"difficulty": difficulty,
		"mistakes": mistakes,
		"hints": Hints,
		"grid": []
	}
	
	# Save the current state of the grid
	for row in range(GRID_SIZE):
		for col in range(GRID_SIZE):
			var tile = grid.get_tile(row,col)
			save_data["grid"].append({
				"value": tile.value,
				"open": tile.open,
				"true_value": tile.trueValue,
			})
	
	# Save to file
	var save_file = FileAccess.open("user://maps/" + grid.name + ".save", FileAccess.WRITE)
	save_file.store_string(JSON.stringify(save_data))
	
	save_file.close()

func load_game(grid_name: String):
	print("loading")
	
	cleanup_grid_container()
	
	if not FileAccess.file_exists("user://maps/" + grid_name + ".save"):
		print("No save file found!")
		return false
	
	var save_file = FileAccess.open("user://maps/" + grid_name + ".save", FileAccess.READ)
	var json_string = save_file.get_as_text()
	save_file.close()

	var save_data = JSON.parse_string(json_string)
	if save_data == null:
		print("Invalid save file!")
		return false
	
	
	var grid = Grid.Grid.new()
	
	grid.load_from_saved_data(save_data)
	
	Hints = save_data["hints"]
	difficulty = save_data["difficulty"]
	mistakes = save_data["mistakes"]
	banner(grid.name + " loaded")
	
	update_hint_button()
	update_mistakes_label()
	
	for i in range(9):
		for j in range(9):
			var tile = grid.get_tile(i, j)
			var texture = preload("res://numbers/grid-tile.png")
			var region = Rect2(0, 0, TILE_SIZE, TILE_SIZE)
			tile.setup_sprite(texture, region)
		
		

	# Recreate the grid
	generate_sudoku_board(grid)

	return true



func _on_edit_name_pressed(name_label: Label, grid):
	print("clicked")
	var edit_dialog = AcceptDialog.new()
	edit_dialog.title = "Edit Grid Name"
	var line_edit = LineEdit.new()
	line_edit.text = grid.name
	edit_dialog.add_child(line_edit)
	edit_dialog.register_text_enter(line_edit)
	
	edit_dialog.connect("confirmed", func():
		var new_name = line_edit.text
		if new_name.strip_edges() != "":
			grid.name = new_name
			name_label.text = new_name
	)
	
	add_child(edit_dialog)
	edit_dialog.popup_centered()


func _on_board_selected(board_name: String):
	load_game(board_name)
	
func show_load_board_popup():
	load_board_popup.populate_dropdown()
	load_board_popup.popup_centered()
func cleanup_grid_container():
	var grid_containers = get_tree().get_nodes_in_group("grid_containers")
	for container in grid_containers:
		print("removing all containers")
		container.queue_free()


func _on_enter_button_pressed():
	var input_text = $Control/VBoxContainer/LineEdit.text
	if input_text not in "123":
		input_text = "3"
	difficulty = input_text.to_int()
	
	generate_sudoku_board()
