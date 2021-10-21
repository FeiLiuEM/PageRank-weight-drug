import pandas as pd
import numpy as np

#读取原始数据
#data=pd.read_csv("/Users/liufei/DATA/AutoDock/DATA_TOTAL.csv")

all_drugs=pd.read_csv("./data/all_drugs.csv").iloc[:,0].values.tolist()
drug_len=len(all_drugs)

#data.get("CIRP1")["Column3"]


def motrix_generate(file_path):
    data=pd.read_excel(file_path,sheet_name=None)

    keys=[]
    protein_len=0

    motrix=pd.DataFrame()

    list_protein=[]
    list_drug=[]
    list_value=[]
    

    #motrix["drugs"]=all_drugs

    for key in data:
        data_protein=data.get(key)



        test1=data_protein.sort_values(by='Column3', ascending=True) #按数值排序
        test2=test1.drop_duplicates(subset=['Column1'])   #去重
        test2["Column4"] = 0-test2["Column3"]        #获取正值

        test3=test2.sort_values(by='Column1', ascending=True) #药物名称排序统一
        
        drug_list=test3.iloc[:,0].values.tolist()    #提取这个蛋白的药物排名

        protein_value=test3.iloc[:,3].values.tolist()  #提取数据值

        #如果某些值小于特定值，则设定这个值为0
        for value in range(len(protein_value)):
            if protein_value[value] < 5:
                protein_value[value]=0

        #sum=np.sum(protein_value)

        '''
        for value1 in range(len(protein_value)):
            protein_value[value1]=protein_value[value1]/sum
        '''


        #明确药物列表中是否有缺失，如果有缺失的话需要添加上，并且值设定为0
        for drug_x in all_drugs:
            if drug_x not in drug_list:
                drug_list.append(drug_x)
                protein_value.append(0)

        protein_data_df=pd.DataFrame({'drug':drug_list,'protein':protein_value})

        protein_data_df1=protein_data_df.sort_values(by='drug', ascending=True) #药物名称排序统一

        protein_value_end=protein_data_df1.iloc[:,1].values.tolist()

        list_protein.extend([key]*drug_len)

        list_drug.extend(all_drugs)

        list_value.extend(protein_value_end)
        
        #motrix[key]=protein_value_end

        #protein_len=protein_len + 1

    #motrix.index=all_drugs

    motrix['protein']=list_protein
    motrix['durg']=list_drug
    motrix['value']=list_value

    return motrix



#test=motrix_generate("../data/DATA.xlsx")

