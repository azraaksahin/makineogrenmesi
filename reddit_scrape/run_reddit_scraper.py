from reddit_fetcher import fetch_search_results
from filters import SUBREDDITS, SEARCH_QUERIES, is_relevant_post
from saver import save_csv
import time


MAX_PER_QUERY = 50


def remove_duplicates(posts):
    unique = {}

    for post in posts:
        if post["id"] not in unique:
            unique[post["id"]] = post

    return list(unique.values())


def main():
    all_posts = []

    for subreddit in SUBREDDITS:
        for query in SEARCH_QUERIES:
            print(f"r/{subreddit} içinde aranıyor: {query}")

            posts = fetch_search_results(
                subreddit=subreddit,
                query=query,
                max_posts=MAX_PER_QUERY
            )

            filtered_posts = []

            for post in posts:
                if is_relevant_post(post["title"], post["selftext"]):
                    filtered_posts.append(post)

            print(f"Bulunan: {len(posts)} | Filtre sonrası: {len(filtered_posts)}")

            all_posts.extend(filtered_posts)

            time.sleep(2)

    all_posts = remove_duplicates(all_posts)

    save_csv(all_posts)

    print("\nReddit scraping tamamlandı.")
    print(f"Toplam temiz post: {len(all_posts)}")
    print("Dosya: data/reddit_software_resume_posts.csv")


if __name__ == "__main__":
    main()