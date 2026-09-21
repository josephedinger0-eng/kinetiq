# Define the Day class
class Day:
    # Basic constructor for a day
    def __init__(self, date):
        self.date = date
        self.meals = []
        self.workouts = []

    # Method to add a meal to the day
    def add_meal(self, meal):
        self.meals.append(meal)

    # Method to add a workout to the day
    def add_workout(self, workout):
        self.workouts.append(workout)

    # Sum the information from each meal throughout the day
    def get_meal_totals(self):
        totals = {"kcal": 0, "pro": 0, "carb": 0, "fat": 0}

        for meal in self.meals:
            meal_totals = meal.get_meal_totals()
            for key in meal_totals:
                totals[key] += meal_totals[key]

        return totals        

    # Sum the volume of all workouts in a day
    def get_workout_volume(self):
        total = 0
        for workout in self.workouts:
            total += workout.get_volume()

        return total


    # Print the information for a date
    def display_date(self):
        print(f"Date: {self.date}\n========================\n")

        print("NUTRITION\n")
        for meal in self.meals:
            print(f"\n{meal.name}:\n")
            meal.display_foods()

        print("TRAINING\n")
        for workout in self.workouts:
            workout.workout_summary()
        
