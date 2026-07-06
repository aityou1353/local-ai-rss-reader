from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.models import db
from rss import rss_reader

router = APIRouter(
    prefix="/api/rss",
    tags=["RSS"]
)


class RSSFeedCreate(BaseModel):
    name: str
    url: str
    category_id: int | None = None


@router.get("/list")
async def list_feeds():

    feeds = db.fetchall("""
        SELECT *
        FROM rss_feeds
        ORDER BY name
    """)

    return feeds


@router.post("/add")
async def add_feed(feed: RSSFeedCreate):

    feed_id = db.insert(
        "rss_feeds",
        {
            "name": feed.name,
            "url
          from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from database.models import db
from rss import rss_reader

router = APIRouter(
    prefix="/api/rss",
    tags=["RSS"]
)


class RSSFeedCreate(BaseModel):
    name: str
    url: HttpUrl
    category_id: int | None = None


class RSSFeedUpdate(BaseModel):
    name: str | None = None
    url: HttpUrl | None = None
    category_id: int | None = None
    enabled: bool | None = None


@router.get("/list")
async def list_feeds():
    return db.fetchall("""
        SELECT *
        FROM rss_feeds
        ORDER BY name
    """)


@router.post("/add")
async def add_feed(feed: RSSFeedCreate):

    exists = db.fetchone(
        "SELECT id FROM rss_feeds WHERE url=?",
        (str(feed.url),)
    )

    if exists:
        raise HTTPException(
            status_code=409,
            detail="RSS feed already exists."
        )

    feed_id = db.insert(
        "rss_feeds",
        {
            "name": feed.name,
            "url": str(feed.url),
            "category_id": feed.category_id
        }
    )

    return {
        "success": True,
        "feed_id": feed_id
    }


@router.put("/{feed_id}")
async def update_feed(
    feed_id: int,
    feed: RSSFeedUpdate
):

    current = db.fetchone(
        "SELECT * FROM rss_feeds WHERE id=?",
        (feed_id,)
    )

    if current is None:
        raise HTTPException(
            status_code=404,
            detail="Feed not found."
        )

    values = {}

    if feed.name is not None:
        values["name"] = feed.name

    if feed.url is not None:
        values["url"] = str(feed.url)

    if feed.category_id is not None:
        values["category_id"] = feed.category_id

    if feed.enabled is not None:
        values["enabled"] = int(feed.enabled)

    if values:
        db.update(
            "rss_feeds",
            values,
            "id=?",
            (feed_id,)
        )

    return {"success": True}


@router.delete("/{feed_id}")
async def delete_feed(feed_id: int):

    row = db.fetchone(
        "SELECT id FROM rss_feeds WHERE id=?",
        (feed_id,)
    )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Feed not found."
        )

    db.delete(
        "rss_feeds",
        "id=?",
        (feed_id,)
    )

    return {"success": True}


@router.post("/update")
async def update_all():

    total = rss_reader.update_all()

    return {
        "success": True,
        "new_articles": total
    }


@router.post("/update/{feed_id}")
async def update_one(feed_id: int):

    feed = db.fetchone(
        "SELECT * FROM rss_feeds WHERE id=?",
        (feed_id,)
    )

    if feed is None:
        raise HTTPException(
            status_code=404,
            detail="Feed not found."
        )

    count = rss_reader.fetch_feed(feed)

    return {
        "success": True,
        "new_articles": count
    }
