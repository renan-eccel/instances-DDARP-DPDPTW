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
    attribute_list = ["name", "number_of_vehicles",
                      "vehicle_capacity", "max_route_time"]
    for attribute in attribute_list:
        line_info = current_line.split()
        if attribute != "name":
            line_dict[attribute] = int(line_info[1])
        else:
            line_dict[attribute] = line_info[1]
        current_line = from_file.readline()
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
                         "pickup_location_id": int(line_info[1]),
                         "delivery_location_id": int(line_info[2]),
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
        pickup_location_id_string = "pickup_location_id"
        delivery_location_id_string = "delivery_location_id"
        pickup_location_id = request.get(pickup_location_id_string)
        delivery_location_id = request.get(delivery_location_id_string)
        request[pickup_location_id_string] = \
            coordinates[pickup_location_id]
        request[delivery_location_id_string] = \
            coordinates[delivery_location_id]


def transform_instance(ROOT, from_directory, filename):
    new_filename = filename.rsplit(".")[0] + ".json"
    to_directory = "json_instances" + "/" + from_directory + "/"
    with open(ROOT + from_directory + "/" + filename) as instace_file:
        static_info = get_static_info(instace_file)
        coordinates = get_coordinates_info(instace_file)
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
        print(directory + "/" + filename)
        transform_instance(ROOT, directory, filename)
