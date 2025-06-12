import random
import requests

REDDIT_URL = "https://www.reddit.com/r/videos/top.json"
HEADERS = {"User-Agent": "RandomViralClip/0.1"}
PARAMS = {"t": "month", "limit": 100}

def fetch_random_clip():
    response = requests.get(REDDIT_URL, headers=HEADERS, params=PARAMS, timeout=10)
    response.raise_for_status()
    data = response.json()
    videos = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        url = post.get("url")
        if post.get("is_video") or "v.redd.it" in url or url.endswith((".mp4", ".gif", ".gifv")):
            videos.append({
                "title": post.get("title"),
                "url": url,
                "permalink": "https://reddit.com" + post.get("permalink", "")
            })
    if not videos:
        raise RuntimeError("No video posts found in the last month")
    return random.choice(videos)

if __name__ == "__main__":
    clip = fetch_random_clip()
    print("Title:", clip["title"])
    print("Video URL:", clip["url"])
    print("Reddit Link:", clip["permalink"])
