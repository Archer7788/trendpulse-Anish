import pandas as pd
import numpy as np
import os

# Configuration
INPUT_FILE="data/trends_clean.csv"
OUTPUT_FILE="data/trends_analysed.csv"

def main():
    # Checking if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"File not found:{INPUT_FILE}")
        return

    # Loading data
    df=pd.read_csv(INPUT_FILE)

    print(f"\nLoaded data: {df.shape}")

#  Pandas Analysis
    # printing first 5 rows for understanding the data
    print("\nFirst 5 rows:")
    print(df.head())

    # Averages 
    avg_score=df["score"].mean()                  #Average score
    avg_comments=df["num_comments"].mean()        #Average num-comments

    print(f"\nAverage score   : {avg_score:.0f}")
    print(f"Average comments: {avg_comments:.0f}")



# Numpy Analysis

    print("\n--- NumPy Stats ---")

    scores=df["score"].to_numpy()        #Converting score column to numpy array for analysis

    mean_score=np.mean(scores)           #Calculating mean score
    median_score=np.median(scores)       #Calculating median score
    std_score=np.std(scores)             #Calculating standard deviation of scores

    # Finding max and min scores
    max_score=np.max(scores)
    min_score=np.min(scores)


    print(f"Mean score   : {mean_score:.0f}")
    print(f"Median score : {median_score:.0f}")
    print(f"Std deviation: {std_score:.0f}")
    print(f"Max score    : {max_score}")
    print(f"Min score    : {min_score}")


# Category Analysis
    # Category with most stories is printed
    top_category=df["category"].value_counts().idxmax()      #Finding the category with the most stories
    top_count=df["category"].value_counts().max()            #Finding the count of stories in that category
    
    print(f"\nMost stories in: {top_category} ({top_count} stories)")


    # Finding the  commented story
    max_comments_idx=np.argmax(df["num_comments"].to_numpy())     #Finding the index of the story with the most comments
    top_story=df.iloc[max_comments_idx]                           #Getting the details of that story using iloc

    print(f'\nMost commented story: "{top_story["title"]}" — {top_story["num_comments"]} comments')

    

#Creating new features for further analysis(adding new colums to the dataframe)

    # Engagement = comments per score (adding 1 to score to avoid division by zero)
    df["engagement"]=df["num_comments"]/(df["score"]+1)

    # Popular if greater than average score (Boolenan column True/False)
    df["is_popular"]=df["score"]>avg_score



# Saving the analysed data to a new CSV file (if exists it will be overwritten)
    df.to_csv(OUTPUT_FILE,index=False)

    print(f"\nSaved to {OUTPUT_FILE}")
    print()


if __name__=="__main__":
    main()