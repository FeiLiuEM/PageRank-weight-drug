import pandas as pd
import numpy as np
import itertools

from pandas.io.parsers import read_csv

rank1=pd.read_csv('../result/pagerank_weight.csv')
rank_list=rank1["urls"].values.tolist()
#rank1.head(20)

def parallel_rank(motrix,num_parallel,num_drug)

motrix=pd.read_csv("../data/motrix.csv")
num_parallel=2 #多少种药物联合
num_drug=50  #选取排名前XX的药物进行联合分析

motrix.head()


protein1=motrix["protein"].values.tolist()

drug1=motrix["drug"].values.tolist()

len_motrix=len(protein1)

value1=[5 for x in range(0,len_motrix)]

protein=motrix["protein"].values.tolist()+drug1
drug=motrix["drug"].values.tolist()+protein1
value=motrix["value"].values.tolist()+value1


new_motrix=pd.DataFrame()

new_motrix["protein"]=protein
new_motrix["drug"]=drug
new_motrix["value"]=value


new_motrix.loc[new_motrix["drug"]==6]

list(set(protein1))

#筛选出所有的类别
all_protein = list(set(protein1))
#all_drug = list(set(drug1)) #所有药物
all_drug =  rank_list[len(all_protein)-1:len(all_protein)+num_drug-1]

#进行排序
all_protein.sort(key=protein1.index)
#all_drug.sort(key=drug1.index)
#len(all_drug)

#生成药物联合治疗的排列组合
drug_combination=list(itertools.combinations(all_drug, num_parallel))  #生成药物联合治疗的排列组合

#len(drug_combination)

#int(drug_combination[0][0])

#drug_test_motrix=drug_test_motrix.append(new_motrix.loc[new_motrix["drug"]==int("6")])


for drug_test in drug_combination:
    drug_test_motrix=pd.DataFrame()

    for a_drug in drug_test:
        a_drug=int(a_drug)
        drug_test_motrix=drug_test_motrix.append(new_motrix.loc[new_motrix["drug"]==a_drug])
        drug_test_motrix=drug_test_motrix.append(new_motrix.loc[new_motrix["protein"]==a_drug])


    #pagerank计算部分
    drug_test_motrix.columns=['source','target','weight']

    df=drug_test_motrix

    G=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph)

    G_weighted=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph, edge_attr='weight')

    weights = [i * 5 for i in df['weight'].tolist()]


    #加权计算部分
    simple_pagerank = nx.pagerank(G, alpha=0.85)
    personalized_pagerank = nx.pagerank(G, alpha=0.85, personalization={'CIRP1':1.71134, 'CIRP2':1.71134, 'NQO1':1.552828, 'RBM3':0.20732618, 'SLC5A3':0, 'TXNIP':0.91961218})
    nstart_pagerank = nx.pagerank(G, alpha=0.85, nstart={'CIRP1':1.71134, 'CIRP2':1.71134, 'NQO1':1.552828, 'RBM3':0.20732618, 'SLC5A3':0, 'TXNIP':0.91961218})
    weighted_pagerank = nx.pagerank(G_weighted, alpha=0.85)
    weighted_personalized_pagerank = nx.pagerank(G_weighted, alpha=0.85, personalization={'CIRP1':1.71134, 'CIRP2':1.71134, 'NQO1':1.552828, 'RBM3':0.20732618, 'SLC5A3':0, 'TXNIP':0.91961218})

    df_metrics = pd.DataFrame(dict(
        simple_pagerank = simple_pagerank,
        personalized_pagerank = personalized_pagerank,
        nstart_pagerank = nstart_pagerank,
        weighted_pagerank = weighted_pagerank,
        weighted_personalized_pagerank = weighted_personalized_pagerank,
    ))
    df_metrics.index.name='urls'
    result1=df_metrics.sort_values(by='weighted_personalized_pagerank', ascending=False) 
    result1.to_csv('result/pagerank_weight.csv')




