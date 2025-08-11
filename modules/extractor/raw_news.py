from newsapi import NewsApiClient
import json

# Init
newsapi = NewsApiClient(api_key='c3188351f9a947ac8ba407c39a5edfe2')
query = '"mortgage rates " OR "real estate market" OR "property taxs" OR "housing market trends"' 


# /v2/everything
all_articles = newsapi.get_everything(q=query,
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)


with open("../../data/news_example/house_all_articles.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, indent=2, ensure_ascii=False)

print("✅ News saved to san_mateo_news.json")
