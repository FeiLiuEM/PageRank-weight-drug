import pandas as pd
import numpy as np
import itertools
import networkx as nx


def parallel_rank(all_protein, data, motrix, weight_dict, weight_dict1, rank1, num_parallel, num_drug):

    '''
    all_protein=pd.read_csv('../data/all_protein.csv')['0'].values.tolist()
    all_drug=pd.read_csv('../data/all_drug.csv')['0'].values.tolist()



    rank1=pd.read_csv('../result/pagerank_weight.csv')

    weight_dict={'CIRP1':3.2746, 'CIRP2':3.2746, 'NQO1':2.9339, 'RBM3':1.154546, 'SLC5A3':0.5, 'TXNIP':1.8916067}

    #rank1.head(20)

    motrix=pd.read_csv("../data/motrix.csv")
    motrix.columns=['protein','drug','value']
    num_parallel=2 #多少种药物联合
    num_drug=50  #选取排名前XX的药物进行联合分析

    motrix.head()
    '''
    #rank_list=rank1['urls'].tolist()

    drug2drug=pd.DataFrame(dict(
    protein=all_protein,
    drug=all_protein,
    value=[10]*len(all_protein)
    ))

    rank_list=rank1.index.tolist()

    selected_drug1=rank_list[len(all_protein):len(all_protein)+num_drug]

    #筛选每个蛋白排名靠前的药物
    drug_each_protein=[]
    for key in data:
        data_protein=data.get(key)
        drug_each_protein+=data_protein['drug'][:num_drug].values.tolist()

    selected_drug=list(set(drug_each_protein+selected_drug1))

    #len(selected_drug)

    #生成药物联合治疗的排列组合
    drug_combination=list(itertools.combinations(selected_drug, num_parallel))  #生成药物联合治疗的排列组合

    #len(drug_combination)

    #int(drug_combination[0][0])

    #drug_test_motrix=drug_test_motrix.append(new_motrix.loc[new_motrix["drug"]==int("6")])

    parallel_motrix=pd.DataFrame()
    #parallel_debug=pd.DataFrame()
    #drug_test=drug_combination[1]

    for drug_test in drug_combination:
        drug_test_motrix=pd.DataFrame()

        drug_list=[]
        drug_list_nstart=[]
        for a_drug in drug_test:
            #a_drug=int(a_drug)
            temp_df1=motrix.loc[motrix["protein"]==a_drug]
            temp_list1=temp_df1['value'].tolist()
            temp_list2=[20-i for i in temp_list1]
            temp_df1['value']=temp_list2

            drug_test_motrix=drug_test_motrix.append(temp_df1.loc[temp_df1["drug"]==a_drug])


            drug_test_motrix=drug_test_motrix.append(motrix.loc[motrix["drug"]==a_drug])
            #drug_test_motrix=drug_test_motrix.append(motrix.loc[motrix["drug"]=='5282330'])
            #drug_test_motrix=drug_test_motrix.append(motrix.loc[motrix["protein"]=='5282330'])
            drug_test_motrix=drug_test_motrix.drop_duplicates(subset=['protein','drug'])

            drug_list.append(a_drug)
            drug_list_nstart.append(0)

        drug_test_motrix=drug_test_motrix.append(drug2drug)

        dict_drug=dict(zip(drug_list,drug_list_nstart))
        weight_dictx1={}
        for k,v in weight_dict1.items():
            weight_dictx1[k]=v

        for k,v in dict_drug.items():
            weight_dictx1[k]=v

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
        #nstart_pagerank = nx.pagerank(G, alpha=0.88, nstart=weight_dict)
        weighted_pagerank = nx.pagerank(G_weighted, alpha=0.88)
        weighted_personalized_pagerank = nx.pagerank(G_weighted, alpha=0.88, personalization=weight_dict, nstart=weight_dictx1)

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

        #parallel_debug=parallel_debug.append(result1)
        #parallel_debug.head(20)

        drug1=[]
        parallel_num=[]
        parallel_num1=[]
        for a_drug in drug_test:
            drug1.append(a_drug)
            #a_drug=int(a_drug)
            
            parallel_num.append(result1.loc[a_drug,'weighted_personalized_pagerank'])


        for num in parallel_num:
            parallel_num1.append(num)
            parallel_num1.append(100*num/sum(parallel_num))

        parallel_num1.append(sum(parallel_num))

        #这部分是分析药物联合跟最终结果的差异的
        x=0
        for protein in all_protein:
            #protein='CIRP1'
            rank=result1.loc[protein,'weighted_personalized_pagerank']
            expression=weight_dict.get(protein)
            x=x+rank*expression

        resultx=sum(parallel_num)*x/result1.loc[all_protein[0],'weighted_personalized_pagerank']
        parallel_num1.append(resultx)
        x=0
        #parallel_num1.append(sum(parallel_num)/(result1.loc[protein[0],'weighted_personalized_pagerank']))
        #parallel_num1.append(result1.loc[protein[0],'weighted_personalized_pagerank'])
        parallel_num1=drug1+parallel_num1

        parallel_motrix=parallel_motrix.append(pd.DataFrame(pd.DataFrame(parallel_num1).values.T))
        parallel_motrix=parallel_motrix.sort_values(by=parallel_motrix.columns.tolist()[-2], ascending=False) 
    

    column1=list("drug" for i in range(num_parallel))
    column2=['value','persentage']*num_parallel
    column3=column1+column2+['personalized_weight_pagerank','Drug-protein-expression fit score']
    parallel_motrix.columns=column3

    return parallel_motrix

