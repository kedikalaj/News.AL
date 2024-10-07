from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Function to fetch news articles from the database
def get_all_news():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    
    # Fetch all articles
    cursor.execute('SELECT id, title, link, content, image_url, date FROM news_articles')
    articles = cursor.fetchall()
    
    # Convert the articles into a list of dictionaries
    news_list = []
    for article in articles:
        news_dict = {
            'id': article[0],
            'title': article[1],
            'link': article[2],
            'content': article[3],
            'image_url': article[4],
            'date': article[5]
        }
        news_list.append(news_dict)
    
    conn.close()
    return news_list

# Endpoint to get all news articles
@app.route('/news', methods=['GET'])
def news():
    try:
        articles = get_all_news()
        return jsonify({
            'status': 'success',
            'data': articles
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
