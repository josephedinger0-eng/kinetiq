import sqlite3 # Import SQLite
from models.food import Food

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

connection.close()