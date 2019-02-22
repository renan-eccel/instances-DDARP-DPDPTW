import pandas as pd
import numpy as np
import analysis_tools
import test_poisson
import plots


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


if __name__ == '__main__':
    # parameters
    create_and_save_plots = False
    perfect_interarrival_parameter = 'planing_horizon'

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

    hdf = calculate_dynamism_and_urgency(df, perfect_interarrival_parameter)
    hdf.to_pickle('./hdf.zip', compression='zip')

    if create_and_save_plots:
        test_poisson.create_and_plot_poisson_scenarios(
            hdf, perfect_interarrival_parameter)
        plots.plot_figures(hdf, (15, 7), columns_to_group,
                           perfect_interarrival_parameter)
