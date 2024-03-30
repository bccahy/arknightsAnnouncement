import requests
from bs4 import BeautifulSoup

url = 'https://ak.hypergryph.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href is not None:
        if href.startswith('http'):
            links.append(href)
        elif href.startswith('/'):
            links.append(url + href)

prefix = 'https://ak.hypergryph.com/news/20'
new_list = [url for url in links if url.startswith(prefix)]

print(new_list)

# 飞书机器人的 Webhook URL
webhook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/612a16cf-3a85-4969-87fc-27c95db1d960'

# 发送消息给飞书机器人
def send_message_to_feishu(text):
    data = {
        'msg_type': 'text',
        'content': {
            'text': text
        }
    }
    
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 200:
        print('消息发送成功')
    else:
        print('消息发送失败')

headers = {
    'authority': 'ak.hypergryph.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': '_gid=GA1.2.1578983983.1711725936; _ga_BTSPKX9610=GS1.1.1711725935.2.1.1711726279.0.0.0; _ga_74340XWSQV=GS1.1.1711725936.2.1.1711726279.0.0.0; _ga=GA1.2.197109454.1699282635; _gat_gtag_UA_186227413_1=1',
    'if-modified-since': 'Fri, 29 Mar 2024 09:00:14 GMT',
    'if-none-match': 'W/"6606831e-48621"',
    'referer': 'https://ak.hypergryph.com/',
    'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

for url in new_list:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('div', class_='article-title').get_text(strip=True)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    strong_texts = [strong.get_text(strip=True) for strong in soup.find_all('strong')]

    article_content = [title]

    for paragraph in paragraphs:
        if paragraph in strong_texts:
            article_content.append(f"{paragraph}")
        else:
            article_content.append(paragraph)

    article_text = '\n'.join(article_content)
    send_message_to_feishu(article_text)
