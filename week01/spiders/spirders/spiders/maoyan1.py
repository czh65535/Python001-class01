import scrapy
from bs4 import BeautifulSoup
from spirders.items import SpirdersItem

class Maoyan1Spider(scrapy.Spider):
    name = 'maoyan1'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    origin_url = "https://maoyan.com"

    ori_cookies = '__mta=119970487.1593248693021.1593248693021.1593248709765.2; uuid_n_v=v1; uuid=422A2290B85511EA909D9FF2C00A78C33DF95AF3C0364359AA70EDE98D6AD01C; _csrf=9c1968f7a55beacc30bf9358b0665d7d35d1fa79fbb8ad2629708bb611c5db17; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593248693; _lxsdk_cuid=172f505bae6c8-0fd9a42996c596-5f4e2917-384000-172f505bae6c8; _lxsdk=422A2290B85511EA909D9FF2C00A78C33DF95AF3C0364359AA70EDE98D6AD01C; mojo-uuid=8bc7559757bf3519eba8028179e30516; mojo-session-id={"id":"0168f376a1045cf7a419ef291126225f","time":1593248693013}; __mta=119970487.1593248693021.1593248693021.1593248693021.1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593248710; mojo-trace-id=3; _lxsdk_s=172f505bae7-dd9-7b1-4e0%7C%7C4'
    cookies = {}
    for line in ori_cookies.split(';'):
        key, value = line.split('=')
        cookies[key] = value

    def start_requests(self):
        for i in range(0, 1):
            target_url = f'https://maoyan.com/films?showType=3&offset={i * 30}'
            yield scrapy.Request(url=target_url, callback=self.parse, cookies=self.cookies)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for tags in soup.find_all('div', attrs = {'channel-detail movie-item-title'}, limit = 10):
            movie_name = tags.find('a').text
            movie_sub_url = self.origin_url + tags.find('a').get('href')

            item = SpirdersItem()
            item['movie_name'] = movie_name
            yield scrapy.Request(url=movie_sub_url, meta={'item': item}, callback=self.parse2, cookies=self.cookies)

    def parse2(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'html.parser')

        type = []
        for tags in soup.find('li', attrs={'class': 'ellipsis'}).find_all('a'):
            type.append(tags.text.strip())
        movie_type = ','.join(type)

        for tags in soup.find_all('li', attrs={'class': 'ellipsis'}):
            pass
        if tags:
            release_time = tags.text

        item['movie_type'] = movie_type
        item['release_time'] = release_time
        yield item