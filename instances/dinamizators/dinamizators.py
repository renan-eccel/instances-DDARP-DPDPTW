import numpy as np
import math
import random as rnd


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


def elementwise_max(x, y):
    x = x.copy()
    x[x < y] = y
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
                                        delivery_location_y_coord)
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


def dinamize_as_pureza_laporte(depot_location_x,
                               depot_location_y,
                               pickup_location_x_coord,
                               pickup_location_y_coord,
                               pickup_lower_tw,
                               pickup_upper_tw,
                               beta):

    travel_time = calculate_travel_time(depot_location_x,
                                        depot_location_y,
                                        pickup_location_x_coord,
                                        pickup_location_y_coord)
    arrival_time = (
        elementwise_min(
                pickup_lower_tw,
                elementwise_max(
                    pickup_upper_tw - travel_time - beta,
                    rnd.randint(1, 5)
                   )
          )
    )
    return arrival_time


def dinamize_as_pankratz(depot_location_x,
                         depot_location_y,
                         pickup_location_x_coord,
                         pickup_location_y_coord,
                         delivery_location_x_coord,
                         delivery_location_y_coord,
                         pickup_upper_tw,
                         pickup_lower_tw,
                         delivery_upper_tw,
                         pickup_service_time,
                         beta):

    pickup_delivery_travel_time = calculate_travel_time(
        pickup_location_x_coord,
        pickup_location_y_coord,
        delivery_location_x_coord,
        delivery_location_y_coord
    )
    depot_pickup_travel_time = calculate_travel_time(
        depot_location_x,
        depot_location_y,
        pickup_location_x_coord,
        pickup_location_y_coord
    )
    a_latest = (
        elementwise_min(
            pickup_upper_tw,
            (delivery_upper_tw
             - pickup_delivery_travel_time - pickup_service_time)
        )
        - depot_pickup_travel_time
    )

    arrival_time = beta * a_latest

    return arrival_time


def dinamize_as_fabri_recht(pickup_location_x_coord,
                            pickup_location_y_coord,
                            delivery_location_x_coord,
                            delivery_location_y_coord,
                            pickup_lower_tw,
                            delivery_upper_tw):

    pickup_delivery_travel_time = calculate_travel_time(
        pickup_location_x_coord,
        pickup_location_y_coord,
        delivery_location_x_coord,
        delivery_location_y_coord,
    )
    arrival_time = rnd.randint(
        0,
        elementwise_min(
            pickup_lower_tw,
            delivery_upper_tw - pickup_delivery_travel_time
        )
    )

    return arrival_time
