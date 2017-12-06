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
    totalCounts = 1
    city = 0
    name = "meituan"
    download_delay = 5
    cityName = ["杭州","广州","上海","北京","深圳","西安","重庆","南京","武汉","成都","兰州"]
    start_urls = [
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%9D%AD%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%B9%BF%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E4%B8%8A%E6%B5%B7&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%8C%97%E4%BA%AC&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%B7%B1%E5%9C%B3&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E8%A5%BF%E5%AE%89&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E9%87%8D%E5%BA%86&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%8D%97%E4%BA%AC&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%AD%A6%E6%B1%89&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%88%90%E9%83%BD&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%85%B0%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1"
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
        self.city += 1
        # 带着cookie向网站服务器发请求，表明我们是一个已登录的用户
        if self.start_urls[self.city-1]:
            yield Request(self.start_urls[self.city-1], callback=self.parse, cookies=self.cookie,
                      headers=self.headers, meta=self.meta)
        else:
            return

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @scrapes name
        """

        next_url = "http://hz.meituan.com/meishi/"
        url = [
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%9D%AD%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%B9%BF%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E4%B8%8A%E6%B5%B7&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%8C%97%E4%BA%AC&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%B7%B1%E5%9C%B3&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E8%A5%BF%E5%AE%89&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E9%87%8D%E5%BA%86&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%8D%97%E4%BA%AC&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%AD%A6%E6%B1%89&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%88%90%E9%83%BD&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%85%B0%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page="
               ]

        jsDict = json.loads(response.body)
        jsData = jsDict['data']
        self.totalCounts = jsData['totalCounts']
        if self.i > self.totalCounts:
            self.i = 1
            self.start_requests()
        jsPoiInfos = jsData['poiInfos']
        for each in jsPoiInfos:
                item = MTItem()
                next = next_url+str(each['poiId'])+"/"
                if next:
                    yield Request(next, meta={'item': item,'each':each}, callback=self.nextPage)

        url[self.city] = url[self.city] + str(self.i)
        yield Request(url[self.city], callback=self.parse)


    def nextPage(self,response):
        item = response.meta['item']
        each = response.meta['each']
        lon = re.search('"longitude":((\\d\d\d)(\\.\\d+))',response.body,re.S).group(0)
        lat = re.search('"latitude":((\\d\d)(\\.\\d+))',response.body,re.S).group(0)
        longitude = lon.split(":")
        latitude = lat.split(":")
        item['city'] = self.cityName[self.city-1]
        item['title'] = each['title']
        item['address'] = each['address']
        item['avgPrice'] = each['avgPrice']
        item['avgScore'] = each['avgScore']
        item['longitude'] = longitude[1]
        item['latitude'] = latitude[1]
        self.i += 1
        return item

