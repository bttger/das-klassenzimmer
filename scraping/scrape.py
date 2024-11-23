import praw
import sqlite3

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
for submission in subreddit.hot(limit=5):
    if submission.is_self:
        continue

    # Insert the Reddit post into the database
    cursor.execute(
        """
        INSERT OR REPLACE INTO RedditPost (id, title, author, date, score, num_comments, text, is_video_created)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            submission.name,  # id
            submission.title,  # title
            submission.author,  # author
            submission.created_utc,  # date
            submission.score,  # score
            submission.num_comments,  # num_comments
            submission.selftext,  # text
            0,  # is_video_created
        ),
    )
    reddit_post_id = cursor.lastrowid

    # Insert comments
    top_level_comments = list(submission.comments)
    top_level_comments.sort(key=lambda x: x.score, reverse=True)

    for comment in top_level_comments:
        if comment.score < 3:
            break

        cursor.execute(
            """
            INSERT OR REPLACE INTO RedditComment (
                id, reddit_post_id, author, date, score, content
            )
            VALUES (?, ?, ?, ?, ?, ?)
            
            """,
            (
                comment.id,  # id
                reddit_post_id,  # reddit_post_id
                comment.author,  # author
                comment.created_utc,  # date
                comment.score,  # score
                comment.body,  # content
            ),
        )

# Commit the changes and close the connection
conn.commit()
conn.close()
