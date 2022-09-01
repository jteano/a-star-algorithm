import math

# Class to create a city object which has name, longitude and latitude as attributes
class City:
    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude

# Function to take departing city and arriving city (as input arguments)

# Function to compute the straight line distance using the Haversine formula
# city_1 is the origin, city_2 is the destination
def straight_line_distance(city_1, city_2):
    # Radius of the earth
    r = 3958.8


# Function to convert degrees to radians
def degrees_to_radians(degrees):
    return math.radians(degrees)

# Function to parse coordinates.txt and map.txt and store in a lookup table