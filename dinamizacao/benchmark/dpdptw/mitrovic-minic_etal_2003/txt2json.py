import os
import json
import re


def get_requests_info(directory, filename):
    parameter_list = ["id", "arrival_time", "pickup_service_time",
                      "pickup_location_x_coord", "pickup_location_y_coord",
                      "pickup_lower_tw", "pickup_upper_tw",
                      "delivery_service_time", "delivery_location_x_coord",
                      "delivery_location_y_coord", "delivery_lower_tw",
                      "delivery_upper_tw"]
    with open(from_directory + filename) as testfile:
        file_info = testfile.readlines()
        requests_list = []

    for line_info in file_info[6:]:
        line_info_list = line_info.split()
        request_dict = {}
        pickup_location = {}
        delivery_location = {}
        request_dict["load"] = 0

        for value, parameter in zip(line_info_list, parameter_list):
            if 'coord' in parameter:
                if 'pickup' in parameter:
                    coord = re.search(r'._(\w_coord)', parameter)
                    coord = coord.group(1)
                    pickup_location[coord] = float(value)

                if 'delivery' in parameter:
                    coord = re.search(r'._(\w_coord)', parameter)
                    coord = coord.group(1)
                    delivery_location[coord] = float(value)

            elif parameter == "id":
                request_dict[parameter] = int(value) + 1

            else:
                request_dict[parameter] = float(value)

        request_dict['pickup_location'] = pickup_location
        request_dict['delivery_location'] = delivery_location
        requests_list.append(request_dict)

    return requests_list


def get_static_info(filename):
    vehicle_set_size_dict = {"100": 20, "300": 40, "500": 60, "1000": 80}
    number_of_requests = re.search(r'Rnd\d_10h_(\d\d\d\d?)_\d\d\d.txt',
                                   filename).group(1)
    static_dict = {}
    static_dict["problem"] = 'dpdptw'
    static_dict["benchmark"] = 'mitrovic-minic_etal_2003'
    static_dict["instance"] = filename.split('.')[0]
    static_dict["number_of_vehicles"] = \
        vehicle_set_size_dict.get(number_of_requests)
    static_dict["vehicles_capacity"] = "inf"
    static_dict["max_route_time"] = 600
    static_dict["planing_horizon"] = 600
    static_dict["euclidean_plane_size"] = "[0,60] X [0,60]"
    static_dict["travel_time_between_nodes"] = "EuclideanDistance / 60"
    static_dict["depot_location"] = {"x_coord": 20, "y_coord": 30}
    return static_dict


from_directory = "./instancias/"
to_directory = "./json_instances/"
for subdirectory in os.listdir(from_directory):
    for filename in os.listdir(from_directory + subdirectory):
        new_filename = filename.rsplit(".")[0] + ".json"
        static_info = get_static_info(filename)
        requests = get_requests_info(from_directory,  subdirectory + "/" +
                                     filename)
        instance_dict = {}
        instance_dict["static_info"] = static_info
        instance_dict["requests"] = requests

        if not os.path.exists(to_directory + subdirectory):
            os.makedirs(to_directory + subdirectory)

        with open(to_directory + subdirectory + "/" + new_filename, 'w') as \
                file:
            json.dump(instance_dict, file, indent=4)
