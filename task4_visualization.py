import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# Loading analysed data from Task 3
df=pd.read_csv("data/trends_analysed.csv")

# Creating outputs folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)



                # CHART 1 #
# Top 10 stories by score (horizontal bar chart)

# Sorting by score and took the top 10 using head
top_stories=df.sort_values(by="score",ascending=False).head(10)

# titles max length is 50 characters
top_stories["short_title"]=top_stories["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

# Plotting horizontal bar chart
plt.figure()
plt.barh(top_stories["short_title"], top_stories["score"])

# Adding labels and title
plt.xlabel("Score")               
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

plt.gca().invert_yaxis()                        # making sure highest score is at the top

plt.tight_layout()                              # Adjusting layout to prevent label cutoff
plt.savefig("outputs/chart1_top_stories.png")   # Saving the chart 
plt.close()




                # CHART 2 #
# Stories per category (bar chart)

category_counts=df["category"].value_counts()             # Counting number of stories in each category using value_counts()

# Plotting bar chart
colors = plt.cm.tab10(np.arange(len(category_counts)))
plt.figure()
plt.bar(category_counts.index, category_counts.values, color=colors)
# Adding labels and title
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.xticks(rotation=46)                  # Rotating x-axis labels by 46* for better readability
# Adjusting layout to prevent label cutoff
plt.tight_layout()
# Saving the chart
plt.savefig("outputs/chart2_categories.png")
plt.close()

            #  CHART 3   #
# Scatter plot: score vs comments
#comaparison of popular and non-popular stories with scores and num_comments

plt.figure()

# Spliting data by popularity
popular=df[df["is_popular"]==True]
non_popular=df[df["is_popular"]==False]
# Plotting popular and non-popular stories with different colors
plt.scatter(popular["score"],popular["num_comments"],label="Popular",color="red")
plt.scatter(non_popular["score"],non_popular["num_comments"],label="Not Popular",color="yellow")
# Adding labels and title
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
# Adjusting layout to prevent label cutoff
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")       # Saving the chart
plt.close()


# Dashboard: Combining all charts into a single dashboard

fig,axes=plt.subplots(1,3,figsize=(18,5))

# Chart 1 inside dashboard
axes[0].barh(top_stories["short_title"],top_stories["score"])
axes[0].set_title("Top Stories")
axes[0].invert_yaxis()

# Chart 2 inside dashboard
axes[1].bar(category_counts.index,category_counts.values)
axes[1].set_title("Categories")
axes[1].tick_params(axis='x',rotation=45)

# Chart 3 inside dashboard
axes[2].scatter(popular["score"],popular["num_comments"],label="Popular",color="red")
axes[2].scatter(non_popular["score"],non_popular["num_comments"],label="Not Popular",color="yellow")
axes[2].set_title("Score vs Comments")
axes[2].legend()

# Adding overall title for the dashboard
fig.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

# plt.show() is not used because we are saving the charts instead of displaying them interactively
print("All charts saved successfully in outputs/ folder.")