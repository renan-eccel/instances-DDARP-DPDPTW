import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
        {1: '(a) altamente dinâmico',
         2: '(b) um pouco menos dinâmico',
         3: '(c) menos dinâmico',
         4: '(d) não tão dinâmico',
         5: '(e) quase não dinâmico',
         6: '(f) não dinâmico'}
        )
    )
)
g = sns.FacetGrid(df, col='level', col_wrap=2, height=1, aspect=5)
g.map(sns.rugplot, 'value', height=1)
g.set_titles('{col_name}')
g.set_xlabels('Instante de chegada do pedido (min)')
g.set(xlim=(0, 10))
plt.tight_layout()
plt.savefig('./fig/dynamism_sample.eps')
plt.savefig('./fig/dynamism_sample.png')
