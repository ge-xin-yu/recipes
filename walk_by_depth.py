# -*- coding: utf-8 -*-
"""
os.walk虽可遍历目录，但无法指定深度。本小程序扩展了os.walk功能，
可以在遍历目录的时候的指定深度。
os.walk遍历目录的工作原理：
::os.walk为一生成器。首先从根目录开始，每次循环将本目录下的目
录及文件，及本目录放入三个列表变量中，循环次序从根目录始，遍历第
一个子目录，此目录遍历完毕后再返回遍历根目录下的第二个子目录，直
至结束。并非先完全遍历所有子目录一层，然后第二层，直至结束。总而
言之，os.walk是采用深度优先的原则遍历。
::os.walk返回三元组，root为字符串，dirs为目录名列表，files
亦为列表。目录列表不包含路径。完整路径必须使用join(root,dirs)
指定。
"""

import re
import os, sys, shutil
from os.path import join, getsize


def walk_by_depth(root_dir, depth=1):
    """
    参数：
        root_dir: 待遍历目录
        depth: 遍历深度，如不指定，默认深度为1.即只遍历此目录。
    返回值:
        无。由于os.walk本身返回的是生成器，本处于在遍历大目录的
        情况下节省内存；如将遍历数据保存并返回，实乃画蛇添足。因
        此，程序并未考虑返回值。对于目录及文件数据直接置于函数中
        处理；这种处理方式带来的缺点是不方便便携。
    """
    pattern = re.compile(r'/|\\')
    #判断根目录深度
    root_depth = len(pattern.split(root_dir))
    for root, dirs, files in os.walk(root_dir):
        #指定深度仅需一行代码即可，极简单；但解决了很多实际问题。
        if len(pattern.split(root)) > root_depth + depth -1:
            break
        else:
            """
            此处置入目录或文件处理代码。比如以下文件大小统计代码。            
            """
        total_size = sum([getsize(join(root,file)) for file in files])
        print('文件总大小 {:.2f}KB'.format(total_size/1024))
    return 0
    

def main():
    folder_path = "d:\\bios"
    walk_by_depth(folder_path, depth=3)


if __name__ == '__main__':
    main()


        
    
    