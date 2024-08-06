class_name Ingredient

var name: String
var price: float
var original_amount: float
var current_amount: float


func _init(name: String, price: float, original_amount: float):
	self.name = name
	self.price = price
	self.original_amount = original_amount
	self.current_amount = original_amount
