extends AudioStreamPlayer



var song1 = preload("res://Audio/Background_Music/Stream Loops 2024-04-24_01.ogg")
var song2 = preload("res://Audio/Background_Music/Stream Loops 2024-04-24_02.ogg")
var song3 = preload("res://Audio/Background_Music/Stream Loops 2024-04-24_03.ogg")
var song4 = preload("res://Audio/Background_Music/Stream Loops 2024-05-01_01.ogg")
var song5 = preload("res://Audio/Background_Music/Stream Loops 2024-05-01_02.ogg")
var song6 = preload("res://Audio/Background_Music/Stream Loops 2024-05-08.ogg")
var song7 = preload("res://Audio/Background_Music/Stream Loops 2024-05-15.ogg")
var song8 = preload("res://Audio/Background_Music/Stream Loops 2024-06-05_v02.ogg")

var song_list: Array = [song1, song2, song3, song4, song5, song6, song7, song8]
var song_dict: Dictionary = {
	"Flower Moon": song1,
	"Autum Shower": song2,
	"Crescent": song3,
	"Feel True": song4,
	"Mercy Placement": song5,
	"Jubillation": song6,
	"Candy Dropped": song7,
	"Well Of Hope": song8
}

var playback_position = null

var previous_song = []
var current_song_index = null
var loop = false

func _ready():
	add_to_group("music_player")
	var volume_slider = get_tree().get_first_node_in_group("volume_slider")
	finished.connect(_on_song_finsihed)
	if volume_slider:
		set_volume(volume_slider.value)
	stream = begin_music()
	play()
	
func toggle_music():
	if playing:
		playback_position = get_playback_position()
		stop()
	else:
		if playback_position == null:
			play()
		else:
			seek(playback_position)
			play()
			
		
		
func set_volume(value):
	
	volume_db = linear_to_db(value)
func get_random_song():
	
	playback_position = null
	var random_index = randi() % song_list.size()
	current_song_index = random_index
	var song = song_list[random_index]

	return song
	
func play_next():
	previous_song.append(song_list[current_song_index])
	current_song_index += 1
	stream = begin_music(current_song_index)
	play()
	
func begin_music(index=0):
	if index >= song_list.size():
		index = 0
	playback_position = null
	var song = song_list[index]
	current_song_index = index
	return song

func play_previous():
	var song = previous_song.pop_back()
	if song:
		playback_position = null
		current_song_index = song_list.find(song)
		stream = begin_music(current_song_index)
		play()
	
func _on_song_finsihed():
	if loop == false:
		play_next()
	else:
		stream = begin_music(current_song_index)
		play()
	
func shuffle():
	song_list.shuffle()
	stream = begin_music()
	play()

func show_song():
	for name1 in song_dict.keys():
		if song_dict[name1] == song_list[current_song_index]:
			return name1
			
func toggle_loop():
	if loop:
		loop = false
	else:
		loop = true
	
