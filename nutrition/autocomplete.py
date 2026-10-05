from nutrition.food_database import FOODS

# Autocomplete a query
def autocomplete(query, limit=15):
    query = query.lower().strip()

    if not query:
        return []

    matches = []

    for fdc_id, food in FOODS.items():

        description = food["description"]

        if not description.lower().startswith(query):
            continue

        matches.append({
            "fdc_id": fdc_id,
            "description": description
        })

        if len(matches) == limit:
            break

    return matches