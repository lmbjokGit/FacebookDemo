# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy_splash import SplashRequest
import time
import os
from FacebookDemo.items import ProductItem

class lmSpider(Spider):
    name = 'lm'
    allowed_domains = ['localhost']

    url = 'file:///fd.html'
    seq = 0

    def start_requests(self):    #网页爬虫入口
        yield Request(self.url, callback=self.parse)


    def parse(self, response):   #网页数据分析
        _names = (response._url).split("/")     #数据存盘
        if len(_names[-1]) < 3:
            _fn = _names[-2]
        else:
            _fn = _names[-1]


        item = ProductItem()
        self.seq=int(time.time())
        sitelikes = response.xpath('//div[@id="pages_side_column"]').re_first(r'([0-9,]+) 位用户赞了')   #re规则取得点赞用户数
        sitelooks = response.xpath('//div[@id="pages_side_column"]').re_first(r'([0-9,]+) 位用户关注了') #re规则取得关注用户数
        item['sitelikes'] = sitelikes.replace(",", "")
        item['sitelooks'] = sitelooks.replace(",", "")
        item['sitename'] = '\''+_fn+'\''
        item['seq'] = self.seq
        item['likes']=''
        yield item

        articles = response.xpath('//div[@role="article"]')     #取得所有的article， 然后分析每一个article
        for article in articles:
            item = ProductItem()
            comment = '`'.join(article.xpath(
                './/div[contains(@class, " userContent ")]//div[@class="text_exposed_root"]//text()').extract()).strip()
            item['comment']='\''+comment.replace("'", "\"")+'\''
            likes = article.xpath(
                './/form[@class="commentable_item"]//span[@aria-label]//a[@aria-label]//text()').extract()
            if len(likes) > 0:
                item['like1'] = likes[0]
                if len(likes) == 1:
                    likes.append(0)

                item['like2'] = likes[1]
                item['likes'] = int(likes[0]) + int(likes[1])
                item['seq'] = self.seq
                item['sitelikes']=''
                yield item

    def error_parse(self, response):
        pass
