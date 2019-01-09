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
interarrival_gap_by_index = {}
for values in hdf.itertuples():
    if values.interarrival < values.perfect_interarrival:
        if last_values is None:
            # Case 1
            interarrival_gap_by_index[values.Index] = \
                values.perfect_interarrival - values.interarrival
        elif str(last_values.interarrival) == 'nan':
            # Case 2
            interarrival_gap_by_index[values.Index] = \
                values.perfect_interarrival - values.interarrival
        else:
            # Case 3
            interarrival_gap_by_index[values.Index] = \
                values.perfect_interarrival - values.interarrival \
                + ((values.perfect_interarrival - values.interarrival)
                    / values.perfect_interarrival) \
                * interarrival_gap_by_index.get(last_values.Index)

    else:
        # Case 0
        interarrival_gap_by_index[values.Index] = 0
    last_values = values

# check if all rows of the dataframe resulted in an interarrival_deviation
assert hdf.shape[0] == len(interarrival_gap_by_index)

interarrival_gap = pd.Series(interarrival_gap_by_index)
