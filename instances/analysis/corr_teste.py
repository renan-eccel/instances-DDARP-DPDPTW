import pandas as pd
import numpy as np

df_corr = (pd.DataFrame(np.random.random_sample(10**3), columns=['x'])
             .assign(y=lambda x: np.random.uniform(0, x.x)))
value = df_corr.corr().reset_index().iloc[0, 2]
print('base correlation coefficient: ' + str(value))
