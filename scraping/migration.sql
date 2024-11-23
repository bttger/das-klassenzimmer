-- Enable foreign key support (important for SQLite)
PRAGMA foreign_keys = ON;

-- Create table for Reddit posts
CREATE TABLE IF NOT EXISTS RedditPost (
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    date TEXT,
    article_url TEXT,
    article_title TEXT,
    article_author TEXT,
    article_publish_date TEXT,
    article_text TEXT,
    score INTEGER,
    num_comments INTEGER,
    is_video_created INTEGER DEFAULT 0  -- 0 for False, 1 for True
);

-- Create table for scripts associated with Reddit posts
CREATE TABLE IF NOT EXISTS GeneratedVideoScript (
    id INTEGER PRIMARY KEY,
    reddit_post_id INTEGER UNIQUE,
    title TEXT,
    script TEXT,
    FOREIGN KEY (reddit_post_id) REFERENCES RedditPost(id)
);

-- Create table for comments with hierarchical replies
CREATE TABLE IF NOT EXISTS RedditComment (
    id TEXT PRIMARY KEY,
    reddit_post_id TEXT,
    author TEXT,
    date TEXT,
    score INTEGER,
    content TEXT,
    FOREIGN KEY (reddit_post_id) REFERENCES RedditPost(id)
);
