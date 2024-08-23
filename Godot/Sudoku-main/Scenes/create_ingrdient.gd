extends Control

signal ingredient_created()
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_enter_button_pressed():
	var name1: String = $Panel/VBoxContainer/IngrdientNameLine.text.to_lower()
	var price_text: String = $Panel/VBoxContainer/PriceLine.text
	var amount_text: String = $Panel/VBoxContainer/AmountLine.text
	
	if name1 == "" or price_text == "" or amount_text == "":
		display_alert_message("All Fields Are required to create Ingredient")
		$Panel/VBoxContainer/IngrdientNameLine.clear()
		$Panel/VBoxContainer/PriceLine.clear()
		$Panel/VBoxContainer/AmountLine.clear()
		return
	
	var price_valid: bool = price_text.is_valid_float()
	var amount_valid: bool = amount_text.is_valid_float()
	
	if not price_valid or not amount_valid:
		display_alert_message("Price or Amount has an incorrect value")
		$Panel/VBoxContainer/IngrdientNameLine.clear()
		$Panel/VBoxContainer/PriceLine.clear()
		$Panel/VBoxContainer/AmountLine.clear()
		return
	
	var price = float(price_text)
	var amount = float(amount_text)
	
	var ingredient = Ingredient.new(name1, price, amount)
	
	save_ingredient(ingredient)
	
	$Panel/VBoxContainer/IngrdientNameLine.clear()
	$Panel/VBoxContainer/PriceLine.clear()
	$Panel/VBoxContainer/AmountLine.clear()
	
	
	$".".hide()
	
	
		
		
func _on_timer_timeout(node, timer):
	node.queue_free()
	timer.queue_free()
	
func display_alert_message(message: String, type="error"):
	var alert_message = AcceptDialog.new()
	var timer = Timer.new()
	
	alert_message.title = type
	alert_message.add_theme_font_size_override("font_size", 30)
	alert_message.show()
	alert_message.size = Vector2(100,100)
	var center = $Panel/VBoxContainer/EnterButton.get_screen_position()
	alert_message.position = center
	alert_message.grab_focus()
	alert_message.dialog_text = message
	
	$Panel.add_child(alert_message)
	$".".add_child(timer)
	
	
	timer.wait_time = 5
	timer.start()
	timer.timeout.connect(_on_timer_timeout.bind(alert_message, timer))

func save_ingredient(item: Ingredient):
	var dir = DirAccess.open("user://")
	
	if not dir:
		display_alert_message("user directory does not exist")
		return
		
	if not dir.dir_exists("ingredients"):
		dir.make_dir("ingredients")
		
	dir.change_dir("ingredients")
	
	var save_data: Dictionary = {
		"name" : item.name.to_lower(),
		"price": item.price,
		"original_amount": item.original_amount,
		"current_amount": item.current_amount
	}
	
	var file_path = "user://ingredients/" + item.name + ".save"
	
	
	if FileAccess.file_exists(file_path):
		display_alert_message("That ingredient already exist, change name, update values, or delte old ingredient")
		return 
		
			
	var save_file = FileAccess.open(file_path, FileAccess.WRITE)
	save_file.store_string(JSON.stringify(save_data))
	
	save_file.close()
	display_alert_message("Ingredient Created Successfully", "Notice")
	
	emit_signal("ingredient_created")


func _on_cancel_button_pressed():
	$".".hide()
