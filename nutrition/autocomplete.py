import csv
import re

FOODS_FILE = "data/food.csv"
NUTRIENTS_FILE = "data/food_nutrient.csv"
FOUNDATION_FILE = "data/foundation_food.csv"

REQUIRED_NUTRIENTS = {
    1003,  # Protein
    1004,  # Total lipid (fat)
    1005,  # Carbohydrate
    1008,  # Energy
    2047,  # Energy, Atwater general factors
    2048   # Energy, Atwater specific factors
}

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

    print("Foundation foods:", len(foundation_ids))
    print("Complete Foundation foods:", len(valid_foods))

    return valid_foods

VALID_FOOD_IDS = get_valid_food_ids()

# Autocomplete a query
def autocomplete(query, limit=15):
    query = query.lower().strip()

    if not query:
        return []

    matches = []
    seen = set()

    with open(FOODS_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if row["fdc_id"] not in VALID_FOOD_IDS:
                continue

            description = row["description"]
            name = re.sub(r"\s+", " ", description).strip().lower()

            if not name.startswith(query):
                continue

            if name in seen:
                continue

            seen.add(name)

            matches.append({
                "fdc_id": row["fdc_id"],
                "description": description
            })

            if len(matches) == limit:
                break

    return matches