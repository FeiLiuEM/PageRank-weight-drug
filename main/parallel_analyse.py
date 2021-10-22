import pandas as pd
import numpy as np
from pandas.core.reshape.merge import merge

motrix=pd.read_csv("~/SYNC/CODE/ML-AI/Ranking/pagerank-weight/data/motrix.csv")

motrix.head()


protein1=motrix["protein"].values.tolist()

drug1=motrix["drug"].values.tolist()

len_motrix=len(protein1)

value1=list=[5 for x in range(0,len_motrix)]

len(value1)


protein=motrix["protein"].values.tolist()+drug1
drug=motrix["drug"].values.tolist()+protein1
value=motrix["value"].values.tolist()+value1


new_pd=pd.DataFrame()

new_pd["protein"]=protein
new_pd["drug"]=drug
new_pd["value"]=value



