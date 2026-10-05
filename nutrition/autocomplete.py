import csv
import re
from nutrition.food_database import VALID_FOOD_IDS, FOODS

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

# Autocomplete a query
def autocomplete(query, limit=15):
    query = query.lower().strip()

    if not query:
        return []

    matches = []
    seen = set()

    for fdc_id, food in FOODS.items():

        description = food["description"]
        name = re.sub(r"\s+", " ", description).strip().lower()

        if not name.startswith(query):
            continue

        if name in seen:
            continue

        seen.add(name)

        matches.append({
            "fdc_id": fdc_id,
            "description": description
        })

        if len(matches) == limit:
            break

    return matches