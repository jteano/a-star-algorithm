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
        self.adjacent_cities = find_adjacent_cities(name)
        #self.distance_to_other_cities = {}

# Function to take departing city and arriving city (as input arguments)
# city_1 is the departing city. city_2 is the arriving city
# Returns the best route as a list and total distance as a float
def optimal_route_finder(city_1, city_2):
    # Set a start and end point
    departing_city = find_city_data(city_1)
    arriving_city = find_city_data(city_2)
    current_city = departing_city
    lowest_current_cost = 0
    current_cost = 0
    lowest_cost = math.inf
    optimal_path_list = []
    test_list = []
    not_found = True

    # Starting at the departing_city, iterate through all the adjacent cities and compute for f(n)
    # Repeat this process until we reach our destination
    while not_found:
        test_list.clear()
        for adj_city in current_city.adjacent_cities:
            if(adj_city[0] == arriving_city.name):
                not_found = False
                print(optimal_path_list)
                print(current_cost)
                break
            f_sum = adj_city[1] + straight_line_distance(adj_city[0], arriving_city.name)
            test_list.append(f_sum)
            #print(f_sum)
            if(f_sum < lowest_cost):
                lowest_cost = f_sum
                lowest_current_cost = adj_city[1]
                lowest_cost_city = adj_city[0]
        lowest_cost = math.inf
        print(current_city.name)
        print(test_list)
        print(lowest_cost_city + " is the lowest cost city")
        # Choose city with the lowest f(n) and store it in a list. Add g(n) value to a counter
        # replace current_city with the lowest f(n)
        optimal_path_list.append(lowest_cost_city)
        current_cost += lowest_current_cost
        current_city = find_city_data(lowest_cost_city)

                    

# Function to compute the straight line distance using the Haversine formula
# city_1 is the origin, city_2 is the destination
def straight_line_distance(city_1_name, city_2_name):
    city_1 = find_city_data(city_1_name)
    city_2 = find_city_data(city_2_name)
    # Radius of the earth
    radius = 3958.8
    distance = 2 * radius * math.asin(math.sqrt((math.sin((city_2.latitude - city_1.latitude) / 2) ** 2) + math.cos(city_1.latitude) * math.cos(city_2.latitude) * math.sin((city_2.longitude - city_1.longitude) / 2) ** 2))
    return distance

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

# Function to generate a dictionary that contains the straight line distance of each location from the destination
# key = city name
# value = straight line distance to destination
def compute_distance(destination):
    dict = {}
    with open('coordinates.txt', 'r') as city_data:
        contents = city_data.readlines()
        for city_line in contents:
            city = re.search(r"([a-zA-z]+)", city_line)
            print(city.group(1))
            dict.update({city.group(1): straight_line_distance(find_city_data(city.group(1)), find_city_data(destination))})
    return dict

#print("From city:" + sys.argv[1])
#print("To city: " + sys.argv[2])
#print(compute_distance("LongBeach"))
#print(straight_line_distance(find_city_data("LongBeach"),find_city_data("Eureka")))
print(optimal_route_finder("SanFrancisco", "LongBeach"))