# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, re, time

url = 'http://shenzhen.qfang.com/map/sale/roomList'
payload = {'latitudeFrom': 22.484438,
           'latitudeTo': 22.83449,
           'longitudeFrom': 113.844809,
           'longitudeTo': 114.52206,
           'gardenId': '',
           'zoom': 12}
headers = {'Host': 'shenzhen.qfang.com',
           'Origin': 'http://shenzhen.qfang.com',
           'Referer': 'http://shenzhen.qfang.com/map/sale',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
params = {'currentPage': 1,
          'pageSize': 15,
          's': time.time()}
response = requests.post(url, data=payload, headers=headers, params=params)
content = BeautifulSoup(response.text, 'lxml')
# print content

rommPageSize = re.search('roomPageSize=(\d*)', content.script.text).group(1)
params['pageSize'] = rommPageSize
for page in range(int(rommPageSize)):
    params['currentPage'] = page + 1
    ##更新页数之后，需要重新request，然后用BeautifulSoup进行分析在爬取数据
    response = requests.post(url, data=payload, headers=headers, params=params)
    content = BeautifulSoup(response.text, 'lxml')
    for li in content.find_all('li', class_='clearfix'):
        roomid = li.get('roomid')
        lat = li.get('lat')
        lng = li.get('lng')
        title = li.get('title')
        pSpan = li.find('p', class_='hs-info-model clearfix')
        model = pSpan.span
        area = model.find_next('span')
        direction = area.find_next('span')
        print roomid, lat, lng, title, model.text, area.text, direction.text
