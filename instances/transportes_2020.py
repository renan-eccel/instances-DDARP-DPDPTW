import pandas as pd
import instances.analysis.dinamize_all as dinamize_all
import instances.analysis.analyse as analyse

columns_to_group = ['problem', 'benchmark', 'instance', 'dinamizator']
df_static_requests = (
    pd.read_pickle('./instances/analysis/df_static_requests.zip')
      .assign(number_of_requests=lambda x:
              x.groupby(['benchmark', 'instance']).id.transform('count'))
)
df_dynamic_requests = dinamize_all.dinamize_all(df_static_requests)
perfect_interarrival_parameter = 'planing_horizon'
df_dynamism_urgency = (
    analyse.calculate_dynamism_urgency_and_scale(
        df_dynamic_requests,
        columns_to_group,
        perfect_interarrival_parameter
    )
)
