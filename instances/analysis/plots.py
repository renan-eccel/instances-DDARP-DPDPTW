import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import locale


def weighted_hist(x, weights, **kwargs):
    plt.hist(x, weights=weights, **kwargs)


def column_hist(hdf, column, column_plt, benchmark, folder,
                perfect_interarrival_parameter):
    upper_xlim = (
        hdf[perfect_interarrival_parameter].filter(like=benchmark).max()
    )
    series = hdf[column].filter(like=benchmark)
    weights = np.ones_like(series) / len(series)
    weighted_hist(series, weights)
    plt.ylabel('Frequência')
    plt.xlim((0, upper_xlim))
    plt.xlabel(column_plt)
    plt.tight_layout()
    plt.savefig(folder + 'hist_' + column + '_' + benchmark + '_'
                + perfect_interarrival_parameter
                + '.png')
    plt.savefig(folder + 'hist_' + column + '_' + benchmark + '_'
                + perfect_interarrival_parameter
                + '.eps')
    plt.close()


def histplot_by_benchmark(hdf, column, column_plt, folder,
                          perfect_interarrival_parameter,
                          upper_xlims=None, sharex=False,
                          sharey=False, ylim=None, xlim=None,
                          bins=10):

    def set_xlim_for_axes(axes, x_upper_lims):
        for i in range(len(axes)):
            axes[i].set_xlim(0, x_upper_lims[i])

    def create_weight_column(hdf):
        hdf_out = (
            hdf.copy()
               .assign(weight=lambda x: 1 / x.reset_index()
                       .groupby(['problem', 'benchmark'])
                       .id.count())
        )
        return hdf_out

    hdf_notnull = (
        hdf.dropna(subset=[column])
           .pipe(create_weight_column)
    )
    g = sns.FacetGrid(hdf_notnull, col='citation', hue='citation',
                      sharey=sharey, sharex=sharex, palette='colorblind',
                      despine=False, col_wrap=3, height=2.5, aspect=1.5,
                      ylim=ylim, xlim=xlim)
    g.map(weighted_hist, column, 'weight', bins=bins)
    g.set_titles('{col_name}')
    g.set_xlabels(column_plt)
    g.set_ylabels('Frequência')
    axes = g.axes
    if upper_xlims is not None:
        set_xlim_for_axes(axes, upper_xlims)
    plt.tight_layout()
    plt.savefig(folder + 'hist_' + column + '_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')
    plt.savefig(folder + 'hist_' + column + '_by_benchmark_'
                + perfect_interarrival_parameter
                + '.eps')
    plt.close()


def scatterplot_by_benchmark(hdf, x_column, y_column, x_column_plt,
                             y_column_plt, folder,
                             perfect_interarrival_parameter, ylim=None,
                             sharey=False):
    g = sns.FacetGrid(hdf, col='citation', hue='citation', sharey=sharey,
                      palette='colorblind', despine=False, xlim=(0, 1),
                      ylim=ylim, col_wrap=3, height=2.5, aspect=1.5)
    g.map(plt.scatter, x_column, y_column, s=0.5)
    g.set_titles('{col_name}')
    g.set_xlabels(x_column_plt)
    g.set_ylabels(y_column_plt)
    plt.tight_layout()
    plt.savefig(folder + 'scatterplot_' + x_column + '_x_' + y_column + '_'
                + perfect_interarrival_parameter
                + '.png')
    plt.savefig(folder + 'scatterplot_' + x_column + '_x_' + y_column + '_'
                + perfect_interarrival_parameter
                + '.eps')
    plt.close()


def jointplot(hdf, x_column, y_column, x_column_plt, y_column_plt, folder,
              perfect_interarrival_parameter):
    g = sns.jointplot(x=x_column, y=y_column, data=hdf)
    g.set_xlabel(x_column_plt)
    g.set_ylabel(y_column_plt)
    plt.tight_layout()
    return (g)


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
        plt.savefig(folder + 'pairplot_' + benchmark + '_'
                    + perfect_interarrival_parameter
                    + '.eps')
        plt.close()


def boxplot_by_benchmark(hdf, column, column_plt):
    figsize = (10, 4)
    fig, ax = plt.subplots(figsize=figsize)
    sns.boxplot(x=column, y='citation', data=hdf, ax=ax,
                palette='colorblind')
    if column == 'dynamism':
        ax.set_xlim(0, 1)
    ax.set_ylabel('')
    ax.set_xlabel(column_plt)


def boxplot_by_benchmark_save(hdf, column, column_plt, folder,
                              perfect_interarrival_parameter):
    boxplot_by_benchmark(hdf, column, column_plt)
    plt.tight_layout()
    plt.savefig(folder + 'boxplot_' + column + '_by_benchmark_'
                + perfect_interarrival_parameter
                + '.png')
    plt.savefig(folder + 'boxplot_' + column + '_by_benchmark_'
                + perfect_interarrival_parameter
                + '.eps')
    plt.close()


def scatterplot(hdf, benchmark, x_column, y_column, color, x_column_plt,
                y_column_plt, color_plt, folder,
                perfect_interarrival_parameter):
    hdf_benchmark = hdf.filter(like=benchmark, axis=0)
    g = sns.scatterplot(x=x_column, y=y_column, hue=color, data=hdf_benchmark)
    g.set_xlabel(x_column_plt)
    g.set_ylabel(y_column_plt)
    g.set_label(color_plt)
    plt.tight_layout()
    plt.savefig(folder + 'scatterplot_' + x_column + '_x_' + y_column + '_'
                + benchmark + '_' + perfect_interarrival_parameter
                + '.png')
    plt.savefig(folder + 'scatterplot_' + x_column + '_x_' + y_column + '_'
                + benchmark + '_' + perfect_interarrival_parameter
                + '.eps')
    plt.close()


def facetgrid_scatterplot(hdf, x_column, y_column, color, x_column_plt,
                          y_column_plt, color_plt, folder,
                          perfect_interarrival_parameter,
                          **kwargs):
    g = sns.FacetGrid(hdf, col='citation', col_wrap=3, sharey=False,
                      sharex=False, despine=False, height=2.5, aspect=1.5,
                      **kwargs)
    g = g.map(sns.scatterplot, x_column, y_column, color, sizes=(40, 40))
    g.set_xlabels(x_column_plt)
    g.set_ylabels(y_column_plt)
    g.set_titles('{col_name}')
    plt.savefig(folder + 'facetgrid_scatterplot_' + x_column + '_x_' + y_column
                + '_' + perfect_interarrival_parameter + '.png')
    plt.savefig(folder + 'facetgrid_scatterplot_' + x_column + '_x_' + y_column
                + '_' + perfect_interarrival_parameter + '.eps')
    plt.close()


def plot_figures(hdf, columns_to_group, folder,
                 perfect_interarrival_parameter):
    sns.set(style='ticks', font="Times New Roman", font_scale=1.35)
    locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')
    plt.rcParams.update({'axes.formatter.use_locale': True})
    dynamisnm_plt = 'Dinamismo'
    urgency_plt = 'Urgência (min)'
    urgency_norm_max_plt = 'Urgência normalizada'
    urgency_mean_plt = 'Urgência média\n' + '(min)'
    urgency_mean_norm_plt = 'Urgência média\n' + 'normalizada'
    interarrival_plt = 'Intervalo entre chegadas\n' + '(min)'
    arrival_time_plt = 'Instante de chegada\n' + '(min)'
    arrival_time_norm_h_plt = 'Instante de chegada\n' + 'normalizado'
    pickup_upper_tw_plt = ('Limite superior da janela\n'
                           + 'de tempo de coleta (min)')
    putw_norm_h_plt = ('Limite superior normalizado\n'
                       + 'da janela de tempo de coleta')
    pltw_norm_h_plt = ('Limite inferior normalizado\n'
                       + 'da janela de tempo de coleta')
    pickup_lower_tw_plt = ('Limite inferior da janela\n'
                           + 'de tempo de coleta (min)')
    inter_mean_plt = 'Intervalo médio entre\n' + 'chegadas de pedidos (min)'
    inter_mean_norm_plt = inter_mean_plt + ' normalizada'
    # requests_per_vehicles_plt = 'N. de pedidos por veículos'

    # create an histogram for each bechmark showing the distribution of request
    # numbers over the planing_horizon
    histplot_by_benchmark(hdf, 'arrival_time', arrival_time_plt, folder,
                          perfect_interarrival_parameter,
                          bins=np.arange(0, 1, 0.1))

    # create an histogram for each bechmark showing the distribution of request
    # numbers over the planing_horizon
    histplot_by_benchmark(hdf, 'arrival_time_norm_h', arrival_time_norm_h_plt,
                          folder, perfect_interarrival_parameter,
                          ylim=(0, 0.75), xlim=(-0.05, 1),
                          bins=np.arange(0, 1, 0.1))

    # create an histogram for each benchmark showing the distribution of
    # pickup_lower_tw
    histplot_by_benchmark(hdf, 'pickup_lower_tw', pickup_lower_tw_plt,
                          folder, perfect_interarrival_parameter)

    # create an histogram for each benchmark showing the distribution of
    # pltw_norm_h
    histplot_by_benchmark(hdf, 'pltw_norm_h', pltw_norm_h_plt,
                          folder, perfect_interarrival_parameter,
                          ylim=(0, 0.75), xlim=(-0.05, 1),
                          bins=np.arange(0, 1, 0.1))

    # create an histogram for each benchmark showing the distribution of
    # putw_norm_h
    histplot_by_benchmark(hdf, 'putw_norm_h', putw_norm_h_plt,
                          folder, perfect_interarrival_parameter,
                          ylim=(0, 0.75), xlim=(-0.05, 1),
                          bins=np.arange(0, 1, 0.1))

    # create an histogram for each benchmark showing the distribution of
    # real_pltw_norm_h
    histplot_by_benchmark(hdf, 'real_pltw_norm_h', pltw_norm_h_plt,
                          folder, perfect_interarrival_parameter,
                          ylim=(0, 0.75), xlim=(-0.05, 1),
                          bins=np.arange(0, 1, 0.1))

    # create an histogram for each benchmark showing the distribution of
    # pickup_lower_tw
    histplot_by_benchmark(hdf, 'pickup_upper_tw', pickup_upper_tw_plt,
                          folder, perfect_interarrival_parameter)

    # create an histogram for each benchmark showing the distribution of
    # urgency values
    histplot_by_benchmark(hdf, 'urgency', urgency_plt, folder,
                          perfect_interarrival_parameter)

    # create an histogram for each benchmark showing the distribution of
    # interarrivals
    histplot_by_benchmark(hdf, 'interarrival', interarrival_plt, folder,
                          perfect_interarrival_parameter)

    # create a dataframe to analyse dynamism and urgency measures for each
    # instance
    hdf_instances = (
        hdf.loc[:, ['citation', 'dynamism', 'urgency_mean', 'urgency_std',
                    'inter_mean_norm', 'planing_horizon']]
           .assign(urgency_mean_norm_max=lambda x:
                   x.urgency_mean
                   / x.groupby(level='benchmark').urgency_mean.max())
           .groupby(columns_to_group + ['citation']).max().reset_index()
    )

    # create a boxplot graph for the dynamism in each benchmark and save it
    boxplot_by_benchmark_save(hdf_instances, 'dynamism', dynamisnm_plt,
                              folder, perfect_interarrival_parameter)

    # create a boxplot for the urgency mean in each benchmark and save it
    boxplot_by_benchmark_save(hdf_instances, 'urgency_mean', urgency_plt,
                              folder, perfect_interarrival_parameter)

    # create a boxplot for the urgency mean normalized in each benchmark
    # and save it
    boxplot_by_benchmark_save(hdf_instances, 'urgency_mean_norm_max',
                              urgency_mean_norm_plt, folder,
                              perfect_interarrival_parameter)

    # create a boxplot for the urgency in each benchmark and save it
    boxplot_by_benchmark_save(hdf_instances, 'inter_mean_norm',
                              inter_mean_norm_plt, folder,
                              perfect_interarrival_parameter)

    # create a histogram with interarrivals mean values for each benchmark
    histplot_by_benchmark(hdf, 'inter_mean', inter_mean_plt, folder,
                          perfect_interarrival_parameter)

    # create a histogram with interarrivals mean values normalized for
    # each benchmark
    histplot_by_benchmark(hdf, 'inter_mean_norm', inter_mean_norm_plt, folder,
                          perfect_interarrival_parameter, sharex=True)

    # create scatterplts with dynamism x urgency_mean values for each
    # benchmark, each point represents an instance
    scatterplot_by_benchmark(hdf_instances, 'dynamism', 'urgency_mean',
                             dynamisnm_plt, urgency_mean_plt, folder,
                             perfect_interarrival_parameter)

    # create scatterplts with dynamism x urgency_mean_norm_max
    # values for each benchmark, each point represents an instance
    scatterplot_by_benchmark(hdf_instances, 'dynamism',
                             'urgency_mean_norm_max',
                             dynamisnm_plt, urgency_mean_norm_plt, folder,
                             perfect_interarrival_parameter, ylim=(0, 1),
                             sharey=True)

    # create scatterplts with dynamism x urgency values for each benchmark
    # each point represents a request
    scatterplot_by_benchmark(hdf, 'dynamism', 'urgency',
                             dynamisnm_plt, urgency_plt, folder,
                             perfect_interarrival_parameter)

    # create a real_pltw_norm_h x arrival_time_norm_h for each benchmark
    facetgrid_scatterplot(hdf, 'real_pltw_norm_h', 'arrival_time_norm_h',
                          'urgency_norm_max',
                          pltw_norm_h_plt, arrival_time_norm_h_plt,
                          urgency_norm_max_plt, folder,
                          perfect_interarrival_parameter,
                          xlim=(-0.05, 1),
                          ylim=(0, 1))

    # create a putw_norm_h x arrival_time_norm_h for each benchmark
    facetgrid_scatterplot(hdf, 'putw_norm_h', 'arrival_time_norm_h',
                          'urgency_norm_max',
                          putw_norm_h_plt, arrival_time_norm_h_plt,
                          urgency_norm_max_plt, folder,
                          perfect_interarrival_parameter,
                          xlim=(-0.05, 1),
                          ylim=(0, 1))

    # create a pickup_upper_tw x arrival_time for berbelgia
    scatterplot(hdf, 'berbeglia', 'pickup_upper_tw', 'arrival_time', 'urgency',
                pickup_upper_tw_plt, arrival_time_plt, urgency_plt, folder,
                perfect_interarrival_parameter)

    # create a pickup_lower_tw x arrival_time for pureza
    scatterplot(hdf, 'pureza', 'pickup_lower_tw', 'arrival_time', 'urgency',
                pickup_lower_tw_plt, arrival_time_plt, urgency_plt, folder,
                perfect_interarrival_parameter)

    # create a pickup_upper_tw x arrival_time for pankratz
    scatterplot(hdf, 'pankratz', 'pickup_upper_tw', 'arrival_time', 'urgency',
                pickup_upper_tw_plt, arrival_time_plt, urgency_plt, folder,
                perfect_interarrival_parameter)

    # create a pickup_lower_tw x arrival_time for fabri
    scatterplot(hdf, 'fabri', 'pickup_lower_tw', 'arrival_time', 'urgency',
                pickup_lower_tw_plt, arrival_time_plt, urgency_plt, folder,
                perfect_interarrival_parameter)

    # create a pickup_lower_tw x arrival_time for gendreau
    scatterplot(hdf, 'gendreau', 'pickup_lower_tw', 'arrival_time', 'urgency',
                pickup_lower_tw_plt, arrival_time_plt, urgency_plt, folder,
                perfect_interarrival_parameter)

    # create a pickup_lower_tw x arrival_time for pankratz
    scatterplot(hdf, 'mitrovic', 'pickup_lower_tw', 'arrival_time', 'urgency',
                pickup_lower_tw_plt, arrival_time_plt, urgency_plt, folder,
                perfect_interarrival_parameter)

    # create pairplot with dynamism x urgency x scale for each benchmark
    # pairplot_by_benchmark(hdf,
    #                       ['dynamism', 'urgency', 'requests_per_vehicle'],
    #                       [dynamisnm_plt, urgency_plt,
    #                        requests_per_vehicles_plt],
    #                       folder, perfect_interarrival_parameter)
    plt.close('all')
