import pandas as pd


def calculate_dynamism(df, perfect_interarrival_parameter):
    '''
    Calculate the dynamism measure proposed by van_lon_2016
    params:
        df
        perfect_interarrival_parameter: choose between 'planing_horizon' or
                                        'arrival_horizon'
    '''
    columns_to_group = ['problem', 'benchmark', 'instance']

    hdf = (
        df.set_index(['problem', 'benchmark', 'instance', 'id'])
        .sort_values(['problem', 'benchmark', 'instance', 'arrival_time'])
        .assign(arrival_horizon=lambda x:
                x.groupby(['problem', 'benchmark']).arrival_time.max()
                - x.groupby(['problem', 'benchmark']).arrival_time.min())
        .assign(interarrival=lambda x:
                x.groupby(['problem', 'benchmark', 'instance'])
                 .arrival_time.diff(periods=-1)*(-1))
        .assign(perfect_interarrival=lambda x:
                x[perfect_interarrival_parameter] / x.number_of_requests)
    )

    last_values = None
    info_by_index = {'interarrival_gap': {},
                     'perfect_interarrival_gap': {}
                     }
    '''
    Calculate the interarrival_gap and the perfect_interarrival_gap for each
    request. This values are designeted by a piece-wise function which
    independent variables are: interarrival,perfect_interarrival and the
    previous interarrival_gap.

    For better understandig please read session 4.3 of van_lon_2016
    '''
    for values in hdf.itertuples():
        if str(values.interarrival) == 'nan':
            # Case nan
            info_by_index.get('interarrival_gap')[values.Index] = None
            info_by_index.get('perfect_interarrival_gap')[values.Index] = None

        elif values.interarrival < values.perfect_interarrival:
            if last_values is None:
                # Case 1, first row of the instance (i==0)
                info_by_index.get('interarrival_gap')[values.Index] = \
                    values.perfect_interarrival - values.interarrival

                info_by_index.get('perfect_interarrival_gap')[values.Index] = \
                    values.perfect_interarrival

            elif str(last_values.interarrival) == 'nan':
                # Case 1, other rows (i==0)
                info_by_index.get('interarrival_gap')[values.Index] = \
                    values.perfect_interarrival - values.interarrival

                info_by_index.get('perfect_interarrival_gap')[values.Index] = \
                    values.perfect_interarrival

            else:
                # Case 2 (i>0)
                info_by_index.get('interarrival_gap')[values.Index] = \
                    values.perfect_interarrival - values.interarrival \
                    + ((values.perfect_interarrival - values.interarrival)
                        / values.perfect_interarrival) \
                    * info_by_index.get('interarrival_gap').get(
                        last_values.Index)

                info_by_index.get('perfect_interarrival_gap')[values.Index] = \
                    values.perfect_interarrival \
                    + ((values.perfect_interarrival - values.interarrival)
                        / values.perfect_interarrival) \
                    * info_by_index.get('interarrival_gap').get(
                        last_values.Index)

        else:
            # Case 3, otherwise
            info_by_index.get('interarrival_gap')[values.Index] = 0
            info_by_index.get('perfect_interarrival_gap')[values.Index] = \
                values.perfect_interarrival
        last_values = values

    # check if all rows of the dataframe resulted in an interarrival_deviation
    assert hdf.shape[0] == len(info_by_index.get('interarrival_gap'))
    assert hdf.shape[0] == len(info_by_index.get('perfect_interarrival_gap'))

    interarrival_gap = pd.Series(info_by_index.get('interarrival_gap'))
    perfect_interarrival_gap = pd.Series(info_by_index.get(
        'perfect_interarrival_gap'))
    hdf = (
        hdf.assign(interarrival_gap=interarrival_gap)
           .assign(perfect_interarrival_gap=perfect_interarrival_gap)
           .assign(dynamism=lambda x: 1
                   - x.groupby(columns_to_group).interarrival_gap.sum()
                   / x.groupby(columns_to_group).perfect_interarrival_gap
                                                .sum())
    )

    # check if correlation between perfect_interval and perfect_interval_gap is
    # valid
    mask = (hdf.interarrival_gap
            + hdf.perfect_interarrival
            - hdf.perfect_interarrival_gap
            < 0.01) | \
           (hdf.interarrival_gap
            + hdf.interarrival
            - hdf.perfect_interarrival_gap
            < 0.01)
    df_grouped = df.groupby(columns_to_group)
    assert hdf[~mask].shape[0] == df_grouped.id.count().shape[0]
    return(hdf)


def calculate_urgency(df):
    '''
    Calculate the urgency of each request using the following equation:
        urgency = pickup_uppper_tw - arrival_time
    '''
    return df.assign(urgency=lambda x: x.pickup_upper_tw - x.arrival_time)


def calculate_requests_per_vehicle(df):
    '''
    Calculate the scale of each request using the following equation:
        scale = number_of_requests / number_of_vehicles
    '''
    df_out = (
        df.copy()
        .assign(number_of_vehicles=lambda x:
                pd.to_numeric(x.number_of_vehicles.astype(str).str
                              .extract(r'^(\d*)', expand=False)))
        .assign(requests_per_vehicle=lambda x: x.number_of_requests
                / x.number_of_vehicles)
    )
    return df_out
