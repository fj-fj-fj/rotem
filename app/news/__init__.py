"""News API package.

see https://newsapi.org/docs/client-libraries/python

"""
import os

from newsapi import NewsApiClient


NEWSAPI_KEY: str | None = os.getenv("NEWSAPI_KEY")


def init_news(api_key: str | None = NEWSAPI_KEY) -> NewsApiClient:
    """Return hhe core client object used to fetch data from News API endpoints."""
    return NewsApiClient(api_key=api_key)


def fetch_top_headlines(
    newsapi: NewsApiClient = init_news(),
    q="medicine",
    sources="all",
    category="medical",
    language="en",
    country="us",
) -> dict:  # requests.get(...).json()
    # /v2/top-headlines
    """Call the `/top-headlines` endpoint.

    Fetch live top and breaking headlines.

    This endpoint provides live top and breaking headlines for a country,
    specific category in a country, single source, or multiple sources.
    You can also search with keywords.  Articles are sorted by the earliest
    date published first.

    """
    top_headlines = newsapi.get_top_headlines(
        q=q,
        sources=sources,
        category=category,
        language=language,
        country=country,
    )
    return top_headlines


def fetch_all_articles(
    newsapi: NewsApiClient = init_news(),
    q="covid",
    sources=None,
    domains=None,
    from_param=None,
    to=None,
    language="en",
    sort_by="relevancy",
    page=5,
) -> dict:  # requests.get(...).json()
    # /v2/everything
    """Call the `/everything` endpoint.

    Search through millions of articles from over 30,000 large and small news
    sources and blogs.

    """
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


def fetch_sources(newsapi: NewsApiClient = init_news()) -> dict:
    # /v2/top-headlines/sources
    """Call the `/sources` endpoint.

    Fetch the subset of news publishers that /top-headlines are available from.

    """
    return newsapi.get_sources()  # requests.get(...).json()
