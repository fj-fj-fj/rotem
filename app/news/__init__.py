import os
from typing import Optional

from newsapi import NewsApiClient

NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')


def init_news(api_key: Optional[str] = NEWSAPI_KEY) -> NewsApiClient:
    return NewsApiClient(api_key=api_key)


def fetch_top_headlines(
    newsapi=init_news(),
    q='medicine',
    sources='all',
    category='medical',
    language='en',
    country='us',
) -> NewsApiClient:
    """/v2/top-headlines"""
    top_headlines = newsapi.get_top_headlines(
        q=q,
        sources=sources,
        category=category,
        language=language,
        country=country,
    )
    return top_headlines


def fetch_all_articles(
    newsapi=init_news(),
    q='covid',
    sources=None,
    domains=None,
    from_param=None,
    to=None,
    language='en',
    sort_by='relevancy',
    page=5,
) -> NewsApiClient:
    """/v2/everything"""
    all_articles = newsapi.get_everything(
        q=q,
        sources=sources,
        domains=domains,
        from_param=from_param,
        to=to,
        language=language,
        sort_by=sort_by,
        page=page,
    )
    return all_articles


def fetch_sources(newsapi=init_news()) -> NewsApiClient:
    """/v2/top-headlines/sources"""
    return newsapi.get_sources()
