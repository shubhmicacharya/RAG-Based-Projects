import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_news(topic, num_articles=5):
    api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsapi.org/v2/everything?q={topic}&language=en&sortBy=publishedAt&pageSize={num_articles}&apiKey={api_key}"
    res = requests.get(url)

    if res.status_code != 200:
        print("News API error:", res.json())
        return []

    articles = res.json().get("articles", [])

    
    filtered = [
        a for a in articles if topic.lower() in (
            (a.get("title") or "").lower() +
            (a.get("description") or "").lower() +
            (a.get("content") or "").lower()
        )
    ]

    if not filtered:
        print(f"No relevant articles found for topic: {topic}")
        return []

    return filtered
