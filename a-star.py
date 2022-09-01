import sys
import math

# Class to create a city object which has name, longitude and latitude as attributes
# adjacent_cities is a list of tuples that contain adjacent city name and distance
class City:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = math.radians(latitude)
        self.longitude = math.radians(longitude)
        self.adjacent_cities = []

    def add_adjacent_city(self, adjacent_city_name, distance_in_miles):
        self.adjacent_cities.append((adjacent_city_name, distance_in_miles))
        
# Function to take departing city and arriving city (as input arguments)

# Function to compute the straight line distance using the Haversine formula
# city_1 is the origin, city_2 is the destination
def straight_line_distance(city_1, city_2):
    # Radius of the earth
    r = 3958.8
    d = 2 * r * math.asin(math.sqrt((math.sin((city_2.latitude - city_1.latitude) / 2) ** 2) + math.cos(city_1.latitude) * math.cos(city_2.latitude) * math.sin((city_2.longitude - city_1.longitude) / 2) ** 2))
    return d

# Function to convert degrees to radians
def degrees_to_radians(degrees):
    return math.radians(degrees)

# Function to parse coordinates.txt and map.txt


LongBeach = City("LongBeach", 33.77162218, -118.1838742)
SanJose = City("SanJose", 37.38305013, -121.8734782)

LongBeach.add_adjacent_city("LosAngeles", 24.1)

print(LongBeach.adjacent_cities)
