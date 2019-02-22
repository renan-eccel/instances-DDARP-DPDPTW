import pandas as pd
import numpy as np
import analysis_tools
import matplotlib.pyplot as plt


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
                create_dynamism_sample(
                    10**3,
                    int(values.number_of_requests),
                    getattr(values, perfect_interarrival_parameter),
                    values.Index[0],
                    values.Index[1]
                ).assign(statistic=function)
            )
    return df_poisson


def create_and_plot_poisson_scenarios(hdf, perfect_interarrival_parameter):
    hdf_poisson = (
        build_poisson_generated_scenarios(hdf, perfect_interarrival_parameter)
        .reset_index()
        .set_index(['problem', 'benchmark', 'statistic', 'instance', 'id'])
    )
    # plot dynamism of hdf_poisson instances
    hdf_poisson.boxplot(column='dynamism',
                        by=['benchmark', 'statistic'],
                        figsize=(50, 7)).set_ylim(0, 1)
    plt.savefig('./figures/dynamism_boxplot_benchmark_and_statistic_'
                + perfect_interarrival_parameter
                + '.png')
    plt.close()


def create_dynamism_sample(number_of_instances,
                           number_of_requests_desired, planing_horizon,
                           problem='gdvrp', benchmark='poisson_test'):
    '''
    Create a poisson bechmark for the a generic DVRP
    params:
        number_of_requests
        planing_horizon
        number_of_instances
    return:
        pandas.Series with calculated dynamism values
    '''
    def build_arrival_time_column(df):
        arrival_time_list = []
        for name, group in df.groupby('instance'):
            last_interarrival = 0
            for row in group.itertuples():
                new_interarrival = last_interarrival + row.interarrival
                arrival_time_list.append(new_interarrival)
                last_interarrival = new_interarrival
        return df.assign(arrival_time=arrival_time_list)

    lambda_poisson = number_of_requests_desired / planing_horizon

    exp_beta = 1 / lambda_poisson

    id_list = (
        [1 + i for i in range(number_of_requests_desired)]
        * number_of_instances
    )

    instance_list = (
        [1 + int(i/number_of_requests_desired)
         for i in range(number_of_instances * number_of_requests_desired)]
    )
    array_interarrivals = (
        np.random.exponential(exp_beta,
                              size=number_of_instances
                              * number_of_requests_desired)
    )
    data = {
        'problem': problem,
        'benchmark': benchmark,
        'instance': instance_list,
        'id': id_list,
        'planing_horizon': planing_horizon,
        'interarrival': list(array_interarrivals)
    }

    df = (
        pd.DataFrame(data)
          .pipe(build_arrival_time_column)
          .loc[lambda x: x.arrival_time <= planing_horizon]
          .assign(number_of_requests=lambda x:
                  x.groupby(['problem', 'benchmark', 'instance'],
                            as_index=False).arrival_time.transform('count'))
          .loc[lambda x: x.number_of_requests == number_of_requests_desired]
          .pipe(analysis_tools.calculate_dynamism, 'planing_horizon')
    )
    return (df)
