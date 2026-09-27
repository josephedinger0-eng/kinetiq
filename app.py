from flask import Flask, render_template, request, redirect, url_for
from database.database import *
from models.day import Day
from models.meal import Meal

app = Flask(__name__)

# Display recent days on the home page
@app.route("/")
def home():
    days = get_days()
    return render_template("index.html", days=days)

# Display the day creation page
@app.route("/day/new", methods=["GET", "POST"])
def new_day():
    if request.method == "POST":
        day_date = request.form["date"]
        day = Day(day_date)
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
@app.route("/day/<int:day_id>/meal/new", methods=["GET","POST"])
def new_meal(day_id):

    if request.method == "POST":
        meal_name = request.form["name"]
        meal = Meal(meal_name)
        save_meal(meal, day_id)

        return redirect(url_for("day_page",day_id=day_id))


    return render_template("new_meal.html",day_id=day_id)

# Add a food entry to a meal
@app.route("/day/<int:day_id>/meal/<int:meal_id>/food/new", methods=["GET", "POST"])
def new_food(day_id, meal_id):
    foods = get_foods()

    if request.method == "POST":
        food_id = request.form["food_id"]
        quantity = request.form["quantity"]

        add_food_to_meal(meal_id, food_id, quantity)

        return redirect(url_for("day_page", day_id=day_id))

    return render_template("new_food.html", day_id=day_id, meal_id=meal_id,foods=foods)

# Display the about section
@app.route("/about")
def about():
    return "Kinetiq is a personal nutrition and training analytics platform."

if __name__ == "__main__":
    app.run(debug = True)

