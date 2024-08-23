extends Control

var ingredients_for_recepie: Array = []
var recepie_list: Array = []

signal recepie_saved()

# Called when the node enters the scene tree for the first time.
func _ready():
	load_recepies()
	fill_container(recepie_list)
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


	
func _close_window(window):
	window.queue_free()

func _on_ingredient_list_ingredient_added(item):
	
	var window = Window.new()
	window.title = "Add %s" % item.name.capitalize()
	window.min_size = Vector2(425,150)
	window.close_requested.connect(_close_window.bind(window))

	var vbox = VBoxContainer.new()
	
	var message = Label.new()
	var value = LineEdit.new()
	var Enter = Button.new()
	
	value.add_to_group("line_value")
	Enter.text = "Enter"
	
	
	value.expand_to_text_length= true
	
	message.text = "How much would you like to use?"
	value.placeholder_text = "Current amount is %s oz" % item.current_amount
	
	value.text_submitted.connect(get_line_text.bind(item, window))
	
	Enter.pressed.connect(_enter_button_pressed.bind(item, window))
	
	var center = get_tree().get_first_node_in_group("center")
	window.position = center.position
	
	
	
	vbox.add_child(message)
	vbox.add_child(value)
	vbox.add_child(Enter)
	
	window.add_child(vbox)
	
	$Panel.add_child(window)
	
	
	

func get_line_text(input_text: String, item, window):
	
	
	var amount: float
	if input_text.is_valid_float():
		amount = float(input_text)
		
		if amount > item.current_amount:
			DisplayMessage.display_alert_message("That Amount is more than you have Avaialble")
			return
		elif amount == item.current_amount:
			DisplayMessage.display_alert_message("There is no more of that item left")
			return
		
		add_item(item, amount)
		
		
	else:
		DisplayMessage.display_alert_message("Value is not correct")
		return
		

func add_item(item, amount):
	var name_label = Label.new()
	var cost_label = Label.new()
	var used_label = Label.new()
	var hbox = HBoxContainer.new()
	
	hbox.add_to_group("recepie_creator")
	
	var unit_price = (item.price / item.original_amount) * amount
	
	name_label.text = "Ingredient: %s " % item.name.capitalize()
	used_label.text = "Used Amount: %s " % str(amount) + "oz "
	cost_label.text = "Cost: $" + str(snappedf(unit_price, .01))
	
	var data = {
		"name" : item.name,
		"amount" : amount,
		"unit_price": snappedf(unit_price, .01)
		}
	
	ingredients_for_recepie.append(data)
	
	
	
	hbox.add_child(name_label)
	hbox.add_child(used_label)
	hbox.add_child(cost_label)
	
	hbox.add_theme_constant_override("separation", 10)
	
	$Panel/VBoxContainer.add_child(hbox)
	
	DisplayMessage.display_alert_message("Ingredient Added Successfully", "Notice")
	


func _on_ingredient_button_pressed():
	$IngredientList.show()

func _enter_button_pressed(item, window):
	
	var line = get_tree().get_first_node_in_group("line_value")
	
	var text = line.text
	
	var amount: float
	if text.is_valid_float():
		amount = float(text)
		
		if amount > item.current_amount:
			DisplayMessage.display_alert_message("That Amount is more than you have Avaialble")
			return
		
		add_item(item, amount)
		window.queue_free()
		
		
	else:
		DisplayMessage.display_alert_message("Value is not correct")
		return
		


func _on_save_button_pressed():
	var recepie: String = $Panel/HBoxContainer/LineContainer/NameLine.text
	
	for item in recepie_list:
		if item["name"] == recepie:
			DisplayMessage.display_alert_message("A recepie With That Name Already Exist", "Notice")
			return
	
	if recepie == "":
		DisplayMessage.display_alert_message("Name field can't be empty")
		return
	
	var ingredient_names : Array = []
	var total_cost: float
	var total_amount: float
	
	if ingredients_for_recepie.size() <= 0:
		DisplayMessage.display_alert_message("No Ingredients Selected")
		return
	
	for item in ingredients_for_recepie:
		ingredient_names.append(item["name"])
		total_cost += item["unit_price"]
		total_amount += item["amount"]
		
		UpdateResources.update_ingredient_amount(item["name"].to_lower(), item["amount"])
	
	save_recepie(recepie, ingredient_names, total_cost, total_amount)
	
	$IngredientList.reload_ingredients()
	$Panel/HBoxContainer/LineContainer/NameLine.clear()
	
	
func save_recepie(recepie, ingredients, cost, amount):
	var dir = DirAccess.open("user://")
	
	if not dir.dir_exists("recepies"):
		dir.make_dir("recepies")
		
	dir.change_dir("recepies")
	
	var save_data: Dictionary = {
		"name" : recepie,
		"ingredients": ingredients,
		"cost": cost,
		"amount": amount
	}
	
	var file_path = "user://recepies/" + recepie + ".save"
	
	var save_file = FileAccess.open(file_path,FileAccess.WRITE)
	save_file.store_string(JSON.stringify(save_data))
	
	save_file.close()
	
	DisplayMessage.display_alert_message("Recepie Saved", "Notice")
	
	recepie_saved.emit()
	
	
	


func _on_recepie_saved():
	var container = $Panel/ScrollContainer/RecepiesContainer.get_children()
	if container:
		for child in container:
			child.queue_free()
			
	var container2 = $Panel/VBoxContainer.get_children()
	
	if container2:
		for child in container2:
			child.queue_free()
	
	ingredients_for_recepie.clear()
	
	load_recepies()
	
func load_recepies():
	recepie_list.clear()
	var dir = DirAccess.open("user://")
	
	if not dir.dir_exists("recepies"):
		dir.make_dir("recepies")
		
	dir.change_dir("recepies")
	
	dir.list_dir_begin()
	
	var file = dir.get_next()
	print(file, "file")
	while file != "":
		
		var save_file = FileAccess.open("user://recepies/" + file, FileAccess.READ)
		var json_string = save_file.get_as_text()
		
		save_file.close()
		
		var save_data = JSON.parse_string(json_string)
		
		if save_data == null:
			DisplayMessage.display_alert_message("error getting save file")
			return
			
		recepie_list.append(save_data)
		
		file = dir.get_next()
	
	fill_container(recepie_list)
	

func fill_container(list):
	var container = $Panel/ScrollContainer/RecepiesContainer.get_children()
	
	if container:
		for child in container:
			child.queue_free()
	
	for item in list:
		
		var hbox = HBoxContainer.new()
		hbox.add_to_group("item_list")
		hbox.add_theme_constant_override("separation", 15)
		
		
		var vbox_label = VBoxContainer.new()
		var vbox_value = VBoxContainer.new()
		
		var delete_button = Button.new()
		
		
		
		var name_label = Label.new()
		var name_value = Label.new()
		
		var price_label = Label.new()
		var price_value = Label.new()
		
		var amount_label = Label.new()
		var amount_value = Label.new()
		
		var recepies_label = Label.new()
		var recepies_value= Label.new()
		
		delete_button.text = "Delete"
		delete_button.pressed.connect(_on_delete_button_pressed.bind(item["name"]))
		
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
		name_value.text = item["name"].capitalize()
		
		recepies_label.text = "Ingredients"
		recepies_value.text = ""
		for ing in item["ingredients"]:
			recepies_value.text += ing.capitalize() + ", "
		recepies_value.text = recepies_value.text.trim_suffix(", ")
		
		
		amount_label.text = "oz"
		amount_value.text = str(item["amount"])
		
		price_label.text = "Price"
		price_value.text = "$" + str(item["cost"])
		
		vbox_label.add_child(name_label)
		vbox_label.add_child(recepies_label)
		vbox_label.add_child(amount_label)
		vbox_label.add_child(price_label)
		vbox_label.add_child(delete_button)
		
		
		vbox_value.add_child(name_value)
		vbox_value.add_child(recepies_value)
		vbox_value.add_child(amount_value)
		vbox_value.add_child(price_value)
		
		
		
		hbox.add_child(vbox_label)
		hbox.add_child(vbox_value)
		
		$Panel/ScrollContainer/RecepiesContainer.add_child(hbox)
		
		



	
func _on_delete_button_pressed(name):
	var dir = DirAccess.open("user://recepies/")
	
	dir.list_dir_begin()
	
	var file = dir.get_next()
	
	while file != "":
		if file == name + ".save":
			
			var err = dir.remove(file)
			if err == OK:
				DisplayMessage.display_alert_message("Recepie Deleted", "Notice")
			else:
				DisplayMessage.display_alert_message("Failed to Delelte Recepie", err)
			break
		file = dir.get_next()
	
	load_recepies()
	fill_container(recepie_list)
