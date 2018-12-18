import pandas as pd
import numpy as np

df = pd.read_pickle('df_requests.zip')
# fix inf values represented as NaN
df.vehicle_capacity.fillna(np.inf, inplace=True)
df.max_ride_time.fillna(np.inf, inplace=True)

hdf = df.set_index(['problem', 'benchmark', 'instance', 'id']).sort_index()
