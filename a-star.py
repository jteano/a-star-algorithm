import sys
import math
import re

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
# city_1 is the departing city. city_2 is the arriving city
def optimal_route_finder(city_1, city_2):
    print(sys.argv[1])
        
# Function to compute the straight line distance using the Haversine formula
# city_1 is the origin, city_2 is the destination
def straight_line_distance(city_1, city_2):
    # Radius of the earth
    radius = 3958.8
    distance = 2 * radius * math.asin(math.sqrt((math.sin((city_2.latitude - city_1.latitude) / 2) ** 2) + math.cos(city_1.latitude) * math.cos(city_2.latitude) * math.sin((city_2.longitude - city_1.longitude) / 2) ** 2))
    return distance

# Function to convert degrees to radians
def degrees_to_radians(degrees):
    return math.radians(degrees)

# Function to parse coordinates.txt to create the city object with their respective latitude and longitude
# Return City object with information from coordinates.txt
def find_city_data(city_name):
    with open('coordinates.txt', 'r') as city_data:
        contents = city_data.readlines()
        # Find matching city name, longitude and latitude from each line using regex and return as a new city object
        for city_line in contents:
            line = re.search(r"([a-zA-Z]*)\:\(([0-9]*[.][0-9]*)\,([-][0-9]*[.][0-9]*)", city_line)
            if(city_name == line.group(1)):
                city_object = City(line.group(1), float(line.group(2)), float(line.group(3)))
    return city_object

# Function to parse map.txt and get information of adjacent cities
# Return a list of tuples that contain the adjacent cities
def find_adjacent_cities(city_name):
    with open('map.txt', 'r') as adjacent_data:
        contents = adjacent_data.readlines()
        # Find adjacent cities from each line using regex and return as a list of tuples
        for adjacent_line in contents:
            origin_city = re.findall(r"([\w]+)\-", adjacent_line)

            # Find all matches
            adjacent_cities = re.findall(r"([\w]+)\(([\d]*\.?[\d]*)\)", adjacent_line)

            # Convert all tuples to list in order to be able to change the data type of distance to float
            adjacent_cities = [list(city) for city in adjacent_cities]

            if(city_name == origin_city[0]):
                # Convert the distance between cities to float
                for city_data in adjacent_cities:
                    city_data[1] = float(city_data[1])
                return adjacent_cities



LongBeach = City("LongBeach", 33.77162218, -118.1838742)
SanJose = City("SanJose", 37.38305013, -121.8734782)

LongBeach.add_adjacent_city("LosAngeles", 24.1)

print(find_adjacent_cities(LongBeach.name))