import requests
import pandas
from bs4 import BeautifulSoup as bs


user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
cookie = '__mta=119970487.1593248693021.1593248693021.1593248709765.2; uuid_n_v=v1; uuid=422A2290B85511EA909D9FF2C00A78C33DF95AF3C0364359AA70EDE98D6AD01C; _csrf=9c1968f7a55beacc30bf9358b0665d7d35d1fa79fbb8ad2629708bb611c5db17; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593248693; _lxsdk_cuid=172f505bae6c8-0fd9a42996c596-5f4e2917-384000-172f505bae6c8; _lxsdk=422A2290B85511EA909D9FF2C00A78C33DF95AF3C0364359AA70EDE98D6AD01C; mojo-uuid=8bc7559757bf3519eba8028179e30516; mojo-session-id={"id":"0168f376a1045cf7a419ef291126225f","time":1593248693013}; __mta=119970487.1593248693021.1593248693021.1593248693021.1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593248710; mojo-trace-id=3; _lxsdk_s=172f505bae7-dd9-7b1-4e0%7C%7C4'

request_header = {
    'user-agent' : user_agent,
    'cookie' : cookie
}

origin_url = "https://maoyan.com"

request_url = "https://maoyan.com/films?showType=3"


response = requests.get(request_url, headers = request_header)

bs_info = bs(response.text, 'html.parser')

tag_list = []
for tags in bs_info.find_all('div', attrs = {'channel-detail movie-item-title'}, limit = 10):
    title = tags.find('a').text
    sub_link = origin_url + tags.find('a').get('href')

    sub_response = requests.get(sub_link, headers=request_header)
    sub_bs_info = bs(sub_response.text, 'html.parser')

    movie_type = []
    for sub_tag in sub_bs_info.find('li', attrs={'class': 'ellipsis'}).find_all('a'):
        movie_type.append(sub_tag.text.strip())

    for sub_tag in sub_bs_info.find_all('li', attrs={'class': 'ellipsis'}):
        pass
    if sub_tag:
        release_time = sub_tag.text
    item = {}
    item["title"] = title
    item["type"] = movie_type
    item["time"] = release_time
    tag_list.append(item)

movie1 = pandas.DataFrame(data = tag_list)
movie1.to_csv('./maoyan_movie.csv', encoding = 'utf8', index = False, header= False)


