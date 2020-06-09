import pandas as pd
import instances.dinamizators.dinamizators as din
import math


def simplest_test():
    '''
    Test if the dinamizators are running
    '''
    df = (
        pd.read_pickle('./instances/analysis/df_requests.zip')
          .reset_index()
    )
    din.dinamize_as_berbeglia(df.pickup_location_x_coord,
                              df.pickup_location_y_coord,
                              df.delivery_location_x_coord,
                              df.delivery_location_y_coord,
                              df.pickup_upper_tw,
                              df.delivery_upper_tw,
                              df.pickup_service_time,
                              0.5,
                              60)

    din.dinamize_as_pureza_laporte(df.depot_location_x,
                                   df.depot_location_y,
                                   df.pickup_location_x_coord,
                                   df.pickup_location_y_coord,
                                   df.pickup_lower_tw,
                                   df.pickup_upper_tw,
                                   0)

    din.dinamize_as_pankratz(df.depot_location_x,
                             df.depot_location_y,
                             df.pickup_location_x_coord,
                             df.pickup_location_y_coord,
                             df.delivery_location_x_coord,
                             df.delivery_location_y_coord,
                             df.pickup_upper_tw,
                             df.delivery_upper_tw,
                             df.pickup_service_time,
                             0.5)

    din.dinamize_as_fabri_recht(df.pickup_location_x_coord,
                                df.pickup_location_y_coord,
                                df.delivery_location_x_coord,
                                df.delivery_location_y_coord,
                                df.pickup_lower_tw,
                                df.delivery_upper_tw)


def test_calculate_travel_time():
    pickup_location_x_coord = -1
    pickup_location_y_coord = -1
    delivery_location_x_coord = 1
    delivery_location_y_coord = 1
    expected_travel_time = math.ceil(math.sqrt(2) + math.sqrt(2))
    calculated_travel_time = (
        din.calculate_travel_time(
            pickup_location_x_coord,
            pickup_location_y_coord,
            delivery_location_x_coord,
            delivery_location_y_coord)
    )
    assert (expected_travel_time == calculated_travel_time)


def test_series_elementwise_max():
    x = pd.Series([1, 2, 3])
    y = pd.Series([3, 2, 1])
    expected_max = pd.Series([3, 2, 3])
    calculated_max = din.elementwise_max(x, y)
    assert (expected_max == calculated_max).all()


def test_dataframe_elementwise_max():
    x = pd.DataFrame([[1, 2, 3], [3, 2, 1]])
    y = pd.DataFrame([[3, 2, 1], [1, 2, 3]])
    expected_max = pd.DataFrame([[3, 2, 3], [3, 2, 3]])
    calculated_max = din.elementwise_max(x, y)
    assert (expected_max == calculated_max).all().all()


def test_series_elementwise_min():
    x = pd.Series([1, 2, 3])
    y = pd.Series([3, 2, 1])
    expected_min = pd.Series([1, 2, 1])
    calculated_min = din.elementwise_min(x, y)
    assert (expected_min == calculated_min).all()


def test_dataframe_elementwise_min():
    x = pd.DataFrame([[1, 2, 3], [3, 2, 1]])
    y = pd.DataFrame([[3, 2, 1], [1, 2, 3]])
    expected_min = pd.DataFrame([[1, 2, 1], [1, 2, 1]])
    calculated_min = din.elementwise_min(x, y)
    assert (expected_min == calculated_min).all().all()


def test_dinamize_as_berbeglia():
    pickup_location_x_coord = pd.Series([1])
    pickup_location_y_coord = pd.Series([1])
    delivery_location_x_coord = pd.Series([-1])
    delivery_location_y_coord = pd.Series([-1])
    pickup_upper_tw = pd.Series([10.0])
    delivery_upper_tw = pd.Series([12.0])
    pickup_service_time = pd.Series([1.0])
    alpha = 0
    beta = 1
    # tempo esperado usando a equação de dinamização de berbeglia
    expected_arrival_time = pd.Series([7])
    calculated_arrival_time = (
        din.dinamize_as_berbeglia(
            pickup_location_x_coord,
            pickup_location_y_coord,
            delivery_location_x_coord,
            delivery_location_y_coord,
            pickup_upper_tw,
            delivery_upper_tw,
            pickup_service_time,
            alpha,
            beta
        )
    )
    assert (expected_arrival_time == calculated_arrival_time).all()


def test_dinamize_as_pureza_laporte():
    depot_location_x = pd.Series([0])
    depot_location_y = pd.Series([0])
    pickup_location_x_coord = pd.Series([1])
    pickup_location_y_coord = pd.Series([1])
    pickup_lower_tw = pd.Series([2])
    pickup_upper_tw = pd.Series([10])
    beta = 1
    # tempo esperado usando a equação de dinamização de pureza e laporte
    expected_arrival_time = 2
    calculated_arrival_time = (
        din.dinamize_as_pureza_laporte(
            depot_location_x,
            depot_location_y,
            pickup_location_x_coord,
            pickup_location_y_coord,
            pickup_lower_tw,
            pickup_upper_tw,
            beta
        )
    )
    assert (expected_arrival_time == calculated_arrival_time).all()


def test_dinamize_as_pankratz():
    depot_location_x = pd.Series([0])
    depot_location_y = pd.Series([0])
    pickup_location_x_coord = pd.Series([-1])
    pickup_location_y_coord = pd.Series([-1])
    delivery_location_x_coord = pd.Series([1])
    delivery_location_y_coord = pd.Series([1])
    pickup_upper_tw = pd.Series([10])
    delivery_upper_tw = pd.Series([20])
    pickup_service_time = pd.Series([1])
    beta = 0.6
    # tempo esperado usando a equação de dinamização de pankratz e arredondado
    # para o próximo inteiro
    expected_arrival_time = 5
    calculated_arrival_time = (
        din.dinamize_as_pankratz(
            depot_location_x,
            depot_location_y,
            pickup_location_x_coord,
            pickup_location_y_coord,
            delivery_location_x_coord,
            delivery_location_y_coord,
            pickup_upper_tw,
            delivery_upper_tw,
            pickup_service_time,
            beta
        )
    )
    assert (expected_arrival_time == calculated_arrival_time).all()


def test_dinamize_as_fabri_recht():
    pickup_location_x_coord = pd.Series([-1])
    pickup_location_y_coord = pd.Series([-1])
    delivery_location_x_coord = pd.Series([1])
    delivery_location_y_coord = pd.Series([1])
    pickup_lower_tw = pd.Series([5])
    delivery_upper_tw = pd.Series([20])
    expected_mean = 2.5
    calculated_arrival_times = [
        din.dinamize_as_fabri_recht(
            pickup_location_x_coord,
            pickup_location_y_coord,
            delivery_location_x_coord,
            delivery_location_y_coord,
            pickup_lower_tw,
            delivery_upper_tw
        )
        for i in range(500)
    ]
    calculated_mean = (sum(calculated_arrival_times)
                       / len(calculated_arrival_times))
    error = abs(calculated_mean - expected_mean)
    expected_error = 0.1
    assert(error < expected_error).all()
