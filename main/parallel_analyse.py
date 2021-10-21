import pandas as pd
import numpy as np

motrix=pd.read_csv("../data/motrix.csv")

motrix.head()


protein1=motrix["protein"].values.tolist()

drug1=motrix["drug"].values.tolist()

len_motrix=len(protein1)

