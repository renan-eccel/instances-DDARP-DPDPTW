import numpy as np
import math


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
        ) ** (0.5)
    )

    return np.ceil(euclidian_distance)


def elementwise_min(x, y):
    x = x.copy()
    x[x > y] = y
    return x


def dinamize_as_berbeglia(pickup_location_x_coord,
                          pickup_location_y_coord,
                          delivery_location_x_coord,
                          delivery_location_y_coord,
                          pickup_upper_tw,
                          delivery_upper_tw,
                          pickup_service_time,
                          alpha,
                          beta):
    travel_time = calculate_travel_time(pickup_location_x_coord,
                                        pickup_location_y_coord,
                                        delivery_location_x_coord,
                                        pickup_location_y_coord)
    a_latest = elementwise_min(pickup_upper_tw,
                               delivery_upper_tw
                               - travel_time
                               - pickup_service_time)
    arrival_time = a_latest.subtract(beta).rename('arrival_time')
    static_requests = (
        arrival_time.sample(round(alpha * arrival_time.size))
    )
    arrival_time[static_requests.index] = 0

    return arrival_time
