# bookInfoSpider
Python爬虫豆瓣网书籍信息

#简介
根据 https://book.douban.com/tag/  地址的图书标签，可以分别爬取各图书标签点进去后的书籍列表的信息，例如点击小说后的网址是https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4，在这个网页上可以得到书名，书籍图片链接，作者，译者，出版社，出版时间，价格的信息。
另外，还需要进入书籍具体界面获取更多信息，例如点击解忧杂货店进入的https://book.douban.com/subject/25862578/，会在这个我网页上获得ISBN信息（有的书会没有ISBN而是统一书号，那就获取统一书号）以及内容简介信息。
然后会爬虫到数据库里，还会生成同名日志文件


#使用说明
拉取bookInfoSpider.py文件，把share_bookdb.sql运行生成对应的share_bookdb数据库。
运行bookInfoSpider.py文件（想爬什么小标签里的所有书籍，就把标签名加入book_tag_lists中，另外大标签名赋值给big_tag_list）。
就可以把书籍信息增加到book_inf表中，以及r_book_category表会更新，这表示是每本书与对应的大标签ID关系的表。