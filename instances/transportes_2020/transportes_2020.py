import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
df_dyn_urg_req = (
    analyse.calculate_dynamism_urgency_and_scale(
        df_dynamic_requests,
        columns_to_group,
        perfect_interarrival_parameter
    )
)
df_dyn_urg_ins = (
    df_dyn_urg_req
    .reset_index()
    .assign(
        urgency_mean_norm_max=lambda x:
        x.urgency_mean
        / x.groupby(['benchmark', 'dinamizator']).urgency_mean.transform('max')
    )
    .groupby(['problem', 'benchmark', 'dinamizator',
              'instance']).max().reset_index()
)

g = sns.FacetGrid(df_dyn_urg_ins, col='benchmark', row='dinamizator_short',
                  despine=False)
g.map(sns.scatterplot, 'dynamism', 'urgency_mean_norm_max', 'benchmark')
plt.savefig('instances/transportes_2020/fig/urgency_x_dynamism.png')
plt.close()


g = sns.FacetGrid(df_dyn_urg_ins, col='benchmark', despine=False)
g.map(sns.boxplot, 'dynamism', 'dinamizator_short')
plt.savefig('instances/transportes_2020/fig/dynamism_boxplot.png')
plt.close()
