# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
import pymysql


class SpirdersPipeline:
    def process_item(self, item, spider):
        movie_name = item['movie_name']
        movie_type = item['movie_type']
        release_time = item['release_time']
        ## output = f'|{movie_name}|\t|{movie_type}|\t|{release_time}|\n'
        ## with open('./maoyan_movie_request.csv', 'a+', encoding='utf-8') as article:
        ##     article.write(output)

        if spider.name == 'maoyan2':
            settings = get_project_settings()
            db = DataBaseHandle(host=settings['MYSQL_HOST'], username=settings['MYSQL_USER'],
                                password=settings['MYSQL_PASSWD'], port=settings['MYSQL_PORT'],
                                database=settings['MYSQL_DBNAME'], charset=settings['MYSQL_CHARSET'])
            sql = f"insert into scrapy_maoyan_movie(`movie_name`, `movie_type`, `release_time`) values('{movie_name}', '{movie_type}', '{release_time}');"
            db.insert_db(sql)
            db.close_db()
        return item


class DataBaseHandle():
    def __init__(self, host, username, password, port, database, charset):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database
        self.charset = charset
        self.db = pymysql.connect(host=self.host, user=self.username, password=self.password, port=self.port,
                                  database=self.database, charset=self.charset)

    def insert_db(self, sql):
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            self.cursor.close()

    def fetch_all(self, sql):
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except:
            print("Error: unable to fetch data")
        finally:
            self.cursor.close()

    def close_db(self):
        self.db.close()
