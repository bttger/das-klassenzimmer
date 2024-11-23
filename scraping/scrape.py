import praw

# Reddit API credentials
reddit = praw.Reddit(
    client_id="PfXfiktXz50qjyFlOrBo_w",
    client_secret="T8BZf98JrIvR4IPiQEVbHzVZhRNS4g",
    user_agent="ElectricVehiclesReader/0.1 (by Usual_Diamond_666)",
)

# Specify the subreddit
subreddit = reddit.subreddit("electricvehicles")

# Fetch the submissions (e.g., hot, new, top)
for submission in subreddit.hot(limit=5):
    if submission.is_self:
        continue

    print(f"\n\nSubmission Title: {submission.title}")
    print(f"ID: {submission.name}")
    print(f"URL: {submission.url}")
    print(f"Score: {submission.score}")
    print(f"Number of Comments: {submission.num_comments}")
    print(f"Author: {submission.author}")
    print(f"Is self: {submission.is_self}")
    print(f"Selftext: {submission.selftext}")

    # Load comments
    print("\n--- Comments ---")
    top_level_comments = list(submission.comments)
    top_level_comments.sort(key=lambda x: x.score, reverse=True)
    for comment in top_level_comments:
        if comment.score < 3:
            break
        print(f"\nID: {comment.id}")
        print(f"Parent ID: {comment.parent_id}")
        print(f"Comment: {comment.body}")
        print(f"Author: {comment.author}")
        print(f"Score: {comment.score}")
        print(f"Replies: {comment.replies}")
