# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy_splash import SplashRequest
from FacebookDemo.items import ProductItem
import time


lua_login_script = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local ok, reason = splash:go(splash.args.url)
    user_name = splash.args.user_name
    user_passwd = splash.args.user_passwd
    user_text = splash:select("#email")
    pass_text = splash:select("#pass")
    login_btn = splash:select("#loginbutton")
    splash:wait(1)
    if (user_text and pass_text and login_btn) then
        user_text:send_text(user_name)
        pass_text:send_text(user_passwd)
        login_btn:mouse_click({})
    end

    splash:wait(math.random(5, 10))
    
    return {
        url = splash:url(),
        cookies = splash:get_cookies(),
        headers = splash.args.headers,
      }
end
"""

lua_script = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    splash.images_enabled = false
    local url = splash.args.url
    local ok, reason = splash:go(url)
    local loop=splash.args.loop
    local i=0
    splash:wait(3)
    
    while (i < loop) do
        --local ok2, reason2 = pcall(splash:runjs([[window.scrollTo(0, document.body.scrollHeight)]])) 
        --local ok2, reason2 = splash:runjs([[window.scrollTo(0, document.body.scrollHeight)]])
        ok2 = assert(splash:runjs([[window.scrollTo(0, document.body.scrollHeight)]]))
        --print("*****",response.status(),"******")
        if not ok2 then
            --print(reason2)
            break
        else
            splash:wait(math.random(1,2))
            htmlsave=splash:html()
            i = i+1
            print("======= url= ",url, " ===== iii=",i," ========")
        end
        
    end

    return {
        url = splash:url(),
        html = htmlsave,
        cookies = splash:get_cookies(),
    }
end
"""


class facebookSpider(Spider):
    name = 'facebook'
    allowed_domains = ['www.facebook.com']

    url = 'http://www.facebook.com'
    login_url = 'http://www.facebook.com/login.php'

    seq=0

    def start_requests(self):    #网页爬虫入口， 使用splash登录facebook，获得cookies
        user = "limeng@fsig.com.cn"
        password = "n3F-STQ-ZKJ-gdX"

        yield SplashRequest(
            url=self.login_url,
            endpoint="execute",
            args={
                "lua_source": lua_login_script,
                "user_name": user,
                "user_passwd": password,
            },
            callback=self.after_login,
        )

    def after_login(self, response):     #登录facebook成功后， 调度生成（yield）多个网页的分析程序
        for site in self.settings.get('FACEBOOKSITES'):
            site_url = site[0]
            site_looptimes = site[1]

            yield SplashRequest(
                url=site_url,
                endpoint="execute",
                args={
                    "loop": site_looptimes,
                    "lua_source": lua_script,
                },
                callback=self.parse,
            )

    def parse(self, response):    #解析生成的网页数据
        _names = (response._url).split("/")     #数据存盘
        if len(_names[-1]) < 3:
            _fn = _names[-2]
        else:
            _fn = _names[-1]
        ll = response.body.decode("utf-8")
        fp = open(_fn, "w")
        fp.write(ll)
        fp.close()

        item = ProductItem()
        self.seq=int(time.time())
        sitelikes = response.xpath('//div[@id="pages_side_column"]').re_first(r'([0-9,]+) 位用户赞了')
        sitelooks = response.xpath('//div[@id="pages_side_column"]').re_first(r'([0-9,]+) 位用户关注了')
        item['sitelikes'] = sitelikes.replace(",", "")
        item['sitelooks'] = sitelooks.replace(",", "")
        item['seq'] = self.seq
        item['likes']=''
        yield item

        articles = response.xpath('//div[@role="article"]')
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
