extends Control

var words: Array = []
var word: String 
var mistakes: int = 6
# Called when the node enters the scene tree for the first time.
func _ready():
	var word_data = FileAccess.open("res://Words/words.txt", FileAccess.READ)
	var word_content = word_data.get_as_text()
	word_data.close()
	
	words = word_content.split("\n")
	
	pick_word()
	set_word()
	$VBoxContainer/TriesLabel.text = str(mistakes) + " tries left"
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func pick_word():
	var random_index = randi() % words.size()
	word = words[random_index]
	
func set_word():
	for letter in word:
		set_letter(letter)
		
func set_letter(letter):
	var vbox = VBoxContainer.new()
	var line_label = Label.new()
	var label = Label.new()
	
	vbox.add_to_group("letter_holder")
	label.add_to_group(letter)
	label.text = letter
	var label_setting = preload("res://Themes/labels.tres")
	label.theme = label_setting
	label.hide()
	
	line_label.text = "_____"
	
	vbox.add_child(label)
	vbox.add_child(line_label)
	
	$WordContainer.add_child(vbox)
	



func _on_guess_button_pressed():
	var text = $VBoxContainer2/LineEdit.text.to_lower()
	
	if text not in "abcdefghijklmnopqrstuvwxyz ":
		$VBoxContainer2/LineEdit.clear()
		DisplayMessage.display_alert_message("Invalid guess, try again")
		return
		
	else:
		if text not in word:
			mistakes -= 1
			
			if mistakes == 5:
				$ManContainer/HeadTexture.show()
			elif mistakes == 4:
				$ManContainer/BodyMesh.show()
			elif mistakes == 3:
				$ManContainer/ArmMesh.show()
			elif mistakes == 2:
				$ManContainer/ArmMesh2.show()
			elif mistakes == 1:
				$ManContainer/LegMesh.show()
			elif mistakes == 0:
				$ManContainer/LegMesh2.show()
			
			if mistakes == 0:
				DisplayMessage.display_alert_message("Game Over, You did not Guess The Word", "Notice")
				$VBoxContainer/TriesLabel.text = str(mistakes) + " tries left"
				for char in word:
					var char_nodes = get_tree().get_nodes_in_group(char)
					
					if char_nodes:
						for child in char_nodes:
							child.show()
				
				
			else:
				$VBoxContainer/TriesLabel.text = str(mistakes) + " tries left"
				$VBoxContainer2/LineEdit.clear()
		else:
			var letters = get_tree().get_nodes_in_group(text)
			
			if letters:
				for node in letters:
					node.show()
			$VBoxContainer2/LineEdit.clear()
			
			var all_char_solved = true
			for char in word:
				var char_nodes = get_tree().get_nodes_in_group(char)
				if char_nodes:
					for node in char_nodes:
						if node.visible == false:
							all_char_solved = false
							break
			
			if all_char_solved == true:
				DisplayMessage.display_alert_message("Congratulations, You Solved It", "Notice")
				return
					
				
		$VBoxContainer/TriedLettersLabel.text += text


func _on_restart_button_pressed():
	var children = $WordContainer.get_children()
	
	for child in children:
		child.queue_free()
	
	var container = $ManContainer.get_children()
	for child in container:
		child.hide()
		
	mistakes = 6
	$VBoxContainer/TriesLabel.text = str(mistakes) + " tries left"
	$VBoxContainer/TriedLettersLabel.text = ""
	$VBoxContainer2/LineEdit.clear()
	pick_word()
	set_word()
	
