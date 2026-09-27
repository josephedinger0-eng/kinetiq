import os
import requests
from dotenv import load_dotenv
from models.food import Food

load_dotenv()

API_KEY = os.getenv("USDA_API_KEY")

BASE_URL = "https://api.nal.usda.gov/fdc/v1"

# Search the USDA API for query
def search_foods(query):
    url = f"{BASE_URL}/foods/search"

    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 10
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()

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

    conversion_factor = 100 / data["servingSize"]

    name = data["description"]

    kcal = None
    pro = None
    fat = None
    carb = None

    for nutrient in data["foodNutrients"]:
        if nutrient["nutrientId"] == 1008:
            kcal = nutrient["value"]
        elif nutrient["nutrientId"] == 1003:
            pro = nutrient["value"]
        elif nutrient["nutrientId"] == 1004:
            fat = nutrient["value"]
        elif nutrient["nutrientId"] == 1005:
            carb = nutrient["value"]

    kcal *= conversion_factor
    pro *= conversion_factor
    fat *= conversion_factor
    carb *= conversion_factor
    return Food(name, kcal, pro, carb, fat)