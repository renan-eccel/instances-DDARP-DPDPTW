import numpy as np
import pandas as pd


def calculate_travel_time(pickup_location_x_coord,
                          pickup_location_y_coord,
                          delivery_location_x_coord,
                          delivery_location_y_coord):
    '''
    Calculate euclidian distance between 2 points
    '''
    euclidian_distance = (
        (
         (delivery_location_x_coord - pickup_location_x_coord)**2
         + (delivery_location_y_coord - pickup_location_y_coord)**2
        )
        ** (0.5))

    return np.ceil(euclidian_distance)


def elementwise_min(vector_a, vector_b):
    return pd.concat([vector_a, vector_b], axis=1).min(axis=1)


def dinamize_as_berbeglia(pickup_location_x_coord,
                          pickup_location_y_coord,
                          delivery_location_x_coord,
                          delivery_location_y_coord,
                          pickup_upper_tw,
                          delivery_upper_tw,
                          pickup_service_time,
                          beta):
    travel_time = calculate_travel_time(pickup_location_x_coord,
                                        pickup_location_y_coord,
                                        delivery_location_x_coord,
                                        pickup_location_y_coord)
    a_latest = elementwise_min(pickup_upper_tw,
                               delivery_upper_tw
                               - travel_time
                               - pickup_service_time)
    return a_latest - beta
