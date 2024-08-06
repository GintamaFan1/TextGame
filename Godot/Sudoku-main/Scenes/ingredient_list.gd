extends Control

var ingredients_list: Array = []

signal ingredient_added(item)

# Called when the node enters the scene tree for the first time.
func _ready():
	
	reload_ingredients()
			
		

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_add_ingre_button_pressed():
	$CreateIngrdient.show()

func load_ingredients():
	ingredients_list.clear()
	var dir = DirAccess.open("user://")
	
	if not dir.dir_exists("ingredients"):
		dir.make_dir("ingredients")
		
	dir.change_dir("ingredients")
	
	if dir.get_files().size() <= 0:
		DisplayMessage.display_alert_message("No ingredients to load", "Notice")
		return 
		
	else:
		dir.list_dir_begin()
		var file = dir.get_next()
		
		while file != "":
			print(file, "first load")
			var save_file = FileAccess.open("user://ingredients/" + file, FileAccess.READ)
			var json_string = save_file.get_as_text()
			
			save_file.close()
			
			var save_data = JSON.parse_string(json_string)
			
			if save_data == null:
				DisplayMessage.display_alert_message("Error getting save file")
				return
			print("fist laod cleared")
			var name1 = save_data["name"]
			var price = float(save_data["price"])
			var original_amount = float(save_data["original_amount"])
			var current_amount = float(save_data["current_amount"])
			
			var ingredient = Ingredient.new(name1, price, original_amount)
			
			ingredient.current_amount = current_amount
			
			ingredients_list.append(ingredient)
			
			file = dir.get_next()
			
func fill_itemlist(ingredients: Array):
	
	var contianer = $PanelContainer/ItemList/VBoxContainer.get_children()
	
	if contianer:
		for child in contianer:
			child.queue_free()
	
	for item in ingredients:
		
		var hbox = HBoxContainer.new()
		hbox.add_to_group("item_list")
		
		var add_button = Button.new()
		var delete_button = Button.new()
		
		
		var vbox_label = VBoxContainer.new()
		var vbox_value = VBoxContainer.new()
		
		
		var name_label = Label.new()
		var name_value = Label.new()
		
		var price_label = Label.new()
		var price_value = Label.new()
		
		var original_label = Label.new()
		var original_value = Label.new()
		
		var current_label = Label.new()
		var current_value = Label.new()
		
		add_button.text = "Add To Recepie"
		add_button.pressed.connect(_on_add_button_pressed.bind(item))
		
		delete_button.text = "Delete Ingredient"
		delete_button.pressed.connect(_delete_button_pressed.bind(item))
		
		var del_norm = preload("res://Themes/Button Styles/delete Button normal.tres")
		var del_hover = preload("res://Themes/Button Styles/delete button hover.tres")
		var del_pressed = preload("res://Themes/Button Styles/delete button pressed.tres")
		
		delete_button.add_theme_stylebox_override("normal", del_norm)
		delete_button.add_theme_stylebox_override("hover", del_hover)
		delete_button.add_theme_stylebox_override("pressed", del_pressed)
		delete_button.add_theme_stylebox_override("focus", del_pressed)
		delete_button.add_theme_color_override("font_color", Color(.9, .6, .83, 1))
		delete_button.add_theme_color_override("font_hover_color", Color(.9,.6,.83,1))
		
		
		
		
		name_label.text = "Name"
		name_value.text = item.name.capitalize()
		
		price_label.text = "Price"
		price_value.text = "$" + str(item.price)
		
		original_label.text = "Original Amount"
		original_value.text = str(item.original_amount) + "oz"
		
		current_label.text = "Current Amount"
		current_value.text = str(item.current_amount) + "oz" 
		
		
		
		
		vbox_label.add_child(name_label)
		vbox_label.add_child(price_label)
		vbox_label.add_child(original_label)
		vbox_label.add_child(current_label)
		vbox_label.add_child(add_button)
		
		
		vbox_value.add_child(name_value)
		vbox_value.add_child(price_value)
		vbox_value.add_child(original_value)
		vbox_value.add_child(current_value)
		vbox_value.add_child(delete_button)
		
		
		hbox.add_child(vbox_label)
		hbox.add_child(vbox_value)
		
		
		$PanelContainer/ItemList/VBoxContainer.add_child(hbox)
		
	
func reload_ingredients():
	load_ingredients()
	fill_itemlist(ingredients_list)

func _on_create_ingrdient_ingredient_created():
	reload_ingredients()
	
func _on_add_button_pressed(item):

	ingredient_added.emit(item)


func _on_close_button_pressed():
	$".".hide()

func _delete_button_pressed(item):
	var dir = DirAccess.open("user://ingredients/")
	
	dir.list_dir_begin()
	
	var file = dir.get_next()
	
	while file != "":
		if file == item.name + ".save":
			
			var err = dir.remove(file)
			if err == OK:
				DisplayMessage.display_alert_message("Ingredient Deleted", "Notice")
			else:
				DisplayMessage.display_alert_message("Failed to Delelte Ingredient", err)
			break
		file = dir.get_next()
	reload_ingredients()




func _on_delete_button_pressed():
	var dir = DirAccess.open("user://ingredients")
	
	if dir.get_files().size() > 0:
		dir.list_dir_begin()
		
		var file = dir.get_next()
		
		while file != "":
			
			dir.remove(file)
	
			file = dir.get_next()
	reload_ingredients()
