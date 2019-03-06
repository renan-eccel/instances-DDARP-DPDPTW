import pandas as pd
import numpy as np
import analysis_tools
import test_poisson
import plots
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks')


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
        .assign(lam_poisson=lambda x:
                (x.number_of_requests / x.planing_horizon)
                .groupby(columns_to_group).max())
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
                   perfect_interarrival_parameter):
    test_poisson.create_and_plot_poisson_scenarios(
        hdf, perfect_interarrival_parameter)
    plots.plot_figures(hdf, columns_to_group, folder,
                       perfect_interarrival_parameter)


if __name__ == '__main__':
    # parameters
    create_and_save_plots = True
    perfect_interarrival_parameter = 'planing_horizon'
    folder = './figures/'

    df = pd.read_pickle('df_requests.zip')
    columns_to_group = ['problem', 'benchmark', 'instance']
    columns_plt = {'dynamism': 'Dinamismo',
                   'urgency': 'Urgência (min)',
                   'interarrival': 'Intervalo entre chegadas (min)',
                   'arrival_time': 'Instante de chegada (min)'}
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
                       perfect_interarrival_parameter)
