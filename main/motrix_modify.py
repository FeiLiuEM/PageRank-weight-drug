import pandas as pd
import numpy as np

def motrix_modify(motrix):

    protein=motrix.columns.values.tolist()
    drug=motrix.index.values.tolist()

    protein_len=len(protein)
    drug_len=len(drug)

    #数据矩阵上方的额外矩阵创建
    extra_pd1=pd.DataFrame(np.zeros((protein_len,protein_len)),columns=protein,index=protein)
        
    motrix1=pd.concat([extra_pd1,motrix],axis=0) #上下结合

    #数据矩阵右侧的额外矩阵创建
    extra_pd2=pd.DataFrame(np.zeros((protein_len+drug_len,drug_len)),columns=drug,index=protein+drug)

    motrix_end=pd.concat([motrix1,extra_pd2],axis=1)

    return motrix_end