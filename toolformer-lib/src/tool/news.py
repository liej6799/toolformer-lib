from newsapi import NewsApiClient
from model.news_model import NewsModel

class News:
    newsapi = NewsApiClient
    # https://newsapi.org/docs/endpoints/top-headlines
    category = ['business', 'entertainment', 'entertainment', 'health', 'science', 'sports', 'technology']
    
    def __init__(self, api_key):
        self.newsapi = NewsApiClient(api_key=api_key)

    def query(self, query):
        query = query.lower()
        selected_category = ''
        for category in self.category:
            if query in category:
                selected_category = category
                break
        
        result = []
        if selected_category:
            top_headlines = self.newsapi.get_top_headlines(q=query,
                                                category=selected_category,
                                                language='en',
                                                country='us')
            for article in top_headlines['articles']:
                # filter out empty url, title, source
                if article['title'] and article['source'] and article['url']:
                    result.append(NewsModel(article['title'], article['source'], article['url']))
                    # just get top 5
                    if len(result) == 5:
                        break
                
        # specific query
        else:
            top_headlines = self.newsapi.get_everything(q=query,
                                                language='en')
            for article in top_headlines['articles']:
                # filter out empty url, title, source
                if article['title'] and article['source'] and article['url']:
                    result.append(NewsModel(article['title'], article['source'], article['url']))
                    # just get top 5
                    if len(result) == 5:
                        break

        return result