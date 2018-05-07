# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------
    FileName:       proxy_validate_login_auto.py
    Description:    代理服务器验证/双队列/自动登录
    Author:         LaoG
-----------------------------------------------------------
"""

import re
import time

import requests
from threading import Thread
from queue import Queue, Empty
from bs4 import BeautifulSoup, element


#定义线程池数量
POOL_SIZE=100
#定义http请求头部
HEADER = {'User-Agent':'Mozilla/5.0'}

def nth_of_nextsibling(reference_tag, depths):
    """
    获取第n个非'\n'的兄弟节点。解决BeautifulSoup中的nextsibling方法遍历时会将'\n'作为有效的兄弟节点的问题。
    
    :param reference_tag: 起始标签节点
    :param depths: 自起始标签始第n个非'\n'兄弟节点
    :rtype: bs4.element.Tag    
    """
    result = reference_tag
    for _ in range(depths):
        result = result.next_sibling
    return result   
    
#获取有效验证次数。
def get_counts_of_visited(url, session):
    """
    获取有效的验证次数。
    
    :param url: 保存验证有效次数链接地址
    :param session: 网站会话，携带cookies
    :rtype: int
    
    """
    target_page = session.get(url, headers=HEADER)
    soup = BeautifulSoup(target_page.text, 'lxml')
    visited_tag = nth_of_nextsibling(soup.find('td', string='访问推广'), 4)
    visited_counts = int(visited_tag.get_text())
    return visited_counts

#代理服务器验证
def proxy_validate(host):   
    """
    验证代理服务器有效性
    
    :param host: 代理服务器主机地址；形式为host:port
    :return: 代理服务器是否有效的打印信息。
    :rtype: str    
    """
    header={'User-agent':'Mozilla/5.0'}
    timeout=30
    domain='http://'+host
    proxy={'http':host}
    url='http://bbs.pinggu.org/?fromuid=9753530'
    regex=re.compile(r"经管之家")
    try:
        r=requests.get(url, headers=header, proxies=proxy, timeout=timeout)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
    except:
#        result='{:40}连接失败'.format(domain)
        pass
    else:
        if regex.search(r.text):
            result='{:40}代理有效'.format(domain)
            with open("d:/valid_proxy.txt", 'a') as f:
                f.write(domain+'\n')
        else:
            result='{:40}无效代理'.format(domain)
        #注意：如果需要返回连接失败信息，return语句需向前置于整个函数之下
        #而不能置于else语句之下。
        return result  


def worker(work_queue, result_queue):
    """
    工作队列，调用proxy_validate函数验证队列中的每个代理服务器地址。
    
    :param work_queue: 保存代理服务器地址的队列
    :param result_queue: 结果队列，保存代理服务器是否有效的打印信息。
    :return: None    
    """
    while not work_queue.empty():
        try:
            item = work_queue.get()            
        except Empty:
            break
        else:
            result = proxy_validate(item)
            if result:
                result_queue.put(result)
            work_queue.task_done()
            

def print_worker(result_queue):
    """
    打印后台队列。不断循环，只要发现结果队列中有数据即输出。后台队列的特点是非阻塞，主线程退出，即自动退出。
    
    :param result_queue: 结果队列，存放代理服务器是否有效的打印信息。
    :return: None    
    """
    count = 0
    while True:
        count += 1
        item = result_queue.get()
        print('{:<4}  {}'.format(count,item))
        result_queue.task_done()        
                

def main():    
    work_queue = Queue()
    result_queue = Queue()
    with open('d:/proxy.txt', 'r') as f:
        lines=f.readlines()        
        for line in lines:
            host=line.split('@')[0]
            work_queue.put(host)            
    threads=[Thread(target=worker, args=(work_queue,result_queue))
             for _ in range(POOL_SIZE)]   
    print_thread=Thread(target=print_worker, args=(result_queue,))
    print_thread.daemon=True
    for thread in threads:
        thread.start() 
    print_thread.start()         
    work_queue.join()
    while threads:
        threads.pop().join()
         

if __name__ == "__main__" :    
    rounds = 0
    #登录地址
    login_url = "http://passport.pinggu.org/login/ajaxLogin"
    #登录后的获取有效验证次数地址
    url_after_login = 'http://bbs.pinggu.org/home.php?mod=spacecp&ac=credit&op=log&suboperation=creditrulelog'
    #模拟自动登录
    login_data = {
            'username': '网吧流浪者', 
            'password': 'd167c5297ee8e068b4e411d32d70c3d9'
    }   
    session = requests.Session()
    r = session.post(login_url, data=login_data)
    #通过cookies值判断是否成功登录。网站返回cookies包含两个键，i分别为sso_hash、sso_hash_low.
    if 'sso_hash' and 'sso_hash_low' in r.cookies.keys():
        for _ in range(1):        
            main()
            rounds += 1
            counts = get_counts_of_visited(url_after_login, session)
            print('第{}轮验证：有效次数 {} 次\n'.format(rounds,counts))
            if counts >= 30:
                break
    else:
        print('Login Failed!')
    print('本次共测试 {} 轮'.format(rounds))            
        
        
        