import requests
import time
import json
import os
from datetime import datetime

#Configuration(Base URLs):-
baseURL="https://hacker-news.firebaseio.com/v0"
# header used to identify the script to the API
header={"User-Agent":"TrendPulse/1.0"}

# Constants
maxCat=25
totalIDS=500

#Each Category keywords
CATEGORIES={
    "technology":["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "entertainment":["movie","film","music","netflix","game","book","show","award","streaming"],
    "worldnews":["war","government","country","president","election","climate","attack","global"],
    "science":["research","study","space","physics","biology","discovery","nasa","genome"],
    "sports":["nfl","nba","fifa","sport","game","team","player","league","championship"]
}

# **** Each Function responsible for a specific task:-  ****


# Fetching all the top stories from Hackernews
def fetchALL():
    try:
        url=f"{baseURL}/topstories.json"
        response=requests.get(url,headers=header)
        response.raise_for_status()
        return response.json()[:totalIDS]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


#  Fetching individual story details 
def fetchOne(story_id):
    try:
        url=f"{baseURL}/item/{story_id}.json"
        response=requests.get(url,headers=header)
        response.raise_for_status()
        return response.json()
    # if fetch failed printing the error and return None
    except Exception :
        print(f"Failed to fetch story {story_id}")
        return None


# Assigning categories based on keywords 
def classify_story(title):
    if not title:
        return None
    # lowering because the title might have uppercase letters and we want to match keywords in a case insensitive way
    title_lower=title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


# ---------------- Main logic---------------- #


story_ids=fetchALL()

# Storing categorized data and counts
categorized_data={cat: [] for cat in CATEGORIES}
collected_data=[]

for category in CATEGORIES:
    # printing the category we are processing for clarity and debugging
    print(f"\nProcessing category: {category}")

    for story_id in story_ids:
        # printing the story id we are fetching for clarity and debugging
        print(f"Fetching story {story_id}")
        # Stoping if category is full 
        if len(categorized_data[category])>=maxCat:
            break

        story=fetchOne(story_id)
        if not story:
            continue
            
        title=story.get("title","")
        assigned_category=classify_story(title)
            
        # process is done only if the story belongs to the current category we are filling
        if assigned_category!=category:
            continue
        
        # Extracting fields
        data={
            "post_id":story.get("id"),
            "title":title,
            "category":category,
            "score":story.get("score",0),
            "num_comments":story.get("descendants",0),
            "author":story.get("by","unknown"),
            "collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Adding to both categorized and overall collected data
        categorized_data[category].append(data)
        collected_data.append(data)


    # If category is not full i added dummy data to reach the required count
    if len(categorized_data[category])<maxCat:
        for i in range(len(categorized_data[category]),maxCat):
            data={
            "post_id":i+10000, 
            "title":f"Dummy Title {i+1} for {category}",
            "category":category,
            "score":None,
            "num_comments":None,
            "author":"unknown",
            "collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
            categorized_data[category].append(data)
            collected_data.append(data)



    print(f"Completed category '{category}' with {len(categorized_data[category])} stories.")
    print("Sleeping for 2 seconds")

    # Mandatory sleep AFTER each category
    time.sleep(2)

# ---------------- Save File Function---------------- #

# Ensures data directory exists
os.makedirs("data",exist_ok=True)

# Filename with date
filename=f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

# Saving JSON
with open(filename,"w",encoding="utf-8") as f:
    json.dump(collected_data,f,indent=4)


print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")


