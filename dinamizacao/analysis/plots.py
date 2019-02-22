import matplotlib.pyplot as plt
import seaborn as sns


def histplot_by_benchmark(hdf, column, figsize,
                          perfect_interarrival_parameter):
    f, axes = plt.subplots(3, 2, figsize=figsize)
    for i in range(3):
        for j in range(2):
            benchmark = hdf.index.levels[1][2*i + j]
            ax = axes[i, j]
            ax.set_title(benchmark)
            sns.distplot(hdf[column].dropna().filter(like=benchmark),
                         ax=ax,
                         norm_hist=True)
    plt.savefig('./figures/' + column + '_hist_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def scatterplot_by_benchmark(hdf, x_column, y_column, figsize,
                             perfect_interarrival_parameter):
    f, axes = plt.subplots(3, 2, figsize=figsize)
    for i in range(3):
        for j in range(2):
            benchmark = hdf.index.levels[1][2*i + j]
            ax = axes[i, j]
            ax.set_title(benchmark)
            (hdf.reset_index().loc[lambda x: x.benchmark == benchmark]
             .plot(x=x_column, y=y_column, kind='scatter',
                   ax=ax))

    plt.savefig('./figures/' + x_column + '_x_' + y_column + '_scatterplot_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def plot_figures(hdf, figsize, columns_to_group,
                 perfect_interarrival_parameter):

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

    # create scatterplts with dynamism x urgency values for each benchmark
    scatterplot_by_benchmark(hdf, 'dynamism', 'urgency', (15, 15),
                             perfect_interarrival_parameter)
    plt.close('all')
