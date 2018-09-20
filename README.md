FACEBOOK 爬虫Demo尝试
===

##项目内容概述
本项目是使用python3语言，利用开源的scrapy爬虫架构和splash插件爬取facebook特定网页的一个demo版本。因时间和经验的限制，本版本只做了一些功能点的尝试，没有完成全部功能，也没有做整体的架构设计（如任务框架，回调等），还有很多需要完善之处，仅供参考。<br>
项目实现了对特定facebook网页内容的动态获取，分析获取的数据并保存到数据库中。设计多个网页的并行爬取---因facebook单个页面内容的动态加载需要延时等待（可能需要数秒钟的时间）。而在等待的期间，机器可以去爬取另一个facebook网页，从而提高效率。

##项目缘起说明，及获取facebook网页数据的途径和爬虫程序的选择
2018年9月19日到9月21日间，某公司让我尝试写一个爬取facebook特定网页数据的程序，不使用facebook的API。

facebook和爬虫对我而言都是新的内容：此前，没有使用过facebook网站，也没有爬虫的编写经验。<br>
Fighting UP， 我首先得找找网上有哪些轮子可以用（最好有同样功能要求的sample，可惜没有）。在互联网上搜索facebook数据获取及爬虫程序的快速入门方法。我汇总分析搜索的结论如下：

###获取facebook数据的途径：
1. 通过Facebook发布的Graph API。 此种方式是Facebook官方的数据获取通道，数据资料最准确，权威，API通用且快速（可能是直接从数据库中提取数据）。但使用前要申请，说明使用用途，且有使用限制（包括单位时间内使用的次数等等），API也时不时根据facebook的需要调整。某公司先使用该方案在获取数据中。
2. 爬取facebook网页。对少数的网页可以使用此方案，可以独立自主维护管理。但需要了解facebook网页的生成方式，网页内容分析等，而且要考虑facebook封爬虫IP等。
3. 黑客facebook，直接get数据库。最NB的方式，能黑facebook的人不会坐在这写文档啦。

###爬虫程序
互联网上的爬虫程序一大堆，现在最热门火爆的编程语言是python，用python编写的开源爬虫程序中也最多。<br>
在Github上搜索"scrape"，以"most star"排名，第一名是scrapy（29.2k）。scrapy在网上的案例多，说明详细，入手较快，就选定他了。scrapy的Github网站：https://github.com/scrapy/scrapy； 说明文档：https://scrapy-chs.readthedocs.io/zh_CN/stable/index.html。<br>
网页动态加载常用的有两种：selenium+phantomjs；splash+lua。我这次选择了splash。 splash的Github网站：https://github.com/scrapy-plugins/scrapy-splash；  中文说明文档：https://scrapy-chs.readthedocs.io/zh_CN/stable/index.html。

##程序说明及测试使用
###Demo程序整体思路是:
1. 首先登录facebook，获得facebook网站的cookies。避免网页爬取时被login拦截，登录使用lua语言。
2. 同步加载(yield)多个网页的爬取程序（如上所述，并行爬取提升效率）。
3. 爬取某网页时，splash进行多次下拉到页尾，获取所需的内容。爬网使用lua语言，splash下拉的次数以参数形式提供。
4. 分析splash取得的网页，获取所需的内容，并保存到数据库中。

###测试使用
1. 基础环境部署-包括python3，scrapy, splash,  mysql，pymysql。 具体参考对应的安装文档；
2. 在mysql数据库中建立数据库、用户及表（建表及授权语句在pipelines.py文件中）， 修改pipelines.py中对应的参数；
3. 启动splash, 运行scrapy crawl lm 测试本地实际。 运行scrapy crawl facebook抓取网站数据。

 
##存在的问题
1. lua爬取网页时报504错误。 splash官网的解释如https://splash-cn-doc.readthedocs.io/zh_CN/latest/faq.html#i-m-getting-lots-of-504-timeout-errors-please-help
2. https://www.facebook.com/HankyuHanshinHD/ BootLoader加载还未搞定，需要时间研究。



##过程中感受及困难
在编写此demo过程中，第一次接触facebook网站，对facebook网站的页面深表佩服---facebook可能因为是一个社交网站，为了数据安全，网页内容基本都是使用javascript动态加载，而且为了避免被爬虫轻易获取，做了相当多的措施：需要登录，多层嵌套，DOM的动态id等等，还有某些页面，在显示后，在网页源代码中找不到显示的内容。如https://www.facebook.com/HankyuHanshinHD/网页。
因此原因，所以爬取facebook对新手比较困难，需要给与足够的时间去分析，才能取得更好的结果。<br>
古人云：`道高一尺魔高一丈`。对超级大神而言，facebook的各种防护都是小菜，所以也有facebook数据泄露的事情。


