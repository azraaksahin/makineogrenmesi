import requests
import time


def fetch_search_results(subreddit, query, max_posts=80):
    posts = []
    after = None
    count = 0

    headers = {
        "User-Agent": "makineogrenmesi-dataset-project/1.0"
    }

    while len(posts) < max_posts:
        url = f"https://www.reddit.com/r/{subreddit}/search.json"

        params = {
            "q": query,
            "restrict_sr": "true",
            "sort": "relevance",
            "t": "all",
            "limit": 100,
            "count": count
        }

        if after:
            params["after"] = after

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=20
            )

            if response.status_code != 200:
                print(f"r/{subreddit} | {query} hata kodu: {response.status_code}")
                break

            data = response.json()
            children = data.get("data", {}).get("children", [])

            if not children:
                break

            for child in children:
                post = child.get("data", {})

                posts.append({
                    "id": post.get("id", ""),
                    "subreddit": subreddit,
                    "query": query,
                    "title": post.get("title", ""),
                    "selftext": post.get("selftext", ""),
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "created_utc": post.get("created_utc", ""),
                    "url": "https://www.reddit.com" + post.get("permalink", "")
                })

                if len(posts) >= max_posts:
                    break

            after = data.get("data", {}).get("after")
            count += len(children)

            if not after:
                break

            time.sleep(2)

        except Exception as e:
            print(f"r/{subreddit} | {query} hata:", e)
            break

    return posts