# -*- coding: utf-8 -*-
"""
--------------------------------------------------
    File Name：    cms_template_download.py    
    Description：  模板之家后台模板批量下载
    Author：       LaoG
    Date：         2017/5/5
--------------------------------------------------
"""

import requests
import re
from bs4 import BeautifulSoup


def get_html_text(url):
    """页面获取
    
    :param url: 总页面链接
    :return: 返回页面文本
    :rtype: str
    """
    header = {'User-Agent':'Mozilla/5.0'} 
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('Connect Error!')
        return 0 


def page_parse(base_url, page_text):
    """页面解析
    
    :param page_text: 页面文本，用于解析。
    :return: 返回全部下载链接
    :rtype: list
    """
    link = []
    soup = BeautifulSoup(page_text, 'lxml')
    #获取总页数
    pages = re.findall(r'\d{1,}', soup.table.span.text)
    pages = int(pages[0])
    
    #解析下载地址    
    for page in range(pages):
        if page == 0:
            url = base_url + 'index.shtml'
        else:
            url = base_url + 'index_' +str(page) + '.shtml'  
        soup = BeautifulSoup(get_html_text(url), 'lxml')
        lis = soup.find('ul', class_='thumbItem large clearfix').find_all('li')
        for li in lis:
            try:
                down_page ='http://www.cssmoban.com' + li.a['href']
                soup = BeautifulSoup(get_html_text(down_page), 'lxml')
                down_link = soup.find(title='免费下载')['href']
                link.append(down_link)
            except:
                pass    
    return link


def file_download(link, file_name):
    """文件下载
    
    :param link: 待下载链接。
    :return:
    """
    #若文件很大，可以考虑将stream置为True，同时iter_content指定块大小。
    saved_path = os.path.join('D:\\后台模板', file_name)
    r = requests.get(link, stream=False)    
    f = open(saved_path, 'wb')
    for chunk in r.iter_content():
        f.write(chunk)
    f.close()
    

def main():
    url = 'http://www.cssmoban.com/cssthemes/houtaimoban/'
    page = get_html_text(url)
    print('正在解析下载地址，请稍候...')
    down_link = page_parse(url, page)
    print('地址解析完毕，开始下载...\n')
    count = 0
    for link in down_link:  
        count += 1
        file_name = link.split('/')[-1]
        print('{:4}正在下载 {:50}'.format(count, file_name), end='')
        file_download(link, file_name)
        print('下载完成！')
    
    
if __name__ == '__main__':
    main()    
    
    
