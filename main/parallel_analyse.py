import pandas as pd
import numpy as np


motrix=pd.read_csv("~/SYNC/CODE/ML-AI/Ranking/pagerank-weight/data/motrix.csv")
num_parallel=2 #多少种药物联合

motrix.head()


protein1=motrix["protein"].values.tolist()

drug1=motrix["drug"].values.tolist()

len_motrix=len(protein1)

value1=[5 for x in range(0,len_motrix)]

len(value1)


protein=motrix["protein"].values.tolist()+drug1
drug=motrix["drug"].values.tolist()+protein1
value=motrix["value"].values.tolist()+value1


new_pd=pd.DataFrame()

new_pd["protein"]=protein
new_pd["drug"]=drug
new_pd["value"]=value


new_pd.loc[new_pd["drug"]==6]

list(set(protein1))

#筛选出所有的类别
all_protein = list(set(protein1))
all_drug = list(set(drug1))

#进行排序
all_protein.sort(key=protein1.index)
all_drug.sort(key=drug1.index)
len(all_drug)


