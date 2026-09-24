import sqlite3 # Import SQLite
from models.food import Food
from models.meal import Meal


connection = sqlite3.connect("kinetiq.db") # Conenct SQLite to the database

# Create the foods table with values (columns) if it doesn't exist already
connection.execute("""
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        kcal REAL NOT NULL,
        protein REAL NOT NULL,
        carbs REAL NOT NULL,
        fat REAL NOT NULL    
    )
""")

connection.commit()

# Save a food object into the foods database
def save_food(food):
    connection.execute("""
        INSERT INTO foods (name, kcal, protein, carbs, fat)
        VALUES (?,?,?,?,?)
    """, (food.name, food.kcal, food.pro, food.carb, food.fat))

    connection.commit()

# Load a food from the database
def get_foods():
    cursor = connection.execute("SELECT * FROM foods")
    rows = cursor.fetchall()

    foods = []

    for row in rows:
        food = Food(row[1], row[2], row[3], row[4], row[5])
        foods.append(food)

    return foods


# Create the meals table 
connection.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL    
    )
""")

# Create the meal_foods table 
connection.execute("""
    CREATE TABLE IF NOT EXISTS meal_foods (
        meal_id INTEGER NOT NULL,
        food_id INTEGER NOT NULL,
        quantity REAL NOT NULL   
    )
""")

connection.commit()

def save_meal(meal):
    cursor = connection.execute("""
        INSERT INTO meals (name)
        VALUES (?)
    """, (meal.name,))

    meal_id = cursor.lastrowid

    for entry in meal.entries:
        connection.execute("""
            INSERT INTO meal_foods (meal_id, food_id, quantity)
            VALUES(?,?,?)
        """, (meal_id, entry.food.id, entry.quantity))

    connection.commit()

def get_meal(meal_id):
    cursor = connection.execute("""
        SELECT name
        FROM meals
        WHERE id = ?
    """, (meal_id,))

    row = cursor.fetchone()
    meal = Meal(row[0])

    cursor = connection.execute("""
            SELECT food_id, quantity
            FROM meal_foods
            WHERE meal_id = ?
        """, (meal_id,))

    row = cursor.fetchall()

    for food_entry in row:
        food_id = food_entry[0]
        quantity = food_entry[1]

        cursor = connection.execute("""
                    SELECT *
                    FROM foods
                    WHERE id = ?
                """, (food_id,))

        food_row = cursor.fetchone()

        food = Food(food_row[1], food_row[2], food_row[3], food_row[4], food_row[5], food_row[0])

        meal.add_food(food, quantity)
        

    return meal
