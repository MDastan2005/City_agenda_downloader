import requests
from bs4 import BeautifulSoup
import time
import re
import os


def download_pdf(url, filename, dir):
    response = requests.get(url, stream=True)
    
    os.makedirs(f'data/{dir}', exist_ok=True)
    with open(f'data/{dir}/{filename}', 'wb') as pdf_file:
        for chunk in response.iter_content(chunk_size=1024):
            pdf_file.write(chunk)


def get_data(url):
    os.makedirs('data', exist_ok=True)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find_all('table', class_='resultsTable')[1]
    rows = table.find_all('tr')[3:]
    for row in rows:
        items = row.find_all(class_='listItem')
        date = items[0].text
        name = items[1].text.replace(' ', '_')
        year = date.split()[-1]
        try:
            agenda = items[3].find('a').get('href')
        except:
            continue
        print(f'year: {year}, agenda: {agenda}')
        download_pdf('https:' + agenda, name + '.pdf', 'year_' + year)


def main():
    urls = [
        'https://napa.granicus.com/ViewPublisher.php?view_id=21',
    ]
    for url in urls:
        get_data(url)


if __name__ == '__main__':
    main()
