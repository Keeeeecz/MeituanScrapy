# -*- coding: utf-8 -*-
import scrapy, sys
import scrapy.spiders
from scrapy.conf import settings
from scrapy import Request
from debug.items import MTItem
import json
import re
# 设置编码格式
reload(sys)
sys.setdefaultencoding('gbk')


class DmozSpider(scrapy.spiders.Spider):
    i = 1
    name = "meituan"
    download_delay = 10
    start_urls = [
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%9D%AD%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1"
    ]

    cookie = settings['COOKIE']  # 带着Cookie向网页发请求
    # 发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需要
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302],  # 对哪些异常返回进行处理
    }

    # 爬虫的起点
    def start_requests(self):
        # 带着cookie向网站服务器发请求，表明我们是一个已登录的用户
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie,
                      headers=self.headers, meta=self.meta)

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @scrapes name
        """
        if self.i > 19:
            return
        next_url = "http://hz.meituan.com/meishi/"
        url = "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%9D%AD%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page="

        jsDict = json.loads(response.body)
        jsData = jsDict['data']
        jsPoiInfos = jsData['poiInfos']
        for each in jsPoiInfos:
                item = MTItem()
                next = next_url+str(each['poiId'])+"/"
                item['title'] = each['title']
                item['address'] = each['address']
                item['avgPrice'] = each['avgPrice']
                item['avgScore'] = each['avgScore']
                if next:
                    yield Request(next, meta={'item': item}, callback=self.nextPage)
                if each['poiId']==2508925:
                    return
                yield item
        self.i += 1
        url = url + str(self.i)
        yield Request(url, callback=self.parse)


    def nextPage(self,response):
        item = response.meta['item']
        lon = re.search('"longitude":((\\d\d\d)(\\.\\d+))',response.body,re.S).group(0)
        lat = re.search('"latitude":((\\d\d)(\\.\\d+))',response.body,re.S).group(0)
        longitude = lon.split(":")
        latitude = lat.split(":")
        item['longitude'] = longitude[1]
        item['latitude'] = latitude[1]
        return item

