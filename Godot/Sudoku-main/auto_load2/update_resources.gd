extends Node


func update_ingredient_amount(name: String, amount: float):
	var dir = DirAccess.open("user://ingredients/")
	
	dir.list_dir_begin()
	
	var file = dir.get_next()
	
	while file != "":
		
		if file == name + ".save":
			
			var save_file = FileAccess.open("user://ingredients/" + file, FileAccess.READ_WRITE)
			var json_string = save_file.get_as_text()
			
			var save_data = JSON.parse_string(json_string)
			
			if save_data == null:
				DisplayMessage.display_alert_message("Error updating ingredient",)
				return
			
			var float_amount = float(save_data["current_amount"])
			
			float_amount -= amount
			
			save_data["current_amount"] = str(float_amount)
			
			save_file.store_string(JSON.stringify(save_data))
			
			save_file.close()
			
			DisplayMessage.display_alert_message("Ingredient Updated Successfully", "Notice")
			
			
			
			return
		file = dir.get_next()
			
		
			
