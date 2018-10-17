import os
import json
import math

def dynamize_instances(from_dir, to_dir, alpha, beta):
    for filename in os.listdir(from_dir):
        with open(from_dir + filename) as from_file:
            instance_dict = json.load(from_file)
        for request in instance_dict.get("requests"):
            arrival_time = calculate_arrival_time(request, alpha, beta)
            request["arrival_time"] = arrival_time
        with open(to_dir + filename, 'w') as to_file:
            json.dump(instance_dict, to_file, indent=4)



def calculate_arrival_time(request_dict, alpha, betha):
    '''
    Generate a arrival time based on berbceglia_2012 method.
    a_i^{last} = min{l_i, l_{n+1} - t_{(i,n+i)} - d_i}

    Keyword arguments:
        static_instance_dict: dictionary with instace information
        betha: time interval between a_i and a_i^{last}
        alpha: percentage of a priori known requests [0,1]
    '''
    pickup_upper_tw = request_dict.get("pickup_upper_tw")
    delivery_upper_tw = request_dict.get("delivery_upper_tw")
    pickup_location = request_dict.get("pickup_location")
    delivery_location = request_dict.get("delivery_location")
    travel_time_pickup_delivery = get_travel_time_between(pickup_location,
                                                          delivery_location)
    pickup_service_time = request_dict.get("pickup_service_time")
    a_last = min(pickup_upper_tw, delivery_upper_tw -
                 travel_time_pickup_delivery - pickup_service_time)
    return max(a_last - betha, 0)



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

dynamize_instances("./cordeau_laporte_2003/json_static_instances/",
                   "./cordeau_laporte_2003/json_dynamic_instances/",
                   0, 60)
