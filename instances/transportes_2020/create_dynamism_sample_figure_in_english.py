import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

sns.set(style='ticks', font="Times New Roman", font_scale=1.35)
matplotlib.rc('text', usetex=True)

data = (
    {'seq': [i for i in range(1, 7) for j in range(1, 11)],
     'value': [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5,
               0.5, 1.2, 2.9, 3.3, 4.2, 5.1, 6.9, 7.3, 8.5, 9.9,
               0.5, 0.7, 0.9, 3.3, 3.5, 4.1, 7.9, 8.3, 8.5, 9.9,
               0.5, 0.7, 0.9, 0.3, 0.6, 8.1, 8.4, 8.5, 8.6, 9.9,
               4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.6, 4.8, 4.9, 5.0,
               1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1]}
)
df = (
    pd.DataFrame(data)
      .assign(level=lambda x: x.seq.map(
        {1: '(a) highest degree of  dynamism',
         2: '(b) high degree of dynamism',
         3: '(c) not so high degree of dynamism',
         4: '(d) not so low degree of dynamism',
         5: '(e) low degree of dynamism',
         6: '(f) lowest degree of dynamism'}
        )
    )
)
g = sns.FacetGrid(df, col='level', col_wrap=2, height=1.5, aspect=3.5)
g.map(sns.rugplot, 'value', height=1)
g.set_titles('{col_name}')
g.set_xlabels('Request arrival time')
g.set(xlim=(0, 10))
g.axes[4].set_xticklabels(['0', '', '', '', '', '10'])
g.axes[5].set_xticklabels(['0', '', '', '', '', '$H$'])
for i in range(6):
    g.axes[i].spines['left'].set_color('white')
    g.axes[i].get_yaxis().set_visible(False)
plt.tight_layout()
plt.savefig('instances/transportes_2020/fig/dynamism_sample_en.eps',
            bbox_inches='tight')
plt.savefig('instances/transportes_2020/fig/dynamism_sample_en.png',
            bbox_inches='tight')
