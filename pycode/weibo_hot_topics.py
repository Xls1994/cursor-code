import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_weibo_hot_topics():
    url = 'https://tophub.today/n/KqndgxeLl9'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', class_='table')
    rows = table.find_all('tr')
    
    hot_topics = []
    for row in rows:  # 跳过表头
        columns = row.find_all('td')
        rank = columns[0].text.strip()
        title = columns[1].text.strip()
        heat = columns[2].text.strip()
        link = columns[1].find('a')['href']
        
        hot_topics.append({
            '排名': rank,
            '标题': title,
            '热度': heat,
            # '链接': link
        })
    
    return hot_topics

def save_to_csv(hot_topics):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'weibo_hot_topics_{timestamp}.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['排名', '标题', '热度', '链接']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for topic in hot_topics:
            writer.writerow(topic)
    
    return filename

if __name__ == '__main__':
    hot_topics = get_weibo_hot_topics()
    saved_filename = save_to_csv(hot_topics)
    print(f'已成功爬取 {len(hot_topics)} 条微博热榜话题并保存到 {saved_filename} 文件中。')
