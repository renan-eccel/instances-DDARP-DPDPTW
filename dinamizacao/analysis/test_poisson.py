import pandas as pd
import numpy as np
import analysis_tools


def create_df_poisson(number_of_instances, number_of_requests_desired,
                      planing_horizon):
    '''
    Create a poisson bechmark for the a generic DVRP
    params:
        number_of_requests
        planing_horizon
        number_of_instances
    return:
        pandas.DataFrame with calculated dynamism
    '''
    def build_arrival_time_column(df):
        arrival_time_list = []
        for name, group in df.groupby('instance'):
            last_interarrival = 0
            for row in group.itertuples():
                new_interarrival = last_interarrival + row.interarrival
                arrival_time_list.append(new_interarrival)
                last_interarrival = new_interarrival
        return df.assign(arrival_time=arrival_time_list)

    lambda_poisson = number_of_requests_desired / planing_horizon

    exp_beta = 1 / lambda_poisson

    id_list = (
        [1 + i for i in range(number_of_requests_desired)]
        * number_of_instances
    )

    instance_list = (
        [1 + int(i/number_of_requests_desired)
         for i in range(number_of_instances * number_of_requests_desired)]
    )
    array_interarrivals = (
        np.random.exponential(exp_beta,
                              size=number_of_instances
                              * number_of_requests_desired)
    )
    data = {
        'problem': 'gdvrp',
        'benchmark': 'poisson_test',
        'instance': instance_list,
        'id': id_list,
        'planing_horizon': planing_horizon,
        'interarrival': list(array_interarrivals)
    }

    df = (
        pd.DataFrame(data)
          .pipe(build_arrival_time_column)

          .loc[lambda x: x.arrival_time <= planing_horizon]
          .assign(number_of_requests=lambda x:
                  x.groupby(['problem', 'benchmark', 'instance'],
                            as_index=False).arrival_time.transform('count'))
          .loc[lambda x: x.number_of_requests == number_of_requests_desired]
          .pipe(analysis_tools.calculate_dynamism, 'planing_horizon')
    )
    return df
