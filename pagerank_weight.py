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
import pickle

from main import xlsx2motrix
from main import parallel_analyse


weight_dict_0_5h={'ciart':1.3792, 'chac1':1.3437, 'nudt22':1.3199}
weight_dict_1h={'cdsn':1.43, 'nr1d1':1.4181, 'chac1':1.4093}
weight_dict_2h={'cirp':1.7468, 'armcx5':1.583, 'ccdc122':1.4073}
weight_dict_4h={'cirp':2.2545, 'ramp3':1.8776, 'ceacam1':1.8247}
weight_dict_8h={'cirp':2.9716, 'ramp3':2.5125, 'nqo1':2.2651}
weight_dict_18h={'cirp':3.2746, 'ramp3':2.5017, 'nqo1':2.9339}

weight_dict1_0_5h={'ciart':8.0218, 'chac1':9.642, 'nudt22':9.4038}
weight_dict1_1h={'cdsn':8.167, 'nr1d1':10.6623, 'chac1':9.7105}
weight_dict1_2h={'cirp':9.4334, 'armcx5':5.9664, 'ccdc122':8.0592}
weight_dict1_4h={'cirp':9.8015, 'ramp3':9.0459, 'ceacam1':7.111}
weight_dict1_8h={'cirp':10.2, 'ramp3':9.4661, 'nqo1':10.8736}
weight_dict1_18h={'cirp':10.34, 'ramp3':9.4599, 'nqo1':11.2469}


weight_dict=weight_dict_18h
weight_dict1=weight_dict1_18h
group='_18h'
save_result='./result/h'+group+'.xlsx'
open_data='./data/DATA'+group+'.xlsx'


def get_translate(dict1,parallel_data):

    parallel_data1=parallel_data.sort_values(by='personalized_weight_pagerank', ascending=False)

    num_drug=len(parallel_data['drug'].columns)

    drug_dataframe=pd.DataFrame(index=parallel_data.index)

    for i in range(num_drug):
        #i=0
        drug_list1=[]
        rank1=parallel_data['drug'].values[:,i].tolist()
        for drug1 in rank1:
            drug_name1=dict1.get(str(int(drug1)))
            if drug_name1 is None:
                drug_name1=drug1
            drug_list1.append(drug_name1)
        drug_dataframe.loc[:,str(i+1)]=drug_list1

    parallel_data2=pd.concat([drug_dataframe,parallel_data1],axis=1)

    parallel_data3=parallel_data2.drop('drug', axis='columns') # 删除列 

    return parallel_data3



#data=pd.read_excel('./data/DATA.xlsx')

all_protein, data, motrix=xlsx2motrix.motrix_generate(open_data)

#补全nstart的药物部分字典值
all_drug_pd=pd.read_csv('./data/all_drugs.csv')
all_drug=all_drug_pd['drugs'].values.tolist()
all_drug_nstart=[0]*len(all_drug)
dict_drug=dict(zip(all_drug,all_drug_nstart))
dict_drug1=dict(zip(all_drug,[1]*len(all_drug)))
#weight_dictx1=weight_dict1
#weight_dictx1.update(dict_drug)

weight_dictx1={}
for k,v in weight_dict1.items():
    weight_dictx1[k]=v

for k,v in dict_drug.items():
    weight_dictx1[k]=v

weight_dictx={}
for k,v in weight_dict.items():
    weight_dictx[k]=v

for k,v in dict_drug1.items():
    weight_dictx[k]=v

#pd.DataFrame(all_protein).to_csv('./data/all_protein.csv',index=False)
#pd.DataFrame(all_drug).to_csv('./data/all_drug.csv',index=False)

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


simple_pagerank = nx.pagerank(G, alpha=0.85)
personalized_pagerank = nx.pagerank(G, alpha=0.85, personalization=weight_dict)
#nstart_pagerank = nx.pagerank(G, alpha=0.85, nstart=weight_dict)
weighted_pagerank = nx.pagerank(G_weighted, alpha=0.85)
weighted_personalized_pagerank = nx.pagerank(G_weighted, alpha=0.85, personalization=weight_dictx,nstart=weight_dictx1,max_iter=10000,tol=1e-7)

df_metrics = pd.DataFrame(dict(
    simple_pagerank = simple_pagerank,
    personalized_pagerank = personalized_pagerank,
    #nstart_pagerank = nstart_pagerank,
    weighted_pagerank = weighted_pagerank,
    weighted_personalized_pagerank = weighted_personalized_pagerank,
))

df_metrics.index.name='urls'
result1=df_metrics.sort_values(by='weighted_personalized_pagerank', ascending=False) 
#result1.to_csv('result/pagerank_weight.csv')

result1.head(20)


#翻译模块
f_read = open('./data/dict_file.pkl', 'rb')
dict1 = pickle.load(f_read)
#print(dict1)
f_read.close()

translation=result1.index.values.tolist()
drug_list=[]

for drug in translation:
    drug_name=dict1.get(str(drug))
    if drug_name is None:
        drug_name=drug
    drug_list.append(drug_name)

result2=result1.sort_values(by='weighted_personalized_pagerank', ascending=False) 
result2.index=drug_list
result2.head(20)

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
parallel_data_2=parallel_analyse.parallel_rank(all_protein, data, motrix,weight_dict,weight_dict1,result1,2,20)  #2代表联用药物数量，20代表前20的药物
parallel_data_2.head(20)

parallel_data_3=parallel_analyse.parallel_rank(all_protein, data, motrix,weight_dict,weight_dict1,result1,3,10)  #2代表联用药物数量，20代表前20的药物
parallel_data_3.head(20)
#parallel_data.to_csv('result/parallel_pagerank_weight1.csv') #保存结果


parallel_data_2_1=get_translate(dict1,parallel_data_2)
parallel_data_3_1=get_translate(dict1,parallel_data_3)

'''
#保存结果
writer = pd.ExcelWriter(save_result)

data_xlsx = result2
data_xlsx.to_excel(writer, sheet_name='comprehensive')

data_xlsx = parallel_data_2_1
data_xlsx.to_excel(writer, sheet_name='parallel_2',index=False)

data_xlsx = parallel_data_3_1
data_xlsx.to_excel(writer, sheet_name='parallel_3',index=False)

writer.save()
'''