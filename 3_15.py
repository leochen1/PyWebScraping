import re
from bs4 import BeautifulSoup
import requests

root = 'https://subslikescript.com'
website = f'{root}/movies'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')
print(soup.prettify())

box = soup.find('article', class_='main-article')

links = []
for link in box.find_all('a', href=True):
    links.append(link['href'])

print(links)

for link in links:
    website = f'{root}{link}'
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('article', class_='main-article')

    title = box.find('h1').get_text()
    transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

    # 移除 Windows 不允許的檔名字元
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
    with open(f'{safe_title}.txt', 'w', encoding='utf-8') as f:
        f.write(transcript)


