import pandas as pd
import numpy as np

columns_to_group = ['problem', 'benchmark', 'instance']
df = pd.read_pickle('df_requests.zip')
# fix inf values represented as NaN
df.vehicle_capacity.fillna(np.inf, inplace=True)
df.max_ride_time.fillna(np.inf, inplace=True)
# count the number of request for each instance
df = (df.assign(number_of_requests=df.groupby(columns_to_group)
                .id.transform('count'))
      )

df_grouped = df.groupby(columns_to_group)

# check for any null value in df
assert df.notnull().all().all(), 'There are null values in the DataFrame'
# check if count is correct
assert (df_grouped.id.count() == df_grouped.number_of_requests.max()).all()

hdf = (
    df.set_index(['problem', 'benchmark', 'instance', 'id'])
    .sort_values(['problem', 'benchmark', 'instance', 'arrival_time'])
    .assign(interarrival=lambda x:
            x.groupby(['problem', 'benchmark', 'instance'])
             .arrival_time.diff(periods=-1)*(-1))
    .assign(perfect_interarrival=lambda x:
            x.planing_horizon / x.number_of_requests)
)

last_values = None
info_by_index = {'interarrival_gap': {},
                 'perfect_interarrival_gap': {}
                 }
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
                * info_by_index.get('interarrival_gap').get(last_values.Index)

            info_by_index.get('perfect_interarrival_gap')[values.Index] = \
                values.perfect_interarrival \
                + ((values.perfect_interarrival - values.interarrival)
                    / values.perfect_interarrival) \
                * info_by_index.get('interarrival_gap').get(last_values.Index)

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
               / x.groupby(columns_to_group).perfect_interarrival_gap.sum())
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
assert hdf[~mask].shape[0] == df_grouped.id.count().shape[0]
