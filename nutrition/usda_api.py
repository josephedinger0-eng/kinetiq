import os
import requests
from dotenv import load_dotenv
from models.food import Food
from nutrition.food_database import FOODS

load_dotenv()

API_KEY = os.getenv("USDA_API_KEY")

BASE_URL = "https://api.nal.usda.gov/fdc/v1"

FOODS_FILE = "data/food.csv"
NUTRIENTS_FILE = "data/food_nutrient.csv"

ENERGY_IDS = {1008, 2047, 2048}

# Search the USDA API for query
def search_foods(query):
    url = f"{BASE_URL}/foods/search"

    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 100
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    for food in data.get("foods", []):
        print(
            food["description"],
            "|",
            food.get("dataType")
        )

    return data

# Return the details of a food at fdc_id
def get_food_details(fdc_id):
    url = f"{BASE_URL}/food/{fdc_id}"

    params = {
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()

# Translate USDA json object into necessary info
def create_food_from_usda(fdc_id):
    data = get_food_details(fdc_id)

    name = data["description"]

    kcal = None
    pro = None
    fat = None
    carb = None

    for nutrient in data["foodNutrients"]:
        nutrient_info = nutrient.get("nutrient", {})
        nutrient_id = nutrient_info.get("id")
        value = nutrient.get("value")

        if value is None:
            continue

        if nutrient_id == 1008:
            kcal = value
        elif nutrient_id == 1003:
            pro = value
        elif nutrient_id == 1004:
            fat = value
        elif nutrient_id == 1005:
            carb = value

    required_nutrients = {
        "kcal": kcal,
        "protein": pro,
        "fat": fat,
        "carbs": carb
    }

    for nutrient_name, value in required_nutrients.items():
        if value is None:
            raise ValueError(
                f"USDA food is missing required nutrient: {nutrient_name}"
            )
    
    return Food(name, kcal, pro, carb, fat, fdc_id)

# Create a food object from local data
def create_food_from_local_data(fdc_id):
    fdc_id = str(fdc_id)

    if fdc_id not in FOODS:
        raise ValueError(f"Food {fdc_id} was not found.")

    food_data = FOODS[fdc_id]

    return Food(
        food_data["description"],
        food_data["kcal"],
        food_data["protein"],
        food_data["carbs"],
        food_data["fat"],
        fdc_id
    )

# Rerank results by our relevance
def score_food(food, query):
    name = food["description"].lower().strip()
    query = query.lower().strip()

    if not query:
        return 0

    # Exact match
    if name == query:
        return 1000

    # Food name starts with the query
    if name.startswith(query):
        return 900

    # A word in the name starts with the query
    words = name.replace(",", " ").split()

    for word in words:
        if word.startswith(query):
            return 700

    # Query appears somewhere inside the name
    if query in name:
        return 300

    return 0