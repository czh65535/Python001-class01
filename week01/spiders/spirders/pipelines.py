# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SpirdersPipeline:
    def process_item(self, item, spider):
        movie_name = item['movie_name']
        movie_type = item['movie_type']
        release_time = item['release_time']
        output = f'|{movie_name}|\t|{movie_type}|\t|{release_time}|\n'
        with open('./maoyan_movie_request.csv', 'a+', encoding='utf-8') as article:
            article.write(output)
        return item

