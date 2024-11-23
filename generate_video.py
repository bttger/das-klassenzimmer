from dataclasses import dataclass
import sqlite3
from openai_wrapper import get_video_script


def connect_to_db(db_name):
    """Connect to the SQLite database."""
    conn = sqlite3.connect(db_name)
    return conn


def query_reddit_post(conn):
    """Query a Reddit post by its ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RedditPost WHERE is_video_created = 0 LIMIT 1")
    post = cursor.fetchone()
    return post


def query_reddit_comments(conn, reddit_post_id):
    """Query Reddit comments by the Reddit post ID."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM RedditComment WHERE reddit_post_id = ? ORDER BY score ASC LIMIT 10",
        (reddit_post_id,),
    )
    comments = cursor.fetchall()
    return comments


@dataclass
class RedditPost:
    """
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
    """

    id: str
    title: str
    author: str
    date: str
    article_url: str
    article_title: str
    article_author: str
    article_publish_date: str
    article_text: str
    score: int
    num_comments: int
    is_video_created: int


@dataclass
class RedditComment:
    """
        CREATE TABLE IF NOT EXISTS RedditComment (
        id TEXT PRIMARY KEY,
        reddit_post_id TEXT,
        author TEXT,
        date TEXT,
        score INTEGER,
        content TEXT,
        FOREIGN KEY (reddit_post_id) REFERENCES RedditPost(id)
    );
    """

    id: str
    reddit_post_id: str
    author: str
    date: str
    score: int
    content: str


def main():
    db_name = "scraping/reddit_data.db"

    conn = connect_to_db(db_name)
    post = query_reddit_post(conn)
    if post:
        reddit_post = RedditPost(*post)
    else:
        exit("No Reddit post found.")

    # Get all related comments for the Reddit post
    comments = query_reddit_comments(conn, reddit_post.id)
    reddit_comments = [RedditComment(*comment) for comment in comments]

    # Create a prompt from the article text and all the comments
    prompt = f"{reddit_post.article_text}\n\n"
    prompt += "\n".join(
        [
            f"Comment {num+1}: {comment.content.replace('\n', ' ')}"
            for num, comment in enumerate(reddit_comments)
        ]
    )

    # Generate a video script from the prompt
    video_script = get_video_script(prompt)
    print("Video Script:", video_script)

    conn.close()


if __name__ == "__main__":
    main()
