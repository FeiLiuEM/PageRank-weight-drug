import pandas as pd
import numpy as np

motrix=pd.read_csv("~/SYNC/CODE/ML-AI/Ranking/pagerank-weight/data/motrix.csv")

motrix.head()


protein1=motrix["protein"].values.tolist()

drug1=motrix["drug"].values.tolist()

len_motrix=len(protein1)

value1=list=[5 for x in range(0,len_motrix)]

len(value1)

new_pd=pd.DataFrame()

new_pd["protein"]=drug1
new_pd["drug"]=protein1
new_pd["value"]=value1





