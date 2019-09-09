import os
import json
import math
import random as rnd


def generate_arrival_time(depot_location, request_dict, beta):
    '''
    Generate a arrival time based on pureza_laporte_2008 method.
    a_i = min{e_i, max{U(1,5), l_i - t_{(0,i)} - beta}}

    Keyword arguments:
        beta: reaction time before call is received
    '''
    pickup_lower_tw = request_dict.get("pickup_lower_tw")
    pickup_upper_tw = request_dict.get("pickup_upper_tw")
    pickup_location = request_dict.get("pickup_location")
    travel_time_depot_pickup = get_travel_time_between(depot_location,
                                                       pickup_location)
    random_number = rnd.randint(1, 5)

    return min(pickup_lower_tw, max(random_number, pickup_upper_tw -
                                    travel_time_depot_pickup - beta))


def get_travel_time_between(origin, destination):
    '''
    Calculate EuclideanDistance between 2 points

    Keyword arguments:
        origin: dict containing 'x_coord' and 'y_coord'
        detination: dict containing 'x_coord' and 'y_coord'
    '''
    origin_x = origin.get('x_coord')
    origin_y = origin.get('y_coord')
    destination_x = destination.get('x_coord')
    destination_y = destination.get('y_coord')

    return math.ceil(math.sqrt(abs(destination_x - origin_x)**2
                               + abs(destination_y - origin_y)**2))


static_instances_folder = "./json_static_instances/"
dynamic_instaces_folder = "./json_dynamic_instances/"

# only the instances with 100, 200 e 400 nodes were used by
# pureza_laporte_2005
dynamized_instances_folders = ["pdp_100/", "pdp_200/", "pdp_400/"]

# pureza_and_laporte_2005 used beta = [0, 100, 200, 300] to create four
# dynamic instances for each static one.
beta_values = [0, 100, 200, 300]

for folder in dynamized_instances_folders:
    for filename in os.listdir(static_instances_folder + folder):
        for beta in beta_values:
            with open(static_instances_folder + folder + filename) \
                    as instance_file:
                instance_dict = json.load(instance_file)

            new_filename = filename.rsplit(".")[0] + "_b" + str(beta) + ".json"
            static_info = instance_dict.get('static_info')
            static_info['problem'] = 'dpdptw'
            static_info['benchmark'] = 'pureza_laporte_2008'
            static_info['instance'] = new_filename.split('.')[0]
            depot_location = static_info.get('depot_location')
            requests = instance_dict.get('requests')

            for request in requests:
                arrival_time = generate_arrival_time(depot_location, request,
                                                     beta)
                request["arrival_time"] = arrival_time

            if not os.path.exists(dynamic_instaces_folder + folder):
                os.makedirs(dynamic_instaces_folder + folder)

            with open(dynamic_instaces_folder
                      + folder
                      + new_filename, "w") as json_instance_file:
                json.dump(instance_dict, json_instance_file, indent=4)
