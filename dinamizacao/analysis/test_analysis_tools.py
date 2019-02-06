import pandas as pd
import importlib
analysis_tools = importlib.import_module('analysis_tools')

df = pd.read_csv('df_test.csv')
hdf = analysis_tools.calculate_dynamism(df)

assert hdf.groupby(['instance']).dynamism.max().a == 0.5
assert hdf.groupby(['instance']).dynamism.max().b - 0.276 < 0.001
