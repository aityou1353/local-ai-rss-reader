from pathlib import Path
import sqlite3

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "rss.db"


def create_database():
    DB_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()

    # ==========================
    # RSS
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rss_feeds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        category_id INTEGER,
        enabled INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==========================
    # Categories
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    """)

    # ==========================
    # Articles
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,
        ai_title TEXT,

        content TEXT,
        summary TEXT,
        merged_content TEXT,

        url TEXT UNIQUE,

        source TEXT,

        published DATETIME,
        fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,

        category_id INTEGER,

        importance INTEGER DEFAULT 0,

        language TEXT,

        duplicate_group INTEGER,

        is_master INTEGER DEFAULT 0,

        favorite INTEGER DEFAULT 0,

        is_read INTEGER DEFAULT 0,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==========================
    # Tags
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS article_tags (
        article_id INTEGER,
        tag_id INTEGER,

        PRIMARY KEY(article_id, tag_id),

        FOREIGN KEY(article_id)
            REFERENCES articles(id)
            ON DELETE CASCADE,

        FOREIGN KEY(tag_id)
            REFERENCES tags(id)
            ON DELETE CASCADE
    );
    """)

    # ==========================
    # Settings
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)

    # ==========================
    # Duplicate Cache
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS duplicate_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article1 INTEGER,
        article2 INTEGER,
        result INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==========================
    # Merge Jobs
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merge_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        duplicate_group INTEGER,

        status TEXT,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

        started_at DATETIME,

        finished_at DATETIME,

        error_message TEXT
    );
    """)

    # ==========================
    # AI Logs
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        article_id INTEGER,

        task TEXT,

        model TEXT,

        duration REAL,

        success INTEGER,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==========================
    # RSS Logs
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rss_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        feed_id INTEGER,

        status TEXT,

        message TEXT,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==========================
    # Error Logs
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        module TEXT,

        message TEXT,

        traceback TEXT,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==========================
    # Full Text Search
    # ==========================

    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS article_fts
    USING fts5(
        title,
        content,
        summary,
        source
    );
    """)

    # ==========================
    # Indexes
    # ==========================

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_articles_published
    ON articles(published);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_articles_source
    ON articles(source);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_articles_group
    ON articles(duplicate_group);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_articles_importance
    ON articles(importance);
    """)

    conn.commit()
    conn.close()

    print(f"Database created: {DB_PATH}")


if __name__ == "__main__":
    create_database()
