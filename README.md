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
└── README.md
```

## Architecture

Kinetiq separates application responsibilities into several layers:

**Models** represent the application's core objects:

```text
Day
├── Meals
│   └── Food Entries
│       └── Food
├── Workouts
│   └── Exercises
│       └── Sets
└── Cardio Sessions
```

**Database functions** handle persistent storage in SQLite.

**Nutrition modules** handle USDA data processing, food searching, and food creation.

**Flask routes and templates** provide the web interface.

## Data Persistence

Kinetiq uses SQLite to store application data.

The database uses relational tables for foods, meals, food entries, days, workouts, exercises, sets, and cardio sessions. Foreign keys are used to connect related records.

The USDA dataset is not loaded directly every time the application starts. Instead, `process_usda.py` converts the relevant USDA data into a smaller processed dataset that Kinetiq can load efficiently.

## Development Goals

Kinetiq is being developed incrementally to expand both its functionality and software architecture.

### Implemented

* [x] Python data models
* [x] Flask web application
* [x] SQLite persistence
* [x] Nutrition tracking
* [x] Meal and food-entry system
* [x] Workout and exercise tracking
* [x] Set and training-volume tracking
* [x] Cardio tracking
* [x] USDA Foundation Food integration
* [x] Food autocomplete
* [x] USDA data preprocessing
* [x] In-memory food database

### In Development

* [ ] Improved editing and deletion workflows
* [ ] Expanded training analytics
* [ ] Expanded nutrition analytics
* [ ] Improved user interface
* [ ] Automated testing

### Planned

* [ ] Micronutrient tracking
* [ ] Historical nutrition and training analysis
* [ ] Data visualization
* [ ] Additional USDA food data
* [ ] More advanced analytics

## Project Goals

Kinetiq is also a learning project focused on building practical software with Python.

The project provides experience with:

* Object-oriented programming
* Relational database design
* SQL and foreign keys
* Flask web development
* REST API integration
* CSV data processing
* Data validation and preprocessing
* Application architecture
* Git and GitHub

## Status

**Active development**

Kinetiq currently has a functional Flask application with persistent SQLite storage, nutrition and training models, and an integrated USDA Foundation Foods database.

The project is being expanded incrementally as new features and analytics are developed.

## Author

**Joseph Edinger**

GitHub: [josephedinger0-eng](https://github.com/josephedinger0-eng)
