import os
import json
import pandas as pd

def structure_segmented_df(df, activity):
    if activity == 'delivery':
        opposite_activity = 'pickup'
    else:
        opposite_activity = 'delivery'

    del df[activity + '_index']
    del df['stop_type']
    columns = [activity + "_id",
               activity + "_location_x_coord",
               activity + "_location_y_coord",
               activity + "_load",
               activity + "_lower_tw",
               activity + "_upper_tw",
               activity + "_service_time",
               opposite_activity + "_index"]
    df.columns = columns
    if activity == 'delivery':
        df = df.assign(pickup_delivery_index =
                       lambda x: x.pickup_index.map(str)
                       + "-"
                       + x.delivery_id.map(str))
    else:
        df = df.assign(pickup_delivery_index =
                       lambda x: x.pickup_id.map(str)
                       + "-" +
                       + x.delivery_index.map(str))
    return df


def build_instance_dict(directory, subdirectory, filename):
    df = pd.read_csv(directory + subdirectory + filename, sep="\\t",
                     header=None, skiprows=1)

    with open(directory + subdirectory + filename) as f:
        first_line = f.readline().split()

    df.columns = ["id", "coord_x", "coord_y", "load", "lower_tw", "upper_tw",
                  "service_time", "pickup_index", "delivery_index"]
    depot_info = df.iloc[0, :]
    df['stop_type'] = df.apply(lambda row: "pickup" if row['pickup_index'] == 0
                               else "delivery", axis=1)

    df_without = df.drop([0])
    pickup_df = df_without[df_without['stop_type'] == 'pickup']
    pickup_df = structure_segmented_df(pickup_df, 'pickup')

    delivery_df = df_without[df_without['stop_type'] == 'delivery']
    delivery_df = structure_segmented_df(delivery_df, 'delivery')

    df_final = pd.merge(pickup_df, delivery_df,
                        on="pickup_delivery_index").transpose()

    df_dict = df_final.to_dict()

    requests_list = []
    for key in df_dict:
        request_dict_raw = df_dict.get(key)
        request_dict_clean = {
            "id": key+1,
            "pickup_location": {
                "x_coord": request_dict_raw.get('pickup_location_x_coord'),
                "y_coord": request_dict_raw.get('pickup_location_y_coord')
            },
            "delivery_location": {
                "x_coord": request_dict_raw.get('delivery_location_x_coord'),
                "y_coord": request_dict_raw.get('delivery_location_y_coord')
            },
            "pickup_lower_tw": request_dict_raw.get('pickup_lower_tw'),
            "pickup_upper_tw": request_dict_raw.get('pickup_upper_tw'),
            "pickup_service_time": request_dict_raw.get("pickup_service_time"),
            "delivery_lower_tw": request_dict_raw.get('delivery_lower_tw'),
            "delivery_upper_tw": request_dict_raw.get('delivery_upper_tw'),
            "delivery_service_time": request_dict_raw.get(
                "delivery_service_time"),
            "load": request_dict_raw.get('pickup_load')
        }
        requests_list.append(request_dict_clean)

    output_dict = {
        "static_info": {
            "name": filename,
            "number_of_vehicles": int(first_line[0]),
            "vehicle_capacity": int(first_line[1]),
            "max_route_time": int(depot_info["upper_tw"]),
            "planing_horizon": int(depot_info["upper_tw"]),
            "euclidean_plane_size": "[0,100] X [0,100]",
            "travel_time_between_nodes": "EuclideanDistance",
            "depot_location": {
                "x_coord": int(depot_info["coord_x"]),
                "y_coord": int(depot_info["coord_y"])
            }
        },
        "requests" : requests_list
    }
    return output_dict


DIRECTORY = "./instancias/"

for subdirectory in os.listdir(DIRECTORY):
    for filename in os.listdir(DIRECTORY + subdirectory):
        instance_dict = build_instance_dict(DIRECTORY, subdirectory
                                            + "/", filename)

        to_directory = "./json_instances/" + subdirectory + "/"
        if not os.path.exists(to_directory):
            os.makedirs(to_directory)

        new_filename = filename.rsplit(".")[0] + ".json"
        with open(to_directory + new_filename, 'w')  as json_instance_file:
            json.dump(instance_dict, json_instance_file, indent=4)
