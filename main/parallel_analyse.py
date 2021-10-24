import pandas as pd
import numpy as np
import itertools
import networkx as nx


def parallel_rank(motrix, weight_dict, rank1, num_parallel, num_drug):

    '''
    rank1=pd.read_csv('../result/pagerank_weight.csv')

    weight_dict={'CIRP1':1.71134, 'CIRP2':1.71134, 'NQO1':1.552828, 'RBM3':0.20732618, 'SLC5A3':0, 'TXNIP':0.91961218}

    #rank1.head(20)

    motrix=pd.read_csv("../data/motrix.csv")
    num_parallel=2 #多少种药物联合
    num_drug=50  #选取排名前XX的药物进行联合分析

    motrix.head()
    '''
    #rank_list=rank1['urls'].tolist()
    rank_list=rank1.index.tolist()

    protein_change=motrix["protein"].values.tolist()

    drug_change=motrix["drug"].values.tolist()

    len_motrix=len(protein_change)

    #value_change=[5 for x in range(0,len_motrix)]
    value_change=[0.5*x for x in motrix["value"].values.tolist()]

    protein=motrix["protein"].values.tolist()+drug_change
    drug=motrix["drug"].values.tolist()+protein_change
    value=motrix["value"].values.tolist()+value_change


    new_motrix=pd.DataFrame()

    new_motrix["protein"]=protein
    new_motrix["drug"]=drug
    new_motrix["value"]=value


    new_motrix.loc[new_motrix["drug"]==6]

    list(set(protein_change))

    #筛选出所有的类别
    all_protein = list(set(protein_change))
    #all_drug = list(set(drug_change)) #所有药物
    all_drug =  rank_list[len(all_protein)-1:len(all_protein)+num_drug-1]

    #进行排序
    all_protein.sort(key=protein_change.index)
    #all_drug.sort(key=drug1.index)
    #len(all_drug)

    #生成药物联合治疗的排列组合
    drug_combination=list(itertools.combinations(all_drug, num_parallel))  #生成药物联合治疗的排列组合

    #len(drug_combination)

    #int(drug_combination[0][0])

    #drug_test_motrix=drug_test_motrix.append(new_motrix.loc[new_motrix["drug"]==int("6")])

    parallel_motrix=pd.DataFrame()
    #parallel_debug=pd.DataFrame()

    for drug_test in drug_combination:
        drug_test_motrix=pd.DataFrame()

        for a_drug in drug_test:
            a_drug=int(a_drug)
            drug_test_motrix=drug_test_motrix.append(new_motrix.loc[new_motrix["drug"]==a_drug])
            drug_test_motrix=drug_test_motrix.append(new_motrix.loc[new_motrix["protein"]==a_drug])


        #pagerank计算部分
        drug_test_motrix.columns=['source','target','weight']
        
        df=pd.DataFrame()
        df['source']=drug_test_motrix['source'].values.tolist()
        df['target']=drug_test_motrix['target'].values.tolist()
        df['weight']=drug_test_motrix['weight'].values.tolist()

        G=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph)

        G_weighted=nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph, edge_attr='weight')

        #weights = [i * 5 for i in df['weight'].tolist()]


        #加权计算部分
        simple_pagerank = nx.pagerank(G, alpha=0.88)
        personalized_pagerank = nx.pagerank(G, alpha=0.88, personalization=weight_dict)
        nstart_pagerank = nx.pagerank(G, alpha=0.88, nstart=weight_dict)
        weighted_pagerank = nx.pagerank(G_weighted, alpha=0.88)
        weighted_personalized_pagerank = nx.pagerank(G_weighted, alpha=0.88, personalization=weight_dict)

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

        #parallel_debug=parallel_debug.append(result1)
        #parallel_debug.head(20)

        drug1=[]
        parallel_num=[]
        parallel_num1=[]
        for a_drug in drug_test:
            drug1.append(a_drug)
            a_drug=int(a_drug)
            
            parallel_num.append(result1.loc[a_drug,'weighted_personalized_pagerank'])


        for num in parallel_num:
            parallel_num1.append(num)
            parallel_num1.append(100*num/sum(parallel_num))

        
        parallel_num1.append(sum(parallel_num)/(result1.loc[protein[0],'weighted_personalized_pagerank']))
        #parallel_num1.append(result1.loc[protein[0],'weighted_personalized_pagerank'])
        parallel_num1=drug1+parallel_num1

        parallel_motrix=parallel_motrix.append(pd.DataFrame(pd.DataFrame(parallel_num1).values.T))
        parallel_motrix=parallel_motrix.sort_values(by=6, ascending=False) 
    
    parallel_motrix.columns=['drug1','drug2','value1','persentage1','value2','persentage2','pagerank_weight']

    return parallel_motrix


