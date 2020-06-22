import pandas as pd
import instances.dinamizators.dinamizators as din
import random


def dinamize_all(df_in):
    static_atributes = ['problem', 'benchmark', 'instance', 'id',
                        'number_of_requests', 'number_of_vehicles',
                        'planing_horizon',
                        'delivery_lower_tw', 'delivery_service_time',
                        'delivery_upper_tw', 'pickup_lower_tw',
                        'pickup_service_time', 'pickup_upper_tw',
                        'depot_location_x', 'depot_location_y',
                        'delivery_location_x_coord',
                        'delivery_location_y_coord',
                        'pickup_location_x_coord',
                        'pickup_location_y_coord']
    df = (
          df_in
          .reset_index()
          .loc[:, static_atributes]
          .replace(to_replace='fabri_and_rencht_2006',
                   value='fabri_rencht_2006')
          .assign(berbeglia_2012_1=lambda df:
                  din.dinamize_as_berbeglia(df.pickup_location_x_coord,
                                            df.pickup_location_y_coord,
                                            df.delivery_location_x_coord,
                                            df.delivery_location_y_coord,
                                            df.pickup_upper_tw,
                                            df.delivery_upper_tw,
                                            df.pickup_service_time,
                                            0,
                                            60),
                  berbeglia_2012_2=lambda df:
                  din.dinamize_as_berbeglia(df.pickup_location_x_coord,
                                            df.pickup_location_y_coord,
                                            df.delivery_location_x_coord,
                                            df.delivery_location_y_coord,
                                            df.pickup_upper_tw,
                                            df.delivery_upper_tw,
                                            df.pickup_service_time,
                                            0,
                                            random.randint(60, 240)),
                  pureza_laporte_2008_1=lambda df:
                  din.dinamize_as_pureza_laporte(df.depot_location_x,
                                                 df.depot_location_y,
                                                 df.pickup_location_x_coord,
                                                 df.pickup_location_y_coord,
                                                 df.pickup_lower_tw,
                                                 df.pickup_upper_tw,
                                                 0),
                  pureza_laporte_2008_2=lambda df:
                  din.dinamize_as_pureza_laporte(df.depot_location_x,
                                                 df.depot_location_y,
                                                 df.pickup_location_x_coord,
                                                 df.pickup_location_y_coord,
                                                 df.pickup_lower_tw,
                                                 df.pickup_upper_tw,
                                                 100),
                  pureza_laporte_2008_3=lambda df:
                  din.dinamize_as_pureza_laporte(df.depot_location_x,
                                                 df.depot_location_y,
                                                 df.pickup_location_x_coord,
                                                 df.pickup_location_y_coord,
                                                 df.pickup_lower_tw,
                                                 df.pickup_upper_tw,
                                                 200),
                  pureza_laporte_2008_4=lambda df:
                  din.dinamize_as_pureza_laporte(df.depot_location_x,
                                                 df.depot_location_y,
                                                 df.pickup_location_x_coord,
                                                 df.pickup_location_y_coord,
                                                 df.pickup_lower_tw,
                                                 df.pickup_upper_tw,
                                                 300),
                  pankratz_2005_1=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.1),
                  pankratz_2005_2=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.2),
                  pankratz_2005_3=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.3),
                  pankratz_2005_4=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.4),
                  pankratz_2005_5=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.5),
                  pankratz_2005_6=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.6),
                  pankratz_2005_7=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.7),
                  pankratz_2005_8=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.8),
                  pankratz_2005_9=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           0.9),
                  pankratz_2005_10=lambda df:
                  din.dinamize_as_pankratz(df.depot_location_x,
                                           df.depot_location_y,
                                           df.pickup_location_x_coord,
                                           df.pickup_location_y_coord,
                                           df.delivery_location_x_coord,
                                           df.delivery_location_y_coord,
                                           df.pickup_upper_tw,
                                           df.delivery_upper_tw,
                                           df.pickup_service_time,
                                           1.00),
                  fabri_rencht_2006=lambda df:
                  din.dinamize_as_fabri_recht(df.pickup_location_x_coord,
                                              df.pickup_location_y_coord,
                                              df.delivery_location_x_coord,
                                              df.delivery_location_y_coord,
                                              df.pickup_lower_tw,
                                              df.delivery_upper_tw)
                  )
    )
    columns = list(df.columns)
    id_vars = columns[:len(static_atributes)]
    value_vars = columns[len(static_atributes):]
    df_tidy = (
        df.melt(id_vars=id_vars, value_vars=value_vars,
                var_name='dinamizator', value_name='arrival_time')
          .assign(dinamizator_short=lambda x:
                  x.dinamizator.str.extract(r'(\w*\d{4})', expand=False))
    )
    return df_tidy
