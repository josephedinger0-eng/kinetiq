# Define the Food class
class Food:
    # Basic constructor for a Food
    def __init__(self, name, kcal, pro, carb, fat, id = None):
        self.name = name
        self.kcal = kcal
        self.pro = pro
        self.carb = carb
        self.fat = fat
        self.id = id

    # Calculate the nutrients of food in amount quantity
    def get_nutrition(self, quantity):
        multiplier = quantity / 100
        return {"kcal": self.kcal * multiplier,
                "pro": self.pro * multiplier,
                "carb": self.carb * multiplier,
                "fat": self.fat * multiplier
        }

    # str method to return the qualities of a food
    def __str__(self):
        return (f"{self.name}\n"
                f"Calories: {self.kcal}\n"
                f"Protein: {self.pro}g\n"
                f"Carbohydrates: {self.carb}g\n"
                f"Fat: {self.fat}g"
        )