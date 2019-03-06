import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('ticks')


def histplot_by_benchmark(hdf, column, folder,
                          perfect_interarrival_parameter):
    from scipy.stats import expon
    g = sns.FacetGrid(hdf, col='citation', hue='citation', sharey=False,
                      sharex=False, palette='colorblind', despine=False,
                      col_wrap=3, height=2.5, aspect=1.5)
    g.map(sns.distplot, column,  fit=expon, kde=False)
    g.set_titles('{col_name}')
    plt.tight_layout()
    plt.savefig(folder + column + '_hist_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def scatterplot_by_benchmark(hdf, x_column, y_column, folder,
                             perfect_interarrival_parameter):
    g = sns.FacetGrid(hdf, col='citation', hue='citation', sharey=False,
                      palette='colorblind', despine=False, xlim=(0, 1),
                      col_wrap=3, height=2.5,
                      aspect=1.5)
    g.map(plt.scatter, x_column, y_column, s=0.5)
    g.set_titles('{col_name}')
    plt.tight_layout()
    plt.savefig(folder + x_column + '_x_' + y_column + '_scatterplot_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def pairplot_by_benchmark(hdf, columns, folder,
                          perfect_interarrival_parameter):
    hdf_metrics = hdf.loc[:, columns]
    for benchmark in hdf_metrics.index.levels[1]:
        plot = sns.pairplot(hdf_metrics.filter(like=benchmark, axis=0))
        plot.axes[0, 0].set_ylim(0, 1)
        plot.axes[0, 0].set_xlim(0, 1)
        plt.savefig(folder + 'pairplot_' + benchmark + '_'
                    + perfect_interarrival_parameter
                    + '.png')
        plt.close()


def boxplot_by_benchmark(hdf, column, figsize, folder,
                         perfect_interarrival_parameter):
    fig, ax = plt.subplots(figsize=figsize)
    sns.boxplot(x=column, y='citation', data=hdf, ax=ax,
                palette='colorblind')
    if column == 'dynamism':
        ax.set_xlim(0, 1)
    ax.set_ylabel('')
    plt.tight_layout()
    plt.savefig(folder + column + '_boxplot_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def plot_figures(hdf, columns_to_group, folder,
                 perfect_interarrival_parameter):

    # create an histogram for each bechmark showing the distribution of request
    # numbers over the planing_horizon
    histplot_by_benchmark(hdf, 'arrival_time', folder,
                          perfect_interarrival_parameter)

    # create an histogram for each benchmark showing the distribution of
    # interarrivals
    histplot_by_benchmark(hdf, 'interarrival', folder,
                          perfect_interarrival_parameter)

    # create a dataframe to analyse dynamism and urgency measures for each
    # instance
    hdf_instances = (
        hdf.loc[:, ['citation', 'dynamism', 'urgency_mean', 'urgency_std']]
           .groupby(columns_to_group + ['citation']).max().reset_index()
    )

    # create a boxplot graph for the dynamism in each benchmark and save it
    boxplot_by_benchmark(hdf_instances, 'dynamism', (10, 4), folder,
                         perfect_interarrival_parameter)

    # create a boxplot for the urgency in each benchmark and save it
    # boxplot_by_benchmark(hdf_instances, 'urgency_mean', (12, 7), folder,
    #                    perfect_interarrival_parameter)

    # create scatterplts with dynamism x urgency values for each benchmark
    scatterplot_by_benchmark(hdf, 'dynamism', 'urgency', folder,
                             perfect_interarrival_parameter)

    # create pairplot with dynamism x urgency x scale for each benchmark
# pairplot_by_benchmark(hdf, ['dynamism', 'urgency', 'requests_per_vehicle'],
    #                     folder, perfect_interarrival_parameter)
    plt.close('all')
