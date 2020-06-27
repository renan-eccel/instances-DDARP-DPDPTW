import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import instances.analysis.dinamize_all as dinamize_all
import instances.analysis.analyse as analyse

sns.set(style='ticks', font="Times New Roman", font_scale=1.35)

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
        / x.groupby(['benchmark']).urgency_mean.transform('max')
    )
    .groupby(['problem', 'benchmark', 'dinamizator',
              'instance']).max().reset_index()
    .assign(
        cite_benchmark=lambda x:
        x.benchmark.map(
             {'cordeau_2006': 'Ropke et al. (2007)',
              'li_lim_2003': 'Li and Lim (2003)',
              'cordeau_laporte_2003': 'Cordeau and Laporte (2003)'}
        ),
        cite_dinamizator=lambda x:
        x.dinamizator_short.map(
            {'berbeglia_2012': 'Berbeglia et al. (2012)',
             'fabri_rencht_2006': 'Fabri and Recht (2006)',
             'pankratz_2005': 'Pankratz (2005)',
             'pureza_laporte_2008': 'Pureza and Laporte (2008)'}
        )
    )
)

g = sns.FacetGrid(df_dyn_urg_ins,
                  col='cite_benchmark',
                  row='cite_dinamizator',
                  hue='cite_benchmark',
                  despine=False,
                  palette='colorblind',
                  xlim=(0, 1),
                  height=2.5,
                  aspect=1.5,
                  )
g.map(plt.scatter, 'dynamism', 'urgency_mean_norm_max', s=4)
g.set_titles('{col_name}\nby {row_name}')
g.set_xlabels('Dynamism')
g.set_ylabels('Normalized\n urgency average')
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/urgency_x_dynamism.png')
plt.close()

g = sns.FacetGrid(df_dyn_urg_ins,
                  row='cite_benchmark',
                  palette='colorblind',
                  despine=False,
                  xlim=(0, 1),
                  height=2.5,
                  aspect=2.5,
                  )
g.map(sns.boxplot, 'dynamism', 'cite_dinamizator')
g.set_titles('{row_name}')
g.set(ylabel=None)
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/dynamism_boxplot.png')
plt.close()

g = sns.boxplot(x='dynamism',
                y='cite_dinamizator',
                hue='cite_benchmark',
                data=df_dyn_urg_ins,
                palette='colorblind',
                )
g.set_xlabel('Dynamism')
g.legend(title=None)
g.set_ylabel(None)
plt.xlim(0, 1)
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/dynamism_boxplot_2.png')
plt.close()
