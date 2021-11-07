import matplotlib.pyplot as plt
from networkx.algorithms.link_analysis.pagerank_alg import pagerank
%matplotlib inline
plt.rcParams.update({
    'figure.figsize': (80, 80),
    'axes.spines.right': False,
    'axes.spines.left': False,
    'axes.spines.top': False,
    'axes.spines.bottom': False})
import networkx as nx
import pandas as pd
import numpy as np

from main import xlsx2motrix
from main import parallel_analyse

motrix=xlsx2motrix.motrix_generate('./data/DATA.xlsx')

weight_dict={'CIRP1':3.2746, 'CIRP2':3.2746, 'NQO1':2.9339, 'RBM3':1.154546, 'SLC5A3':0.5, 'TXNIP':1.8916067}

#motrix.to_csv("./data/motrix.csv") 

motrix.columns=['source','target','weight']

df=motrix

G=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph)

G_weighted=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph, edge_attr='weight')

weights = [i * 5 for i in df['weight'].tolist()]

'''
#可视化部分
pos = nx.spring_layout(G, k=0.9)
nx.draw_networkx_edges(G, pos, edge_color='#06D6A0', arrowsize=0.5, width=weights)
nx.draw_networkx_nodes(G, pos,node_color='#EF476F', node_size=100)
nx.draw_networkx_labels(G, pos, font_size=4, font_weight='bold', font_color='white')
plt.gca().margins(0.1, 0.1)
plt.show()
'''

#设置权重


simple_pagerank = nx.pagerank(G, alpha=0.9)
personalized_pagerank = nx.pagerank(G, alpha=0.9, personalization=weight_dict)
nstart_pagerank = nx.pagerank(G, alpha=0.9, nstart=weight_dict)
weighted_pagerank = nx.pagerank(G_weighted, alpha=0.9)
weighted_personalized_pagerank = nx.pagerank(G_weighted, alpha=0.9, personalization=weight_dict)

df_metrics = pd.DataFrame(dict(
    simple_pagerank = simple_pagerank,
    personalized_pagerank = personalized_pagerank,
    nstart_pagerank = nstart_pagerank,
    weighted_pagerank = weighted_pagerank,
    weighted_personalized_pagerank = weighted_personalized_pagerank,
))

df_metrics.index.name='urls'
result1=df_metrics.sort_values(by='weighted_personalized_pagerank', ascending=False) 
#result1.to_csv('result/pagerank_weight.csv')

result1.head(20)

'''
#pagerank计算结果的可视化
node_size = [i * 4000 for i in df_metrics['weighted_personalized_pagerank'].to_list()]
node_size


weights = [i * 5 for i in df['weight'].tolist()]
nx.draw_networkx_edges(G_weighted, pos, edge_color='#06D6A0', arrowsize=22, width=weights)
nx.draw_networkx_nodes(G_weighted, pos,node_color='#EF476F', node_size=node_size)
nx.draw_networkx_labels(G_weighted, pos, font_size=10, font_weight='bold', font_color='white')
plt.gca().margins(0.1, 0.1)
plt.show()
'''


#并行分析部分，parallel pagerank
motrix.columns=['protein','drug','value']
parallel_data=parallel_analyse.parallel_rank(motrix,weight_dict,result1,2,20)
print(parallel_data.head())

