-- Enable foreign key support (important for SQLite)
PRAGMA foreign_keys = ON;

-- Create table for news articles
CREATE TABLE IF NOT EXISTS NewsArticle (
    id INTEGER PRIMARY KEY,
    date DATETIME,
    title TEXT,
    author TEXT,
    content TEXT,
    sources TEXT,
    reddit_post_id INTEGER UNIQUE, 
    FOREIGN KEY (reddit_post_id) REFERENCES RedditPost(id)
);

-- Create table for Reddit posts
CREATE TABLE IF NOT EXISTS RedditPost (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    date DATETIME,
    score INTEGER,
    num_comments INTEGER,
    text TEXT,
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
    id INTEGER PRIMARY KEY,
    reddit_post_id INTEGER,
    parent_comment_id INTEGER,
    author TEXT,
    date DATETIME,
    score INTEGER,
    content TEXT,
    FOREIGN KEY (reddit_post_id) REFERENCES RedditPost(id),
    FOREIGN KEY (parent_comment_id) REFERENCES RedditComment(id)
);
