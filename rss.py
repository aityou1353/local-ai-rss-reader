from __future__ import annotations

import logging
from datetime import datetime
from email.utils import parsedate_to_datetime

import feedparser

from database.models import db

logger = logging.getLogger("local-ai-rss")


class RSSReader:

    def __init__(self):

        self.user_agent = "LocalAI-RSS/1.0"

    def get_enabled_feeds(self):

        return db.fetchall("""
            SELECT *
            FROM rss_feeds
            WHERE enabled=1
            ORDER BY id
        """)

    def article_exists(self, url: str) -> bool:

        row = db.fetchone(
            "SELECT id FROM articles WHERE url=?",
            (url,)
        )

        return row is not None

    def save_article(self, article: dict):

        db.insert(
            "articles",
            article
        )

    def normalize_date(self, entry):

        if hasattr(entry, "published_parsed") and entry.published_parsed:

            return parsedate_to_datetime(
                entry.published
            ).isoformat()

        return datetime.utcnow().isoformat()

    def fetch_feed(self, feed: dict):

        logger.info("RSS: %s", feed["name"])

        rss = feedparser.parse(feed["url"])

        count = 0

        for entry in rss.entries:

            url = entry.get("link", "")

            if not url:

                continue

            if self.article_exists(url):

                continue

            title = entry.get("title", "")

            content = ""

            if "summary" in entry:

                content = entry.summary

            article = {

                "title": title,

                "content": content,

                "url": url,

                "source": feed["name"],

                "published": self.normalize_date(entry),

                "category_id": feed["category_id"]

            }

            self.save_article(article)

            count += 1

        logger.info(
            "%s : %d new articles",
            feed["name"],
            count
        )

        return count

    def update_all(self):

        total = 0

        feeds = self.get_enabled_feeds()

        for feed in feeds:

            try:

                total += self.fetch_feed(feed)

            except Exception:

                logger.exception(
                    "RSS update failed: %s",
                    feed["name"]
                )

        return total


rss_reader = RSSReader()
