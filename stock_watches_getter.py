# -*- coding: utf-8 -*-
"""
----------------------------------------------
    FileName:       stock_watchers_getter
    Description:    获取A股股票关注人数
    Author:         LaoG
----------------------------------------------
"""
from selenium import webdriver
#以下一句可以不导入，原因是在webdriver文件夹内的初始化文件已经导入,
#并重命名为FirefoxOptions. 但导入的是相对路径，因此引用时必须加前缀
#完整的引用方法为webdriver.FirefoxOptions
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from queue import Queue, Empty
from multiprocessing.dummy import Pool 
from threading import Thread

import re
from time import time 
from bs4 import BeautifulSoup


class GetWatchCount:  
    """获取个股关注人数.
    
    Attributes:
        _firefox_options: 配置firefox属性。主要设置其无头属性'-headless'。
        _driver_path: firefox执行驱动geckodriver路径。
        _pattern_sh: 上证A股匹配模式，'60'开头。
        _pattern_sz: 深证A股匹配模式，'00'或'30'开头。
    """
    _firefox_options = webdriver.FirefoxOptions()
    _driver_path = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe'
    _firefox_options.add_argument('-headless') 
    _pattern_sh = re.compile(r'^60')
    _pattern_sz = re.compile(r'^(?:00|30)')
    
    def __init__(self, stock_code):
        """
        Args:
            stock_code: 股票代码. 类型: str        
        """
        self.stock_code = stock_code
        self.driver = webdriver.Firefox(executable_path=self._driver_path, 
                                        options=self._firefox_options)
        #关注人数初始化为0
        self.number_of_watches = 0        
        
    def get_page(self):
        """页面获取
        
        Returns:
            返回页面文本，以供BeautifulSoup分析.
        """
        self.driver.get(self.url)
        #等待页面中出现class名'hint'的标签，出现即返回。最长等待时间为10秒。
        WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'hint')))
        page_text = self.driver.page_source
        return page_text       

    def get_counts(self):
        """页面分析，获取关注人数"""
        
        try:
            page_text = self.get_page()
            soup = BeautifulSoup(page_text, 'lxml')
            number_of_watches = soup.find('li', class_='hint').span.text
            #将关注人数设置为实例属性，方便获取
            self.number_of_watches = eval(number_of_watches)
        except:
#            print('此页面无法获取关注人数: {}'.format(self.url))
            pass
    
    def driver_close(self):
        """关闭 geckodriver 驱动"""
        
        self.driver.quit()

    @property
    def url(self):  
        """根据个股上市地点构造个股页面地址.
        
        使用@property装饰器，这样做的好处是无需增加实例属性即可象属性一样调用此函数.
        
        Returns:
            返回个股页面url        
        """
        if self._pattern_sh.match(self.stock_code):
            link = 'https://gupiao.baidu.com/stock/sh' + self.stock_code + '.html'
        elif self._pattern_sz.match(self.stock_code):
            link = 'https://gupiao.baidu.com/stock/sz' + self.stock_code + '.html'
        else:
            print('Invalid stock code！')
            return 
        return link


def get_watch(args):
    """获取股票关注人数
    
    Args:
        args: 股票代码与结果队列的二元组.    
    """
    stock_code, result_queue = args
    watch = GetWatchCount(stock_code)
    watch.get_counts()
    #关闭连接
    watch.driver_close()
    result_queue.put('{:<12}{}'.format(watch.stock_code, watch.number_of_watches))
#    return watch.stock_code, watch.number_of_watches


def get_result(result_queue):
    """获取结果队列中数据并输出至文件
    
    使用一个无限循环监视结果队列，一有数据即写入文件
    
    param: result_queue: 结果队列
    rtype: None
    """
    num = 0
    #daemon线程退出时，不会执行close()关闭文件。因此缓冲区数据不会写入文件。解决方法有二：
    #1、使用flush()方法；
    #2、打开文件时设置buffering=1,配置行缓冲模式。所谓行缓存，意指遇到换行符即写入文件。
    with open('d:/stock_watches.txt', 'wt', buffering=1) as f:
        while True:
            num += 1
            item = result_queue.get()
            f.write('{:<10}{}\n'.format(num, item))


def main():
    result_queue = Queue()    
    stock_codes = []
    
    with open('d:/A股代码.txt') as f:
        for line in f:
            #去除空行
            if not line.split():
                continue
            stock_codes.append(line.strip())      
    
    #建立一个股票代码及队列的二元组，方便使用map方法。
    args = zip(stock_codes, [result_queue]*len(stock_codes))
    pool = Pool(5)
    #注意这儿不能使用map方法，因map方法是堵塞的，需等待全部任务完成之后才会继续执行其后代码，
    #其后的监控线程不会立即启动，map_async在这儿是合适的，此方法不会堵塞其后线程启动，只会
    #堵塞在join()方法出。
    #另外，此处亦不可使用with关键字。异步调用不能使用with关键字，apply_async同理。测试发
    #如在异步方法使用with关键字，进程池实际上并没有启动。主线程会立即退出。因此需手动实现堵塞。
    pool.map_async(get_watch, args) 
    #建立监控线程，监控结果队列
    Thread(target=get_result, args=(result_queue,), daemon=True).start()
    pool.close()
    pool.join()


if __name__ == '__main__':
    start = time()
    main()
    end = time()
    print('总耗时 {:.2f} 分钟'.format((end-start)/60))