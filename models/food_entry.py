# Define the Food Entry class
class FoodEntry:
    # Basic constructor for a food entry
    def __init__(self, food, quantity, id=None):
        self.food = food
        self.quantity = quantity
        self.id = id

    # Get the nutritrion for a food entry
    @property
    def nutrition(self):
        return self.food.get_nutrition(self.quantity)