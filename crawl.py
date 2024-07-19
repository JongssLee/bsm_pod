import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests_html import HTMLSession

session = HTMLSession()

url = 'https://www.podbbang.com/channels/1776176'
r= session.get(url)

r.html.render(sleep=5, keep_page=True)

soup = BeautifulSoup(r.html.html, 'html.parser')
articles = soup.find_all('article', class_='podcast-episode-list-item-component list-item has-image')
i=0
for article in articles:
    title = article.find('h3').text
    img_link = article.find('img')['src']
    #link example: https://img.podbbang.com/pbi/t/430/240/0/988/461/000461988/461988.jpg
    #change 430 -> 640, 240->375
    img_link = img_link.replace('430', '1280').replace('240', '750')
    # save image
    img_data = requests.get(img_link).content
    with open(f'images/{i}.jpg', 'wb') as handler:
        handler.write(img_data)
    print(title)
    print(img_link) 
    i+=1