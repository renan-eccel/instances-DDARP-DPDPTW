import pandas as pd

df = pd.read_pickle('df_requests.zip')
hdf = df.set_index(['problem', 'benchmark', 'instance', 'id']).sort_index()
