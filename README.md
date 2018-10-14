# doubanspider

豆瓣网爬虫（此代码中仅提供爬取"豆瓣读书"下的新书速递和最受关注的图书，代码思想)

1.从豆瓣网首页（https://www.douban.com/）爬取所有分类信息目录，例如：豆瓣读书,https://book.douban.com

2.存储到文件执行当前目录下的info下，例如：./info/doubancategory.txt

3.根据爬取的分类信息，判别不同的类别，启动不同类别的线程爬虫。

4.例如：进入豆瓣读书，获取豆瓣读书页面中的"新书速递"和"最受关注的图书"的“更多”页面URL

5.将"新书速递"和"最受关注的图书"的“更多”页面URL，
	存储到./info/book/1_book_url.txt，
	存储格式：新书速递:https://book.douban.com/latest?icn=index-latestbook-all
	
6.爬取"新书速递"和"最受关注的图书"页面下所有的图书简介信息及URL
	存储到./info/book/2_new_book_info.txt
	存储格式：https://book.douban.com/subject/30309781/,爱情、疯狂和死亡的故事,[乌拉圭]奥拉西奥·基罗加,后浪丨四川文艺出版社,2018-11,“拉丁美洲短篇小说之王”奥拉西奥·基罗加短篇小说集。
	（注意：此处存储分隔符应该慎重，不应该为‘,’，避免简介中包含‘,’导致后期数据提取不便）————代码中不再更改
	
7.根据不同的URL，启动“爬取图书详情页爬虫程序”开始爬取每本书的详情信息，
	存储到./info/book/3_new_book_infos.txt
	存储格式（字典）：{'名称': '祖国旅店', '作者': '[土] 尤瑟夫·阿提冈', '出版社': '三辉图书 / 人民日报出版社', '出品方': '三辉图书', '原作名': 'Anayurt Oteli', '译者': '刘琳', '出版年': '2018-10', '装帧': '精装', '丛书': '三辉书系：阿提冈作品', 'ISBN': '9787511555823'}

