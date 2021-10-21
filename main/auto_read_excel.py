import pandas as pd
import os

class File_Hanlder():
    def __init__(self):
        pass
 
 
    def list_excel_dir(self,dir_path):
        self.dir_path = dir_path
        # 遍历目录
        excels_file = [i for i in os.listdir(self.dir_path) if i.endswith('.xlsx')]
        excels_path = [os.path.join(self.dir_path,i) for i in excels_file]
 
        # 保存该路径下所有的 excel 文件名的 列表
        self.excels_file = excels_file
        # 保存该路径下所有的 excel 文件名的 相对路径， './source_datas/表格名 '
        self.excels_path = excels_path
 
        return excels_file,excels_path
 
 
    def list_dir_all_files(self,source_dir):
        """
        给需要遍历的 目录路径，返回 所有文件的路径的列表 及 此文件所在目录的路径列表，俩个位子一一对应
        :param source_dir:
        :return:
        """
        father_dir_paths = []
        file_paths = []
        for root,dirs,files in os.walk(source_dir):
            for file in files:
                #获取文件所属目录
                father_dir_paths.append(root)
                #获取文件路径
                file_paths.append(os.path.join(root,file))
        return file_paths,father_dir_paths
 
    def single_excel_read(self,excel_path):
        """
        :param excel_path: 一张 excel表的 路径
        :return: excel 的 {sheet:dict} 数据 或者 单个DataFrame数据
        """
        io = pd.io.excel.ExcelFile(excel_path)
 
        content_tmp = pd.read_excel(io, sheet_name=None)
        # 判断源excel是否有多个 sheet
        if isinstance(content_tmp,dict):
            # 保存为 dict 数据
            self.content_dict = content_tmp
        else:
            # 保存为 DataFrame 数据
            self.content_df = content_tmp
        return content_tmp
 
    def single_excel_save(self, single_excel_sheets, excel_name, report_dir_path, sheet_names=None):
        """
        :param single_excel_sheets: 一张需要保存的 excel 的 {keys：df} 字典数据
        :excel_name  待保存的 源excel的名字
        :param report_path: 需要保存地址的 dir 路径
        :sheet_names 保存的excel表的sheet名，默认使用源数据字典的 key名
        :return:
        """
 
        utils.check_directory(report_dir_path)
        report_excel_name = 'report_' + excel_name
        report_excel_name = os.path.join(report_dir_path, report_excel_name)
 
        writer = pd.ExcelWriter(report_excel_name, engine='openpyxl')
 
        keys_iter = list(single_excel_sheets.keys())
        if sheet_names is None:
            sheet_names = keys_iter
        else:
            # 必须指定保存的 sheets 与 源表 dict 的 keys 数相同
            assert len(sheet_names) == len(keys_iter)
 
        logger.info('start save excel:{} ... '.format(excel_name))
        num = 1
        for idx, key in enumerate(keys_iter):
            # 下面的保存文件处填写writer，结果会不断地新增sheet，避免循环时被覆盖
            single_excel_sheets[key].to_excel(excel_writer=writer, sheet_name=sheet_names[idx], encoding="GBK")
            logger.info(sheet_names[idx] + "  保存成功！共%d个，这个 sheet 是第%d个。" % (len(sheet_names), num))
            num += 1
        writer.save()
        writer.close()
        logger.info('finish save excel:{} ... '.format(excel_name))
 
    def data_preprocess(self,dataframe):
        """
        预处理 DataFrame 的 NULL 值
        :return:
        """
        return dataframe.dropna()
 
    def multi_excels_read(self):
        pass
    def multi_excels_save(self):
        pass
 
 
 
if __name__ == '__main__':
 
    file_obj = File_Hanlder()
    _,files_path = file_obj.list_excel_dir('/Users/liufei/SYNC/CODE/ML-AI/Ranking/PageRank-Durg-Development/data')
    file_obj.single_excel_read(files_path[0])

    type(file_obj.content_dict)