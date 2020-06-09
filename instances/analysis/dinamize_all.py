import pandas as pd
import instances.dinamizators.dinamizators as din
import random

df = (
    pd.read_pickle('./instances/analysis/df_requests.zip')
      .reset_index()
      .rename({'arrival_time': 'original_arrival_time'}, axis=1)
      .assign(a_berbeglia_1=lambda df:
              din.dinamize_as_berbeglia(df.pickup_location_x_coord,
                                        df.pickup_location_y_coord,
                                        df.delivery_location_x_coord,
                                        df.delivery_location_y_coord,
                                        df.pickup_upper_tw,
                                        df.delivery_upper_tw,
                                        df.pickup_service_time,
                                        0,
                                        60),
              a_berbeglia_2=lambda df:
              din.dinamize_as_berbeglia(df.pickup_location_x_coord,
                                        df.pickup_location_y_coord,
                                        df.delivery_location_x_coord,
                                        df.delivery_location_y_coord,
                                        df.pickup_upper_tw,
                                        df.delivery_upper_tw,
                                        df.pickup_service_time,
                                        0,
                                        random.randint(60, 240)),
              a_pureza_laporte_1=lambda df:
              din.dinamize_as_pureza_laporte(df.depot_location_x,
                                             df.depot_location_y,
                                             df.pickup_location_x_coord,
                                             df.pickup_location_y_coord,
                                             df.pickup_lower_tw,
                                             df.pickup_upper_tw,
                                             0),
              a_pureza_laporte_2=lambda df:
              din.dinamize_as_pureza_laporte(df.depot_location_x,
                                             df.depot_location_y,
                                             df.pickup_location_x_coord,
                                             df.pickup_location_y_coord,
                                             df.pickup_lower_tw,
                                             df.pickup_upper_tw,
                                             100),
              a_pureza_laporte_3=lambda df:
              din.dinamize_as_pureza_laporte(df.depot_location_x,
                                             df.depot_location_y,
                                             df.pickup_location_x_coord,
                                             df.pickup_location_y_coord,
                                             df.pickup_lower_tw,
                                             df.pickup_upper_tw,
                                             200),
              a_pureza_laporte_4=lambda df:
              din.dinamize_as_pureza_laporte(df.depot_location_x,
                                             df.depot_location_y,
                                             df.pickup_location_x_coord,
                                             df.pickup_location_y_coord,
                                             df.pickup_lower_tw,
                                             df.pickup_upper_tw,
                                             300),
              )
)
