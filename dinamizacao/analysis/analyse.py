import pandas as pd
import locale
import numpy as np
import analysis_tools
import test_poisson
import plots
import matplotlib.pyplot as plt
import importlib
import seaborn as sns
sns.set(style='ticks', font="Times New Roman", font_scale=1.35)
locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')
plt.rcParams.update({'axes.formatter.use_locale': True})


def calculate_dynamism_urgency_and_scale(df, perfect_interarrival_parameter):
    hdf = (
        df.pipe(analysis_tools.calculate_dynamism,
                perfect_interarrival_parameter)
        .pipe(analysis_tools.calculate_urgency)
        .pipe(analysis_tools.calculate_requests_per_vehicle)
        .assign(urgency_mean=lambda x:
                x.groupby(columns_to_group).urgency.mean())
        .assign(urgency_std=lambda x:
                x.groupby(columns_to_group).urgency.std())
        .assign(inter_mean=lambda x:
                x.groupby(columns_to_group).interarrival.mean())
        .assign(inter_mean_norm=lambda x:
                x.groupby(columns_to_group).interarrival.mean()
                / x.groupby(columns_to_group).planing_horizon.max())
        .assign(inter_std_norm=lambda x:
                x.groupby(columns_to_group).interarrival.std()
                / x.groupby(columns_to_group).planing_horizon.max())
        .assign(lam_poisson=lambda x:
                (x.number_of_requests / x.planing_horizon)
                .groupby(columns_to_group).max())
        .assign(real_pickup_lower_tw=lambda x:
                x.loc[:, ['arrival_time', 'pickup_lower_tw']]
                 .apply(max, axis='columns'))
        .assign(pltw_norm_h=lambda x:
                x.pickup_lower_tw / x.planing_horizon)
        .assign(real_pltw_norm_h=lambda x:
                x.real_pickup_lower_tw / x.planing_horizon)
        .assign(arrival_time_norm_h=lambda x:
                x.arrival_time / x.planing_horizon)
        .assign(urgency_norm_max=lambda x:
                x.urgency / x.groupby(level='benchmark').urgency.max())
    )
    return hdf


def create_citation_column(df):
    benchmarks = df.reset_index().benchmark.unique()
    citation = ['Berbeglia et al. (2012)', 'Fabri e Recht (2006)',
                'Gendreau et al. (2006)', 'Mitrovic-Minic et al. (2004)',
                'Pankratz e Krypczyk (2009)', 'Pureza e Laporte (2008)']
    citation_by_benchmark = dict(zip(benchmarks, citation))
    df_out = (
        df.copy()
          .assign(citation=lambda x: x.benchmark.map(citation_by_benchmark))
    )
    return df_out


def create_figures(hdf, columns_to_group, folder,
                   perfect_interarrival_parameter, save_test):
    if save_test:
        test_poisson.create_and_plot_poisson_scenarios(
            hdf, perfect_interarrival_parameter)
    plots.plot_figures(hdf, columns_to_group, folder,
                       perfect_interarrival_parameter)


if __name__ == '__main__':
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
    pltw_norm_h_plt = ('Limite inferior normalizado\n'
                       + 'da janela de tempo de coleta')
    pickup_lower_tw_plt = ('Limite inferior da janela\n'
                           + 'de tempo de coleta (min)')
    inter_mean_plt = 'Intervalo médio entre\n' + 'chegadas de pedidos (min)'
    inter_mean_norm_plt = inter_mean_plt + ' normalizada'

    # parameters
    create_and_save_plots = True
    save_poisson_test = False
    perfect_interarrival_parameter = 'planing_horizon'
    folder = './fig/analyses/'

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

    hdf = (
        df.pipe(create_citation_column)
        .pipe(calculate_dynamism_urgency_and_scale,
              perfect_interarrival_parameter)
    )
    if create_and_save_plots:
        create_figures(hdf, columns_to_group, folder,
                       perfect_interarrival_parameter, save_poisson_test)
