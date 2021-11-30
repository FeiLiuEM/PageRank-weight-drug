##########################
#  Designed by Fei Liu.
#     code = UTF-8
##########################

#This is a function to generate the motrix for the drug-protein interaction.

import pandas as pd
import numpy as np

#读取原始数据
#data=pd.read_excel("../data/DATA.xlsx",sheet_name=None)
#data_protein=data.get('CIRP1')
#data_protein.loc[data_protein["drug"]==all_drugs[0]].values.tolist()[0][2]
#test3.loc[test3["drug"]==all_drugs[0]].values.tolist()[0][2]

all_drugs=pd.read_csv("./data/all_drugs.csv").iloc[:,0].values.tolist()
drug_len=len(all_drugs)

#data.get("CIRP1")["value"]


def motrix_generate(file_path):
    data=pd.read_excel(file_path,sheet_name=None)

    proteins=[]
    protein_len=0

    motrix=pd.DataFrame()

    list_protein=[]
    list_drug=[]
    list_value=[]
    

    #motrix["drugs"]=all_drugs

    for key in data:
        data_protein=data.get(key)

        proteins.append(key)



        test1=data_protein.sort_values(by='value', ascending=True) #按数值排序
        test2=test1.drop_duplicates(subset=['drug'])   #去重
        test2["x1"] = 0-test2["value"]        #获取正值

        test3=test2.sort_values(by='drug', ascending=True) #药物名称排序统一
        
        drug_list=test3.iloc[:,0].values.tolist()    #提取这个蛋白的药物列表

        protein_value=test3.iloc[:,3].values.tolist()  #提取docking数据值

        #如果某些值小于特定值，则设定这个值为0
        for value in range(len(protein_value)):
            if protein_value[value] < 1:
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
            #添加药物到蛋白的数据
            #list_protein.extend([drug_x])

            #list_drug.extend([key])

            #a=test3.loc[test3["drug"]==drug_x].values.tolist()[0][3]
            #if a < 1:
            #    b=1
            #else:
            #    b=1/a
            #list_value.extend([b])   #添加药物到蛋白的数据


        protein_data_df=pd.DataFrame({'drug':drug_list,'protein':protein_value})

        protein_data_df1=protein_data_df.sort_values(by='drug', ascending=True) #药物名称排序统一

        protein_value_end=protein_data_df1.iloc[:,1].values.tolist()

        #添加蛋白到药物的数据
        list_protein.extend([key]*drug_len)

        list_drug.extend(all_drugs)

        list_value.extend(protein_value_end)

        #添加药物到蛋白的数据
        list_protein.extend(all_drugs)

        list_drug.extend([key]*drug_len)

        list_value.extend(protein_value_end)        

        #添加蛋白到蛋白的数据
        list_protein.extend([key])
        list_drug.extend([key])
        list_value.extend([10])

        
        #motrix[key]=protein_value_end

        #protein_len=protein_len + 1

    #motrix.index=all_drugs

    #添加药物到药物的数据   
    list_protein.extend(all_drugs)

    list_drug.extend(all_drugs)

    list_value.extend([10]*drug_len) 

    motrix['protein']=list_protein
    motrix['durg']=list_drug
    motrix['value']=list_value

    return proteins, data, motrix

#motrix.to_csv("../data/motrix.csv",index=False)

#test=motrix_generate("../data/DATA.xlsx")

