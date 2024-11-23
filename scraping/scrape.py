import praw
import sqlite3
from datetime import datetime
import newspaper


# Load Reddit API credentials
reddit = praw.Reddit(
    client_id="PfXfiktXz50qjyFlOrBo_w",
    client_secret="T8BZf98JrIvR4IPiQEVbHzVZhRNS4g",
    user_agent="ElectricVehiclesReader/0.1 (by Usual_Diamond_666)",
)


# Database setup
def initialize_db(db_file, migration_file):
    """Initialize the SQLite database using the migration file."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(migration_file, "r") as f:
        migration = f.read()

    cursor.executescript(migration)
    conn.commit()
    return conn


# Specify database and migration files
DB_FILE = "reddit_data.db"
MIGRATION_FILE = "migration.sql"

# Initialize the database
conn = initialize_db(DB_FILE, MIGRATION_FILE)
cursor = conn.cursor()

# Specify the subreddit
subreddit = reddit.subreddit("electricvehicles")

# Fetch the submissions (e.g., hot, new, top)
for submission in subreddit.hot(limit=30):
    if submission.is_self:
        continue

    # Get the articles data
    try:
        article = newspaper.article(submission.url)

        article_text = article.text
        article_author = article.authors[0] if len(article.authors) > 1 else ""
        article_publish_date = article.publish_date

        # print the article data
        print(article_text)
    except (newspaper.ArticleException, newspaper.ArticleBinaryDataException):
        article_text = ""
        article_author = ""
        article_publish_date = datetime.utcfromtimestamp(
            submission.created_utc
        ).isoformat()

    # Insert the Reddit post into the database
    cursor.execute(
        """
        INSERT OR REPLACE INTO RedditPost (id, title, author, date, article_url, article_title, article_text, article_author, article_publish_date, score, num_comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            submission.id,  # id
            submission.title,  # title
            str(submission.author),  # author
            datetime.utcfromtimestamp(submission.created_utc).isoformat(),  # date
            submission.url,  # article_url
            submission.title,  # article_title
            article_text,  # article_text
            article_author,  # article_author
            article_publish_date,  # article_publish_date
            submission.score,  # score
            submission.num_comments,  # num_comments
        ),
    )

    # Insert comments
    top_level_comments = list(submission.comments)
    top_level_comments.sort(key=lambda x: x.score, reverse=True)

    for comment in top_level_comments:
        if comment.score < 2:
            break

        values = (
            comment.id,  # id
            submission.id,  # reddit_post_id
            str(comment.author),  # author
            datetime.utcfromtimestamp(submission.created_utc).isoformat(),  # date
            comment.score,  # score
            comment.body,  # content
        )
        print(values)

        cursor.execute(
            """
            INSERT OR REPLACE INTO RedditComment (
                id, reddit_post_id, author, date, score, content
            )
            VALUES (?, ?, ?, ?, ?, ?)
            
            """,
            values,
        )

# Commit the changes and close the connection
conn.commit()
conn.close()
