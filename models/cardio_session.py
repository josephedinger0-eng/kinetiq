# Define the cardio class
class CardioSession:
    # Basic constructor for a cardio session
    def __init__(self, name, distance, duration, id = None):
        self.name = name
        self.distance = distance
        self.duration = duration
        self.id = id

    