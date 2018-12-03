import json
import os
import pandas as pd
import re


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
    corner_1 = re.match(r'\[(-?\d*,-?\d*)\] X \[(-?\d*,-?\d*)\]',
                         plane_size)[1]




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


FOLDER = '../benchmark/'

filename = ('../benchmark/ddarp/berbeglia_2012/'
            + 'cordeau_laporte_2003/json_dynamic_instances/'
            + 'pr01.json')

with open(filename, 'r') as file:
    instance_dict = json.load(file)
instance_requests = instance_dict.get('requests')
instance_static_info = instance_dict.get('static_info')
depot_location = instance_static_info.get('depot_location')
planing_horizon = instance_static_info.get('planing_horizon')
plane_size = instance_static_info.get('euclidean_plane_size')
location_columns = ['delivery_location', 'pickup_location']
df = (pd.DataFrame.from_dict(instance_requests)
        .pipe(disjoint_coordinates, location_columns)
        .pipe(delete_columns, location_columns)
        .pipe(normalize_coords_with_depot, depot_location)
)
