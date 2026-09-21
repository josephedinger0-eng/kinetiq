# Define the workout class
class Workout:
    # Basic constructor for a workout
    def __init__(self, name):
        self.name = name
        self.exercises = []

    # Add an exercise to a workout
    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    # Summarize each exercise in a workout
    def workout_summary(self):
        print(self.name)
        print("=================")
        
        for exercise in self.exercises:
            print(exercise)