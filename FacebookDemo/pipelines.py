# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



"""
CREATE DATABASE IF NOT EXISTS python default charset utf8mb4;
create user python@'%' identified by 'python';
grant all on python.* to python@'%';
flush privileges;
use python
create table sites (id int(16) unsigned not null auto_increment, \
				seq int(32),likes int(16),looks int(16),primary key(id));

create table articles (id int(16) unsigned not null auto_increment, \
				seq int(32), \
				comment varchar(16000), \
				like1 int(16), \
				like2 int(16), \
				likes int(16), \
				primary key(id));

"""

import pymysql
from  FacebookDemo import settings


class MysqlPipeline(object):
    def __init__(self):
        self.myhost = settings.MYHOST
        self.myuser = settings.MYUSER
        self.mypassword = settings.MYPASSWORD
        self.mydb = settings.MYDB
        self.myport = settings.MYPORT


    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.myhost,
                                  user=self.myuser,
                                  password=self.mypassword,
                                  db=self.mydb,
                                  #port=self.myport,
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)

        self.cursor=self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self,item, spider):
        if item['sitelikes'] == '' and item['likes'] == '':
            #return None
            pass

        if item['sitelikes'] != '':
            sql='insert into  sites (`seq`, `likes`, `looks`) values (%s, %s, %s)' % (item['seq'], item['sitelikes'], item['sitelooks'])
        else:
            sql='insert into  articles (`seq`, `comment`, `like1`, `like2`, `likes`) values (%s, %s, %s, %s, %s)  ' % (item['seq'], item['comment'], item['like1'], item['like2'], item['likes'])

        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        return item
