# Define the Food class
class Food:
    # Basic constructor for a Food
    def __init__(self, name, kcal, pro, carb, fat, id = None, fdc_id=None):
        self.name = name
        self.kcal = kcal
        self.pro = pro
        self.carb = carb
        self.fat = fat
        self.id = id
        self.fdc_id = fdc_id

    # Calculate the nutrients of food in amount quantity
    def get_nutrition(self, quantity):
        multiplier = quantity / 100
        return {"kcal": round(self.kcal * multiplier, 2),
                "pro": round(self.pro * multiplier, 2),
                "carb": round(self.carb * multiplier, 2),
                "fat": round(self.fat * multiplier, 2)
        }

    # str method to return the qualities of a food
    def __str__(self):
        return (f"{self.name}\n"
                f"Calories: {self.kcal}\n"
                f"Protein: {self.pro}g\n"
                f"Carbohydrates: {self.carb}g\n"
                f"Fat: {self.fat}g"
        )