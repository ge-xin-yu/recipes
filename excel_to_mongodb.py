# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------
    FileName:       excel_to_mongodb
    Description:    读取excel文件指定字段，并存入MongoDB数据库.
    Author:         LaoG
----------------------------------------------------------------
"""


import os
import xlrd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class SaveToMongoDB:
    """字段内容存入mongo数据库"""
    
    def __init__(self, fields, host, port):
        """
        :param fields: excel表待保存的部分字段名, list类型
        :param host: 数据库主机地址 
        :param port: 数据库端口     
        """
        self.fields = fields
        self.host = host
        self.port = port
        self.conn = self.connect()
        #选择数据库
        self.db = self.conn.stock
        #选择集合
        self.collection = self.db.sh        
    
    def connect(self):
        """连接至mongo数据库"""
        try:
            conn = MongoClient(self.host, self.port)
            #判断数据库是否连接成功。pymongo自3.0开始，当连接到数据库时，MongoClient构造
            #函数不再阻塞，也就是说，无论连接成功与否，都不会报错，因此需要此语句检查连接是否
            #有效。ismaster命令无需认证。
            conn.admin.command('ismaster')
            print("Connect to MongoDB Sucessfully.\n")
            return conn
        except ConnectionFailure:
            print("Connection Failure.")
            
    def save(self, row_value):
        """
        :param row_value: 每行的待提取字段内容。注意此值无需初始化为实例变量。
        :rtype: None
        """
        #生成数据字典
        item = dict(zip(self.fields, row_value))
        #向集合中插入数据
        self.collection.insert_one(item)        


def get_field_names(sheet, fields_list):
    """
    :param excel_file: excel文件xlrd对象
    :param fields_list: 待提取字段列表
    :return: 需要的部分字段名。
    :rtype: list
    """    
    #获取excel文件的字段名，一般为第一行。返回类型list,并去除字段名中的空字段。
    field_names =list(filter(None, sheet.row_values(0)))
    #提取需要字段的字段名,注意需要去掉字段名中空格。
    field_names = [field_names[x].strip() for x in fields_list]
#    print(field_names)
    return field_names
    

def main():  
    file_path = 'd:\\上证A股.xlsx'
    fields_list = [0,1,4,5,6]
    host = '192.168.2.102'
    port = 27017
    #读取excel文件
    excel_file = xlrd.open_workbook(file_path)
    sheet = excel_file.sheets()[0]
    fields_names = get_field_names(sheet, fields_list)
    db = SaveToMongoDB(fields_names, host, port)
    
    for index in range(1, sheet.nrows):
        #提取需要的字段值
        lst = [sheet.row_values(index)[x] for x in fields_list]
        #去除文本字段两端可能的空格
        lst = [x.strip() if isinstance(x, str) else x for x in lst]
        #连接并存入数据库
        db.save(lst)   
    
    print('{} saved to MongoDB sucessfully..'.format(os.path.basename(file_path)))


if __name__ == '__main__':
    main()    
    
