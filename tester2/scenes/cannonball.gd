extends Area2D

var player: CharacterBody2D
var speed : float = .5
var player_loaded: bool = false
var player_direction: Vector2
var attack_damage: float = 50.0
var stun_time: float = 2
var knockback: float = 100


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	
	player = get_tree().get_first_node_in_group("player")
	if player:
		player_direction = player.global_position - global_position
		

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:

	if player != null:
		position += (player_direction * delta) * Vector2(speed, speed)


func _on_body_entered(body: Node2D) -> void:
	if body.name == "Character":
		var attack1 = Attack.new()
		attack1.attack_damage = attack_damage
		attack1.stun_time = stun_time
		attack1.knock_back = knockback
		attack1.attacker = self
		attack1.attacked_enemy = body
		var hitbox = body.get_node("HitboxComponent")
		hitbox.damage(attack1)
		queue_free()


func _on_timer_timeout() -> void:
	get_parent().remove_child(self)
	queue_free()

func on_save_game(save_data:Array[SavedData]):
	var data = CannonBallSavedData.new()
	
	data.position = global_position
	data.scene_path = scene_file_path
	data.direction = player_direction

	
	
	save_data.append(data)
	
func on_before_load_game():
	get_parent().remove_child(self)
	queue_free()
	
func on_load_game(data):
	var my_data:CannonBallSavedData = data as CannonBallSavedData
	global_position = my_data.position
	player_direction = my_data.direction
	
	
