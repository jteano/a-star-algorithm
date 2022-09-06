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
# Returns the best route as a list and total distance as a float
def optimal_route_finder(city_1, city_2):
    # Set a start and end point
    # Store departing city in master_f_sum_list since we can computer for f(n)
    master_f_sum_list = [city_1]
    optimal_path_list = []
    path_info = {city_1: {'cost': 0, 'previous': None}}
    not_found = True

    # Starting at the departing_city, iterate through all the adjacent cities and compute for f(n)
    # Repeat this process until we reach our destination
    while not_found:
        # Set the current city whose adjacent cities path cost will be computed
        # Iterate through the master_f_sum list that contains the cities in which we have computed f(n)
        # straight_line_distance represents h(n)
        current_city = None
        for next_city in master_f_sum_list:
            if current_city == None or f_sum(path_info, next_city, city_2) < f_sum(path_info, current_city, city_2):
                current_city = next_city
        
        # Iterate through cities adjacent to current_city
        for adj_city in find_city_data(current_city).adjacent_cities:
            adjacent_city_name = adj_city[0]
            adjacent_city_distance = adj_city[1]
            # Check if adjacent city has not been visited yet by checking both lists
            # If true, append to master_f_sum list, set current_city as previous city of adjacent city
            # append current path cost of current_city to the distance of adjacent city to get g(n)
            master_list = master_f_sum_list + optimal_path_list
            current_city_cost = path_info[current_city]['cost']
            current_city_total_cost = current_city_cost + adjacent_city_distance
            if adjacent_city_name not in master_list:
                path_info[adjacent_city_name] = set_path_info(current_city, current_city_total_cost)
                master_f_sum_list.append(adjacent_city_name)
                
            else:
                # If current path cost is greater than the path from the current city, then it means that the
                # path set by the current city is cheaper
                if path_info[adjacent_city_name]['cost'] > current_city_total_cost:
                    path_info[adjacent_city_name] = set_path_info(current_city, current_city_total_cost)
                    # Remove adjacent city from the optimal path list and place back on the master f sum list
                    if adjacent_city_name in optimal_path_list:
                        master_f_sum_list.append(adjacent_city_name)
                        optimal_path_list.remove(adjacent_city_name)

        # If the current city is the arriving city, then we have reached our destination
        if current_city == city_2:
            final_optimal_path = []
            
            # Go back through the path taken via the previous dictionary
            # Stop when we reach the departing city which has previous set to None
            while True:
                final_optimal_path.append(current_city)
                current_city = path_info[current_city]['previous']
                if path_info[current_city]['previous'] == None:
                    final_optimal_path.append(city_1)
                    break
            
            final_optimal_path.reverse()
            final_optimal_path_string = ' - '.join(final_optimal_path)
            total_distance = "{:.2f}".format(path_info[city_2]['cost'])
            #print(final_optimal_path_string)
            print("From city: " + city_1)
            print("To city: " + city_2)
            print("Best Route: " + final_optimal_path_string)
            print("Total distance: " + total_distance + " mi")
            return final_optimal_path
        optimal_path_list.append(current_city)
        master_f_sum_list.remove(current_city)
    return optimal_path_list
                    

# Function to compute the straight line distance using the Haversine formula
# departing_city is the origin, arriving_city is the destination
def straight_line_distance(city_1_name, city_2_name):
    departing_city = find_city_data(city_1_name)
    arriving_city = find_city_data(city_2_name)
    # Radius of the earth
    radius = 3958.8
    distance = 2 * radius * math.asin(math.sqrt((math.sin((arriving_city.latitude - departing_city.latitude) / 2) ** 2) + math.cos(departing_city.latitude) * math.cos(arriving_city.latitude) * math.sin((arriving_city.longitude - departing_city.longitude) / 2) ** 2))
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
            dict.update({city.group(1): straight_line_distance(city.group(1), destination)})
    return dict

# Function to set path name, cost from origin and previous city
def set_path_info(previous, cost):
    info = {}
    info['previous'] = previous
    info['cost'] = cost
    return info

# Function to computer for f(n)
def f_sum(path_info, city, destination_city):
    f_sum = path_info[city]['cost'] + straight_line_distance(city, destination_city)
    return f_sum

#print("From city:" + sys.argv[1])
#print("To city: " + sys.argv[2])
#print(compute_distance("LongBeach"))
#print(straight_line_distance(find_city_data("LongBeach"),find_city_data("Eureka")))
#optimal_route_finder("SanFrancisco", "LongBeach")
#print(sys.argv[1] + " is the departing city")
#print(sys.argv[2] + " is the arriving city")
optimal_route_finder(sys.argv[1], sys.argv[2])