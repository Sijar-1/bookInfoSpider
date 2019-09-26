# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 14:47:49 2019

@author: Sijar
"""

#-*- coding: UTF-8 -*-

import importlib,sys
import time
import urllib
import urllib.request  
import numpy as np
from bs4 import BeautifulSoup
from openpyxl import Workbook
import logging
from logging.handlers import TimedRotatingFileHandler
import traceback


importlib.reload(sys)


#Some User Agents

hds=[{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'},\
       {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
       {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'},\
       {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},\
       {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
       {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
       {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
       {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'},\
       {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
       {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'}]

#hds=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE")
book_list=[]
book_list2=[]
big_tag_list=""
plain_text=""
def book_spider(book_tag):
    page_num=0
    if book_tag=="经济学":
        page_num=10
    try_times=0
    
    while(1):
        logging.debug("标签的url形式===="+urllib.parse.quote(book_tag))
       # url='http://www.douban.com/tag/%E7%A7%91%E6%99%AE/book?start=0&type=T' # For Test
        url='http://book.douban.com/tag/'+urllib.parse.quote(book_tag)+'?start='+str(page_num*20)+'&type=T'  #quote()可以将中文转换为URL编码格式
        time.sleep(np.random.rand()*20)
       
        try:
           # req = urllib.request.Request(url, headers=hds[page_num%len(hds)])
            req = urllib.request.Request(url)
            #source_code = urllib.request.urlopen(req).read()
            source_code=opener.open(req)
            plain_text=source_code.read()
            logging.info("<start>爬取到 "+book_tag+" 的第 "+str(page_num+1)+" 个网页<start>")
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logging.debug(traceback.format_exc())
            continue
        
        soup = BeautifulSoup(plain_text,'lxml')
        list_soup=soup.find('ul',{'class':'subject-list'})
        logging.info("---find  list_soup ---")
        
        try_times+=1;
        if list_soup==None and try_times<3:
            logging.debug("----------list_soup=None and try_times="+try_times)
            continue
        elif list_soup==None or len(list_soup)<=1:
            logging.debug("----------list_soup=None or len(list_soup)<=1  and list_soup="+str(list_soup))
            break # Break when no informatoin got after 3 times requesting
        for book_info in list_soup.findAll('li'):
            img_pic_path=book_info.find('img')
            if img_pic_path!=None:
                pic_path= img_pic_path.get('src')
                logging.debug("pic_path= "+str(pic_path))
            else:
                pic_path=""
            a_title=book_info.find('h2').find('a')
            title=a_title.get('title')
            logging.info("title="+str(title))          
            more_info_url=a_title.get('href')
            logging.debug("more_info_url=="+more_info_url)                      
            try:
                req2 = urllib.request.Request(more_info_url)
                source_code2 = opener.open(req2)
                plain_text2=source_code2.read()
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                logging.debug(traceback.format_exc())               
                
            soup2 = BeautifulSoup(plain_text2, 'lxml')
            list_soup2 = soup2.find(id="info").get_text('\n','<br/>')
            #logging.debug("list_soup2======"+list_soup2)
            ISBN_position=list_soup2.find('ISBN')
            logging.debug("ISBN_pos====" + str(ISBN_position))
            if ISBN_position==-1:
                ISBN_position=list_soup2.find("统一书号")
            ISBN_info=list_soup2[ISBN_position+5:].strip()
            logging.info("ISBN_info===="+ISBN_info)          
            if soup2.find('div',attrs={'class':'intro'})!=None:    
                brief_intro=soup2.find('div',attrs={'class':'intro'}).get_text()
                logging.debug(" brief_intro=" + str(brief_intro).strip())
            else:
                brief_intro=""
            
            desc=book_info.find('div',{'class':'pub'}).string.strip()
            if desc!="":
                desc_list=desc.split('/')
                try:
                    author_info = desc_list[0].strip()
                    logging.debug("author=" + author_info)
                except:
                    author_info = "暂无"
                    logging.debug("author=" + author_info)
                translator=""
                if len(desc_list)==5:
                    translator=desc_list[1].strip()
                    logging.debug("translator=" + translator)
                try:
                    publisher_info=desc_list[-3].strip()
                    logging.debug("publisher_info="+publisher_info)
                except:
                    publisher_info ="暂无"
                    logging.debug("publisher_info=" + publisher_info)
                try:
                    pub_time=desc_list[-2].strip()
                    logging.debug("pub_time="+pub_time)
                except:
                    pub_time ="暂无"
                    logging.debug("pub_time=" + pub_time)
                try:
                    price_info=desc_list[-1].strip()
                    logging.debug("price_info="+price_info)
                except:
                    price_info="暂无"
                    logging.debug("price_info="+price_info)
                
            book_list.append([pic_path,title, author_info, translator,publisher_info,pub_time,price_info,brief_intro,ISBN_info])
            book_list2=[pic_path,title, author_info, translator,publisher_info,pub_time,price_info,brief_intro,ISBN_info]
            addin_mysql2(book_list2,book_tag)
            sqlBookCategory(ISBN_info,big_tag_list)
 
            
            try_times=0 #set 0 when got valid information
        page_num+=1
        
        #print ('Downloading Information From Page %d' % page_num)
    return book_list




def my_db(host,user,passwd,db,sql,values,port=3306,charset='utf8'):
    import pymysql
    conn=pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cur = conn.cursor()
    values=values
    cur.execute(sql,values)
    if sql.strip()[:6].upper() == 'SELECT':
        res = cur.rowcount
    else:
        conn.commit()
        res='ok'
    cur.close()
    conn.close()
    return res

def addin_mysql2(bl,book_tag_lists):
    sql1="select ISBN from book_inf where ISBN =%s"
    values1=[bl[8]]
    #res=my_db('localhost', 'root', '', 'share_bookdb', sql1, values1, 3306, 'utf8')
    res=my_db('101.37.173.235', 'root', 'Root@0420', 'share_bookdb', sql1, values1, 3306, 'utf8')
    if res==1:
        sql2="update book_inf set BOOK_NAME=%s,AUTHOR=%s,TRANSLATOR=%s,PUBLISHER=%s\
        ,PUB_TIME=%s,PRICE=%s,BRIEF_INTRO=%s,PIC_PATH=%s  where ISBN= %s"
        values2=[bl[1],bl[2],bl[3],bl[4],bl[5],bl[6],bl[7],bl[0],bl[8]]
       # my_db('localhost', 'root', '', 'share_bookdb', sql2, values2, 3306, 'utf8')
        my_db('101.37.173.235', 'root', 'Root@0420', 'share_bookdb', sql2, values2, 3306, 'utf8')
    else:
        sql="insert into book_inf (ISBN,BOOK_NAME,AUTHOR,TRANSLATOR,PUBLISHER,PUB_TIME,\
        PRICE,BRIEF_INTRO,PIC_PATH)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=[bl[8],bl[1],bl[2],bl[3],bl[4],bl[5],bl[6],bl[7],bl[0]]
        #my_db('localhost', 'root', '', 'share_bookdb', sql,values, 3306, 'utf8')
        my_db('101.37.173.235', 'root', 'Root@0420', 'share_bookdb', sql, values, 3306, 'utf8')



def do_spider2(book_tag_lists):
    for book_tag in book_tag_lists:
        logging.debug("book_tag(标签名如科普，互联网)===="+book_tag)
        book_spider(book_tag)



def sqlBookCategory(ISBN,catg_name):
    sql1="select * from r_book_category r, category_inf c where ISBN= %s and r.CATG_ID =c.CATG_ID and CATG_NAME=%s"
    values1=[ISBN,catg_name]
    #res=my_db('localhost', 'root', '', 'share_bookdb', sql1, values1, 3306, 'utf8')
    res=my_db('101.37.173.235', 'root', 'Root@0420', 'share_bookdb', sql1, values1, 3306, 'utf8')
    if res!=1:
        sql2="insert into r_book_category (ISBN,CATG_ID) values(%s,(select CATG_ID from category_inf book_inf where CATG_NAME=%s ))"
        values2=[ISBN,catg_name]
        #my_db('localhost', 'root', '', 'share_bookdb', sql2, values2, 3306, 'utf8')
        my_db('101.37.173.235', 'root', 'Root@0420', 'share_bookdb', sql2, values2, 3306, 'utf8')
    
    

if __name__=='__main__':
    # 日志打印格式
    log_fmt = "%(asctime)s  line %(lineno)s %(levelname)s: %(message)s"
    formatter = logging.Formatter(log_fmt)
    # 创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(filename="bookInfoSpider.log", when="D", interval=1, backupCount=30)
    log_file_handler.suffix = "%Y-%m-%d.log"
    log_file_handler.setLevel('INFO')
    #log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel('INFO')
    logger.addHandler(log_file_handler)
    
    
    http_handler = urllib.request.HTTPHandler(debuglevel=1)
    # 调用build_opener()方法构建一个自定义的opener对象，参数是构建的处理器对象
    opener = urllib.request.build_opener(http_handler)

    #book_tag_lists = ['心理','判断与决策','算法','数据结构','经济','历史']
   
    #文学大类
    #big_tag_list="文学"
    #book_tag_list=['小说','外国文学','文学','随笔','中国文学','经典','日本文学','散文']
    #book_tag_list=['村上春树','诗歌','童话','儿童文学','名著','古典文学','王小波','余华']
    #book_tag_list=['杂文','张爱玲','当代文学','外国名著','钱钟书','鲁迅','诗词','茨威格']
    #book_tag_list=['米兰·昆德拉','杜拉斯','港台']
    
    #流行大类
    #big_tag_list="流行"    
    #book_tag_list=['漫画','推理','绘本','青春','东野奎吾','科幻','悬疑','言情']
    #book_tag_list=['奇幻','武侠','推理小说','日本漫画','耽美','韩寒','网络小说','亦舒']
    #book_tag_list=['三毛','科幻小说','阿加莎·克里斯蒂','安妮宝贝','金庸','穿越','郭敬明','轻小说']
    #book_tag_list=['魔幻','青春文学','几米','J.K.罗琳','幾米','张小娴','古龙','高木直子']
     #book_tag_list=['校园','沧月','余秋雨','落落']
    
    #文化大类
    #big_tag_list="文化"
    #book_tag_lists = ['历史','心理学','哲学','传记','社会学','文化','艺术','社会']
    #book_tag_lists=['设计','政治','建筑','宗教','电影','政治学','数学','中国历史']
    #book_tag_list=['回忆录','思想','国学','人物传记','艺术史','人文','音乐','绘画']
    #book_tag_lists=['戏剧','西方哲学','二战','近代史','军事','佛教','考古','自由主义','美术']
    
    #生活大类
    #big_tag_list="生活"
    #book_tag_list=['爱情','成长','生活','旅行','心理','励志','女性','摄影']
    #book_tag_list=['教育','职场','美食','游记','灵修','健康','情感','人际关系']
    #book_tag_list=['两性','手工','养生','家居','自助游']
    #book_tag_list=['','','','','','','','']
    
    #经管大类
    big_tag_list="经管"
    book_tag_lists = ['经济学','管理','经济','商业','金融','投资','营销','理财','创业','股票','广告','企业史','策划']
    #科技大类
    #big_tag_list="科技"
   # book_tag_lists = ['科普','互联网','编程','科学','交互设计','用户体验','算法','科技','web','交互','通信','UE','UCD','神经网络','程序']

    do_spider2(book_tag_lists)

    
