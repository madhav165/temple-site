from bs4 import BeautifulSoup
import requests
import sqlite3
import modin.pandas as pd
import ray
import time

ray.init(runtime_env={'env_vars': {'__MODIN_AUTOIMPORT_PANDAS__': '1'}})

conn = sqlite3.connect('database.db')

# Read the table into a Pandas DataFrame
df = pd.read_sql_query('SELECT * FROM states', conn)

# Close the connection
conn.close()


url_list = df['url'].tolist()
url = url_list[0]
arr = []

for url in ['https://www.bharattemples.com/ladakh/']:
    print(url)
    resp = requests.get(url)
    print(resp.status_code)
    soup = BeautifulSoup(resp.content, 'html.parser')
    body = soup.body
    desc = body.find('div', {'class': 'taxonomy-description'})
    arr.append([url, desc.text])
    # time.sleep(20)
pd.DataFrame(arr).to_csv('desc.csv', index=False)

arr2 = []
for url in url_list:
    print(url)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    body = soup.body
    articles = body.findAll('article', {'class': 'entry'})
    for article in articles:
        if 'category-lyrics' not in article['class']:
            temple_h2 = article.find('h2', {'class': 'entry-title'})
            temple_title = temple_h2.text
            temple_url = temple_h2.find('a', {'rel': 'bookmark'})['href']
            temple_desc = article.find('div', {'class': 'entry-content'}).text
            print(temple_title)
            print(temple_url)
            print(temple_desc+'\n')
            arr2.append([url, temple_title, temple_url, temple_desc])
    try:
        next_page_url = body.find('a', {'class': 'next'})['href']
        time.sleep(5)
    except:
            next_page_url = None
    while next_page_url is not None:
        print(next_page_url)
        resp = requests.get(next_page_url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        body = soup.body
        articles = body.findAll('article', {'class': 'entry'})
        for article in articles:
            if 'category-lyrics' not in article['class']:
                temple_h2 = article.find('h2', {'class': 'entry-title'})
                temple_title = temple_h2.text
                temple_url = temple_h2.find('a', {'rel': 'bookmark'})['href']
                temple_desc = article.find('div', {'class': 'entry-content'}).text
                print(temple_title)
                print(temple_url)
                print(temple_desc+'\n')
                arr2.append([url, temple_title, temple_url, temple_desc])
        try:
            next_page_url = body.find('a', {'class': 'next'})['href']
            time.sleep(5)
        except:
            next_page_url = None

pd.DataFrame(arr2).to_csv('temples.csv', index=False)

ray.shutdown()
