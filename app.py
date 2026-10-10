from flask import Flask, render_template, request, redirect, url_for, jsonify
from database.database import *
from models.day import Day
from models.meal import Meal
from datetime import date
from nutrition.usda_api import create_food_from_local_data
from nutrition.autocomplete import autocomplete

app = Flask(__name__)

# Display today on home page
@app.route("/")
def home():
    today = date.today()

    day_id = get_or_create_day(today)

    return redirect(url_for("day_page", day_id=day_id))

# Display past days
@app.route("/days")
def days():
    days = get_days()
    return render_template("index.html", days=days)


# Display the day creation page
@app.route("/day/new", methods=["GET", "POST"])
def new_day():

    if request.method == "POST":
        day_date = request.form["date"]

        day = Day(day_date)

        day.add_meal(Meal("Breakfast"))
        day.add_meal(Meal("Lunch"))
        day.add_meal(Meal("Dinner"))
        day.add_meal(Meal("Snacks"))

        day_id = save_day(day)

        return redirect(url_for("day_page",day_id=day_id))

    return render_template("new_day.html")

# Display a day at day_id
@app.route("/day/<int:day_id>")
def day_page(day_id):
    connection = get_connection()
    day = get_day(connection, day_id)
    connection.close()

    return render_template("home.html", day=day)

# Create a new meal in a day
@app.route("/day/<int:day_id>/meal/new", methods=["GET", "POST"])
def new_meal(day_id):

    if request.method == "POST":
        meal_name = request.form["name"].strip()

        if not meal_name:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Please enter a meal name."}), 400

            return redirect(url_for("new_meal", day_id=day_id))

        meal = Meal(meal_name)
        save_meal(meal, day_id)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True, "meal_id": meal.id})

        return redirect(url_for("day_page", day_id=day_id))

    return render_template("new_meal.html", day_id=day_id)

# Add a food entry to a meal
@app.route("/day/<int:day_id>/meal/<int:meal_id>/food/new", methods=["GET", "POST"])
def new_food(day_id, meal_id):

    if request.method == "POST":
        try:
            fdc_id = int(request.form["food_id"])
            quantity = float(request.form["quantity"])

            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            food = create_food_from_local_data(fdc_id)
            save_food(food)

            add_food_to_meal(meal_id, food.id, quantity)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True})

            return redirect(url_for("day_page", day_id=day_id))

        except (ValueError, KeyError):
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({
                    "error": "Choose a food and enter a valid quantity."
                }), 400

            return redirect(url_for("day_page", day_id=day_id))

    return render_template(
        "new_food.html",
        day_id=day_id,
        meal_id=meal_id
    )

# Display yesterday's information
@app.route("/day/<int:day_id>/previous")
def previous_day(day_id):
    days = get_days()

    for i, day in enumerate(days):
        if day[0] == day_id and i + 1 < len(days):
            return redirect(url_for("day_page", day_id=days[i + 1][0]))

    return redirect(url_for("day_page", day_id=day_id))

# Display tomorrow's information
@app.route("/day/<int:day_id>/next")
def next_day(day_id):
    days = get_days()

    for i, day in enumerate(days):
        if day[0] == day_id and i > 0:
            return redirect(url_for("day_page", day_id=days[i - 1][0]))

    return redirect(url_for("day_page", day_id=day_id))

# Delete a meal from a day
@app.route("/day/<int:day_id>/meal/<int:meal_id>/delete")
def delete_meal_route(day_id, meal_id):
    delete_meal(meal_id)

    return redirect(url_for("day_page", day_id=day_id))

# Delete a food_entry from a meal
@app.route("/day/<int:day_id>/meal/<int:meal_id>/food/<int:entry_id>/delete", methods=["POST"])
def delete_food(day_id, meal_id, entry_id):
    delete_food_entry(entry_id)

    return redirect(url_for("day_page", day_id=day_id))

# Edit an existing fodo_entry

@app.route(
    "/day/<int:day_id>/meal/<int:meal_id>/food/<int:entry_id>/edit",
    methods=["GET", "POST"]
)
def edit_food(day_id, meal_id, entry_id):
    if request.method == "POST":
        try:
            quantity = float(request.form["quantity"])

            if not 0 < quantity < float("inf"):
                raise ValueError

        except (ValueError, KeyError):
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({
                    "error": "Enter a valid quantity greater than zero."
                }), 400

            return "Invalid quantity. Enter a number greater than zero.", 400

        update_food_entry(entry_id, quantity)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True})

        return redirect(url_for("day_page", day_id=day_id))

    return render_template(
        "edit_food.html",
        day_id=day_id,
        meal_id=meal_id,
        entry_id=entry_id
    )

# Search Local USDA food dataset
@app.route("/api/foods/search")
def search_foods_api():
    query = request.args.get("q", "").strip()

    if len(query) < 3:
        return {"foods": []}

    results = autocomplete(query, limit=15)

    return {"foods": results}

# Display the about section
@app.route("/about")
def about():
    return "Kinetiq is a personal nutrition and training analytics platform."

if __name__ == "__main__":
    app.run(debug = True)

