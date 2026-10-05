import csv

FOUNDATION_FILE = "data/foundation_food.csv"
FOODS_FILE = "data/food.csv"
NUTRIENTS_FILE = "data/food_nutrient.csv"

OUTPUT_FILE = "data/kinetiq_foods.csv"

ENERGY_IDS = {1008, 2047, 2048}

def get_foundation_ids():
    foundation_ids = set()

    with open(FOUNDATION_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            foundation_ids.add(row["fdc_id"])

    return foundation_ids

def get_food_names(foundation_ids):
    food_names = {}

    with open(FOODS_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            fdc_id = row["fdc_id"]

            if fdc_id not in foundation_ids:
                continue

            food_names[fdc_id] = row["description"]

    return food_names

def get_nutrition_data(foundation_ids):
    nutrition = {}
    
    with open(NUTRIENTS_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            fdc_id = row["fdc_id"]

            if fdc_id not in foundation_ids:
                continue

            amount = row["amount"]

            if amount == "":
                continue

            nutrient_id = int(row["nutrient_id"])
            amount = float(amount)

            if fdc_id not in nutrition:
                nutrition[fdc_id] = {}

            if nutrient_id in ENERGY_IDS and "kcal" not in nutrition[fdc_id]:
                nutrition[fdc_id]["kcal"] = amount

            elif nutrient_id == 1003:
                nutrition[fdc_id]["pro"] = amount

            elif nutrient_id == 1004:
                nutrition[fdc_id]["fat"] = amount

            elif nutrient_id == 1005:
                nutrition[fdc_id]["carb"] = amount

    return nutrition

def create_processed_foods(food_names, nutrition):
    foods = []

    for fdc_id in food_names:

        if fdc_id not in nutrition:
            continue

        food_nutrition = nutrition[fdc_id]

        required = {
            "kcal",
            "pro",
            "carb",
            "fat"
        }

        if not required.issubset(food_nutrition):
            continue

        foods.append({
            "fdc_id": fdc_id,
            "description": food_names[fdc_id],
            "kcal": food_nutrition["kcal"],
            "pro": food_nutrition["pro"],
            "carb": food_nutrition["carb"],
            "fat": food_nutrition["fat"]
        })

    return foods

def save_processed_foods(foods):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "fdc_id",
            "description",
            "kcal",
            "pro",
            "carb",
            "fat"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(foods)

foundation_ids = get_foundation_ids()

food_names = get_food_names(foundation_ids)

nutrition = get_nutrition_data(foundation_ids)

foods = create_processed_foods(food_names, nutrition)

save_processed_foods(foods)

print(f"Processed {len(foods)} foods.")