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
    i = 0            #店家数量计数
    pageCounts = 1   #页数
    totalCounts = 1  #从网页里返回的总店家数
    city = 0         #城市计数
    name = "meituan"
    download_delay = 3
    # ["杭州","广州","上海","北京","深圳","西安","重庆","南京","武汉","成都","兰州"]
    cityName = ["杭州","广州","上海","北京","深圳","西安","重庆","南京","武汉","成都","兰州"]
    start_urls = [
        "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%9D%AD%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://gz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%B9%BF%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://sh.meituan.com/meishi/api/poi/getPoiList?cityName=%E4%B8%8A%E6%B5%B7&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://bj.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%8C%97%E4%BA%AC&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://sz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%B7%B1%E5%9C%B3&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://xa.meituan.com/meishi/api/poi/getPoiList?cityName=%E8%A5%BF%E5%AE%89&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://cq.meituan.com/meishi/api/poi/getPoiList?cityName=%E9%87%8D%E5%BA%86&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://nj.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%8D%97%E4%BA%AC&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://wh.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%AD%A6%E6%B1%89&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://cd.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%88%90%E9%83%BD&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1",
        "http://lz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%85%B0%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1"
    ]

    cookie = settings['COOKIE']  # 带着Cookie向网页发请求
    # 发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需要
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'application/json, text/javascript'
    }
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

        next_url = [
                "http://hz.meituan.com/s/",
                "http://gz.meituan.com/s/",
                "http://sh.meituan.com/s/",
                "http://bj.meituan.com/s/",
                "http://sz.meituan.com/s/",
                "http://xa.meituan.com/s/",
                "http://cq.meituan.com/s/",
                "http://nj.meituan.com/s/",
                "http://wh.meituan.com/s/",
                "http://cd.meituan.com/s/",
                "http://lz.meituan.com/s/"
                    ]
        url = [
                "http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%9D%AD%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://gz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%B9%BF%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://sh.meituan.com/meishi/api/poi/getPoiList?cityName=%E4%B8%8A%E6%B5%B7&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://bj.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%8C%97%E4%BA%AC&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://sz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%B7%B1%E5%9C%B3&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://xa.meituan.com/meishi/api/poi/getPoiList?cityName=%E8%A5%BF%E5%AE%89&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://cq.meituan.com/meishi/api/poi/getPoiList?cityName=%E9%87%8D%E5%BA%86&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://nj.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%8D%97%E4%BA%AC&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://wh.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%AD%A6%E6%B1%89&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://cd.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%88%90%E9%83%BD&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=",
                "http://lz.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%85%B0%E5%B7%9E&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page="
               ]

        jsDict = json.loads(response.body)
        jsData = jsDict['data']
        #此城市总共的店家
        self.totalCounts = jsData['totalCounts']
        #每页32项，计算总的页数
        totalPage = self.totalCounts//32
        jsPoiInfos = jsData['poiInfos']
        #根据店名搜索每一家店的信息
        for each in jsPoiInfos:
            item = MTItem()
            next = next_url[self.city]+each['title']+"/"
            yield Request(next, meta={'item': item,'each':each}, callback=self.nextPage, cookies=self.cookie,
                    headers=self.headers)

        #前往下一页
        self.pageCounts += 1
        if self.totalCounts%32 > 0:
            totalPage += 1
        if self.pageCounts<=totalPage:
            url[self.city] = url[self.city] + str(self.pageCounts)
            print (url[self.city]+"\n")
            yield Request(url[self.city], callback=self.parse,cookies=self.cookie,
                    headers=self.headers)

        #爬完一个城市的数据，前往下一个城市
        #当前城市中有些数据失效，计数器达不到总的店家数
        #所以这一段并没有运行
        #是否有其他方法来判定？？？
        if self.i>=self.totalCounts:
            self.totalCounts = 0
            self.i = 0
            self.pageCounts = 1
            self.city += 1
            yield Request(url[self.city]+"1",callback=self.parse,cookies=self.cookie,
                    headers=self.headers)


    #爬取具体信息
    def nextPage(self,response):
        item = response.meta['item']
        each = response.meta['each']
        lon = re.search('"longitude":((\\d\d\d)(\\.\\d+))',response.body,re.S).group(0)
        lat = re.search('"latitude":((\\d\d)(\\.\\d+))',response.body,re.S).group(0)
        bcn = re.search('"backCateName":(.*?),',response.body,re.S).group(0)
        longitude = lon.split(":")
        latitude = lat.split(":")
        backCateName = bcn.split(":")
        item['city'] = self.cityName[self.city]
        item['title'] = each['title']
        item['address'] = each['address']
        item['avgPrice'] = each['avgPrice']
        item['avgScore'] = each['avgScore']
        item['longitude'] = longitude[1]
        item['latitude'] = latitude[1]
        item['backCateName'] = backCateName[1].strip(",").strip('"')
        self.i += 1
        print(str(self.i) + "     " + str(self.totalCounts) + "\n")
        return item

