# -*- coding: utf-8 -*-
"""
------------------------------------------
    FileName:       file_batch_rename
    Description:    下载文件批量改名
    Author:         LaoG
    Date:           2017-4-6
------------------------------------------
"""

import re
import os
import sys
from string import capwords


def files_batch_rename(dir_path):
    """
    去除路径之下所有目录(包括子目录)及文件中的连字符，并将目录和文件名中的所有单词首字母大写。
    
    :param dir_path: 文件存放路径
    :rtype: None   
    """
    
    #遍历目录及其子目录，注意topdown需要自下往上，因为如果自上往下，则顶层目录
    #修改之后，其后的文件夹名及文件名的路径就出现了问题。
    for root, dirs, files in os.walk(dir_path, topdown=False):
        #修改文件名
        for file in files:
            #分离文件名及扩展名。
            file_name, ext_name = os.path.splitext(file)
            #搜索文件名中的连字符。
            if pattern.search(file_name):
                
                new_file = capwords(pattern.sub(' ', file_name)) + ext_name
                os.rename(os.path.join(root, file), os.path.join(root, new_file))
        #修改目录名
        for dir in dirs:
            if pattern.search(dir):
                #修改单词首字母改大写
                new_dir = capwords(pattern.sub(' ', dir))
                os.rename(os.path.join(root, dir), os.path.join(root,new_dir))            
    return 0
       

def main():
    #定义文件及目录名中需要去除的的连字符。
    pattern = re.compile(r'[\._－+-]')
    dir_path = "D:/Downloads/temp_books"
    files_batch_rename(dir_path)
    
    
if __name__ == "__main__":
   main()