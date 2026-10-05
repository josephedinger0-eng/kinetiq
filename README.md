# Kinetiq

**Personal nutrition and training analytics platform built with Python.**

Kinetiq is a web-based application for organizing nutrition and training data in one place. The project is being developed as a long-term Python software project, with an emphasis on data modeling, persistence, external data integration, and analytics.

## Current Features

### Nutrition

* Create and store foods with nutritional information
* Search for foods using autocomplete
* Import validated food data from the USDA FoodData Central Foundation Foods dataset
* Add foods to meals with a specified quantity
* Calculate meal nutrition totals
* Track calories, protein, carbohydrates, and fat

### Training

* Create workouts
* Add exercises to workouts
* Record sets, repetitions, and weight
* Calculate training volume
* Record cardio sessions with distance and duration

### Daily Tracking

* Organize meals, workouts, and cardio sessions by date
* View the nutrition and training information associated with a day
* Persist data using SQLite

### USDA Food Data Integration

Kinetiq uses USDA FoodData Central data to provide a searchable food database.

The USDA dataset is processed before being used by the application:

```text
USDA Foundation Food Dataset
            ↓
     process_usda.py
            ↓
  Validated food dataset
            ↓
    kinetiq_foods.csv
            ↓
     In-memory database
            ↓
Autocomplete + Food Creation
```

Only Foundation Foods containing the required macronutrient and energy data are included in the processed dataset.

The preprocessing step currently produces approximately 322 complete Foundation Foods.

## Technology Stack

* **Python** — application logic and data processing
* **Flask** — web application framework
* **SQLite** — persistent relational database
* **HTML / CSS / JavaScript** — web interface
* **USDA FoodData Central** — food and nutrition data
* **Requests** — USDA API communication
* **python-dotenv** — environment variable management

## Project Structure

```text
kinetiq/
├── database/
│   └── database.py
├── models/
│   ├── food.py
│   ├── food_entry.py
│   ├── meal.py
│   ├── day.py
│   ├── workout.py
│   ├── exercise.py
│   └── cardio_session.py
├── nutrition/
│   ├── autocomplete.py
│   ├── food_database.py
│   ├── process_usda.py
│   └── usda_api.py
├── static/
│   └── style.css
├── templates/
│   └── ...
├── data/
│   └── kinetiq_foods.csv
├── app.py
├── .gitignore
```
