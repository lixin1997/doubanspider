#! /usr/bin/python3
# 爬虫之豆瓣网信息、
import requests
from lxml import etree

# 豆瓣网主页URL
from python_douban_page.bookdouban import BookSpider

dou_ban_url = 'https://www.douban.com/'

# 存储豆瓣网的分类网址
dou_ban_category = []
# 分类网址存储文件地址
dou_ban_category_text_path = './info/doubancategory.txt'
# 豆瓣读书信息存放路径
dou_ban_book_path='./info/book/'

# 请求信息头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
}
# 定义代理服务器的IP地址和端口
proxy = {
    'http': '106.75.164.15:3128'
}


# 第一步：从豆瓣网的首页中获取豆瓣网所有的网站的分类
def get_dou_ban_index():
    """
    爬取豆瓣网的主页
    获取豆瓣网每个类别的URL
    存储到dou_ban_category集合中
    写到./info/doubancategory.txt文件里
    :return:
    """
    print('info: start request douban first page.')
    # 请求豆瓣网首页
    dou_ban_index = requests.get(dou_ban_url, headers=headers, proxies=proxy)
    # lxml工具对爬取的网页进行修复
    dou_ban_index_html = etree.HTML(dou_ban_index.text)
    # 获取网站的分类信息
    dou_ban_category_info = dou_ban_index_html.xpath('//div[@class="anony-nav-links"]/ul//a')
    # 提取分类名称及地址
    print('info: save category info to File-' + dou_ban_category_text_path)
    with open(dou_ban_category_text_path, 'w', encoding='utf-8') as fp:
        for info in dou_ban_category_info:
            category_url = info.xpath('./@href')[0]
            category_name = info.xpath('./text()')[0]
            fp.write(category_name + ',' + category_url + '\n')
            category = {
                'category_url': category_url,
                'category_name': category_name
            }
            dou_ban_category.append(category)


def judge_category(categories):
    """
    判断分类信息的类别，调用专用的爬取函数进行爬取
    应该线程来进行每个类别的爬取
    :param categories: 集合，存放从豆瓣网首页爬取的豆瓣各类别的URL
    :return:
    """
    print('info: start judge category register spider.')
    for category in categories:
        cate_name = category.get('category_name')
        cate_url = category.get('category_url')
        if cate_name == '豆瓣读书':
            # print('开始爬取“豆瓣读书”！' + cate_url)
            print('info: BookSpider starting working to spider ' + cate_url)
            book_spider = BookSpider(cate_url, headers=headers, proxy=proxy, book_url_opath=dou_ban_book_path)
            book_spider.start()
        elif cate_name == '豆瓣电影':
            # print('开始爬取“豆瓣电影”！' + cate_url)
            pass
        elif cate_name == '豆瓣音乐':
            # print('开始爬取“豆瓣音乐”！' + cate_url)
            pass
        elif cate_name == '豆瓣小组':
            # print('开始爬取“豆瓣小组”！' + cate_url)
            pass
        elif cate_name == '豆瓣同城':
            # print('开始爬取“豆瓣同城”！' + cate_url)
            pass
        elif cate_name == '豆瓣FM':
            # print('开始爬取“豆瓣FM”！' + cate_url)
            pass
        elif cate_name == '豆瓣时间':
            # print('开始爬取“豆瓣时间”！' + cate_url)
            pass
        elif cate_name == '豆瓣豆品':
            # print('开始爬取“豆瓣豆品”！' + cate_url)
            pass
        else:
            pass


def main():
    """
    豆瓣网爬虫程序的主流程
    首先、爬取豆瓣网主页获取豆瓣网分类信息
    其次、根据不同类别开启不同类别的爬虫进行爬取信息
    :return:
    """
    # 获取豆瓣网主页中的分类信息
    get_dou_ban_index()
    # 根据分类信息，调用专用的爬虫线程
    judge_category(dou_ban_category)


# 主程序入口
if __name__ == '__main__':
    main()
