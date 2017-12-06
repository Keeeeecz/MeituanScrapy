# -*- coding: utf-8 -*-

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = "_lxsdk=15fd428d815c8-03a08e975d79ae-464c0328-144000-15fd428d815c2; " \
             "_lxsdk_cuid=15fd42e9318c8-0341ddb0d76f5f-464c0328-144000-15fd42e93187a; " \
             "Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1511103385; iuuid=6646DE3D9AFCCD0E2DEF76E4C728B4ABDD73596F5884797E5641D4458811F99E;" \
             " cityname='%E6%9D%AD%E5%B7%9E'; __utma=74597006.615278503.1511615557.1511615557.1511615557.1; " \
             "__utmz=74597006.1511615557.1.1.utmcsr=hz.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/meishi/; lsu=; " \
             "token2=PeNVmHPw0UYTY3Z8FKNzSRzPYZwAAAAA-QQAABFtvurockFRKHmuZEpIKGGIzvCKKKMlqQfSPc9VW--BsJeuPAx2CAuEBTpr0ZBnqQ; " \
             "_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=214169128.1511095562352.1511619269711.1511774178946.6; " \
             "ci=50; rvct=50%2C1; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=214169128.1511095562352.1511774178946.1511790578419.7; " \
             "uuid=a0ec6c20db798017a365.1511093249.4.0.1; " \
             "oc=2jmLJHbQiQJDg1hI_ix5FvrlEjn7B3tPP-JKBwsyzvtLtGcg7val1mFydLf6R3QLUGq8KdKl64UA-mcrOoqYyjybYLhjqCMrbDG1u0ze6EAhL9g3FojUkpYes0AV5HhSc_c2SdDm3nLZeJemFpQF_rXmxqU4DjMZS-j7H2A_7VA; " \
             "client-id=81c24890-cb45-4924-ae7d-e55c1c2bedf1; _lxsdk_s=15ffdbd7d60-31-e33-430%7C%7C4"
    trans = transCookie(cookie)
    print trans.stringToDict()