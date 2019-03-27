import json
import os
import pandas as pd
import re
from progress.bar import Bar


def normalize_coords_with_depot(df, depot_location):
    location_columns = ['delivery_location_', 'pickup_location_']
    for axis in depot_location:
        for location_column in location_columns:
            depot_axis_value = depot_location.get(axis)
            df[location_column + axis] = df[location_column +
                                            axis].apply(lambda x: x -
                                                        depot_axis_value)
    return df


def normalize_coords_with_plane_size(df, plane_size):
    '''
    upper_corner +---------+
                 |         |
                 |         |
                 +---------+ lower_corner
    '''
    plane_coords = re.match(r'\[(-?\d*),(-?\d*)\] X \[(-?\d*),(-?\d*)\]',
                            plane_size)
    upper_corner_x = int(plane_coords[1])
    upper_corner_y = int(plane_coords[2])
    lower_corner_x = int(plane_coords[3])
    lower_corner_y = int(plane_coords[4])
    df = (df.assign(delivery_location_x_coord=lambda x:
                    100*(x.delivery_location_x_coord
                         / (lower_corner_x - upper_corner_x)))
            .assign(delivery_location_y_coord=lambda x:
                    100*(x.delivery_location_y_coord
                         / (upper_corner_y - lower_corner_y)))
            .assign(pickup_location_y_coord=lambda x:
                    100*(x.pickup_location_y_coord
                         / (upper_corner_y - lower_corner_y)))
            .assign(pickup_location_x_coord=lambda x:
                    100*(x.pickup_location_x_coord
                         / (upper_corner_y - lower_corner_y)))
          )
    return df


def disjoint_coordinates(df, columns):
    for column in columns:
        list_posfix = ['x_coord', 'y_coord']
        for posfix in list_posfix:
            new_column = column + '_' + posfix
            df[new_column] = df[column].apply(lambda x, pf=posfix: x.get(pf))
    return df


def delete_columns(df, columns):
    for column in columns:
        del df[column]
    return df


def build_all_dataframes(root, folders):
    df = pd.DataFrame()
    bar = Bar('Processing', max=1919)
    for folder in folders:
        for folder, subfolders, filenames in os.walk(root + folder):
            for filename in filenames:
                if not subfolders:
                    print(folder + '/' + filename)
                    df = (df.append(build_dataframe(folder + '/' + filename)))
                else:
                    for subfolder in subfolders:
                        df = (df.append(build_dataframe(folder + '/'
                                                        + subfolder + '/'
                                                        + filename)))
                bar.next()
    return df


def build_dataframe(filepath):
    with open(filepath, 'r') as file:
        instance_dict = json.load(file)
    instance_requests = instance_dict.get('requests')
    instance_static_info = instance_dict.get('static_info')
    # depot_location = instance_static_info.get('depot_location')
    # planing_horizon = instance_static_info.get('planing_horizon')
    # plane_size = instance_static_info.get('euclidean_plane_size')
    location_columns = ['delivery_location', 'pickup_location']
    df_requests = (pd.DataFrame.from_dict(instance_requests)
                   .assign(problem=instance_static_info.get('problem'))
                   .assign(benchmark=instance_static_info.get('benchmark'))
                   .assign(instance=instance_static_info.get('instance'))
                   .assign(number_of_vehicles=instance_static_info
                           .get('number_of_vehicles'))
                   .assign(vehicle_capacity=instance_static_info
                           .get('vehicle_capacity'))
                   .assign(max_ride_time=instance_static_info
                           .get('max_ride_time'))
                   .assign(max_route_time=instance_static_info
                           .get('max_route_time'))
                   .assign(planing_horizon=instance_static_info
                           .get('planing_horizon'))
                   .assign(euclidean_plane=instance_static_info
                           .get('euclidean_plane_size'))
                   .assign(travel_time=instance_static_info
                           .get('travel_time_between_nodes'))
                   .assign(depot_location_x=instance_static_info
                           .get('depot_location').get('x_coord'))
                   .assign(depot_location_y=instance_static_info
                           .get('depot_location').get('y_coord'))
                   .pipe(disjoint_coordinates, location_columns)
                   .pipe(delete_columns, location_columns)
                   # .pipe(normalize_coords_with_depot, depot_location)
                   # .pipe(normalize_coords_with_plane_size, plane_size)
                   )
    return df_requests


ROOT = '../benchmark/'

FOLDERS = ['ddarp/berbeglia_2012/cordeau_laporte_2003/json_dynamic_instances/',
           'ddarp/berbeglia_2012/ropke_etal_2007/json_dynamic_instances/',
           'dpdptw/fabri_and_recht_2006/json_instances/',
           'dpdptw/gendreau_etal_2006/json_instances/',
           'dpdptw/mitrovic-minic_etal_2003/json_instances/',
           'dpdptw/pankratz_2005/json_instances/',
           'dpdptw/pureza_laporte_2008/json_dynamic_instances/']

df_requests = build_all_dataframes(ROOT, FOLDERS)
pd.to_pickle(df_requests, './df_requests.zip')
