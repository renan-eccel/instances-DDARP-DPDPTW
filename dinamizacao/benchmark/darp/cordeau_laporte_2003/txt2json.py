import os
import json

DIR = "./instancias/"
for filename in os.listdir(DIR):
    print(filename)
    with open(DIR + filename) as file:
        first_line = file.readline().split()
        number_of_vehicles = int(first_line[0])
        number_of_requests = int(int(first_line[1])/2)
        n = number_of_requests
        max_route_time = int(first_line[2])
        vehicle_capacity = int(first_line[3])
        maximum_ride_time = int(first_line[4])
        depot_info = file.readline().split()
        requests_info = [i.split() for i in file.readlines()]

    requests = []

    for i in range(0, n):
        request_dict = {
            "id": int(requests_info[i][0]),
            "pickup_location": {
                "x_coord": float(requests_info[i][1]),
                "y_coord": float(requests_info[i][2])
            },
            "delivery_location": {
                "x_coord": float(requests_info[i+n][1]),
                "y_coord": float(requests_info[i+n][2]),
            },
            "pickup_lower_tw": int(requests_info[i][5]),
            "pickup_upper_tw": int(requests_info[i][6]),
            "pickup_service_time": int(requests_info[i][3]),
            "delivery_lower_tw": int(requests_info[i+n][5]),
            "delivery_upper_tw": int(requests_info[i+n][6]),
            "delivery_service_time": int(requests_info[i+n][3]),
            "load": int(requests_info[i][4])
        }
        requests.append(request_dict)

    instance_dict = {
        "static_info": {
            "problem": 'darp',
            "benchmark": 'cordeau_laporte_2003',
            "instance": filename.split('.')[0],
            "number_of_vehicles": number_of_vehicles,
            "vehicle_capacity": vehicle_capacity,
            "max_ride_time": maximum_ride_time,
            "max_route_time": max_route_time,
            "planing_horizon": 1440,
            "euclidean_plane_size": "[-10,10] X [10,-10]",
            "travel_time_between_nodes": "EuclideanDistance",
            "depot_location": {
                "x_coord": float(depot_info[1]),
                "y_coord": float(depot_info[2])
            }
        },
        "requests": requests
    }

    to_directory1 = "./json_instances/"
    to_directory2 = "../../ddarp/berbeglia_2012/cordeau_laporte_2003/" \
                    + "json_static_instances/"
    new_filename = filename.rsplit(".")[0] + ".json"
    if not os.path.exists(to_directory1):
        os.makedirs(to_directory1)

    if not os.path.exists(to_directory2):
        os.makedirs(to_directory2)

    with open(to_directory1 + new_filename, 'w') as file1, \
            open(to_directory2 + new_filename, 'w') as file2:
        json.dump(instance_dict, file1, indent=4)
        json.dump(instance_dict, file2, indent=4)
