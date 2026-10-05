import csv

FOODS_FILE = "data/food.csv"
NUTRIENTS_FILE = "data/food_nutrient.csv"
FOUNDATION_FILE = "data/foundation_food.csv"

ENERGY_IDS = {1008, 2047, 2048}

FOODS = {}
VALID_FOOD_IDS = set()

# Returns the IDs of foods that have necessary macros and one of the possible energy forms
def get_valid_food_ids():
    foundation_ids = set()

    with open(FOUNDATION_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            foundation_ids.add(row["fdc_id"])

    nutrients_by_food = {}

    with open(NUTRIENTS_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            fdc_id = row["fdc_id"]

            if fdc_id not in foundation_ids:
                continue

            nutrient_id = int(row["nutrient_id"])

            if fdc_id not in nutrients_by_food:
                nutrients_by_food[fdc_id] = set()

            nutrients_by_food[fdc_id].add(nutrient_id)

    valid_foods = set()

    for fdc_id, nutrients in nutrients_by_food.items():

        has_energy = bool(
            nutrients & {1008, 2047, 2048}
        )

        has_macros = {
            1003,
            1004,
            1005
        }.issubset(nutrients)

        if has_energy and has_macros:
            valid_foods.add(fdc_id)

    return valid_foods

VALID_FOOD_IDS = get_valid_food_ids()

# Load every valid foundational food into a dictionary
def load_foods():
    foods = {}

    for fdc_id in VALID_FOOD_IDS:
        with open(FOODS_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                fdc_id = row["fdc_id"]

                if fdc_id not in VALID_FOOD_IDS:
                    continue

                foods[fdc_id] = {
                    "description": row["description"]
                }

    return foods

FOODS = load_foods()
    
