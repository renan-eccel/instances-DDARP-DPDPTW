'''
Script used to transform Pankratz(2005) instances to
json format.

@author renan-eccel
'''
import os
import json


def read_until(filename, flag):
    current_line = filename.readline()
    line_dict = {}
    while current_line != flag:
        line_info = current_line.split()
        line_dict[line_info[0]] = line_info[1]
        current_line = filename.readline()
    return line_dict


def get_static_info(from_file):
    current_line = from_file.readline()
    line_dict = {}
    line_dict["problem"] = 'dpdtw'
    line_dict["benchmark"] = 'pankratz_2005'
    attribute_list = ["instance", "number_of_vehicles",
                      "vehicle_capacity", "max_route_time"]
    for attribute in attribute_list:
        line_info = current_line.split()
        if attribute == "instance":
            line_dict[attribute] = line_info[1].split('.')[0]
        elif attribute == "number_of_vehicles":
            line_dict[attribute] = 25
        else:
            line_dict[attribute] = int(line_info[1])
        current_line = from_file.readline()
    line_dict["planing_horizon"] = line_dict["max_route_time"]
    line_dict["euclidean_plane_size"] = "[0,100] X [0,100]"
    line_dict["travel_time_between_nodes"] = "EuclideanDistance"
    return line_dict


def get_coordinates_info(from_file):
    flag = "DEMAND_SECTION:\n"
    current_line = from_file.readline()
    coordinates = []
    while current_line != flag:
        line_info = current_line.split()
        coordinates.append({"x_coord": int(line_info[1]),
                            "y_coord": int(line_info[2])})
        current_line = from_file.readline()
    return coordinates


def get_requests_info(from_file):
    flag = "EOF\n"
    current_line = from_file.readline()
    requests = []
    while current_line != flag:
        line_info = current_line.split()
        requests.append({"id": int(line_info[0]),
                         "pickup_location": int(line_info[1]),
                         "delivery_location": int(line_info[2]),
                         "pickup_lower_tw": int(line_info[3]),
                         "pickup_upper_tw": int(line_info[4]),
                         "pickup_service_time": int(line_info[5]),
                         "delivery_lower_tw": int(line_info[6]),
                         "delivery_upper_tw": int(line_info[7]),
                         "delivery_service_time": int(line_info[8]),
                         "load": int(line_info[9]),
                         "arrival_time": int(line_info[10])})
        current_line = from_file.readline()
    return requests


def concatenate_requests_coordinates(requests, coordinates):
    for request in requests:
        pickup_location_string = "pickup_location"
        delivery_location_string = "delivery_location"
        pickup_location = request.get(pickup_location_string)
        delivery_location = request.get(delivery_location_string)
        request[pickup_location_string] = \
            coordinates[pickup_location]
        request[delivery_location_string] = \
            coordinates[delivery_location]


def transform_instance(ROOT, from_directory, filename):
    new_filename = filename.rsplit(".")[0] + ".json"
    to_directory = "json_instances" + "/" + from_directory + "/"
    with open(ROOT + from_directory + "/" + filename) as instace_file:
        static_info = get_static_info(instace_file)
        coordinates = get_coordinates_info(instace_file)
        static_info['depot_location'] = coordinates[0]
        requests = get_requests_info(instace_file)
        concatenate_requests_coordinates(requests, coordinates)
        instance_dict = {}
        instance_dict["static_info"] = static_info
        instance_dict["requests"] = requests

    if not os.path.exists(to_directory):
        os.makedirs(to_directory)

    with open(to_directory + new_filename, 'w') as json_instance_file:
        json.dump(instance_dict, json_instance_file, indent=4)

ROOT = "./DPDPTW-Instances/"
for directory in os.listdir(ROOT):
    for filename in os.listdir(ROOT + directory + "/"):
        transform_instance(ROOT, directory, filename)
