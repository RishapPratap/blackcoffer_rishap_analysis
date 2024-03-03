import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

def extract_article_text(url):
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        article_title = soup.title.text.strip()
        article_body = soup.find('article').text.strip() 
        
        return article_title, article_body
    except Exception as e:
        print(f"Failed to extract article from {url}: {e}")
        return None, None

input_data = pd.read_excel("Input.xlsx")
article_texts_dir = 'article_rishap_texts'
os.makedirs(article_texts_dir, exist_ok=True)

for index, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    article_title, article_text = extract_article_text(url)
    
    if article_text:
        filename = os.path.join(article_texts_dir, f"{url_id}.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(article_title + '\n\n')
            file.write(article_text)
        print(f"Article successfully extracted and saved with URL_ID: {url_id}")
