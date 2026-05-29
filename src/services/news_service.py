"""
Pulls headlines from RSS feeds using feedparser (free, no API key).
Returns categorised headline strings suitable for the news ticker.
"""

import feedparser
from datetime import datetime


def _fetch_feed(url: str, max_items: int) -> list[str]:
    try:
        feed = feedparser.parse(url)
        headlines = []
        for entry in feed.entries[:max_items]:
            title = entry.get("title", "").strip()
            if title:
                headlines.append(title)
        return headlines
    except Exception as exc:
        print(f"[news] feed error ({url}): {exc}")
        return []


def fetch_headlines(
    feeds: dict[str, str],
    headlines_per_feed: int = 5,
) -> list[str]:
    """
    feeds: {"local": <rss_url>, "us": <rss_url>, "world": <rss_url>}
    Returns a flat list of ticker strings like:
      "LOCAL: Headline text here"
      "US: Headline text here"
      "WORLD: Headline text here"
    """
    labels = {
        "local": "LOCAL",
        "us":    "US",
        "world": "WORLD",
    }

    all_headlines: list[str] = []
    for key, url in feeds.items():
        label = labels.get(key, key.upper())
        items = _fetch_feed(url, headlines_per_feed)
        for item in items:
            all_headlines.append(f"{label}: {item}")

    return all_headlines
