from flask import Flask, render_template
from database.database import get_connection, get_day, get_days

app = Flask(__name__)

# Display recent days on the home page
@app.route("/")
def home():
    days = get_days()
    return render_template("index.html", days=days)

# Display a day at day_id
@app.route("/day/<int:day_id>")
def day_page(day_id):
    connection = get_connection()
    day = get_day(connection, day_id)
    connection.close()

    return render_template("home.html", day=day)

# Display the about section
@app.route("/about")
def about():
    return "Kinetiq is a personal nutrition and training analytics platform."

if __name__ == "__main__":
    app.run(debug = True)

