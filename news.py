import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/news/mental-health', methods=['GET'])
def get_mental_health_news():
    api_key = 'f7682ca0b76b4bb6a89cffdfc059f102'
    url = f'https://newsapi.org/v2/everything?q=mental%20health&apiKey={api_key}'

    response = requests.get(url)
    news_data = response.json()

    articles = news_data.get('articles', [])

    # Mengambil atribut yang relevan dari setiap artikel
    results = []
    for article in articles:
        title = article.get('title')
        description = article.get('description')
        url = article.get('url')

        result = {
            'title': title,
            'description': description,
            'url': url
        }
        results.append(result)

    return jsonify(results)

if __name__ == '__main__':
    app.run()
