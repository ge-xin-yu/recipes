# -*- coding: utf-8 -*-
"""
多进程测试
"""

import requests
from multiprocessing import Process, Pool
from multiprocessing import Queue
from time import time


URLS = [
       'https://www.baidu.com',
       'https://download.csdn.net/',
       'https://mp.weixin.qq.com/',
       'http://www.wps.cn/product/beta/',
       'https://www.etymonline.com/',
       'http://docs.python-requests.org/en/master/',
       'https://www.zhihu.com',
       'http://bbs.pinggu.org/',
       'http://www.tianya.cn/',
       'https://coderprog.com/',
       'https://zooqle.com/',    
       ]

HEADER = {'User-Agent': 'Mozilla/5.0'}
#自定义全局进程数
PROCESS_POOL_SIZE = 10
    
def worker(work_queue):
    while not work_queue.empty():
        url = work_queue.get()
        print(url)
        r = requests.get(url, headers=HEADER)        

def main(): 
    #注意多进程的队列和多线程的不同，其队列无需多线程中堵塞操作。因多进程并不共享内存，
    #进程之间的通信与多线程不同。这点需注意。事实上进程队列无task_done及join方法。
    work_queue = Queue()
    
    for url in URLS:    
        work_queue.put(url)
        
    processes = [Process(target=worker, args=(work_queue,)) for _ in range(PROCESS_POOL_SIZE)]
    
    for process in processes:
        process.start()
    
    while processes:
        processes.pop().join()   
 
#测试脚本
if __name__ == '__main__':    
    start = time()
    main()
    end = time()
    print('进程数：{}个\n总耗时：{:.2f} 秒'.format(PROCESS_POOL_SIZE,end-start))
    
    
