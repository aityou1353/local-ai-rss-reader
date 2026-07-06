from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import config
from database.init_db import create_database

# ---------------------------------------
# 初期化
# ---------------------------------------

BASE_DIR = Path(__file__).parent

# 必要なディレクトリ作成
(BASE_DIR / "logs").mkdir(exist_ok=True)
(BASE_DIR / "static").mkdir(exist_ok=True)
(BASE_DIR / "templates").mkdir(exist_ok=True)

# DB作成（初回のみ）
create_database()

# ---------------------------------------
# ログ
# ---------------------------------------

logging.basicConfig(
    level=getattr(logging, config.logging["level"]),
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(
            BASE_DIR / "logs" / "app.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("local-ai-rss")

# ---------------------------------------
# FastAPI
# ---------------------------------------

app = FastAPI(
    title="Local AI RSS Reader",
    version="1.0.0"
)

# ---------------------------------------
# Static
# ---------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

# ---------------------------------------
# Events
# ---------------------------------------

@app.on_event("startup")
async def startup():

    logger.info("Application started")

@app.on_event("shutdown")
async def shutdown():

    logger.info("Application stopped")

# ---------------------------------------
# Routes
# ---------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Local AI RSS Reader"
        }
    )

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "version": "1.0.0"
    }
