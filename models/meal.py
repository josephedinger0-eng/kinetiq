from models.food_entry import FoodEntry

# Define the Meal class
class Meal:
    # Basic constructor for a Meal
    def __init__(self, name):
        self.name = name
        self.entries = []

    # Adds a food (key) to entries with a quantity (value)
    def add_food(self, food, quantity):
        self.entries.append(FoodEntry(food, quantity))

    # Prints each food in a meal
    def display_foods(self):
        for entry in self.entries:
            food_values = entry.food.get_nutrition(entry.quantity)

            print(entry.food.name)
            print(f"Amount: {entry.quantity}g")
            print(f"Calories: {food_values['kcal']}")
            print(f"Protein: {food_values['pro']}g")
            print(f"Carbohydrates: {food_values['carb']}g")
            print(f"Fat: {food_values['fat']}g")
            print("-----------------")

    # Sum the information about each food in the meal
    def get_meal_totals(self):
        totals = {"kcal": 0, "pro": 0, "carb": 0, "fat": 0}

        for entry in self.entries:
            food_values = entry.food.get_nutrition(entry.quantity)
            for key in food_values:
                totals[key] += food_values[key]

        return totals