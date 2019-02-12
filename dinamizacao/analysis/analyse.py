import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import analysis_tools
import test_poisson

df = pd.read_pickle('df_requests.zip')

columns_to_group = ['problem', 'benchmark', 'instance']
# fix inf values represented as NaN
df.vehicle_capacity.fillna(np.inf, inplace=True)
df.max_ride_time.fillna(np.inf, inplace=True)
# count the number of requests for each instance
df = (df.assign(number_of_requests=df.groupby(columns_to_group)
                .id.transform('count'))
      )
df_grouped = df.groupby(columns_to_group)

# check for any null value in df
assert df.notnull().all().all(), 'There are null values in the DataFrame'
# check if count is correct
assert (df_grouped.id.count() == df_grouped.number_of_requests.max()).all()

perfect_interarrival_parameter = 'planing_horizon'
hdf = (
    df.pipe(analysis_tools.calculate_dynamism, perfect_interarrival_parameter)
    .pipe(analysis_tools.calculate_urgency)
    .assign(urgency_mean=lambda x: x.groupby(columns_to_group).urgency.mean())
    .assign(urgency_std=lambda x: x.groupby(columns_to_group).urgency.std())
    # .assign(poisson_lam=lambda x: (x.number_of_requests / x.planing_horizon)
    #        .groupby(columns_to_group).max())
    # .assign(poisson_sample=lambda x: np.random.poisson(x.poisson_lam))
)

# create a dataframe to analyse dynamism and urgency measures for each
# instance
hdf_instances = hdf.loc[:, ['dynamism', 'urgency_mean',
                            'urgency_std']].groupby(columns_to_group).max()

# create an histogram for each bechmark showing the distribution of request
# numbers over the planing_horizon
hdf.arrival_time.hist(by='benchmark', figsize=(20, 10))
plt.savefig('./figures/arrival_times_hist_by_benchmark.png')

# create a boxplot graph for the dynamism in each benchmark and save it
hdf_instances.boxplot(column='dynamism',
                      by='benchmark',
                      figsize=(20, 10)).set_ylim(0, 1)
plt.savefig('./figures/dynamism_by_benchmark_' + perfect_interarrival_parameter
            + '.png')

# create a boxplot for the urgency in each benchmark and save it
hdf_instances.boxplot(column='urgency_mean', by='benchmark', figsize=(20, 10))
plt.savefig('./figures/urgency_by_benchmark_' + perfect_interarrival_parameter
            + '.png')

# test_poisson for the benchmarks contained in the hdf dataframe
hdf_poisson_test = hdf.loc[:, ['number_of_requests', 'planing_horizon']]
