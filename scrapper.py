import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# Database setup using sqlite3
conn = sqlite3.connect('news.db')
cursor = conn.cursor()

# Create the news table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS news_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        content TEXT NOT NULL,
        image_url TEXT,
        date TEXT NOT NULL
    )
''')
conn.commit()

# Function to insert news articles into the database
def save_article_to_db(title, link, content, image_url):
    cursor.execute('''
        INSERT INTO news_articles (title, link, content, image_url, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, link, content, image_url, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()

# Scraping function
def scrape_news(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main content div
    main_content_div = soup.find('div', class_='td-ss-main-content')
    if main_content_div is None:
        print("Main content div not found. Please check the HTML structure.")
        return
    
    # Find all articles based on the provided HTML structure
    articles = main_content_div.find_all('div', class_='td_module_10 td_module_wrap td-animation-stack')
    
    if not articles:
        print("No articles found.")
        return

    for article in articles:
        title = article.find('h1', class_='entry-title td-module-title').get_text()
        link = article.find('a', itemprop='url')['href']
        image_url = article.find('img', itemprop='image')['src']
        content = article.find('div', class_='td-excerpt').get_text(strip=True)

        # Save to the database
        save_article_to_db(title, link, content, image_url)

    print(f"Scraped {len(articles)} articles from {url}")

# URL to scrape from
url = 'https://www.panorama.com.al/category/lajmi-i-fundit/'

# Run the scraper
scrape_news(url)

# Close the database connection
conn.close()
