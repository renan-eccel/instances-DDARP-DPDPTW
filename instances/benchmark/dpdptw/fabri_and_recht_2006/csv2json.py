import json
import os


def get_static_info(directory, subdirectory, filename):
    filepath = directory + subdirectory + filename
    with open(filepath) as requests_file:
        first_line = requests_file.readline().split(sep=";")
    static_info = {}
    static_info['problem'] = 'dpdptw'
    static_info['benchmark'] = 'fabri_and_rencht_2006'
    static_info["instance"] = filename.split('.')[0]
    for i in range(4):
        info = int(first_line[i])
        if i == 0:
            static_info["number_of_vehicles"] = info

        elif i == 1:
            static_info["vehicle_capacity"] = info

        elif i == 3:
            static_info["planing_horizon"] = info

    static_info["max_route_time"] = static_info.get("planing_horizon")
    static_info["euclidean_plane_size"] = "[0,100] X [0,100]"
    static_info["travel_time_between_nodes"] = "EuclideanDistance"
    return(static_info)


def get_coordinates(directory, subdirectory, coord_filename):
    coord_by_id = {}
    filepath = directory + subdirectory + coord_filename
    with open(filepath) as coord_file:
        coord_info = coord_file.readlines()

    for coord in coord_info:
        coord_list = coord.strip().split(sep=";")
        coord_by_id[coord_list[0]] = {"x_coord": int(coord_list[1]),
                                      "y_coord": int(coord_list[2])}
    return coord_by_id


def get_requests(coordinates_by_id, directory, subdirectory, filename):
    parameters = ["pickup_location", "delivery_location",
                  "pickup_lower_tw", "pickup_upper_tw", "delivery_lower_tw",
                  "delivery_upper_tw", "load", "arrival_time",
                  "pickup_service_time", "delivery_service_time"]
    requests_list = []
    filepath = directory + subdirectory + filename
    with open(filepath) as requests_file:
        requests_info = requests_file.readlines()
        requests_info.remove(requests_info[0])

    count = 1
    for request_string in requests_info:
        request_values = request_string.strip().split(sep=";")
        request_dict = {}
        request_dict["id"] = count
        count += 1

        for value, parameter in zip(request_values, parameters):
            if parameter in ["pickup_location", "delivery_location"]:
                request_dict[parameter] = coordinates_by_id.get(value)
            else:
                request_dict[parameter] = int(value)
        requests_list.append(request_dict)
    return requests_list


from_directory = "./Instanzen/"
to_directory = "./json_instances/"
for subdirectory in os.listdir(from_directory):
    subdirectory += "/"
    for filename in os.listdir(from_directory + subdirectory):
        if "coord" not in filename:
            coord_filename = filename.split(sep=".")[0] + "_coord.csv"
            static_info = get_static_info(from_directory, subdirectory,
                                          filename)
            coordinates_by_id = get_coordinates(from_directory, subdirectory,
                                                coord_filename)
            static_info["depot_location"] = coordinates_by_id.get("0")

            requests = get_requests(coordinates_by_id, from_directory,
                                    subdirectory, filename)

            instance_dict = {"static_info": static_info, "requests": requests}

            if not os.path.exists(to_directory + subdirectory):
                os.makedirs(to_directory + subdirectory)
            new_filename = filename.rsplit(".")[0] + ".json"
            with open(to_directory + subdirectory + new_filename, 'w') as file:
                json.dump(instance_dict, file, indent=4)
