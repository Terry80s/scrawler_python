#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import os, sys
print(os.getcwd())
#sys.path.append(os.getcwd())
sys.path.append("..")
import scrapy
import time
import requests
import json
import base64
#from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from newscrawler.items import NewscrawlerItem
#from items import NewscrawlerItem
from scrapy.selector import Selector
from datetime import date, datetime, timezone, timedelta
from googletrans import Translator
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Queue

from twisted.internet import reactor,defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import scrapy.crawler as crawler

settings = get_project_settings()

JST = timezone(timedelta(hours=+9), 'JST')
CST = timezone(timedelta(hours=+8), 'CST')
#loc = datetime.fromtimestamp(now, CST)
#utc = datetime.fromtimestamp(now, timezone.utc)
#time.time()

###############################
#author:ChenRukun             #
#created:20180622             #
#scrapy crawl newscrawler     #
###############################
#金色财经爬虫
class NewsSpider1(scrapy.Spider):
    #爬虫启动参数初始化
    name = "newscrawler"
    allowed_domains= settings['ALLOWED_DOMAINS_1']
    start_urls= settings['START_URLS_1']

    #wp api 参数初始化
    wp_api_id = settings['WP_API_ID']
    wp_api_pw = settings['WP_API_PW']
    end_point_url = settings['END_POINT_URL']

    def parse(self, response):
        #对爬虫对象json解析
        body = response.body.decode('utf-8')
        #jdict = json.loads(response.body)
        jdict = json.loads(body)
        jlists = jdict["list"]
        if jlists:
            #实例化googletrans
            translaor = Translator()
            for list in jlists:
                for live in list["lives"]:
                    item = NewscrawlerItem()
                    #创建日期
                    item["date"] = list["date"]
                    #爬虫源文章ID
                    item["cid"] = live["id"]
                    #中文标题&中文内容
                    str_title_content = live["content"].split('】',1)
                    str_title = str_title_content[0].lstrip('【')
                    str_content = str_title_content[1]
                    item["title"] = str_title
                    item["content"] = str_content
                    #日文标题&日文内容
                    item["title_jp"] = translaor.translate(str_title, dest='ja').text
                    item["content_jp"] = translaor.translate(str_content, dest='ja').text
                    #重要度
                    item["grade"] = live["grade"]
                    #类别
                    item["sort"] = live["sort"]
                    #创建时间
                    loc = datetime.fromtimestamp(live["created_at"], JST)
                    item["created_at"] = loc
                    #好评数
                    item["up_counts"] = live["up_counts"]
                    #差评数
                    item["down_counts"] = live["down_counts"]
                    #赞数
                    item["zan_status"] = live["zan_status"]

                    #WP API投稿
                    wp_api_id = self.wp_api_id
                    wp_api_pw = self.wp_api_pw
                    end_point_url = self.end_point_url

                    p_grade = item["grade"]
                    p_title = str_title
                    p_content = str_content
                    p_title_jp = item["title_jp"]
                    p_content_jp = item["content_jp"]
                    p_category_jp = item["sort"]
                    p_create_at = item["created_at"]
                    p_up_count = item["up_counts"]
                    p_down_count = item["down_counts"]
                    payload = {
                                'title' : p_title,
                                'content' : p_content,
                                'status' : "draft",
                                'fields' : {
                                            'importance': p_grade,
                                            'title_JP' : p_title_jp,
                                            'content_JP' : p_content_jp,
                                            'category_JP' : p_category_jp,
                                            'tag' : "ビッグニュース_",
                                            'newsFrom' : "金色财经",
                                            'created_at' : p_create_at.isoformat(),
                                            'up_count' : p_up_count,
                                            'down_count' : p_down_count
                                            }
                                }
                    headers = {'content-type': "Application/json"}
                    r = requests.post(end_point_url, data=json.dumps(payload), headers=headers, auth=(wp_api_id, wp_api_pw))
                    # print(r)
                    print(item)
                    #yield item
        else:
            print("The news is empty!!!")

#火球财经爬虫
class NewsSpider2(scrapy.Spider):
    #爬虫启动参数初始化
    name = "newscrawler"
    allowed_domains= settings['ALLOWED_DOMAINS_2']
    start_urls= settings['START_URLS_2']

    #wp api 参数初始化
    wp_api_id = settings['WP_API_ID']
    wp_api_pw = settings['WP_API_PW']
    end_point_url = settings['END_POINT_URL']

    def parse(self, response):
        #对爬虫对象解析
        news = Selector(response).xpath("//div[@class='hq_newslist_container']")

        translaor = Translator()

        i = 0
        if news:
            for new in news:
                item = NewscrawlerItem()
                item["created_at"] = new.xpath("//div[@class='hq_newslist_time']/p/text()").extract()[i]
                #中文标题&中文内容
                str_title_content = new.xpath("//div[@class='hq_newslist_content']/p[1]/text()").extract()[i].strip().split('】',1)
                str_title = str_title_content[0].lstrip('【')
                str_content = str_title_content[1]
                item["title"] = str_title
                item["content"] = str_content
                #日文标题&日文内容
                item["title_jp"] = translaor.translate(str_title, dest='ja').text
                item["content_jp"] = translaor.translate(str_content, dest='ja').text
                #快讯下标
                i += 1

                #WP API投稿
                wp_api_id = self.wp_api_id
                wp_api_pw = self.wp_api_pw
                end_point_url = self.end_point_url

                p_title = item["title"]
                p_content = item["content"]
                p_title_jp = item["title_jp"]
                p_content_jp = item["content_jp"]
                p_create_at = item["created_at"]
                payload = {
                            'title' : p_title,
                            'content' : p_content,
                            'status' : "draft",
                            'fields' : {
                                        'importance': "",
                                        'title_JP' : p_title_jp,
                                        'content_JP' : p_content_jp,
                                        'tag' : "ビッグニュース_",
                                        'newsFrom' : "火球财经",
                                        'created_at' : p_create_at
                                        }
                            }
                headers = {'content-type': "Application/json"}
                r = requests.post(end_point_url, data=json.dumps(payload), headers=headers, auth=(wp_api_id, wp_api_pw))
                #print(r)
                print(item)
                #yield item
                if i==3:
                    break
        else:
            print("The news is empty!!!")

#币世界爬虫
class NewsSpider3(scrapy.Spider):
    #爬虫启动参数初始化
    name = "newscrawler"
    allowed_domains= settings['ALLOWED_DOMAINS_3']
    start_urls= settings['START_URLS_3']

    #wp api 参数初始化
    wp_api_id = settings['WP_API_ID']
    wp_api_pw = settings['WP_API_PW']
    end_point_url = settings['END_POINT_URL']

    def parse(self, response):
        #google翻译对象实例化
        translaor = Translator()

        #币世界日期标签
        now = datetime.now()
        nowstr = now.strftime('%Y-%m-%d')
        divtag = "live livetop "+nowstr
        divtag = "//div[@class='kuaixun_list']/div[@class='"+divtag+"']/ul"
        #对爬虫对象解析
        news = Selector(response).xpath(divtag)

        datasCheck = Selector(response).xpath(divtag+"/span[1]/text()").extract()
        for dataCheck in datasCheck:
            if dataCheck:
                print(dataCheck)
                print("币世界在[%s]有数据!"%(nowstr))
                break
            else:
                print("币世界在[%s]还没有数据!"%(nowstr))
                return 0
        i = 0
        for new in news:
            item = NewscrawlerItem()
            item["created_at"] = nowstr+" "+new.xpath("span[1]/text()").extract()[0]
            item["title"] = new.xpath("//h2/a/text()").extract()[i]
            item["content"] = new.xpath("li[1]/div/a/text()").extract()[0].strip()
            # #中文标题&中文内容
            str_title = item["title"]
            str_content = item["content"]
            #日文标题&日文内容
            item["title_jp"] = translaor.translate(str_title, dest='ja').text
            item["content_jp"] = translaor.translate(str_content, dest='ja').text
            #好评数
            item["up_counts"] = new.xpath("li[2]/div[1]/b/text()").extract()[0]
            #差评数
            item["down_counts"] = new.xpath("li[2]/div[2]/b/text()").extract()[0]
            #快讯下标
            i += 1

            #WP API投稿
            wp_api_id = self.wp_api_id
            wp_api_pw = self.wp_api_pw
            end_point_url = self.end_point_url

            p_title = item["title"]
            p_content = item["content"]
            p_title_jp = item["title_jp"]
            p_content_jp = item["content_jp"]
            p_create_at = item["created_at"]
            p_up_count = item["up_counts"]
            p_down_count = item["down_counts"]

            payload = {
                        'title' : p_title,
                        'content' : p_content,
                        'status' : "draft",
                        'fields' : {
                                    'importance': "",
                                    'title_JP' : p_title_jp,
                                    'content_JP' : p_content_jp,
                                    'tag' : "ビッグニュース_",
                                    'newsFrom' : "币世界",
                                    'created_at' : p_create_at,
                                    'up_count' : p_up_count,
                                    'down_count' : p_down_count
                                    }
                        }
            headers = {'content-type': "Application/json"}
            r = requests.post(end_point_url, data=json.dumps(payload), headers=headers, auth=(wp_api_id, wp_api_pw))
            # print(r)
            print(item)
            #yield item
            if i==3:
                break

#Running multiple spiders in the same process
#通过CrawlerRunner
# configure_logging()
# runner = CrawlerRunner()
# runner.crawl(NewsSpider1)
# runner.crawl(NewsSpider2)
# runner.crawl(NewsSpider3)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())
#
# reactor.run() # the script will block here until all crawling jobs are finished

#通过CrawlerProcess
# try:
#     process = CrawlerProcess()
#     process.crawl(NewsSpider1)
#     process.crawl(NewsSpider2)
#     process.crawl(NewsSpider3)
#     process.start()
# except Exception as e:
#     print("错误》》", e)

#↑会报raise error.ReactorNotRestartable()的异常,于是采用下述方法运行复数

# the wrapper to make it run more times
def run_spider(spider):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


print('first run:')
run_spider(NewsSpider1)

print('\nsecond run:')
run_spider(NewsSpider2)

print('\nthird run:')
run_spider(NewsSpider3)


# Usage
# if __name__ == "__main__":
#     #log.start()
#
#     process = CrawlerProcess()
#     crawler = NewsSpider()
#     try:
#         process.crawl(crawler)
#         process.start()
#         print("Completed")
#     except Exception as e:
#         print("错误》》", e)
