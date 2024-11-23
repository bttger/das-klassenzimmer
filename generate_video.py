from dataclasses import dataclass
import sqlite3
from openai_wrapper import (
    get_video_script,
    get_caption,
    get_title,
    get_google_image_search_prompts,
)
import re
import os
from image_scraper import search_prompts_and_save_imgs


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
    generated_content_folder = "generated_content"

    conn = connect_to_db(db_name)
    post = query_reddit_post(conn)
    if post:
        reddit_post = RedditPost(*post)
    else:
        exit("No Reddit post found.")

    # Get all related comments for the Reddit post
    comments = query_reddit_comments(conn, reddit_post.id)
    reddit_comments = [RedditComment(*comment) for comment in comments]
    conn.close()

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

    # Clean the video script by replacing instructions like **[Move the camera...]** and [Move the camera...], and Descriptions like **Body**.
    # We use a regex pattern to match the instructions and descriptions.
    pattern = r"\*\*\[.*?\]\*\*:?|\*\*.*?\*\*:?|\[.*?\]:?|\[.*?\]\:?"
    cleaned_video_script = re.sub(pattern, "", video_script)

    print("Video Script cleaned:", cleaned_video_script)

    # Generate captions for the video script
    caption = get_caption(video_script)
    print("Caption:", caption)

    # Generate a title for the video script
    title = get_title(video_script)
    print("Title:", title)

    # save the video script, caption, and title to the generated_content folder in the subfolder with the title as the name
    if not os.path.exists("generated_content"):
        os.makedirs("generated_content")
    save_path = os.path.join(generated_content_folder, title)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    image_save_path = os.path.join(save_path, "images")
    if not os.path.exists(image_save_path):
        os.makedirs(image_save_path)

    with open(os.path.join(save_path, "cleaned_video_script.txt"), "w") as f:
        f.write(cleaned_video_script)
    with open(os.path.join(save_path, "caption.txt"), "w") as f:
        f.write(caption)
    with open(os.path.join(save_path, "video_script.txt"), "w") as f:
        f.write(video_script)

    # generate a google image search prompt for each session of the video script
    google_image_search_prompts = get_google_image_search_prompts(
        cleaned_video_script
    ).split("\n")
    print("Google Image Search Prompts:", google_image_search_prompts)

    # Remove all punctuation, special characters, and quotation marks from the prompts
    google_image_search_prompts = [
        re.sub(r"[^a-zA-Z\s]", "", prompt) for prompt in google_image_search_prompts
    ]
    print("Cleaned Google Image Search Prompts:", google_image_search_prompts)

    search_prompts_and_save_imgs(google_image_search_prompts, image_save_path)


if __name__ == "__main__":
    main()
