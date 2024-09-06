extends Node2D


class_name RechargeComponent

@export var wait_time: float
@export var user: Node2D

func _ready() -> void:
	$Timer.wait_time = wait_time
	


func _on_timer_timeout() -> void:
	user.charging = false
	
