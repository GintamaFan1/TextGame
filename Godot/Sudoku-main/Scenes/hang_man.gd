extends Control

var words: Array = []
var word: String 
# Called when the node enters the scene tree for the first time.
func _ready():
	var word_data = FileAccess.open("res://Words/words.txt", FileAccess.READ)
	var word_content = word_data.get_as_text()
	word_data.close()
	
	words = word_content.split("\n")
	
	pick_word()
	set_word()
	
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
	var label = Label.new()
	label.add_to_group("label_holder")
	label.text = letter
	var label_setting = preload("res://Themes/labels.tres")
	label.theme = label_setting
	
	
	$WordContainer.add_child(label)
	
	
	
	
	
	
	
