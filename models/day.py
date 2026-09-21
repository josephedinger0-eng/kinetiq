# Define the Day class
class Day:
    # Basic constructor for a day
    def __init__(self, date):
        self.date = date
        self.meals = []

    # Method to add a meal to the day
    def add_meal(self, meal):
        self.meals.append(meal)

    # Sum the information from each meal throughout the day
    def get_totals(self):
        totals = {"kcal": 0, "pro": 0, "carb": 0, "fat": 0}

        for meal in self.meals:
            meal_totals = meal.get_meal_totals()
            for key in meal_totals:
                totals[key] += meal_totals[key]

        return totals

    # Print the information for a date
    def display_date(self):
        print(f"Date: {self.date}")

        for meal in self.meals:
            print(f"\n{meal.name}")
            meal.display_foods()
        
