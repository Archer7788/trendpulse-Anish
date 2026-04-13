import pandas as pd
import os

# configuration:
inputFile="data/trends_20260410.json"    
outputFile="data/trends_clean.csv"



# Checking if input file exists:
if not os.path.exists(inputFile):
    print(f"File not found: {inputFile}")
    

else:
    # Loading if data if exiests
    df=pd.read_json(inputFile)


    print(f"\nLoaded {len(df)} stories from {inputFile}")
    print()


# Data Cleaining Steps:


    # Removing duplicates based on post_id
    before=len(df)
    df=df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")


    # Removing rows with missing important fields (post_id, title, score)
    before=len(df)
    df=df.dropna(subset=["post_id","title","score"])
    print(f"After removing nulls: {len(df)}")


    # Have to make sure the important numeric fields are in correct format for further processing and analysis.

    # Data type conversion
    df["score"]=pd.to_numeric(df["score"],errors="coerce")
    df["num_comments"]=pd.to_numeric(df["num_comments"],errors="coerce")

    # Droping rows where conversion is failed
    df=df.dropna(subset=["score","num_comments"])

    # Converting to integer
    df["score"]=df["score"].astype(int)
    df["num_comments"]=df["num_comments"].astype(int)



    # Removing low quality stories (ie., score < 5)
    before=len(df)
    df=df[df["score"]>=5]
    print(f"After removing low scores: {len(df)}")


    # Cleaning whitespace in title
    df["title"]=df["title"].str.strip()



    # Saving cleaned data to CSV
    os.makedirs("data",exist_ok=True)
    df.to_csv(outputFile,index=False)


    print(f"\nSaved {len(df)} rows to {outputFile}")


    # SUMMARY: 
    category_counts=df["category"].value_counts().reset_index()

    # Removing column names
    category_counts.columns=["",""]

    print("\nStories per category:")
    for category,count in category_counts.itertuples(index=False):
        print(f" {category} \t",f"{count}")
    # print(category_counts.to_string(index=False, header=False)) 
