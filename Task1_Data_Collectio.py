import requests
import time
import json
import os
from datetime import datetime

# ---------------- CONFIG ---------------- #
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

MAX_PER_CATEGORY = 25
TOTAL_IDS_TO_FETCH = 500

# Category keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"]
}

# ---------------- HELPERS ---------------- #

def fetch_top_story_ids():
    try:
        url = f"{BASE_URL}/topstories.json"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:TOTAL_IDS_TO_FETCH]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story(story_id):
    try:
        url = f"{BASE_URL}/item/{story_id}.json"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception :
        print(f"Failed to fetch story {story_id}")
        return None


def classify_story(title):
    """Return category based on keyword match"""
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


# ---------------- MAIN LOGIC ---------------- #

def solve():
    story_ids = fetch_top_story_ids()

    # Storage
    categorized_data = {cat: [] for cat in CATEGORIES}
    collected_data = []

    for category in CATEGORIES:
        print(f"\nProcessing category: {category}")

        for story_id in story_ids:
            # Stop if category full
            print(f"Fetching story {story_id}")
            if len(categorized_data[category]) >= MAX_PER_CATEGORY:
                break

            story = fetch_story(story_id)
            if not story:
                continue

            title = story.get("title", "")
            assigned_category = classify_story(title)

            if assigned_category != category:
                continue
            
           

            # Extract fields safely
            data = {
                "post_id": story.get("id"),
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            categorized_data[category].append(data)
            collected_data.append(data)

        
        print(f"Completed category '{category}' with {len(categorized_data[category])} stories.")
        print("Sleeping for 2 seconds")

        # Mandatory sleep AFTER each category
        time.sleep(2)

    # ---------------- SAVE FILE ---------------- #

    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    solve()