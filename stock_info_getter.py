# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    FileName:       stock_info_getter
    Description:    获取上证深证全部A股名及代码
    Author:         LaoG
    Date:           2017-3-2
-------------------------------------------------
"""

import requests
from bs4 import BeautifulSoup, SoupStrainer
from time import time
import re

HEADER = {'User-Agent': 'Mozilla/5.0'}

def get_html_text(url):
    """
    请求页面并获取页面。    
    
    参数：
        url: 信息数据请求地址
        header: 请求头。此参数可以不以参数形式传递，而是直接定义在本函数内。另外因为所有爬取请
        求都会使用此参数，因此也可以常量的形式定义。
            
    返回值：
        成功，返回页面文本；否，None
        
    返回类型:
        str或None        
    """    
    try:
        r = requests.get(url, headers=HEADER)
        r.raise_for_status
        #以页面实际编码修改默认编码。此步必须，否则可能导致页面中文为乱码。
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print(e)
        return None    

def get_stock_info(page):
    """
    解析页面并获取股票名称和代码
    
    参数：
        page: 页面文本
        
    返回值：
        所有股票名称和代码
        
    返回类型：
        dict    
    """
    stock_dict = {}
    soup = BeautifulSoup(page, 'lxml')
    stock_list = soup.select('div.quotebody ul li')
    pattern = re.compile(r'(.*)\(((?:60|00|30)\d{4})\)')
    #获取股票名称及代码
    for entry in stock_list:
        if pattern.match(entry.text):
            stock_name, stock_code = pattern.findall(entry.text)[0]
            stock_dict[stock_name] = stock_code
    
    return stock_dict
    
    
def main():
    #记录股票总数量
    count = 0
    url = "http://quote.eastmoney.com/stocklist.html"
       
    stock = {}
    page = get_html_text(url)    
    if page:
        stock = get_stock_info(page)   
        
    #写入文件
    with open('d://stock.txt', 'w', encoding='utf-8') as f:
        for stock_name, stock_code in stock.items():
            count += 1
#            f.write('{0:{2}<10}\t{1:}\n'.format(k, v, chr(12288)))
            f.write('{:10}\t{}\n'.format(stock_name, stock_code))
    
    print('A股数量共 {} 支.'.format(count))
    
    
if __name__ == '__main__':
    start = time()
    main()
    end = time()
    print('解析总耗时 {:.2f} 秒.'.format(end-start))

