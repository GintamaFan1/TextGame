extends Node


func _on_timer_timeout(node, timer):
	node.queue_free()
	timer.queue_free()
	
func display_alert_message(message: String, type="error"):
	var alert_message = AcceptDialog.new()
	var timer = Timer.new()
	
	alert_message.theme = load("res://Themes/Universal_label_theme/new_theme.tres")
	alert_message.title = type
	alert_message.add_theme_font_size_override("font_size", 30)
	alert_message.show()
	alert_message.size = Vector2(100,100)
	
	
	
	alert_message.position = Vector2(400,400)
	
	alert_message.grab_focus()
	alert_message.dialog_text = message
	
	add_child(alert_message)
	add_child(timer)
	
	
	timer.wait_time = 5
	timer.start()
	timer.timeout.connect(_on_timer_timeout.bind(alert_message, timer))
