# 🚀 TrendPulse — What's Actually Trending Right Now

TrendPulse is a **4-stage data pipeline project** that collects, cleans, analyzes, and visualizes trending stories from Hacker News.

This project demonstrates practical skills in:

* API data collection
* Data cleaning with Pandas
* Numerical analysis with NumPy
* Data visualization with Matplotlib

---

## 📌 Project Pipeline

```
Task 1 → Fetch Data (API)
Task 2 → Clean Data (Pandas)
Task 3 → Analyze Data (NumPy + Pandas)
Task 4 → Visualize Data (Matplotlib)
```

---

## 📂 Project Structure

```
trendpulse-<yourname>/
│
├── data/
│   ├── trends_YYYYMMDD.json
│   ├── trends_clean.csv
│   └── trends_analysed.csv
│
├── outputs/
│   ├── chart1_top_stories.png
│   ├── chart2_categories.png
│   ├── chart3_scatter.png
│   └── dashboard.png
│
├── task1_data_collection.py
├── task2_data_processing.py
├── task3_analysis.py
├── task4_visualization.py
└── README.md
```

---

## 🧩 Task Breakdown

### 🔹 Task 1 — Data Collection

* Fetches top 500 stories from Hacker News API
* Categorizes stories into:

  * Technology
  * World News
  * Sports
  * Science
  * Entertainment
* Stores 25 stories per category
* Saves data as JSON

📄 Output:

```
data/trends_YYYYMMDD.json
```

---

### 🔹 Task 2 — Data Cleaning

* Loads JSON into Pandas DataFrame
* Removes:

  * Duplicate stories
  * Missing values
  * Low-quality posts (score < 5)
* Fixes data types
* Cleans text formatting

📄 Output:

```
data/trends_clean.csv
```

---

### 🔹 Task 3 — Data Analysis

* Uses NumPy for statistical analysis:

  * Mean, median, standard deviation
* Finds:

  * Most popular category
  * Most commented story
* Adds new features:

  * `engagement` = comments per upvote
  * `is_popular` = score above average

📄 Output:

```
data/trends_analysed.csv
```

---

### 🔹 Task 4 — Visualization

Creates 3 charts using Matplotlib:

1. Top 10 stories by score (horizontal bar chart)
2. Stories per category (bar chart)
3. Score vs comments (scatter plot)

Bonus:

* Combined dashboard with all charts

📄 Outputs:

```
outputs/chart1_top_stories.png
outputs/chart2_categories.png
outputs/chart3_scatter.png
outputs/dashboard.png
```

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Requests (API handling)

---

## ▶️ How to Run

### 1. Clone the repository

```
git clone https://github.com/<username>/trendpulse-<name>.git
cd trendpulse-<name>
```

### 2. Install dependencies

```
pip install pandas numpy matplotlib requests
```

### 3. Run the pipeline step-by-step

```
python task1_data_collection.py
python task2_data_processing.py
python task3_analysis.py
python task4_visualization.py
```

---

## 📊 Key Insights

* Technology stories dominate trending topics
* High score does not always mean high engagement
* Some stories generate more discussion relative to their popularity

---

## 📎 Notes

* Dummy data is used if a category has fewer than 25 stories
* API failures are handled gracefully
* Each script is independent but follows a pipeline structure

---

## 👨‍💻 Author

Anish Vardhan
GitHub: https://github.com/Archer7788

---

## ⭐ Conclusion

TrendPulse demonstrates a complete **data pipeline workflow** — from raw API data to meaningful insights and visualizations.

This project highlights skills essential for:

* Data Science
* Data Analysis
* Backend Data Processing

---
