import math

def pricer(item, used):
    percentage = round(used / item.original_amount, 2)

    
    print(f"using {round(percentage * 100, 2)}% of {item.original_amount} original ounces, which is a cost of ${round(item.price * percentage, 2)}")

    return round(item.price * percentage, 2)

def loss_finder(recepi):
    total_loss = 0

    for item,value in recepi.items():
        total_loss += pricer(item, value)

    
    
    return total_loss



def recepi(items):
    recepi_dict = {}
    for item in items:
        print(f"how many ounces of {item.name} do you need? {item.current_amount} available ")

        value = float(input(""))

        while not isinstance(value, float) or 0 >= value > item.current_amount:
            print("enter valid value: ")

            value = float("")
        
        recepi_dict[item] = value

    return recepi_dict

        

class Item:
    def __init__(self, name, amount, price, unit):
        self.name = name
        self.price = price
        if unit == "g":
            amount = round(amount / 28.3495, 2)
        self.unit = unit 
        self.original_amount = amount
        self._current_amount = amount

    @property
    def current_amount(self):
        return self._current_amount
    
    @current_amount.setter
    def current_amount(self, value):
        if value < 0:
            raise ValueError("Current amount cannot be negative")
        
        self._current_amount = value

    
    def use_amount(self, amount):
        if amount > self._current_amount:
            raise ValueError("Not enough product")
        self._current_amount -= amount
        

    
    def __str__(self):
        return f"{self}"


SOAP = Item("soap",40, 6.89, "oz")
OIL = Item("oil",100, 9.56, "oz")
GEL = Item("gel",76, 15.13, "oz")
RICE = Item("rice", 45, 12, "g")


items = [SOAP, OIL, GEL, RICE]

print(f"${loss_finder(recepi(items))}")



