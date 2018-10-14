#! /usr/bin/python3
# 豆瓣读书爬虫线程类
import threading
import requests
from lxml import etree
from python_douban_page.bookspiderinfo import SpiderBookInfo


# 豆瓣读书-最受关注图书爬虫
class InterestBookSpider(threading.Thread):
    """
    豆瓣读书-最受关注图书
    * _init_:构造方法，用于初始化对象
    * run:线程执行的流程
    * save_interest_book_brief_info:存储最受关注图书的简介信息
    * save_interest_book_detail_info:存储最受关注图书的详情信息
    """
    def __init__(self, interest_book_url, headers, proxy, interest_book_url_opath):
        """
        豆瓣读书-最受关注图书爬虫线程，初始化对象信息
        :param interest_book_url: 最受关注图书主页URL
        :param headers: 请求头信息
        :param proxy: 代理IP
        :param interest_book_url_opath:最受关注图书的信息存储目录
        """
        threading.Thread.__init__(self)
        self.interest_book_url = interest_book_url
        self.headers = headers
        self.proxy = proxy
        self.interest_book_url_opath = interest_book_url_opath

    def run(self):
        """
        最受关注图书页面的爬取
        爬取最受关注图书页面的上显示的每本书的简要信息
        根据每本书的URL详细信息地址，开启详细信息爬虫。
        :return:
        """
        print('new book info: start request interest book page-' + self.interest_book_url)
        # 爬取最受关注图书页面
        interest_book_index = requests.get(self.interest_book_url, headers=self.headers, proxies=self.proxy)
        interest_book_index_html = etree.HTML(interest_book_index.text)
        # 爬取最受关注图书页面中的所有图书信息
        interest_books_urls = interest_book_index_html.xpath('//li[@class="media clearfix"]')
        book_last = interest_book_index_html.xpath('//li[@class="media clearfix last"]')[0]
        with open(self.interest_book_url_opath + '2_interest_book_info.txt', 'a+', encoding='utf-8') as fp:
            # 循环图书列表，爬取简要信息，开启详细信息爬虫
            interest_book_info_opath = self.interest_book_url_opath + '3_interest_book_infos.txt'
            for info in interest_books_urls:
                book_url = self.save_interest_book_brief_info(info, fp)
                self.save_interest_book_detail_info(book_url, headers=self.headers, proxy=self.proxy,
                                                    book_info_opath=interest_book_info_opath)
            book_url_last = self.save_interest_book_brief_info(book_last, fp)
            self.save_interest_book_detail_info(book_url_last, headers=self.headers, proxy=self.proxy,
                                                book_info_opath=interest_book_info_opath)

    def save_interest_book_brief_info(self, info, fp):
        """
        提取并保存<li>标签下的最受关注图书简介信息。
        简要信息包括：图书详情页URL，图书名称，图书作者，图书出版社，图书出版日期，图书价格，图书装订，图书评分，图书售价
        :param info: 包含最受关注图书的<li>标签
        :param fp: 写入到指定文件的输出流
        :return: book_url该图书详细内容的URL网址信息
        """
        # 提取信息
        book_url = info.xpath('.//h2[@class="clearfix"]/a/@href')[0]
        book_name = info.xpath('.//h2[@class="clearfix"]/a/text()')[0]
        book_author_date_publish_price_style = info.xpath('.//p[@class="subject-abstract color-gray"]/text()')[0].strip().split(' / ')
        book_author = book_author_date_publish_price_style[0]
        book_date = book_author_date_publish_price_style[1]
        book_publish = book_author_date_publish_price_style[2]
        book_price = book_author_date_publish_price_style[3]
        book_style = book_author_date_publish_price_style[4]
        book_grade = info.xpath('.//p[@class="clearfix w250"]/span[@class="font-small color-red fleft"]/text()')[0]
        book_buy = info.xpath('.//span[@class="buy-info"]/a/text()')[0].strip()
        fp.write(book_url + ',' + book_name + ',' + book_author + ',' + book_date + ',' + book_publish + ','
              + book_price + ',' + book_style + ',' + book_grade + ',' + book_buy + '\n')
        return book_url

    def save_interest_book_detail_info(self, book_url, headers, proxy, book_info_opath):
        """
        启动每本图书的详情页爬虫
        :param book_url: 图书详情页URL
        :param headers: 请求头信息
        :param proxy: 代理IP
        :param book_info_opath: 图书详情页信息存储文件地址
        :return:
        """
        print('book info : get book info - ' + book_url)
        info_thread = SpiderBookInfo(book_url, headers=headers, proxy=proxy, book_info_opath=book_info_opath)
        info_thread.start()


# 豆瓣读书-新书速递爬虫
class NewBookSpider(threading.Thread):
    """
    豆瓣读书-新书速递
    * _init_:构造方法，用于初始化对象
    * run:线程执行的流程
    * save_new_book_brief_info:存储新书的简介信息
    * save_new_book_detail_info:存储新书的详情信息
    """

    def __init__(self, new_book_url, headers, proxy, new_book_url_opath):
        """
        豆瓣读书-新书速递爬虫线程，初始化对象信息
        :param new_book_url:新书速递的网址URL
        :param headers:请求头信息
        :param proxy:代理IP
        :param new_book_url_opath:新书存储目录
        """
        threading.Thread.__init__(self)
        self.new_book_url = new_book_url
        self.headers = headers
        self.proxy = proxy
        self.new_book_url_opath = new_book_url_opath

    def run(self):
        """
        新书速递页面的爬取
        爬取新书速递页面的上显示的每本书的简要信息
        根据每本书的URL详细信息地址，开启详细信息爬虫。
        :return:
        """
        print('new book info: start request new book page-' + self.new_book_url)
        # 爬取新书速递页面
        new_book_index = requests.get(self.new_book_url, headers=self.headers, proxies=self.proxy)
        new_book_index_html = etree.HTML(new_book_index.text)
        # 新书速递下的虚构类和非虚构类的所有图书<li>标签
        void_new_book_infos = new_book_index_html.xpath('//div[@class="article"]')[0].xpath('.//li')
        solid_new_book_infos = new_book_index_html.xpath('//div[@class="aside"]')[0].xpath('.//li')
        with open(self.new_book_url_opath+'2_new_book_info.txt', 'w', encoding='utf-8') as fp:
            # 循环虚构类图书列表，爬取简要信息，开启详细信息爬虫
            new_book_info_opath = self.new_book_url_opath+'3_new_book_infos.txt'
            for info in void_new_book_infos:
                book_url = self.save_new_book_brief_info(info, fp)
                self.save_new_book_detail_info(book_url, headers=self.headers, proxy=self.proxy, book_info_opath=new_book_info_opath)
            for info in solid_new_book_infos:
                book_url = self.save_new_book_brief_info(info, fp)
                self.save_new_book_detail_info(book_url, headers=self.headers, proxy=self.proxy, book_info_opath=new_book_info_opath)

    def save_new_book_brief_info(self, info, fp):
        """
        提取并保存<li>标签下的新书简介信息。
        简要信息包括：图书详情页URL，图书名称，图书作者，图书出版社，图书出版日期，图书描述
        :param info: 包含新书信息的<li>标签结构
        :param fp: 写入到指定文件的输出流
        :return: book_url该图书详细内容的URL网址信息
        """
        # 提取信息
        book_url = info.xpath('./div[@class="detail-frame"]/h2/a/@href')[0]
        book_name = info.xpath('./div[@class="detail-frame"]/h2/a/text()')[0]
        book_author_publish_date = info.xpath('./div[@class="detail-frame"]/p[2]/text()')[0].strip().split(' / ')
        book_author = book_author_publish_date[0]
        book_publish = book_author_publish_date[1]
        book_date = book_author_publish_date[2]
        book_detail = info.xpath('./div[@class="detail-frame"]/p[3]/text()')[0].strip()
        # 保存信息
        fp.write(book_url + ',' + book_name + ',' + book_author + ','
                 + book_publish + ',' + book_date + ',' + book_detail + '\n')
        return book_url

    def save_new_book_detail_info(self, book_url, headers, proxy, book_info_opath):
        """
        启动每本图书的详情页爬虫
        :param book_url: 图书详情页URL
        :param headers: 请求头信息
        :param proxy: 代理IP
        :param book_info_opath: 图书详情页信息存储文件地址
        :return:
        """
        info_thread = SpiderBookInfo(book_url, headers=headers, proxy=proxy, book_info_opath=book_info_opath)
        info_thread.start()


class BookSpider(threading.Thread):
    """
    爬取豆瓣读书网页——线程类
    """
    def __init__(self, book_url, headers, proxy, book_url_opath):
        """
        线程类的构造方法
        传入豆瓣读书网页的URL
        传入保存的目录，爬取豆瓣读书主页上新书速递中所有书的URL
        :param book_url:豆瓣读书的主页URL
        :param headers: 网址的请求头信息
        :param proxy: 请求网页时的IP代理信息
        :param book_url_opath:主页中新书速递每本书的URL信息的存放地址
        """
        threading.Thread.__init__(self)
        self.book_url = book_url
        self.headers = headers
        self.proxy = proxy
        self.book_url_opath = book_url_opath

    def run(self):
        print('book info-1: start request book douban page-' + self.book_url)
        book_index = requests.get(self.book_url, headers=self.headers, proxies=self.proxy)  # 获取豆瓣读书的首页
        book_index_html = etree.HTML(book_index.text)
        book_link_more_list = book_index_html.xpath('//span[@class="link-more"]')
        new_books_url = self.book_url + book_link_more_list[0].xpath('./a/@href')[0]
        void_inbooks_url = self.book_url + book_link_more_list[1].xpath('./a/@href')[0]
        solid_inbooks_url = self.book_url + book_link_more_list[2].xpath('./a/@href')[0]
        # url存储路径
        path = self.book_url_opath+'1_book_url.txt'
        print('book info-1: save URL to file-' + path)
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write('新书速递:' + new_books_url + '\n')
            fp.write('受关注图书（虚构类）:' + void_inbooks_url + '\n')
            fp.write('受关注图书（非虚构类）:' + solid_inbooks_url + '\n')
        # 新书速递爬取线程
        new_book_spider = NewBookSpider(new_books_url, headers=self.headers, proxy=self.proxy,
                                        new_book_url_opath=self.book_url_opath)
        new_book_spider.start()
        # 受关注图书（虚构类）爬取线程
        void_inbooks_spirder = InterestBookSpider(void_inbooks_url, headers=self.headers, proxy=self.proxy,
                                                  interest_book_url_opath=self.book_url_opath)
        void_inbooks_spirder.start()
        # 受关注图书（非虚构类）爬取线程
        solid_inbooks_spirder = InterestBookSpider(solid_inbooks_url, headers=self.headers, proxy=self.proxy,
                                                   interest_book_url_opath=self.book_url_opath)
        solid_inbooks_spirder.start()


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
    # book = BookSpider("https://book.douban.com", headers=headers, proxy=proxy, book_url_opath='./info/book/')
    # book.start()
    # new_book = NewBookSpider('https://book.douban.com/latest?icn=index-latestbook-all', headers=headers, proxy=proxy,
    #                          new_book_url_opath='./info/book/')
    # new_book.start()
    interest_book = InterestBookSpider('https://book.douban.com/chart?subcat=F&icn=index-topchart-fiction', headers=headers,
                                       proxy=proxy, interest_book_url_opath='./info/book/')
    interest_book.start()
