import os
import csv


def save_csv(posts, path="data/reddit_software_resume_posts.csv"):
    os.makedirs("data", exist_ok=True)

    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "id",
            "subreddit",
            "query",
            "title",
            "selftext",
            "score",
            "num_comments",
            "created_utc",
            "url"
        ])

        for post in posts:
            writer.writerow([
                post["id"],
                post["subreddit"],
                post["query"],
                post["title"],
                post["selftext"],
                post["score"],
                post["num_comments"],
                post["created_utc"],
                post["url"]
            ])