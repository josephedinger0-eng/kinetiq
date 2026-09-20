# Define the Meal class
class Meal:
    # Basic constructor for a Meal
    def __init__(self, name):
        self.name = name
        self.entries = {}

    # Adds a food (key) to entries with a quantity (value)
    def addFodd(self, food, quantity):
        self.entries[food] = quantity

    # Prints each food in a meal
    def display_foods(self):
        for food, quantity in self.entries.items():
            print(food)
            print(f"Amount: {quantity}g")
            print("-----------------")