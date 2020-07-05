
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import instances.analysis.dinamize_all as dinamize_all
import instances.analysis.analyse as analyse
import random


def weighted_hist(x, weights, **kwargs):
    plt.hist(x, weights=weights, **kwargs)


random.seed(42)
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
    .reset_index()
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
        ),
        real_pickup_lower_tw=lambda x:
            x.loc[:, ['arrival_time', 'pickup_lower_tw']].max(axis=1),
        real_pltw_norm_h=lambda x:
            x.real_pickup_lower_tw / x.planing_horizon,
        real_putw_norm_h=lambda x:
            x.pickup_upper_tw / x.planing_horizon,
        arrival_time_norm_h=lambda x:
            x.arrival_time / x.planing_horizon,
        weight=lambda x:
            1 / x.groupby(['problem', 'benchmark']).id.transform('count')
    )
)
df_dyn_urg_ins = (
    df_dyn_urg_req
    .assign(
        urgency_mean_norm_max=lambda x:
        x.urgency_mean
        / x.groupby(['benchmark']).urgency_mean.transform('max'),
        mean_arrival_time_norm_h=lambda x:
        x.groupby(['cite_benchmark', 'cite_dinamizator'])
         .arrival_time_norm_h.transform('mean')
    )
    .groupby(['problem', 'benchmark', 'dinamizator',
              'instance']).max().reset_index()
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
g.set_xlabels('Degree of dynamism')
g.set_ylabels('Normalized\n average urgency')
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/urgency_x_dynamism.png',
            bbox_inches=0)
plt.close()

var_list = list(df_dyn_urg_ins.columns)
var_list.remove('dynamism')
var_list.remove('urgency_mean_norm_max')
df_pivot = df_dyn_urg_ins.melt(id_vars=var_list)

g = sns.FacetGrid(df_pivot,
                  row='cite_benchmark',
                  col='variable',
                  palette='colorblind',
                  despine=False,
                  xlim=(0, 1),
                  height=2.5,
                  aspect=2.4,
                  )
g.map(sns.boxplot, 'value', 'cite_dinamizator')
g.set_titles('{row_name}')
g.set(ylabel=None)
g.axes[2, 0].set_xlabel('Degree of dynamism')
g.axes[2, 1].set_xlabel('Normalized average urgency')
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/dynamism_boxplot.png',
            bbox_inches=0)
plt.close()

g = sns.boxplot(x='dynamism',
                y='cite_dinamizator',
                hue='cite_benchmark',
                data=df_dyn_urg_ins,
                palette='colorblind',
                )
g.set_xlabel('Degree of dynamism')
g.legend(title=None)
g.set_ylabel(None)
plt.xlim(0, 1)
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/dynamism_boxplot_2.png',
            bbox_inches=0)
plt.close()

g = sns.FacetGrid(df_dyn_urg_req,
                  col='cite_benchmark',
                  hue='cite_benchmark',
                  palette='colorblind',
                  height=3.0,
                  aspect=1.5,
                  xlim=(-0.05, 1),
                  despine=False,)
g.map(weighted_hist,
      'real_pltw_norm_h',
      'weight',
      bins=np.arange(0, 1.1, 0.1))

g.map(weighted_hist,
      'real_pltw_norm_h',
      'weight',
      cumulative=True,
      histtype='step',
      bins=np.arange(0, 1, 0.1))
g.set_titles('{col_name}')
g.set_xlabels('Normalized lower limit\n of pickup time window')
g.set_ylabels('Frequency')
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/pickup_lower_tw_hist.png',
            bbox_inches=0)
plt.close()

g = sns.FacetGrid(df_dyn_urg_req,
                  col='cite_benchmark',
                  hue='cite_benchmark',
                  palette='colorblind',
                  height=3.0,
                  aspect=1.5,
                  xlim=(-0.05, 1),
                  despine=False,)
g.map(weighted_hist,
      'real_putw_norm_h',
      'weight',
      bins=np.arange(0, 1.1, 0.1))

g.map(weighted_hist,
      'real_putw_norm_h',
      'weight',
      cumulative=True,
      histtype='step',
      bins=np.arange(0, 1.1, 0.1))
g.set_titles('{col_name}')
g.set_xlabels('Normalized upper limit\n of pickup time window')
g.set_ylabels('Frequency')
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/pickup_upper_tw_hist.png',
            bbox_inches=0)
plt.close()


df_corr_arrival_pltw = (
    df_dyn_urg_req
    .groupby(['cite_benchmark', 'cite_dinamizator'])
    [['arrival_time_norm_h', 'real_pltw_norm_h']]
    .corr()
    .drop('arrival_time_norm_h', axis=1)
    .loc[pd.IndexSlice[:, :, ['arrival_time_norm_h']], :]
    .droplevel(2)
    .rename({'real_pltw_norm_h': 'r'}, axis=1)
    .round(2)
)
df_corr_arrival_pltw.to_csv('instances/transportes_2020/'
                            + 'fig/arrival_time_x_pltw_corr.csv')

df_static_requests_benchmark_per = (
    df_dyn_urg_req
    [df_dyn_urg_req.arrival_time == 0]
    .groupby(['cite_benchmark', 'cite_dinamizator'])
    .arrival_time
    .count()
    /
    df_dyn_urg_req
    .groupby(['cite_benchmark', 'cite_dinamizator'])
    .arrival_time
    .count()
)
df_n_static_requests_instance = (
        df_dyn_urg_req
        [df_dyn_urg_req.arrival_time == 0]
        .groupby(['cite_benchmark', 'cite_dinamizator', 'instance'])
        .arrival_time
        .count()
        /
        df_dyn_urg_req
        .groupby(['cite_benchmark', 'cite_dinamizator', 'instance'])
        .arrival_time
        .count()
)
df_static_requests_benchmark_per_mean_std = (
    df_n_static_requests_instance
    .groupby(['cite_benchmark', 'cite_dinamizator'])
    .agg(['mean', 'std'])
)
df_static_req_info = (
    df_static_requests_benchmark_per_mean_std
    .join(df_static_requests_benchmark_per)
    .rename({'arrival_time': 'total'}, axis=1)
    [['total', 'mean', 'std']]
    .fillna(0)
    .round(3)
    .multiply(100)
)
df_static_req_info.to_csv('instances/transportes_2020/fig/'
                          + 'df_static_requests_per.csv')
