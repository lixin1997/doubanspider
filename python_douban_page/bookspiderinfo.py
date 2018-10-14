#! /usr/bin/python3
# 从图书详情页爬取相应的信息
import threading
import requests
from lxml import etree


class SpiderBookInfo(threading.Thread):
    """
    图书详情页爬虫，线程类
    """
    def __init__(self, book_url, headers, proxy, book_info_opath):
        """
        图书详情页信息爬虫，初始化。
        :param book_url: 图书详情页URL
        :param headers: 请求头信息
        :param proxy: 代理IP
        :param book_info_opath: 图书信息保存目录+文件名，例如：./info/book/3_new_book_info
        """
        threading.Thread.__init__(self)
        self.book_url = book_url
        self.book_info_opath = book_info_opath
        self.headers = headers
        self.proxy = proxy

    def run(self):
        """
        根据传递来的图书URL地址爬取当中的简要信息
        并保存到指定路径下的文件中
        :return:
        """
        book = {}
        book_info_page = requests.get(self.book_url, headers=self.headers, proxies=self.proxy)
        book_info_page_html = etree.HTML(book_info_page.text)
        # 获取图书名称并存储到book字典中
        book_name = book_info_page_html.xpath('//div[@id="mainpic"]/a/@title')[0]
        book['名称'] = book_name
        print('book info: get book info of ' + book_name)
        # 获取其他信息
        info_list = book_info_page_html.xpath('//div[@id="info"]//text()')
        infos = []
        # 删除info_list中没有的信息，并整理信息的格式
        # 奇数行：'key:'
        # 偶数行：'value'
        # 并存储到新的infos新集合中
        for info in info_list:
            cur = info.strip()
            if cur != '':
                if cur == ':':
                    infos[len(infos)-1] += cur
                else:
                    infos.append(cur)
        # 图书的其他信息添加到字段中
        i = 0
        length = len(infos)
        while length > i:
            book[infos[i][0:-1]] = infos[i+1]
            i += 2
        print('book info: save info of ' + book_name)
        with open(self.book_info_opath, 'a+', encoding='utf-8') as fp:
            fp.write(str(book) + '\n')


if __name__ == '__main__':
    """
        测试该文件代码
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
    }
    proxy = {
        'http': '106.75.164.15:3128'
    }
    book_info = SpiderBookInfo('https://book.douban.com/subject/30301369/', headers=headers, proxy=proxy,
                               book_info_opath='./info/book/3_new_book_info')
    book_info.start()
