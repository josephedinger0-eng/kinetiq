from flask import Flask, render_template, request, redirect, url_for, jsonify
from database.database import *
from models.day import Day
from models.meal import Meal
from models.workout import Workout
from models.exercise import Exercise
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

    try:
        day = get_day(connection, day_id)
        print("Day:", day.id)
        print("Workouts:", day.workouts)
        templates = get_workout_templates(connection)
    finally:
        connection.close()

    return render_template("home.html", day=day, templates=templates)

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

# Update existing workouts
@app.route("/workout/<int:workout_id>/update", methods=["POST"])
def update_workout(workout_id):
    connection = get_connection()

    try:
        set_ids = request.form.getlist("set_id")

        for set_id in set_ids:
            reps = request.form.get(f"reps_{set_id}")
            weight = request.form.get(f"weight_{set_id}")

            connection.execute("""
                UPDATE sets
                SET reps = ?, weight = ?
                WHERE id = ?
            """, (reps, weight, set_id))

            connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally: 
        cursor = connection.execute("""
            SELECT day_id
            FROM day_workouts
            WHERE workout_id = ?
        """, (workout_id,))

        day_id = cursor.fetchone()[0]
        connection.close()

    return redirect(url_for("day_page", day_id=day_id))

# Create a workout from a template and add it to a day
@app.route("/day/<int:day_id>/workout/new", methods=["POST"])
def new_workout(day_id):
    try:
        template_id = int(request.form["template_id"])
        if template_id <= 0:
            raise ValueError
    except (ValueError, KeyError):
        return "Please select a valid workout template.", 400

    connection = get_connection()

    try:
        # Confirm that the day exists
        day_row = connection.execute(
            "SELECT id FROM days WHERE id = ?",
            (day_id,)
        ).fetchone()

        if day_row is None:
            return "Day not found.", 404

        # Load the selected template
        workout = get_workout_template(connection, template_id)

        if workout is None:
            return "Workout template not found.", 404

        # Save the workout
        cursor = connection.execute(
            "INSERT INTO workouts (name) VALUES (?)",
            (workout.name,)
        )
        workout_id = cursor.lastrowid

        # Save its exercises and sets
        for exercise in workout.exercises:
            cursor = connection.execute(
                "INSERT INTO exercises (name, workout_id) VALUES (?, ?)",
                (exercise.name, workout_id)
            )
            exercise_id = cursor.lastrowid

            for reps, weight in exercise.sets:
                connection.execute(
                    """INSERT INTO sets (exercise_id, reps, weight)
                       VALUES (?, ?, ?)""",
                    (exercise_id, reps, weight)
                )

        # Link the workout to the selected day
        connection.execute(
            """INSERT INTO day_workouts (day_id, workout_id)
               VALUES (?, ?)""",
            (day_id, workout_id)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("day_page", day_id=day_id))


# Show created workout templates
@app.route("/workout-templates")
def workout_templates_page():
    connection = get_connection()
    try:
        templates = get_workout_templates(connection)
    finally:
        connection.close()
    return render_template("workout_templates.html", templates=templates)

# Display a workout_template
@app.route("/workout-templates/<int:template_id>")
def view_workout_templates(template_id):
    connection = get_connection()
    workout = get_workout_template(connection, template_id)

    if workout is None:
        return "Workout template not found", 404
    
    connection.close()
    return render_template("workout_template_detail.html", workout=workout, template_id=template_id)

# Create a new workout template
@app.route("/workout-templates/new", methods=["GET", "POST"])
def new_workout_template():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        exercise_names = request.form.getlist("exercise_name")

        if not name:
            return "Please enter a workout name.", 400

        if not exercise_names or any(not n.strip() for n in exercise_names):
            return "Every exercise needs a name.", 400

        workout = Workout(name)

        try:
            for i, exercise_name in enumerate(exercise_names):
                exercise = Exercise(exercise_name.strip())

                reps_values = request.form.getlist(f"reps_{i}")
                weight_values = request.form.getlist(f"weight_{i}")

                if not reps_values or len(reps_values) != len(weight_values):
                    return f"Invalid sets for {exercise_name}", 400

                for reps_text, weight_text in zip(reps_values, weight_values):
                    reps = int(reps_text)
                    weight = float(weight_text)

                    if reps <=0 or weight < 0 or weight == float("inf"):
                        raise ValueError

                    exercise.add_set(reps, weight)

                workout.add_exercise(exercise)

        except (ValueError, TypeError):
            return "Enter positive whole-number reps and a nonnegative weight."

        save_workout_template(workout)
        return redirect(url_for("workout_templates_page"))

    return render_template("new_workout_template.html")

@app.route("/exercise/<int:exercise_id>/add-set", methods=["POST"])
def add_set(exercise_id):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT workout_id
            FROM exercises
            WHERE id = ?
        """, (exercise_id,))

        row = cursor.fetchone()

        if row is None:
            return "Exercise not found", 404

        workout_id = row[0]

        cursor = connection.execute("""
            SELECT day_id
            FROM day_workouts
            WHERE workout_id = ?
        """, (workout_id,))

        row = cursor.fetchone()

        if row is None:
            return "Workout not associated with a day", 404

        day_id = row[0]

        add_set_to_exercise(connection, exercise_id)

    finally:
        connection.close()

    return redirect(url_for("day_page", day_id=day_id))

# Display the about section
@app.route("/about")
def about():
    return "Kinetiq is a personal nutrition and training analytics platform."

if __name__ == "__main__":
    app.run(debug = True)

