import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import analysis_tools
import seaborn as sns
import test_poisson


def calculate_dynamism_and_urgency(df, perfect_interarrival_parameter):
    hdf = (
        df.pipe(analysis_tools.calculate_dynamism,
                perfect_interarrival_parameter)
        .pipe(analysis_tools.calculate_urgency)
        .assign(urgency_mean=lambda x:
                x.groupby(columns_to_group).urgency.mean())
        .assign(urgency_std=lambda x:
                x.groupby(columns_to_group).urgency.std())
        .assign(lam_poisson=lambda x:
                (x.number_of_requests / x.planing_horizon)
                .groupby(columns_to_group).max())
    )
    return hdf


def histplot_by_benchmark(hdf, column, figsize,
                          perfect_interarrival_parameter):
    f, axes = plt.subplots(3, 2, figsize=figsize)
    for i in range(3):
        for j in range(2):
            benchmark = hdf.index.levels[1][2*i + j]
            ax = axes[i, j]
            ax.set_title(benchmark)
            sns.distplot(hdf[column].dropna().filter(like=benchmark),
                         ax=ax)

    plt.savefig('./figures/' + column + '_hist_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def plot_figures(hdf, figsize, perfect_interarrival_parameter):

    # create an histogram for each bechmark showing the distribution of request
    # numbers over the planing_horizon
    histplot_by_benchmark(hdf, 'arrival_time', figsize,
                          perfect_interarrival_parameter)

    # create an histogram for each benchmark showing the distribution of
    # interarrivals
    histplot_by_benchmark(hdf, 'interarrival', figsize,
                          perfect_interarrival_parameter)

    # create a dataframe to analyse dynamism and urgency measures for each
    # instance
    hdf_instances = hdf.loc[:, ['dynamism', 'urgency_mean',
                                'urgency_std']].groupby(columns_to_group).max()

    # create a boxplot graph for the dynamism in each benchmark and save it
    hdf_instances.boxplot(column='dynamism', by='benchmark',
                          figsize=figsize).set_ylim(0, 1)
    plt.savefig('./figures/dynamism_boxplot_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')

    # create a boxplot for the urgency in each benchmark and save it
    hdf_instances.boxplot(column='urgency_mean', by='benchmark',
                          figsize=figsize)
    plt.savefig('./figures/urgency_boxplot_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')

    plt.close('all')


def build_poisson_generated_scenarios(hdf, perfect_interarrival_parameter):
    def get_parametes_values(hdf, perfect_interarrival_parameter, func):
        parameters = (
            getattr(
                hdf.loc[:, [perfect_interarrival_parameter,
                            'number_of_requests']]
                .groupby(['problem', 'benchmark']), func)()
        )
        return parameters
    functions = ['min', 'mean', 'max']
    df_poisson = pd.DataFrame()
    for function in functions:
        parameters = get_parametes_values(hdf, perfect_interarrival_parameter,
                                          function)
        for values in parameters.itertuples():
            df_poisson = df_poisson.append(
                test_poisson.create_dynamism_sample(
                    20,
                    int(values.number_of_requests),
                    getattr(values, perfect_interarrival_parameter),
                    values.Index[0],
                    values.Index[1]
                ).assign(statistic=function)
            )
    return df_poisson


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

hdf = calculate_dynamism_and_urgency(df, perfect_interarrival_parameter)

plot_figures(hdf, (15, 7), perfect_interarrival_parameter)

df_poisson = build_poisson_generated_scenarios(hdf,
                                               perfect_interarrival_parameter)



