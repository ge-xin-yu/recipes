# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    FileName:       ciba_words_dedupe.py
    Description:    词霸多个生词本合并并去除重复单词
    Author:         LaoG
    Date:           2017-5-6
----------------------------------------------------
"""

import re
import os
import codecs


def word_dedupe(words_book_path, words):
    """
    参数：
        words_book_path: 多个单词本路径
        words: 空字典
            
    返回值：
        去重之后的全部单词
        
    返回类型：
        dict    
    """
    
    #空列表，存放每一个词条
    entry = []
    #词霸生词表采用utf-16编码格式，因此需要使用codecs模块打开
    with codecs.open(words_book_path, 'r', 'utf-16') as f:
        lines = f.readlines()
        #第一个词条第一行表示单词，不能置于循环中，需要单独处理
        key = lines[0]
        for line in lines[1:]:     
            if not pattern.match(line):
                 entry.append(line)      
            else: 
                if key not in words:
                    words[key] = ''.join(entry)
                key = line
                entry = [] 
    return words


def save_to_file(words_dict, file): 
    """
    参数：
        words_dict: 去重之后的单词本，dict类型。
        file: 新生成的单词本文件。编码格式utf-16.
    
    返回值： 
        无    
    """
    with codecs.open(file, 'a', 'utf-16') as f:
        for k, v in words.items():
            f.write('{}{}'.format(k, v))
    
    
if __name__ == '__main__':
    words_book_path = 'D:\\单词本'
    words = {}
    #搜索模式，行首为+号的为词条
    pattern = re.compile(r'^\+')
    word_counts = 0
    save_file = "d:\\单词本.txt"
    #判断文件是否存在，如存在则清空。
    if os.path.exists(save_file):
        with open(save_file, 'w') as f:
            pass
        
    for word_file in os.scandir(words_book_path):
        words = word_dedupe(os.path.join(words_book_path, word_file.name), words)
    
    save_to_file(words, save_file)        
    print('总的单词数量为 {} 个'.format(len(words)))
    
    
