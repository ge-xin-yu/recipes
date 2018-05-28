# -*- coding: utf-8 -*-
"""
---------------------------------------------
    FileName:       file_hash_calculation 
    Description:    计算文件hash值
    Author:         LaoG
---------------------------------------------
"""

"""
+----------------------------------------------------+
|                                                    |
|  Usage:                                            |
|      file_hash_calculation.py filename hash_type   |
|                                                    |
|  Params:                                           |
|      -h/--help:   for help                         |  
|      filename:    file path                        |
|      hash_type:   hash type, MD5 or SHA1 support.  |
|                                                    |
|  Examples:                                         |
|     file_hash_calculation.py -h                    |
|     file_hash_calculation.py example.ext md5       |
|     file_hash_calculation.py example.ext sha1      |
|                                                    |
+----------------------------------------------------+
"""


import os
import sys
import hashlib


def read_chunks(file, chunksize):
    """分块读文件
    
    Args:
        file: 待读取文件
        chunksize: 块大小
        
    Returns:
        文件块生成器
    """
    while True:
        chunk = file.read(chunksize)
        if not chunk:
            break
        yield chunk



def md5_calculation(file, chunksize=None):
    """计算文件md5值
    
    Args:
        file: 待处理文件
        chunksize: 块大小。默认不分块
    
    Returns:
        文件md5值
    """
    
    md5 = hashlib.md5()
    #已处理的字节数
    processed_bytes = 0
    filesize = os.path.getsize(file)
    with open(file, 'rb') as f:   
        for chunk in read_chunks(f, chunksize):
            md5.update(chunk)
            #显示处理进度
            processed_bytes = processed_bytes + len(chunk)
            print('\r{:.2f}%'.format(processed_bytes*100/filesize), end='')
    return md5.hexdigest()
            
        
def sha1_calculation(file, chunksize=None):
    """计算文件sha1值
    
    Args:
        file: 待处理文件
        chunksize: 块大小。默认不分块。
    
    Returns:
        文件sha1值
    """
    
    sha1 = hashlib.sha1()
    processed_bytes = 0
    filesize = os.path.getsize(file)
    with open(file, 'rb') as f:
        for chunk in read_chunks(f, chunksize):
            sha1.update(chunk)
            #显示处理进度
            processed_bytes = processed_bytes + len(chunk)
            print('\r{:.2f}%'.format(processed_bytes*100/filesize), end='')
    return sha1.hexdigest()
        

def args_parse(args):
    """错误处理
    
    使用错误信息收集器，根据收集器中的错误个数返回参数状态。程序扫描所有参数，
    如第一个参数有误，程序不会停止分析即刻返回，而是会继续扫描下一个参数，直
    至结束，然后输出所有的分析结果。            
    
    Args:
        args: 命令行参数
    """
    err_mesg = []
    if len(args) == 1:
        #如不带参数，则打印帮助信息，并返回False，退出程序。
        print('Usage: {} filename MD5|SHA1'.format(os.path.basename(args[0])))
        return False
    elif len(args) ==  2:
        if args[1] in ['-h', '--help']:
            print('Usage: {} filename MD5|SHA1'.format(os.path.basename(args[0])))
        else:
            err_mesg.append('Error: Unknown parameter. Please retry "-h" or "--help".')      
    elif len(args) == 3:        
        file, digest_type = args[1], args[2]
        digest_type = digest_type.lower()        
        if not os.path.isfile(file):            
            err_mesg.append('File not Found.')            
        if not digest_type in ['md5', 'sha1']:            
            err_mesg.append('DigestTypeError: "{}" not Support! MD5 or SHA1 either.'.format(digest_type))    
    else:
        err_mesg.append('Params Error! Please see "-h" for help.')
    
    err_cnt = len(err_mesg)
    if err_cnt == 0:
        return True
    elif err_cnt == 1:
        print(err_mesg[0])
    elif err_cnt == 2:
        print('ERRORS:')
        for i in range(err_cnt):
            print('{:>5}: {}'.format(i+1, err_mesg[i]))
    return False
        
  
def main():
    #定义每次读取的数据块大小
    chunksize = 1024*1024
    if args_parse(sys.argv):
        file, digest_type = sys.argv[1], sys.argv[2]
        if digest_type.lower() == 'md5':
            hash_value = md5_calculation(file, chunksize)
        else:
           hash_value = sha1_calculation(file, chunksize) 
        print('\n{}: {}'.format(digest_type, hash_value)) 
    
    
if __name__ == '__main__':
    main()       

   