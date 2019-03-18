import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set_style('ticks')


def frequency_hist(series, xlim=None):
    weights = np.ones_like(series) / len(series)
    ax = series.hist(weights=weights)
    ax.set_ylabel('Frequência')
    ax.set_xlim(xlim)
    return ax


def column_hist(hdf, column, column_plt, benchmark, folder,
                perfect_interarrival_parameter):
    upper_xlim = (
        hdf[perfect_interarrival_parameter].filter(like=benchmark).max()
    )
    ax = (
        hdf[column].filter(like=benchmark)
                   .pipe(frequency_hist, (0, upper_xlim))
    )
    ax.set_xlabel(column_plt)
    plt.tight_layout()
    plt.savefig(folder + 'hist_' + column + '_' + benchmark + '_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def histplot_by_benchmark(hdf, column, column_plt, folder,
                          perfect_interarrival_parameter, fit=None,
                          upper_xlims=None):

    def set_xlim_for_axes(axes, x_upper_lims):
        for i in range(len(axes)):
            axes[i].set_xlim(0, x_upper_lims[i])

    hdf_notnull = hdf.dropna(subset=[column])
    g = sns.FacetGrid(hdf_notnull, col='citation', hue='citation',
                      sharey=False, sharex=False, palette='colorblind',
                      despine=False, col_wrap=3, height=2.5, aspect=1.5)
    g.map(sns.distplot, column,  fit=fit, kde=False)
    g.set_titles('{col_name}')
    g.set_xlabels(column_plt)
    axes = g.axes
    if upper_xlims is not None:
        set_xlim_for_axes(axes, upper_xlims)
    plt.tight_layout()
    plt.savefig(folder + 'hist_' + column + '_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def scatterplot_by_benchmark(hdf, x_column, y_column, x_column_plt,
                             y_column_plt, folder,
                             perfect_interarrival_parameter):
    g = sns.FacetGrid(hdf, col='citation', hue='citation', sharey=False,
                      palette='colorblind', despine=False, xlim=(0, 1),
                      col_wrap=3, height=2.5,
                      aspect=1.5)
    g.map(plt.scatter, x_column, y_column, s=0.5)
    g.set_titles('{col_name}')
    g.set_xlabels(x_column_plt)
    g.set_ylabels(y_column_plt)
    plt.tight_layout()
    plt.savefig(folder + 'scatterplot_' + x_column + '_x_' + y_column + '_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def pairplot_by_benchmark(hdf, columns, columns_plt, folder,
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


def boxplot_by_benchmark(hdf, column, column_plt, folder,
                         perfect_interarrival_parameter):
    figsize = (10, 4)
    fig, ax = plt.subplots(figsize=figsize)
    sns.boxplot(x=column, y='citation', data=hdf, ax=ax,
                palette='colorblind')
    if column == 'dynamism':
        ax.set_xlim(0, 1)
    ax.set_ylabel('')
    ax.set_xlabel(column_plt)
    plt.tight_layout()
    plt.savefig(folder + 'boxplot_' + column + '_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def plot_figures(hdf, columns_to_group, folder,
                 perfect_interarrival_parameter):
    dynamisnm_plt = 'Dinamismo'
    urgency_plt = 'Urgência (min)'
    urgency_mean_plt = 'Urgência média (min)'
    interarrival_plt = 'Intervalo entre chegadas (min)'
    arrival_time_plt = 'Instante de chegada (min)'
    # requests_per_vehicles_plt = 'N. de pedidos por veículos'

    # create an histogram for each bechmark showing the distribution of request
    # numbers over the planing_horizon
    upper_xlims = list(hdf.groupby(['problem', 'benchmark']).planing_horizon
                       .max())
    histplot_by_benchmark(hdf, 'arrival_time', arrival_time_plt, folder,
                          perfect_interarrival_parameter,
                          upper_xlims=upper_xlims)

    # create an histogram for each benchmark showing the distribution of
    # interarrivals
    from scipy.stats import expon
    histplot_by_benchmark(hdf, 'interarrival', interarrival_plt, folder,
                          perfect_interarrival_parameter, fit=expon)

    # create a dataframe to analyse dynamism and urgency measures for each
    # instance
    hdf_instances = (
        hdf.loc[:, ['citation', 'dynamism', 'urgency_mean', 'urgency_std']]
           .groupby(columns_to_group + ['citation']).max().reset_index()
    )

    # create a boxplot graph for the dynamism in each benchmark and save it
    boxplot_by_benchmark(hdf_instances, 'dynamism', dynamisnm_plt, folder,
                         perfect_interarrival_parameter)

    # create a boxplot for the urgency in each benchmark and save it
    boxplot_by_benchmark(hdf_instances, 'urgency_mean', urgency_plt, folder,
                         perfect_interarrival_parameter)

    # create scatterplts with dynamism x urgency values for each benchmark
    # each point represents an instance
    scatterplot_by_benchmark(hdf_instances, 'dynamism', 'urgency_mean',
                             dynamisnm_plt, urgency_mean_plt, folder,
                             perfect_interarrival_parameter)

    # create scatterplts with dynamism x urgency values for each benchmark
    # each point represents a request
    scatterplot_by_benchmark(hdf, 'dynamism', 'urgency',
                             dynamisnm_plt, urgency_plt, folder,
                             perfect_interarrival_parameter)

    # create an arrival_time histogram for berbeglia
    column_hist(hdf, 'arrival_time', arrival_time_plt, 'berbeglia', folder,
                perfect_interarrival_parameter)

    # create an urgency histogram for berbeglia
    column_hist(hdf, 'urgency', urgency_plt, 'berbeglia', folder,
                perfect_interarrival_parameter)

    # create an arrival_time histogram for fabri_and_recht
    column_hist(hdf, 'arrival_time', arrival_time_plt, 'fabri', folder,
                perfect_interarrival_parameter)

    # create an urgency histogram for berbeglia
    column_hist(hdf, 'urgency', arrival_time_plt, 'fabri', folder,
                perfect_interarrival_parameter)

    # create pairplot with dynamism x urgency x scale for each benchmark
    # pairplot_by_benchmark(hdf,
    #                       ['dynamism', 'urgency', 'requests_per_vehicle'],
    #                       [dynamisnm_plt, urgency_plt,
    #                        requests_per_vehicles_plt],
    #                       folder, perfect_interarrival_parameter)
    plt.close('all')
