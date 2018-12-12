import json
import os
import pprint
import re


def get_requests(directory, filename):
    requests_list = []
    parameters = ['arrival_time',
                  'pickup_service_time',
                  'pickup_x_coord', 'pickup_y_coord',
                  'pickup_lower_tw', 'pickup_upper_tw',
                  'delivery_service_time',
                  'delivery_x_coord', 'delivery_y_coord',
                  'delivery_lower_tw', 'delivery_upper_tw',
                  'garbage']
    with open(directory + filename) as requests_file:
        requests_info = requests_file.readlines()
        requests_info = requests_info[1:len(requests_info) - 1]
        request_id = 1

    for request_info in requests_info:
        request_info_list = request_info.split()
        request_dict = {}
        pickup_location = {}
        delivery_location = {}
        request_dict["id"] = request_id
        request_dict["load"] = 0
        request_id += 1

        for value, parameter in zip(request_info_list, parameters):
            value = float(value)
            if 'coord' in parameter:
                if 'pickup' in parameter:
                    coord = re.search(r'._(\w_coord)', parameter)
                    coord = coord.group(1)
                    pickup_location[coord] = value

                if 'delivery' in parameter:
                    coord = re.search(r'._(\w_coord)', parameter)
                    coord = coord.group(1)
                    delivery_location[coord] = value
            else:
                request_dict[parameter] = value

        request_dict['pickup_location'] = pickup_location
        request_dict['delivery_location'] = delivery_location
        requests_list.append(request_dict)

    return requests_list


def get_static_info(directory, filename):
    static_dict = {}
    static_dict["problem"] = 'dpdptw'
    static_dict["benchmark"] = 'gendrau_etal_2006'
    static_dict["instance"] = filename.split('.')[0]
    static_dict["number_of_vehicles"] = "10 or 20"
    static_dict["vehicles_capacity"] = "inf"
    max_route_time = re.search(r'req_rapide_\d_(\d\d\d)_\d\d.txt', filename)
    max_route_time = max_route_time.group(1)
    static_dict["max_route_time"] = int(max_route_time) * 60
    static_dict["planing_horizon"] = int(max_route_time) * 60
    static_dict["euclidean_plane_size"] = "[0,5] X [0,5]"
    static_dict["travel_time_between_nodes"] = "EuclideanDistance / 30"
    static_dict["depot_location"] = {"x_coord": 2.0, "y_coord": 2.5}
    return static_dict


directory = "./requests/"
to_directory = "./json_instances/"
for filename in os.listdir(directory):
    new_filename = filename.rsplit(".")[0] + ".json"
    instance_dict = {}
    instance_dict["static_info"] = get_static_info(directory, filename)
    instance_dict["requests"] = get_requests(directory, filename)
    with open(to_directory + new_filename, 'w') as json_instance_file:
        json.dump(instance_dict, json_instance_file, indent=4)

