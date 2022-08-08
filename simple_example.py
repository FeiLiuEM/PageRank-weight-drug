##########################
#  Designed by Fei Liu.
#     code = UTF-8
##########################
#This is a simple example of the research. 
#The data file is in /data/simple_example_data.csv
#The result is in /result/simple_example_result.xlsx

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
import scipy

from main import xlsx2motrix
from main import parallel_analyse


motrix=pd.read_csv('./data/motrix_test.csv') 

weight_dict={'Protein_1':5, 'Protein_2':3, 'Drug_1':0, 'Drug_2':0}


motrix.columns=['source','target','weight']

df=motrix

G=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph)

G_weighted=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph, edge_attr='weight')

weights = [i * 5 for i in df['weight'].tolist()]


#visualization.


pos = nx.spring_layout(G, k=0.9)
nx.draw_networkx_edges(G, pos, edge_color='#06D6A0', arrowsize=28, width=weights)
nx.draw_networkx_nodes(G, pos,node_color='#EF476F', node_size=2000)
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', font_color='white')
plt.gca().margins(0.1, 0.1)
plt.show()


#settign weights


simple_pagerank = nx.pagerank(G, alpha=0.85)
personalized_pagerank = nx.pagerank(G, alpha=0.85, personalization=weight_dict)
nstart_pagerank = nx.pagerank(G, alpha=0.85, nstart=weight_dict)
weighted_pagerank = nx.pagerank(G_weighted, alpha=0.85)
weighted_personalized_pagerank = nx.pagerank(G_weighted, alpha=0.85, personalization=weight_dict,max_iter=10000,tol=1e-7)


df_metrics = pd.DataFrame(dict(
    simple_pagerank = simple_pagerank,
    personalized_pagerank = personalized_pagerank,
    nstart_pagerank = nstart_pagerank,
    weighted_pagerank = weighted_pagerank,
    weighted_personalized_pagerank = weighted_personalized_pagerank,
))
df_metrics.index.name='targets'
result1=df_metrics.sort_values(by='weighted_personalized_pagerank', ascending=False) 

result1.to_csv("./result/simple_example_result.csv")
