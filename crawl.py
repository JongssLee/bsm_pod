# crawl.py
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import hashlib
from pyppeteer import launch
from insta import login, upload
import os

async def fetch_articles():
    url = 'https://www.podbbang.com/channels/1776176'
    
    browser = None
    try:
        browser = await launch(headless=True, args=['--no-sandbox'])
        page = await browser.newPage()
        await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})
        
        await page.waitForSelector('.podcast-episode-list-item-component', {'timeout': 10000})
        
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        articles = soup.find_all('article', class_='podcast-episode-list-item-component list-item has-image')

        article_list = []

        for idx, article in enumerate(articles, start=1):
            title = article.find('h3').text
            img_link = article.find('img')['src']
            img_link = img_link.replace('430', '1280').replace('240', '750')
            unique_id = hashlib.md5(title.encode()).hexdigest()
            
            article_url = await fetch_article_url(browser, title, idx)
            if article_url:
                article_list.append({'id': unique_id, 'title': title, 'img_link': img_link, 'article_link': article_url})
            
            if idx >= 5:  # 처음 5개 항목만 처리 (테스트용)
                break

        return article_list
    except Exception as e:
        print(f"Error in fetch_articles: {e}")
        return []
    finally:
        if browser:
            await browser.close()
            await asyncio.sleep(1)  # 브라우저 종료 후 잠시 대기

async def fetch_article_url(browser, title, idx):
    try:
        page = await browser.newPage()
        await page.goto('https://www.podbbang.com/channels/1776176', {'waitUntil': 'networkidle0'})
        await page.waitForSelector('.podcast-episode-list-item-component', {'timeout': 10000})
        elements = await page.querySelectorAll('.podcast-episode-list-item-component')
        
        if idx <= len(elements):
            element = elements[idx - 1]
            
            await page.evaluate('(element) => element.scrollIntoView({behavior: "smooth", block: "center"})', element)
            await asyncio.sleep(1)

            await page.evaluate('(element) => element.click()', element)
            
            await page.waitForNavigation({'timeout': 10000, 'waitUntil': 'networkidle0'})
            url = page.url
            await page.close()
            return url
        else:
            await page.close()
            return None
    except Exception as e:
        print(f"Error in fetch_article_url: {e}")
        return None

async def save_articles(articles, filename='articles.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

async def load_articles(filename='articles.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            articles = json.load(file)
        return articles
    except FileNotFoundError:
        return []

async def download_image(session, url, id, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filename = f"{id}.jpg"
    filepath = os.path.join(folder, filename)
    
    async with session.get(url) as response:
        if response.status == 200:
            with open(filepath, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
    return filepath

async def check_for_new_articles():
    current_articles = await fetch_articles()
    saved_articles = await load_articles()

    saved_article_ids = {article['id'] for article in saved_articles}
    new_articles = [article for article in current_articles if article['id'] not in saved_article_ids]

    if new_articles:
        print("New article!!!")
        async with aiohttp.ClientSession() as session:
            for article in new_articles:
                local_image_path = await download_image(session, article['img_link'], article['id'])
                await upload(local_image_path, article['title'], article['article_link'])
                
                # 이미지 삭제
                os.remove(local_image_path)
        
        await save_articles(current_articles)


    return new_articles

async def main():
    await login()
    while True:
        new_articles = await check_for_new_articles()
        for article in new_articles:
            print(article['title'])
            print(article['img_link'])
        await asyncio.sleep(3600)  # Check every hour

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())