import csv

FOODS_FILE = "data/kinetiq_foods.csv"

def load_foods():
    foods = {}

    with open(FOODS_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            fdc_id = row["fdc_id"]

            foods[fdc_id] = {
                "description": row["description"],
                "kcal": float(row["kcal"]),
                "protein": float(row["pro"]),
                "carbs": float(row["carb"]),
                "fat": float(row["fat"])
            }

    return foods


FOODS = load_foods()