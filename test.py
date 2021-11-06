import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams.update({
    'figure.figsize': (9, 9),
    'axes.spines.right': False,
    'axes.spines.left': False,
    'axes.spines.top': False,
    'axes.spines.bottom': False})
import networkx as nx
import pandas as pd
import numpy as np

from main import xlsx2motrix
from main import parallel_analyse

#motrix=xlsx2motrix.motrix_generate('./data/DATA.xlsx')

motrix=pd.read_csv('./data/motrix_test.csv')

weight_dict={'A':1, 'B':1, 'C':1}

#motrix.to_csv("./data/motrix.csv") 

motrix.columns=['source','target','weight']

df=motrix

G=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph)

G_weighted=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph, edge_attr='weight')

weights = [i * 5 for i in df['weight'].tolist()]

'''
#可视化部分
weights = [i * 5 for i in df['weight'].tolist()]

pos = nx.spring_layout(G, k=0.9)
nx.draw_networkx_edges(G, pos, edge_color='#06D6A0', arrowsize=22, width=weights)
nx.draw_networkx_nodes(G, pos,node_color='#EF476F', node_size=1000)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_color='white')
plt.gca().margins(0.1, 0.1)
plt.show()
'''

#设置权重


#simple_pagerank = nx.pagerank(G, alpha=0.9)
#personalized_pagerank = nx.pagerank(G, alpha=0.9, personalization=weight_dict)
#nstart_pagerank = nx.pagerank(G, alpha=0.9, nstart=weight_dict)
#weighted_pagerank = nx.pagerank(G_weighted, alpha=0.9)
weighted_personalized_pagerank = nx.pagerank(G_weighted, alpha=0.9, personalization=weight_dict,max_iter=10000,tol=1e-7)

print(weighted_personalized_pagerank)