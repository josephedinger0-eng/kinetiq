# Define the exercise class
class Exercise:
    # Basic constructor for an exercise
    def __init__(self, name):
        self.name = name
        self.sets = [] # index represents set number, value represents reps

    # Add a set to the exercise
    def add_set(self, reps, weight):
        self.sets.append((reps, weight))

    # Print each set in an exercise
    def __str__(self):
        ret = self.name + "\n----------------\n"

        for i in range(len(self.sets)):
            rep_number = self.sets[i][0]
            weight_number = self.sets[i][1]
            ret += f"{i+1}: {rep_number} reps x {weight_number} lbs\n"

        return ret
