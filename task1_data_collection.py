import requests
import json
import os
import time
from datetime import datetime

# Base URLs
topUrl="https://hacker-news.firebaseio.com/v0/topstories.json"
itemUrl="https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header
header={"User-Agent": "TrendPulse/1.0"}

# Category keywords
categories={
    "technology":["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews":["war","government","country","president","election","climate","attack","global"],
    "sports":["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science":["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment":["movie","film","music","netflix","game","book","show","award","streaming"]
}

# Max stories per category
maxCat=25


def fetchAll():
    # Fetching all the top stories from Hackernews
    try:
        response=requests.get(topUrl,header=header)
        response.raise_for_status()
        return response.json()[:500]  # first 500
    except Exception as e:
        print(f"Failed to fetch the story:{e}")
        return []


def fetchStory(story_id):
    #  Fetching individual story details 
    try:
        response=requests.get(itemUrl.format(story_id),header=header)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}:{e}")
        return None


def categorize_title(title):
    # Assigning categories based on keywords 
    if not title:
        return None
    # lowering because the title might have uppercase letters and we want to match keywords in a case insensitive way
    title_lower=title.lower()

    for category,keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None


# ****main funtion****
story_ids=fetchAll()

collected_data=[]
category_counts={cat:0 for cat in categories}

for story_id in story_ids:
    # Stop early if all categories are filled
    if all(count>=maxCat for count in category_counts.values()):
        break
    
    story=fetchStory(story_id)
    if not story:
        continue
    print(f"Fetching story {story_id}")
    title=story.get("title","")
    category=categorize_title(title)

    # Skip if no category match
    if not category:
        continue

    # Skip if category already full
    if category_counts[category]>=maxCat:
        continue

    # Extract required fields
    record={
        "post_id":story.get("id"),
        "title":title,
        "category":category,
        "score":story.get("score",0),
        "num_comments":story.get("descendants",0),
        "author":story.get("by",""),
        "collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    collected_data.append(record)
    category_counts[category]+=1

    # Sleep AFTER finishing each category batch (controlled)
    if category_counts[category]==maxCat:
        print(f"Collected {maxCat} stories for {category}. Sleeping 2 seconds...")
        time.sleep(2)
for i in category_counts:
    print(f"{i}:{category_counts[i]} stories collected.")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Filename with date
filename=f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

# Save JSON
with open(filename,"w",encoding="utf-8") as f:
    json.dump(collected_data, f, indent=4)

print(f"Collected {len(collected_data)} stories. Saved to {filename}")


 